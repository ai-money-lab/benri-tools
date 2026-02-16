#!/usr/bin/env python3
"""Money Machine スケジューラ登録（Windows Task Scheduler / Unix cron 両対応）

2つのタスクを登録:
  1. MoneyMachineDaily   - 毎日06:00 - データ収集→HTML更新→デプロイ
  2. MoneyMachineXPost   - 毎日19:00 - X に1件投稿
"""
import sys
import os
import subprocess
import platform

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

TASKS = [
    {
        'name': 'MoneyMachineDaily',
        'script': os.path.join(BASE_DIR, 'scripts', 'daily_run.py'),
        'hour': 6,
        'minute': 0,
        'desc': 'データ収集・HTML更新・Git Push',
    },
    {
        'name': 'MoneyMachineXPost',
        'script': os.path.join(BASE_DIR, 'scripts', 'x_daily_post.py'),
        'hour': 19,
        'minute': 0,
        'desc': 'X 日次自動投稿',
    },
]


def setup_windows():
    python_exe = sys.executable
    success = 0

    for task in TASKS:
        cmd = [
            'schtasks', '/Create',
            '/TN', task['name'],
            '/TR', f'"{python_exe}" "{task["script"]}"',
            '/SC', 'DAILY',
            '/ST', f'{task["hour"]:02d}:{task["minute"]:02d}',
            '/F',
        ]
        print(f"\n--- {task['name']} ---")
        print(f"  Time: {task['hour']:02d}:{task['minute']:02d} daily")
        print(f"  Desc: {task['desc']}")
        print(f"  Command: {python_exe} {task['script']}")

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  OK: Task '{task['name']}' registered.")
            success += 1
        else:
            print(f"  ERROR: {result.stderr.strip()}")
            if 'Access is denied' in result.stderr:
                print("  Hint: Run as Administrator.")

    print(f"\nResult: {success}/{len(TASKS)} tasks registered.")
    print(f"Verify: schtasks /Query /TN MoneyMachine*")
    return 0 if success == len(TASKS) else 1


def setup_unix():
    python_exe = sys.executable
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        existing = result.stdout if result.returncode == 0 else ''
    except FileNotFoundError:
        print("ERROR: crontab not found")
        return 1

    # 既存エントリを除去
    lines = [l for l in existing.strip().split('\n')
             if l and 'daily_run' not in l and 'x_daily_post' not in l]

    for task in TASKS:
        cron_line = f'{task["minute"]} {task["hour"]} * * * {python_exe} {task["script"]}'
        lines.append(cron_line)
        print(f"  Added: {task['name']} at {task['hour']:02d}:{task['minute']:02d}")

    new_crontab = '\n'.join(lines) + '\n'
    proc = subprocess.run(['crontab', '-'], input=new_crontab, capture_output=True, text=True)
    if proc.returncode == 0:
        print(f"OK: {len(TASKS)} cron entries added.")
        print("Verify: crontab -l")
        return 0
    else:
        print(f"ERROR: {proc.stderr.strip()}")
        return 1


def main():
    print("=== Money Machine Scheduler Setup ===")
    if platform.system() == 'Windows':
        return setup_windows()
    else:
        return setup_unix()


if __name__ == '__main__':
    sys.exit(main())
