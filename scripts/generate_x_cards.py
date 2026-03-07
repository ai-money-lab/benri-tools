"""X投稿用OGP画像を生成するスクリプト"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

# Paths
BASE = Path(r"C:\Users\maulo\OneDrive\マネタイズキット\money-machine")
QUEUE = BASE / "data" / "x_post_queue.json"
OUT_DIR = BASE / "output" / "social" / "x_cards"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Fonts
FONT_BOLD = "C:/Windows/Fonts/NotoSansJP-VF.ttf"
FONT_REG = "C:/Windows/Fonts/NotoSansJP-VF.ttf"

# Image size (Twitter card: 1200x675)
W, H = 1200, 675

# Color palettes for variety
PALETTES = [
    {"bg1": (15, 23, 42), "bg2": (30, 58, 138), "accent": (59, 130, 246), "text": (255, 255, 255), "sub": (148, 163, 184), "highlight": (250, 204, 21)},   # Dark blue + yellow
    {"bg1": (17, 24, 39), "bg2": (88, 28, 135), "accent": (168, 85, 247), "text": (255, 255, 255), "sub": (167, 139, 250), "highlight": (52, 211, 153)},    # Purple + green
    {"bg1": (20, 20, 20), "bg2": (30, 30, 30), "accent": (239, 68, 68), "text": (255, 255, 255), "sub": (163, 163, 163), "highlight": (252, 165, 165)},     # Dark + red
    {"bg1": (7, 89, 133), "bg2": (12, 74, 110), "accent": (14, 165, 233), "text": (255, 255, 255), "sub": (186, 230, 253), "highlight": (253, 224, 71)},    # Sky blue + yellow
    {"bg1": (30, 41, 59), "bg2": (51, 65, 85), "accent": (16, 185, 129), "text": (255, 255, 255), "sub": (148, 163, 184), "highlight": (110, 231, 183)},    # Slate + emerald
    {"bg1": (24, 24, 27), "bg2": (39, 39, 42), "accent": (244, 114, 182), "text": (255, 255, 255), "sub": (161, 161, 170), "highlight": (251, 191, 36)},    # Zinc + pink
    {"bg1": (15, 23, 42), "bg2": (30, 41, 59), "accent": (251, 146, 60), "text": (255, 255, 255), "sub": (148, 163, 184), "highlight": (253, 186, 116)},    # Dark + orange
]

# Card data: (id, headline, subline, number)
CARDS = [
    ("v3_17", "固定費を月1万削るだけで", "年12万、10年で120万浮く", "120万円"),
    ("v3_18", "育休中にもらえるお金", "月給30万なら月20万+一時金115万", "+200万超"),
    ("v3_19", "車の年間維持費", "軽自動車でも年約40万、10年で400万", "年40万円"),
    ("v3_20", "知らないだけで損してる", "お金で損してる人の共通点5つ", "5つの罠"),
    ("v3_21", "20代で絶対やるべき", "お金のこと。30代で気づくと10年分の損", "5つの鉄則"),
    ("v3_22", "同じ年収800万でも", "共働きvs片働きで手取りが変わる", "40万円差"),
    ("v3_23", "ボーナスの手取り", "額面50万→手取り40万。2〜3割消える", "−20%"),
    ("v3_24", "月3万を30年積み立て", "年利5%の複利で元本の2.3倍に", "2,497万"),
    ("v3_25", "年収1000万の手取り", "月の手取りはいくら？意外と少ない", "月60万"),
    ("v3_26", "AIにツール21個作らせた", "コード0行。開発費0円。全部自動生成", "開発費 ¥0"),
    ("v3_27", "無料ツール21個", "お金の計算が全部3秒でできる", "全21個"),
    ("v3_28", "新NISAの節税額", "月3万×20年で非課税メリット", "104万円"),
    ("v3_29", "退職金の相場", "大企業vs中小企業、勤続20年で大差", "600万差"),
    ("v3_30", "電力会社を変えるだけ", "手続き10分、工事なし、解約金なし", "年1.4万節約"),
]


def load_font(path, size, variation=None):
    """Load font with specified size and optional variation."""
    try:
        font = ImageFont.truetype(path, size)
        if variation:
            try:
                font.set_variation_by_name(variation)
            except Exception:
                pass
        return font
    except Exception:
        return ImageFont.load_default()


def draw_gradient(draw, w, h, c1, c2, vertical=True):
    """Draw a gradient background."""
    for i in range(h if vertical else w):
        ratio = i / (h if vertical else w)
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        if vertical:
            draw.line([(0, i), (w, i)], fill=(r, g, b))
        else:
            draw.line([(i, 0), (i, h)], fill=(r, g, b))


def draw_decorative_elements(draw, palette, style_idx):
    """Draw decorative geometric elements."""
    accent = palette["accent"]
    # Subtle circles
    alpha_color = (*accent, 30)
    if style_idx % 3 == 0:
        # Top-right circle
        draw.ellipse([W-200, -100, W+100, 200], outline=(*accent, 80), width=2)
        draw.ellipse([W-150, -50, W+50, 150], outline=(*accent, 40), width=1)
        # Bottom-left circle
        draw.ellipse([-100, H-200, 200, H+100], outline=(*accent, 80), width=2)
    elif style_idx % 3 == 1:
        # Diagonal lines
        for offset in range(-200, W+200, 80):
            draw.line([(offset, 0), (offset+200, H)], fill=(*accent, 25), width=1)
    else:
        # Dots grid
        for x in range(50, W, 60):
            for y in range(50, H, 60):
                draw.ellipse([x-1, y-1, x+1, y+1], fill=(*accent, 30))


def draw_text_wrapped(draw, text, font, max_width, x, y, fill):
    """Draw text with word wrapping for Japanese text."""
    chars = list(text)
    lines = []
    current = ""
    for ch in chars:
        test = current + ch
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] > max_width and current:
            lines.append(current)
            current = ch
        else:
            current = test
    if current:
        lines.append(current)

    current_y = y
    for line in lines:
        draw.text((x, current_y), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        current_y += (bbox[3] - bbox[1]) + 8
    return current_y


def generate_card(card_data, palette_idx):
    """Generate a single card image."""
    post_id, headline, subline, number = card_data
    palette = PALETTES[palette_idx % len(PALETTES)]

    # Create base image
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # Gradient background
    draw_gradient(draw, W, H, palette["bg1"], palette["bg2"])

    # Decorative elements
    draw_decorative_elements(draw, palette, palette_idx)

    # Accent bar on left
    draw.rectangle([0, 0, 6, H], fill=palette["accent"])

    # Load fonts
    font_number = load_font(FONT_BOLD, 96, "Black")
    font_headline = load_font(FONT_BOLD, 44, "Bold")
    font_sub = load_font(FONT_REG, 28, "Regular")
    font_brand = load_font(FONT_REG, 22, "Medium")
    font_tag = load_font(FONT_BOLD, 18, "Bold")

    # Layout
    pad_x = 80
    content_w = W - pad_x * 2

    # Top tag
    tag_text = "Claude AI 副業ラボ"
    tag_bbox = draw.textbbox((0, 0), tag_text, font=font_tag)
    tag_w = tag_bbox[2] - tag_bbox[0] + 24
    tag_h = tag_bbox[3] - tag_bbox[1] + 12
    draw.rounded_rectangle(
        [pad_x, 40, pad_x + tag_w, 40 + tag_h],
        radius=4,
        fill=(*palette["accent"], 180)
    )
    draw.text((pad_x + 12, 43), tag_text, font=font_tag, fill=(255, 255, 255))

    # Big number (right-aligned, slightly transparent)
    num_bbox = draw.textbbox((0, 0), number, font=font_number)
    num_w = num_bbox[2] - num_bbox[0]
    num_x = W - pad_x - num_w
    num_y = 120

    # Number shadow
    draw.text((num_x + 3, num_y + 3), number, font=font_number, fill=(0, 0, 0))
    draw.text((num_x, num_y), number, font=font_number, fill=palette["highlight"])

    # Headline
    headline_y = 280
    draw_text_wrapped(draw, headline, font_headline, content_w, pad_x, headline_y, palette["text"])

    # Subline
    sub_y = 380
    draw_text_wrapped(draw, subline, font_sub, content_w, pad_x, sub_y, palette["sub"])

    # Bottom separator line
    draw.line([(pad_x, H - 80), (W - pad_x, H - 80)], fill=(*palette["accent"], 100), width=1)

    # Bottom branding
    brand_text = "ai-money-lab.github.io/benri-tools"
    draw.text((pad_x, H - 60), brand_text, font=font_brand, fill=palette["sub"])

    # Free tag on bottom right
    free_text = "無料・登録不要"
    free_bbox = draw.textbbox((0, 0), free_text, font=font_tag)
    free_w = free_bbox[2] - free_bbox[0] + 20
    free_h = free_bbox[3] - free_bbox[1] + 10
    free_x = W - pad_x - free_w
    draw.rounded_rectangle(
        [free_x, H - 68, free_x + free_w, H - 68 + free_h],
        radius=4,
        fill=palette["accent"]
    )
    draw.text((free_x + 10, H - 66), free_text, font=font_tag, fill=(255, 255, 255))

    # Save
    out_path = OUT_DIR / f"{post_id}.png"
    img.save(out_path, "PNG", optimize=True)
    return out_path


def main():
    print(f"Generating {len(CARDS)} X post cards...")
    for i, card in enumerate(CARDS):
        path = generate_card(card, i)
        print(f"  [{i+1}/{len(CARDS)}] {card[0]}: {path.name}")
    print(f"\nDone! Cards saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()
