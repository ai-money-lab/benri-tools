#!/usr/bin/env python3
"""Money Machine 日次自動実行スクリプト（クロスプラットフォーム版）"""
import subprocess
import sys
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
DATE_STR = datetime.now().strftime('%Y-%m-%d')
LOG_FILE = os.path.join(LOG_DIR, f'daily_{DATE_STR}.log')

STEPS = [
    ('SIM scraping', [sys.executable, os.path.join(BASE_DIR, 'scrapers', 'sim_scraper.py')]),
    ('HTML generation', [sys.executable, os.path.join(BASE_DIR, 'generators', 'comparison_generator.py')]),
    ('Image generation', [sys.executable, os.path.join(BASE_DIR, 'generators', 'social_image_generator.py')]),
    ('Site index', [sys.executable, os.path.join(BASE_DIR, 'scripts', 'generate_site_index.py')]),
    ('Status', [sys.executable, os.path.join(BASE_DIR, 'scripts', 'status.py')]),
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


def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    ok_count = 0
    total = len(STEPS)

    with open(LOG_FILE, 'a', encoding='utf-8') as fh:
        log(f"===== Money Machine Daily: {DATE_STR} =====", fh)
        for name, cmd in STEPS:
            if run_step(name, cmd, fh):
                ok_count += 1
        log(f"===== Done: {ok_count}/{total} succeeded =====", fh)

    print(f"\nLog: {LOG_FILE}")
    return 0 if ok_count == total else 1


if __name__ == '__main__':
    sys.exit(main())
