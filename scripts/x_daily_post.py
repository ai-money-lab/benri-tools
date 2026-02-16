#!/usr/bin/env python3
"""X(Twitter) 日次自動投稿スクリプト
キューから1件取得し、本文投稿→リプライ（リンク付き）を実行する。

Windows: Task Scheduler から毎日19:00に呼び出し
Linux/VPS: cron + xvfb-run で呼び出し
  例: 0 19 * * * xvfb-run python3 /opt/money-machine/scripts/x_daily_post.py
"""
import sys, os, json, time, platform

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from datetime import datetime
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
QUEUE_PATH = os.path.join(BASE_DIR, 'data', 'x_post_queue.json')
BROWSER_PROFILE = os.path.join(BASE_DIR, 'data', 'x_browser_profile')
os.makedirs(LOGS_DIR, exist_ok=True)

X_EMAIL = 'aijidouca@gmail.com'
X_PASSWORD = 'aijidouca@88'
X_USERNAME = 'claude_sidejob'

IS_WINDOWS = platform.system() == 'Windows'


def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')


def load_queue():
    with open(QUEUE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_queue(queue):
    with open(QUEUE_PATH, 'w', encoding='utf-8') as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)


def get_next_post(queue):
    """未投稿のポストを1件返す"""
    for post in queue:
        if not post.get('posted', False):
            return post
    return None


def is_logged_in(page):
    try:
        compose = page.locator('[data-testid="SideNav_NewTweet_Button"]')
        if compose.count() > 0 and compose.first.is_visible(timeout=3000):
            return True
    except Exception:
        pass
    try:
        timeline = page.locator('[data-testid="primaryColumn"]')
        if timeline.count() > 0 and timeline.first.is_visible(timeout=3000):
            return True
    except Exception:
        pass
    return False


def auto_login(page):
    """X に自動ログイン"""
    log('自動ログイン開始...')
    page.goto('https://x.com/i/flow/login', wait_until='domcontentloaded', timeout=30000)
    time.sleep(4)

    # メールアドレス入力
    try:
        page.wait_for_selector('input[autocomplete="username"], input[name="text"]', timeout=10000)
    except Exception:
        time.sleep(3)

    for sel in ['input[autocomplete="username"]', 'input[name="text"]', 'input[type="text"]']:
        try:
            inp = page.locator(sel)
            if inp.count() > 0 and inp.first.is_visible(timeout=2000):
                inp.first.click()
                time.sleep(0.3)
                page.keyboard.type(X_EMAIL, delay=30)
                break
        except Exception:
            continue

    # 次へ
    for sel in ['button:has-text("次へ")', 'button:has-text("Next")']:
        try:
            btn = page.locator(sel)
            if btn.count() > 0 and btn.first.is_visible(timeout=2000):
                btn.first.click()
                break
        except Exception:
            continue
    time.sleep(4)

    # ユーザー名確認
    try:
        username_input = page.locator('input[data-testid="ocfEnterTextTextInput"]')
        if username_input.count() > 0 and username_input.first.is_visible(timeout=3000):
            username_input.first.click()
            time.sleep(0.3)
            page.keyboard.type(X_USERNAME, delay=30)
            page.keyboard.press('Enter')
            time.sleep(4)
    except Exception:
        pass

    # パスワード入力
    for sel in ['input[name="password"]', 'input[type="password"]']:
        try:
            inp = page.locator(sel)
            if inp.count() > 0 and inp.first.is_visible(timeout=3000):
                inp.first.click()
                time.sleep(0.3)
                page.keyboard.type(X_PASSWORD, delay=30)
                break
        except Exception:
            continue
    time.sleep(0.5)

    # ログインボタン
    for sel in ['button[data-testid="LoginForm_Login_Button"]', 'button:has-text("ログイン")']:
        try:
            btn = page.locator(sel)
            if btn.count() > 0 and btn.first.is_visible(timeout=2000):
                btn.first.click()
                break
        except Exception:
            continue

    time.sleep(6)
    for _ in range(15):
        if is_logged_in(page):
            log('ログイン成功')
            return True
        time.sleep(1)

    log('ログイン失敗')
    return False


def type_text(page, text):
    """テキストを行ごとに入力"""
    lines = text.split('\n')
    for j, line in enumerate(lines):
        if line:
            page.keyboard.type(line, delay=10)
        if j < len(lines) - 1:
            page.keyboard.press('Enter')


def post_tweet(page, text):
    """ツイートを即時投稿し、成功したら True を返す"""
    page.goto('https://x.com/compose/post', wait_until='domcontentloaded', timeout=15000)
    time.sleep(3)

    editor = page.locator('[data-testid="tweetTextarea_0"]')
    if editor.count() == 0:
        page.keyboard.press('n')
        time.sleep(2)
        editor = page.locator('[data-testid="tweetTextarea_0"]')

    if editor.count() == 0:
        log('投稿エディタが見つかりません')
        page.screenshot(path=os.path.join(LOGS_DIR, 'x_daily_no_editor.png'))
        return False

    editor.first.click()
    time.sleep(0.3)
    type_text(page, text)
    time.sleep(0.5)

    for sel in ['[data-testid="tweetButton"]', '[data-testid="tweetButtonInline"]']:
        try:
            btn = page.locator(sel)
            if btn.count() > 0 and btn.first.is_visible(timeout=2000):
                btn.first.click()
                time.sleep(3)
                log('投稿完了')
                return True
        except Exception:
            continue

    log('投稿ボタンが見つかりません')
    page.screenshot(path=os.path.join(LOGS_DIR, 'x_daily_no_submit.png'))
    return False


def post_reply(page, reply_text):
    """最新の自分のツイートにリプライする"""
    time.sleep(2)
    page.goto(f'https://x.com/{X_USERNAME}', wait_until='domcontentloaded', timeout=15000)
    time.sleep(3)

    tweets = page.locator('article[data-testid="tweet"]')
    if tweets.count() == 0:
        log('ツイートが見つかりません')
        return False

    tweets.first.click()
    time.sleep(2)

    reply_editor = page.locator('[data-testid="tweetTextarea_0"]')
    if reply_editor.count() == 0:
        reply_editor = page.locator('[role="textbox"]')

    if reply_editor.count() == 0:
        log('リプライ欄が見つかりません')
        return False

    reply_editor.first.click()
    time.sleep(0.3)
    type_text(page, reply_text)
    time.sleep(0.5)

    for sel in ['[data-testid="tweetButton"]', '[data-testid="tweetButtonInline"]']:
        try:
            btn = page.locator(sel)
            if btn.count() > 0 and btn.first.is_visible(timeout=2000):
                btn.first.click()
                time.sleep(3)
                log('リプライ完了')
                return True
        except Exception:
            continue

    log('リプライ投稿ボタンが見つかりません')
    return False


def run_with_persistent_context(post):
    """Playwright persistent context でブラウザ起動（Windows/Linux両対応）"""
    os.makedirs(BROWSER_PROFILE, exist_ok=True)
    result_code = 1

    with sync_playwright() as p:
        # persistent context: ログイン状態がディスクに保存される
        context = p.chromium.launch_persistent_context(
            user_data_dir=BROWSER_PROFILE,
            headless=False,  # VPSでは xvfb-run 経由で実行
            viewport={'width': 1280, 'height': 900},
            locale='ja-JP',
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-first-run',
            ],
        )

        try:
            page = context.pages[0] if context.pages else context.new_page()
            page.goto('https://x.com/home', wait_until='domcontentloaded', timeout=30000)
            time.sleep(5)

            # ログイン確認
            if not is_logged_in(page):
                log('未ログイン → 自動ログイン')
                if not auto_login(page):
                    log('ログイン失敗。中断。')
                    page.screenshot(path=os.path.join(LOGS_DIR, 'x_daily_login_fail.png'))
                    context.close()
                    return 1
                time.sleep(2)

            log('ログイン済み')

            # 本文投稿
            ok = post_tweet(page, post['body'])
            if not ok:
                log('本文投稿失敗')
                context.close()
                return 1

            # リプライ投稿
            if post.get('reply'):
                time.sleep(2)
                reply_ok = post_reply(page, post['reply'])
                if not reply_ok:
                    log('リプライ投稿失敗（本文は投稿済み）')

            result_code = 0

        except Exception as e:
            log(f'エラー: {e}')
            try:
                page.screenshot(path=os.path.join(LOGS_DIR, 'x_daily_error.png'))
            except Exception:
                pass
        finally:
            context.close()

    return result_code


def run_with_chrome_debug(post):
    """Chrome debug port 経由（Windows向け後方互換）"""
    import subprocess as sp
    import urllib.request

    DEBUG_PORT = 9222
    CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    os.system('taskkill /F /IM chrome.exe 2>nul')
    time.sleep(3)

    debug_user_data = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'ChromeDebug')
    os.makedirs(debug_user_data, exist_ok=True)

    for lock_name in ['lockfile', 'SingletonLock']:
        for subdir in ['', 'Default']:
            lock_path = os.path.join(debug_user_data, subdir, lock_name) if subdir else os.path.join(debug_user_data, lock_name)
            if os.path.exists(lock_path):
                try:
                    os.remove(lock_path)
                except Exception:
                    pass

    log('Chrome起動中...')
    chrome_proc = sp.Popen([
        CHROME_PATH,
        f'--remote-debugging-port={DEBUG_PORT}',
        f'--user-data-dir={debug_user_data}',
        '--no-first-run',
        'https://x.com/home',
    ])

    result_code = 1

    with sync_playwright() as p:
        browser = None
        for attempt in range(20):
            time.sleep(2)
            try:
                urllib.request.urlopen(f'http://127.0.0.1:{DEBUG_PORT}/json/version', timeout=2)
                browser = p.chromium.connect_over_cdp(f'http://127.0.0.1:{DEBUG_PORT}')
                log(f'Chrome接続OK ({(attempt+1)*2}秒)')
                break
            except Exception:
                pass

        if not browser:
            log('Chrome接続失敗')
            chrome_proc.terminate()
            return 1

        try:
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else context.new_page()
            time.sleep(3)

            if 'x.com' not in page.url:
                page.goto('https://x.com/home', wait_until='domcontentloaded', timeout=30000)
                time.sleep(5)

            if not is_logged_in(page):
                log('未ログイン → 自動ログイン')
                if not auto_login(page):
                    log('ログイン失敗。中断。')
                    page.screenshot(path=os.path.join(LOGS_DIR, 'x_daily_login_fail.png'))
                    return 1
                time.sleep(2)

            log('ログイン済み')

            ok = post_tweet(page, post['body'])
            if not ok:
                log('本文投稿失敗')
                return 1

            if post.get('reply'):
                time.sleep(2)
                reply_ok = post_reply(page, post['reply'])
                if not reply_ok:
                    log('リプライ投稿失敗（本文は投稿済み）')

            result_code = 0

        except Exception as e:
            log(f'エラー: {e}')
            try:
                page.screenshot(path=os.path.join(LOGS_DIR, 'x_daily_error.png'))
            except Exception:
                pass
        finally:
            browser.close()
            chrome_proc.terminate()

    return result_code


def main():
    log('===== X Daily Post =====')

    queue = load_queue()
    post = get_next_post(queue)
    if not post:
        log('投稿キューが空です（全件投稿済み）')
        return 0

    log(f'次の投稿: {post["id"]}')

    # Windows: Chrome debug port（既存のログイン状態を再利用）
    # Linux/VPS: Playwright persistent context（xvfb-run 経由）
    if IS_WINDOWS:
        result_code = run_with_chrome_debug(post)
    else:
        result_code = run_with_persistent_context(post)

    if result_code == 0:
        post['posted'] = True
        post['posted_at'] = datetime.now().isoformat()
        save_queue(queue)
        log(f'キュー更新完了: {post["id"]} = posted')

    return result_code


if __name__ == '__main__':
    sys.exit(main())
