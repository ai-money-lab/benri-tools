"""
家賃診断データ同期スクリプト

Google Apps Script の Web App から JSON を取得し、
data/raw_data.json と data/summary.json を更新する。

環境変数:
  GSHEET_JSON_URL: Google Apps Script の Web App URL

使い方:
  python scripts/sync_form_data.py
"""

import json
import os
import sys
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
RAW_DATA_FILE = os.path.join(DATA_DIR, 'raw_data.json')
SUMMARY_FILE = os.path.join(DATA_DIR, 'summary.json')
KPI_FILE = os.path.join(DATA_DIR, 'kpi_history.json')


def fetch_data(url):
    """Google Apps Script Web App からデータを取得"""
    req = Request(url, headers={'User-Agent': 'ROCKEDGE-AI-OS/1.0'})
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except URLError as e:
        print(f'ERROR: データ取得失敗 - {e}')
        return None


def update_raw_data(new_data):
    """raw_data.json を更新（既存データとマージ）"""
    existing = {}
    if os.path.exists(RAW_DATA_FILE):
        with open(RAW_DATA_FILE, 'r', encoding='utf-8') as f:
            existing = json.load(f)

    existing_ids = set()
    if 'entries' in existing:
        existing_ids = {e.get('id') for e in existing['entries']}

    # 新規エントリのみ追加
    new_entries = [e for e in new_data.get('entries', []) if e.get('id') not in existing_ids]
    all_entries = existing.get('entries', []) + new_entries

    result = {
        'lastUpdated': datetime.utcnow().isoformat() + 'Z',
        'totalEntries': len(all_entries),
        'newThisWeek': len(new_entries),
        'entries': all_entries
    }

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(RAW_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f'raw_data.json 更新完了: {len(all_entries)}件 (+{len(new_entries)}件)')
    return result


def update_summary(data):
    """summary.json を更新"""
    summary = data.get('summary', {})
    summary['lastUpdated'] = datetime.utcnow().isoformat() + 'Z'

    with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f'summary.json 更新完了')
    return summary


def update_kpi(raw_data, summary):
    """kpi_history.json に週次KPIを追加"""
    kpi_history = []
    if os.path.exists(KPI_FILE):
        with open(KPI_FILE, 'r', encoding='utf-8') as f:
            kpi_history = json.load(f)

    week_entry = {
        'date': datetime.utcnow().strftime('%Y-%m-%d'),
        'totalData': raw_data.get('totalEntries', 0),
        'newThisWeek': raw_data.get('newThisWeek', 0),
        'averageRent': summary.get('averageRent', 0),
        'averageScore': summary.get('averageScore', 0),
        'averageRentRatio': summary.get('averageRentRatio', 0),
        'totalResponses': summary.get('totalResponses', 0)
    }

    kpi_history.append(week_entry)

    with open(KPI_FILE, 'w', encoding='utf-8') as f:
        json.dump(kpi_history, f, ensure_ascii=False, indent=2)

    print(f'kpi_history.json 更新完了: {len(kpi_history)}週分')


def main():
    url = os.environ.get('GSHEET_JSON_URL')
    if not url:
        print('ERROR: GSHEET_JSON_URL 環境変数が設定されていません')
        print('GitHub Secrets に GSHEET_JSON_URL を追加してください')
        sys.exit(1)

    print('=== 家賃診断データ同期 ===')
    print(f'取得元: {url[:50]}...')

    data = fetch_data(url)
    if not data:
        sys.exit(1)

    raw = update_raw_data(data)
    summary = update_summary(data)
    update_kpi(raw, summary)

    print('=== 同期完了 ===')


if __name__ == '__main__':
    main()
