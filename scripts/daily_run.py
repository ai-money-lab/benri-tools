#!/usr/bin/env python3
"""Money Machine 日次自動実行スクリプト（フルパイプライン版）

06:00 に Task Scheduler から呼び出される。
1. SIMデータ収集
2. HTML生成（格安SIM比較表）
3. アフィリエイトリンク再注入
4. 関連リンク再注入（初回のみ）
5. サイトインデックス再生成
6. SNS画像生成
7. Git auto-commit & push (GitHub Pages デプロイ)
8. ステータスチェック
"""
import subprocess
import sys
import os
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
DATE_STR = datetime.now().strftime('%Y-%m-%d')
LOG_FILE = os.path.join(LOG_DIR, f'daily_{DATE_STR}.log')

STEPS = [
    ('SIM scraping',
     [sys.executable, os.path.join(BASE_DIR, 'scrapers', 'sim_scraper.py')]),

    ('HTML generation',
     [sys.executable, os.path.join(BASE_DIR, 'generators', 'comparison_generator.py')]),

    ('Affiliate link injection',
     [sys.executable, os.path.join(BASE_DIR, 'scripts', 'inject_affiliate_links.py')]),

    ('Site index',
     [sys.executable, os.path.join(BASE_DIR, 'scripts', 'generate_site_index.py')]),

    ('Social image generation',
     [sys.executable, os.path.join(BASE_DIR, 'generators', 'social_image_generator.py')]),

    ('Status',
     [sys.executable, os.path.join(BASE_DIR, 'scripts', 'status.py')]),
]

TIMEOUT_SEC = 300


def log(msg, fh):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line)
    fh.write(line + '\n')
    fh.flush()


def run_step(name, cmd, fh):
    log(f"{name} ... start", fh)
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SEC,
            cwd=BASE_DIR,
            encoding='utf-8',
            errors='replace',
        )
        if result.stdout:
            fh.write(result.stdout + '\n')
        if result.returncode != 0:
            log(f"{name} ... WARN (exit {result.returncode})", fh)
            if result.stderr:
                fh.write(result.stderr + '\n')
            return False
        log(f"{name} ... OK", fh)
        return True
    except subprocess.TimeoutExpired:
        log(f"{name} ... TIMEOUT ({TIMEOUT_SEC}s)", fh)
        return False
    except FileNotFoundError:
        log(f"{name} ... SKIP (script not found)", fh)
        return False
    except Exception as e:
        log(f"{name} ... ERROR: {e}", fh)
        return False


def git_auto_deploy(fh):
    """変更があれば git commit + push で GitHub Pages にデプロイ"""
    log("Git auto-deploy ... start", fh)
    try:
        # 変更チェック
        status = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True, text=True, cwd=BASE_DIR,
            encoding='utf-8', errors='replace',
        )
        changes = [
            line for line in status.stdout.strip().split('\n')
            if line and not any(x in line for x in ['.env', 'credentials', 'settings.local', 'money_machine.db'])
        ]

        if not changes:
            log("Git auto-deploy ... SKIP (no changes)", fh)
            return True

        log(f"  {len(changes)} files changed", fh)

        # git add (output/ と config/ のみ - 安全のため)
        subprocess.run(
            ['git', 'add', 'output/', 'config/', 'data/x_post_queue.json'],
            cwd=BASE_DIR, capture_output=True, text=True,
            encoding='utf-8', errors='replace',
        )

        # commit
        msg = f"auto: daily update {DATE_STR}"
        result = subprocess.run(
            ['git', 'commit', '-m', msg],
            cwd=BASE_DIR, capture_output=True, text=True,
            encoding='utf-8', errors='replace',
        )
        if result.returncode != 0:
            if 'nothing to commit' in result.stdout:
                log("Git auto-deploy ... SKIP (nothing staged)", fh)
                return True
            log(f"Git auto-deploy ... WARN (commit failed): {result.stderr}", fh)
            return False

        fh.write(result.stdout + '\n')

        # push
        result = subprocess.run(
            ['git', 'push', 'origin', 'main'],
            cwd=BASE_DIR, capture_output=True, text=True,
            timeout=60, encoding='utf-8', errors='replace',
        )
        if result.returncode != 0:
            log(f"Git auto-deploy ... WARN (push failed): {result.stderr}", fh)
            return False

        log("Git auto-deploy ... OK", fh)
        return True

    except Exception as e:
        log(f"Git auto-deploy ... ERROR: {e}", fh)
        return False


def check_x_queue(fh):
    """X投稿キューの残数をチェックし、少なければアラートを出す"""
    queue_path = os.path.join(BASE_DIR, 'data', 'x_post_queue.json')
    alerts_path = os.path.join(BASE_DIR, 'data', 'alerts.json')

    try:
        with open(queue_path, 'r', encoding='utf-8') as f:
            queue = json.load(f)
        remaining = sum(1 for p in queue if not p.get('posted', False))
        total = len(queue)
        posted = total - remaining

        log(f"X queue check: {remaining} remaining / {total} total", fh)

        # アラート管理
        alerts = []
        if os.path.exists(alerts_path):
            try:
                with open(alerts_path, 'r', encoding='utf-8') as f:
                    alerts = json.load(f)
            except Exception:
                alerts = []

        # 古いqueue_lowアラートを除去
        alerts = [a for a in alerts if a.get('type') != 'queue_low']

        if remaining <= 5:
            alert = {
                'type': 'queue_low',
                'level': 'critical' if remaining <= 2 else 'warning',
                'message': f'X投稿キュー残り{remaining}件！補充が必要です。',
                'remaining': remaining,
                'created_at': datetime.now().isoformat(),
            }
            alerts.append(alert)
            log(f"ALERT: X queue low! Only {remaining} posts remaining!", fh)
        elif remaining <= 10:
            alert = {
                'type': 'queue_low',
                'level': 'info',
                'message': f'X投稿キュー残り{remaining}件。そろそろ補充を検討。',
                'remaining': remaining,
                'created_at': datetime.now().isoformat(),
            }
            alerts.append(alert)
            log(f"INFO: X queue getting low ({remaining} remaining)", fh)

        with open(alerts_path, 'w', encoding='utf-8') as f:
            json.dump(alerts, f, ensure_ascii=False, indent=2)

    except Exception as e:
        log(f"X queue check ... ERROR: {e}", fh)


def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    ok_count = 0
    total = len(STEPS) + 1  # +1 for git deploy

    with open(LOG_FILE, 'a', encoding='utf-8') as fh:
        log(f"===== Money Machine Daily: {DATE_STR} =====", fh)

        for name, cmd in STEPS:
            if run_step(name, cmd, fh):
                ok_count += 1

        # X投稿キュー残数チェック
        check_x_queue(fh)

        # Git deploy (after all generation steps)
        if git_auto_deploy(fh):
            ok_count += 1

        log(f"===== Done: {ok_count}/{total} succeeded =====", fh)

    print(f"\nLog: {LOG_FILE}")
    return 0 if ok_count == total else 1


if __name__ == '__main__':
    sys.exit(main())
