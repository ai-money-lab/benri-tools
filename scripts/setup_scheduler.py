#!/usr/bin/env python3
"""Money Machine スケジューラ登録（Windows Task Scheduler / Unix cron 両対応）"""
import sys
import os
import subprocess
import platform

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DAILY_SCRIPT = os.path.join(BASE_DIR, 'scripts', 'daily_run.py')
TASK_NAME = 'MoneyMachineDaily'
SCHEDULE_HOUR = 6
SCHEDULE_MINUTE = 0


def setup_windows():
    python_exe = sys.executable
    cmd = [
        'schtasks', '/Create',
        '/TN', TASK_NAME,
        '/TR', f'"{python_exe}" "{DAILY_SCRIPT}"',
        '/SC', 'DAILY',
        '/ST', f'{SCHEDULE_HOUR:02d}:{SCHEDULE_MINUTE:02d}',
        '/F',
    ]
    print(f"Registering Windows Task: {TASK_NAME}")
    print(f"  Time: {SCHEDULE_HOUR:02d}:{SCHEDULE_MINUTE:02d} daily")
    print(f"  Command: {python_exe} {DAILY_SCRIPT}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"OK: Task '{TASK_NAME}' registered.")
        print(f"Verify: schtasks /Query /TN {TASK_NAME}")
    else:
        print(f"ERROR: {result.stderr.strip()}")
        if 'Access is denied' in result.stderr:
            print("Hint: Run as Administrator.")
        return 1
    return 0


def setup_unix():
    python_exe = sys.executable
    cron_line = f'{SCHEDULE_MINUTE} {SCHEDULE_HOUR} * * * {python_exe} {DAILY_SCRIPT}'
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        existing = result.stdout if result.returncode == 0 else ''
    except FileNotFoundError:
        print("ERROR: crontab not found")
        return 1

    if 'daily_run' in existing:
        print("Cron entry already exists. Updating...")
        lines = [l for l in existing.strip().split('\n') if 'daily_run' not in l]
    else:
        lines = [l for l in existing.strip().split('\n') if l]

    lines.append(cron_line)
    new_crontab = '\n'.join(lines) + '\n'

    proc = subprocess.run(['crontab', '-'], input=new_crontab, capture_output=True, text=True)
    if proc.returncode == 0:
        print(f"OK: Cron entry added ({SCHEDULE_HOUR:02d}:{SCHEDULE_MINUTE:02d} daily)")
        print(f"Verify: crontab -l")
    else:
        print(f"ERROR: {proc.stderr.strip()}")
        return 1
    return 0


def main():
    print("=== Money Machine Scheduler Setup ===")
    if platform.system() == 'Windows':
        return setup_windows()
    else:
        return setup_unix()


if __name__ == '__main__':
    sys.exit(main())
