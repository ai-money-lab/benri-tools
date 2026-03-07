#!/usr/bin/env python3
"""投稿文字数チェック（X のウェイト計算）"""
import sys, re, unicodedata
sys.stdout.reconfigure(encoding='utf-8')

# X の文字数カウント: CJK=2, その他=1, URL=23固定
def x_weight(text):
    # URLを除去して別カウント
    urls = re.findall(r'https?://\S+', text)
    t = text
    for u in urls:
        t = t.replace(u, '')
    w = 0
    for ch in t:
        if ch == '\n':
            w += 1
        elif unicodedata.east_asian_width(ch) in ('W', 'F'):
            w += 2
        else:
            w += 1
    w += 23 * len(urls)
    return w

# x_schedule_posts.py から POSTS を読み込み
sys.path.insert(0, '.')
from scripts.x_schedule_posts import POSTS

print('=== 本文 ===')
print(f'{"ID":<25} {"Weight":>7}  状態')
print('-' * 55)
over = 0
for p in POSTS:
    weight = x_weight(p['body'])
    status = 'OK' if weight <= 280 else f'超過 (+{weight - 280})'
    if weight > 280:
        over += 1
    print(f'{p["id"]:<25} {weight:>6}w  {status}')

print()
print('=== リプライ ===')
print(f'{"ID":<25} {"Weight":>7}  状態')
print('-' * 55)
for p in POSTS:
    weight = x_weight(p['reply'])
    status = 'OK' if weight <= 280 else f'超過 (+{weight - 280})'
    if weight > 280:
        over += 1
    print(f'{p["id"]:<25} {weight:>6}w  {status}')

print(f'\n超過: {over}件')
