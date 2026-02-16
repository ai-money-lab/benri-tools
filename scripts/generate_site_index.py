#!/usr/bin/env python3
"""Money Machine サイトインデックスページ生成
DBのtoolsテーブルから公開済みツール一覧を取得し、
output/tools/index.html にランディングページを出力する。
"""
import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(BASE_DIR, 'data', 'money_machine.db')
OUTPUT_PATH = os.path.join(BASE_DIR, 'output', 'tools', 'index.html')

CATEGORY_LABELS = {
    'calculator': '計算機',
    'simulator': 'シミュレーター',
    'checker': 'チェッカー',
    'converter': '変換ツール',
    'generator': '生成ツール',
    'finance': '資産・金融',
    'asset_management': '資産運用',
    'comparison': '比較ツール',
}

CATEGORY_ICONS = {
    'calculator': '🔢',
    'simulator': '📊',
    'checker': '✅',
    'converter': '🔄',
    'generator': '⚙️',
    'finance': '💰',
    'asset_management': '📈',
    'comparison': '⚖️',
}


def get_deployed_tools():
    """ディスク上にindex.htmlが存在するツールをDBから取得"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT name, slug, category FROM tools ORDER BY category, name')
    all_tools = c.fetchall()
    conn.close()

    tools_dir = os.path.join(BASE_DIR, 'output', 'tools')
    deployed = []
    for name, slug, category in all_tools:
        idx = os.path.join(tools_dir, slug, 'index.html')
        if os.path.isfile(idx):
            deployed.append((name, slug, category))
    return deployed


def group_by_category(tools):
    groups = {}
    for name, slug, category in tools:
        cat = category if category in CATEGORY_LABELS else 'calculator'
        groups.setdefault(cat, []).append((name, slug))
    return groups


def generate_html(groups, total_count):
    now = datetime.now().strftime('%Y-%m-%d')

    cards_html = ''
    for cat, tools in sorted(groups.items(), key=lambda x: -len(x[1])):
        label = CATEGORY_LABELS.get(cat, cat)
        icon = CATEGORY_ICONS.get(cat, '🔧')
        cards_html += f'<h2 class="cat-title">{icon} {label}</h2>\n<div class="grid">\n'
        for name, slug in tools:
            cards_html += f'''  <a href="{slug}/index.html" class="card">
    <span class="card-name">{name}</span>
    <span class="card-arrow">→</span>
  </a>
'''
        cards_html += '</div>\n'

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>無料お金ツール集 | Money Machine</title>
<meta name="description" content="年収計算・ローンシミュレーション・投資リターン計算など、お金に関する無料ツールを{total_count}個公開中。">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Hiragino Sans",sans-serif;background:#f5f7fa;color:#1a1a2e;line-height:1.6}}
.header{{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;padding:2.5rem 1rem;text-align:center}}
.header h1{{font-size:1.8rem;margin-bottom:.4rem}}
.header p{{opacity:.9;font-size:.95rem}}
.container{{max-width:900px;margin:0 auto;padding:1.5rem 1rem 3rem}}
.cat-title{{font-size:1.2rem;margin:2rem 0 .8rem;padding-bottom:.4rem;border-bottom:2px solid #667eea}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:.75rem}}
.card{{display:flex;justify-content:space-between;align-items:center;background:#fff;border-radius:10px;padding:1rem 1.2rem;text-decoration:none;color:#1a1a2e;box-shadow:0 1px 3px rgba(0,0,0,.08);transition:transform .15s,box-shadow .15s}}
.card:hover{{transform:translateY(-2px);box-shadow:0 4px 12px rgba(102,126,234,.2)}}
.card-name{{font-weight:600;font-size:.95rem}}
.card-arrow{{color:#667eea;font-size:1.2rem}}
.footer{{text-align:center;padding:2rem 1rem;font-size:.8rem;color:#888}}
</style>
</head>
<body>
<div class="header">
  <h1>無料お金ツール集</h1>
  <p>全{total_count}ツール公開中 ・ スマホ対応 ・ 登録不要</p>
</div>
<div class="container">
{cards_html}
</div>
<div class="footer">
  <p>最終更新: {now} | Money Machine</p>
</div>
</body>
</html>'''
    return html


def main():
    tools = get_deployed_tools()
    if not tools:
        print("No deployed tools found.")
        return

    groups = group_by_category(tools)
    total = len(tools)
    html = generate_html(groups, total)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated: {OUTPUT_PATH}")
    print(f"  Tools: {total}")
    print(f"  Categories: {len(groups)}")


if __name__ == '__main__':
    main()
