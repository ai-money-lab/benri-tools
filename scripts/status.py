#!/usr/bin/env python3
"""Money Machine ステータスダッシュボード"""
import sqlite3
import os
import glob
from datetime import datetime

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
DB_PATH = os.path.join(BASE_DIR, 'data', 'money_machine.db')

def get_db_stats():
    if not os.path.exists(DB_PATH):
        return {}
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    stats = {}
    for table in ['keywords', 'tools', 'comparison_data', 'social_posts', 'revenue', 'templates']:
        try:
            c.execute(f'SELECT COUNT(*) FROM {table}')
            stats[table] = c.fetchone()[0]
        except:
            stats[table] = 0

    # Tool status breakdown
    try:
        c.execute("SELECT deploy_status, COUNT(*) FROM tools GROUP BY deploy_status")
        stats['tool_status'] = dict(c.fetchall())
    except:
        stats['tool_status'] = {}

    conn.close()
    return stats

def list_files(directory, pattern='*'):
    full_path = os.path.join(BASE_DIR, directory)
    if not os.path.exists(full_path):
        return []
    results = []
    for root, dirs, files in os.walk(full_path):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), BASE_DIR)
            size = os.path.getsize(os.path.join(root, f))
            results.append((rel, size))
    return results

def check_scheduler():
    import subprocess
    import platform
    if platform.system() == 'Windows':
        try:
            result = subprocess.run(
                ['schtasks', '/Query', '/TN', 'MoneyMachineDaily'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return "ACTIVE (Task Scheduler)"
            return "NOT SET"
        except Exception:
            return "N/A"
    else:
        try:
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, timeout=5)
            if 'daily_run' in result.stdout:
                return "ACTIVE (cron)"
            return "NOT SET"
        except Exception:
            return "N/A"

def main():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    stats = get_db_stats()

    print("=" * 48)
    print("  MONEY MACHINE STATUS")
    print(f"  Date: {now}")
    print("=" * 48)

    # Database
    print("\n DATABASE")
    for table, count in stats.items():
        if table == 'tool_status':
            continue
        print(f"  {table}: {count} records")

    tool_status = stats.get('tool_status', {})
    if tool_status:
        status_parts = [f"{k}: {v}" for k, v in tool_status.items()]
        print(f"  tools breakdown: {', '.join(status_parts)}")

    # Tools
    print("\n TOOLS (output/tools/)")
    tools = list_files('output/tools')
    if tools:
        for path, size in tools:
            print(f"  {path} ({size:,} bytes)")
    else:
        print("  (none)")

    # Social
    print("\n SOCIAL (output/social/)")
    social = list_files('output/social')
    if social:
        for path, size in social:
            print(f"  {path} ({size:,} bytes)")
    else:
        print("  (none)")

    # Templates
    print("\n TEMPLATES (output/templates/notion/)")
    templates = list_files('output/templates/notion')
    if templates:
        for path, size in templates:
            print(f"  {path} ({size:,} bytes)")
    else:
        print("  (none)")

    # Agents
    print("\n AGENTS (.claude/agents/)")
    agents = list_files('.claude/agents')
    if agents:
        for path, size in agents:
            print(f"  {path}")
    else:
        print("  (none)")

    # Commands
    print("\n COMMANDS (.claude/commands/)")
    commands = list_files('.claude/commands')
    if commands:
        for path, size in commands:
            print(f"  {path}")
    else:
        print("  (none)")

    # Scheduler
    print("\n SCHEDULER")
    sched_status = check_scheduler()
    print(f"  daily_run.py: {sched_status}")

    print("\n" + "=" * 48)

if __name__ == '__main__':
    main()
