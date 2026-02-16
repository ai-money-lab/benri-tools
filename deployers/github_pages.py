#!/usr/bin/env python3
"""GitHub Pages デプロイ自動化（git add → commit → push）"""
import subprocess
import sys
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def run(cmd, **kwargs):
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True, **kwargs)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0 and result.stderr.strip():
        print(result.stderr.strip())
    return result


def main():
    # Check if git repo
    if not os.path.isdir(os.path.join(BASE_DIR, '.git')):
        print("ERROR: Not a git repository. Run 'git init' first.")
        return 1

    # Check for changes
    status = run(['git', 'status', '--porcelain'])
    if not status.stdout.strip():
        print("No changes to deploy.")
        return 0

    date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    msg = f"auto-deploy: {date_str}"

    run(['git', 'add', '-A'])
    result = run(['git', 'commit', '-m', msg])
    if result.returncode != 0:
        print("Commit failed or nothing to commit.")
        return 1

    result = run(['git', 'push'])
    if result.returncode != 0:
        print("Push failed. Check remote configuration.")
        return 1

    print(f"\nDeployed: {msg}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
