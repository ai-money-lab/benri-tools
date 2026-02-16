#!/usr/bin/env python3
"""SNSランキング画像生成スクリプト"""
import sqlite3
import os
import sys
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'money_machine.db')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output', 'social')

def find_japanese_font():
    """日本語フォントを自動検出"""
    font_candidates = [
        # Windows
        "C:/Windows/Fonts/msgothic.ttc",
        "C:/Windows/Fonts/meiryo.ttc",
        "C:/Windows/Fonts/YuGothR.ttc",
        "C:/Windows/Fonts/YuGothM.ttc",
        "C:/Windows/Fonts/yugothic.ttf",
        # Mac
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        # Linux
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/OTF/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
        "/usr/share/fonts/ipa-gothic/ipag.ttf",
        "/usr/share/fonts/truetype/ipafont-gothic/ipag.ttf",
    ]
    for path in font_candidates:
        if os.path.exists(path):
            return path
    return None

def generate():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("  WARNING: Pillow not installed. Run: pip install Pillow")
        print("  Skipping image generation.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""SELECT provider, plan_name, price, data_gb
                 FROM comparison_data
                 WHERE is_current = 1 AND category = 'sim' AND price > 0
                 ORDER BY price ASC LIMIT 5""")
    top5 = [dict(row) for row in c.fetchall()]
    conn.close()

    if not top5:
        print("  No data for ranking image.")
        return

    # Image setup
    W, H = 1200, 675
    img = Image.new('RGB', (W, H), '#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Find font
    font_path = find_japanese_font()

    if font_path:
        font_title = ImageFont.truetype(font_path, 36)
        font_sub = ImageFont.truetype(font_path, 24)
        font_rank = ImageFont.truetype(font_path, 32)
        font_price = ImageFont.truetype(font_path, 28)
        font_small = ImageFont.truetype(font_path, 18)
    else:
        print("  WARNING: No Japanese font found. Using default (English only).")
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_rank = font_title
        font_price = font_title
        font_small = font_title

    # Header bar
    draw.rectangle([(0, 0), (W, 90)], fill='#0d1b3e')
    today = datetime.now()
    title_text = "格安SIM 最安ランキング"
    date_text = f"{today.year}年{today.month}月最新版"

    # Center title
    try:
        bbox = draw.textbbox((0, 0), title_text, font=font_title)
        tw = bbox[2] - bbox[0]
    except:
        tw = len(title_text) * 36
    draw.text(((W - tw) // 2, 22), title_text, fill='#FFFFFF', font=font_title)

    # Date subtitle
    try:
        bbox2 = draw.textbbox((0, 0), date_text, font=font_small)
        tw2 = bbox2[2] - bbox2[0]
    except:
        tw2 = len(date_text) * 18
    draw.text(((W - tw2) // 2, 68), date_text, fill='#aabbcc', font=font_small)

    # Rankings
    medals = ['🥇', '🥈', '🥉', '4.', '5.']
    # Since emoji rendering may not work, use text alternatives
    rank_labels = ['1位', '2位', '3位', '4位', '5位']
    rank_colors = ['#FFD700', '#C0C0C0', '#CD7F32', '#666666', '#666666']
    bg_colors = ['#FFF8E1', '#F5F5F5', '#FFF3E0', '#FAFAFA', '#FAFAFA']

    y_start = 110
    row_h = 100

    for i, plan in enumerate(top5):
        y = y_start + i * row_h

        # Row background
        draw.rectangle([(40, y), (W - 40, y + row_h - 10)], fill=bg_colors[i], outline='#E0E0E0')

        # Rank circle
        cx, cy = 100, y + (row_h - 10) // 2
        r = 28
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=rank_colors[i])
        try:
            bbox_r = draw.textbbox((0, 0), rank_labels[i], font=font_sub)
            rw = bbox_r[2] - bbox_r[0]
            rh = bbox_r[3] - bbox_r[1]
        except:
            rw, rh = 48, 24
        draw.text((cx - rw // 2, cy - rh // 2 - 2), rank_labels[i], fill='#FFFFFF', font=font_sub)

        # Provider name
        draw.text((160, y + 12), plan['provider'], fill='#1a1a1a', font=font_rank)

        # Plan name
        draw.text((160, y + 52), plan['plan_name'], fill='#666666', font=font_small)

        # Price
        price_text = f"月額 {int(plan['price']):,}円"
        try:
            bbox_p = draw.textbbox((0, 0), price_text, font=font_price)
            pw = bbox_p[2] - bbox_p[0]
        except:
            pw = len(price_text) * 28
        draw.text((W - 80 - pw, y + 25), price_text, fill='#1a73e8', font=font_price)

        # Data
        data_text = f"{plan['data_gb']}GB" if plan['data_gb'] < 999 else "無制限"
        draw.text((W - 80 - pw, y + 60), data_text, fill='#888888', font=font_small)

    # Footer
    draw.rectangle([(0, H - 50), (W, H)], fill='#f5f5f5')
    footer_text = "※税込価格 ｜ 最新情報は公式サイトをご確認ください"
    draw.text((40, H - 38), footer_text, fill='#999999', font=font_small)

    # Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{today.strftime('%Y-%m-%d')}_sim_ranking.png"
    out_path = os.path.join(OUTPUT_DIR, filename)
    img.save(out_path, 'PNG')

    size = os.path.getsize(out_path)
    print(f"  Generated: {out_path}")
    print(f"  File size: {size:,} bytes")
    print(f"  Resolution: {W}x{H}")

if __name__ == '__main__':
    print("=== Social Image Generator ===")
    generate()
    print("=== Done ===")
