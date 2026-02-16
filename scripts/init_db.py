#!/usr/bin/env python3
"""Money Machine DB初期化スクリプト"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'money_machine.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. keywords
    c.execute('''CREATE TABLE IF NOT EXISTS keywords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT,
        search_volume INTEGER,
        competition TEXT,
        category TEXT,
        status TEXT DEFAULT 'new',
        tool_type TEXT,
        expected_revenue REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    # 2. tools
    c.execute('''CREATE TABLE IF NOT EXISTS tools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        slug TEXT UNIQUE,
        keyword_id INTEGER,
        category TEXT,
        file_path TEXT,
        deploy_url TEXT,
        deploy_status TEXT DEFAULT 'not_started',
        monthly_pv INTEGER DEFAULT 0,
        monthly_revenue REAL DEFAULT 0,
        affiliate_category TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    # 3. comparison_data
    c.execute('''CREATE TABLE IF NOT EXISTS comparison_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        provider TEXT,
        plan_name TEXT,
        price REAL,
        data_gb REAL,
        data_json TEXT,
        source_url TEXT,
        scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_current BOOLEAN DEFAULT 1
    )''')

    # 4. social_posts
    c.execute('''CREATE TABLE IF NOT EXISTS social_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT,
        content_type TEXT,
        content_text TEXT,
        media_path TEXT,
        status TEXT DEFAULT 'draft',
        scheduled_at DATETIME,
        posted_at DATETIME,
        impressions INTEGER DEFAULT 0,
        clicks INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    # 5. revenue
    c.execute('''CREATE TABLE IF NOT EXISTS revenue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE,
        source TEXT,
        category TEXT,
        amount REAL,
        currency TEXT DEFAULT 'JPY',
        notes TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    # 6. templates
    c.execute('''CREATE TABLE IF NOT EXISTS templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        description TEXT,
        price REAL,
        file_path TEXT,
        platform TEXT,
        sales_count INTEGER DEFAULT 0,
        total_revenue REAL DEFAULT 0,
        status TEXT DEFAULT 'draft',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    # ツール候補50個を一括INSERT
    tools_data = [
        ('年収手取り計算機', 'salary-calculator', 'calculator', '転職サイト'),
        ('退職金計算シミュレーター', 'retirement-calculator', 'simulator', '資産運用'),
        ('電気代計算ツール', 'electricity-cost', 'calculator', '電力比較'),
        ('引越し費用シミュレーター', 'moving-cost', 'simulator', '引越し見積もり'),
        ('通信費節約シミュレーター', 'telecom-savings', 'simulator', '格安SIM'),
        ('生命保険必要額シミュレーター', 'insurance-calculator', 'simulator', '保険相談'),
        ('老後資金シミュレーター', 'retirement-fund', 'simulator', '資産運用'),
        ('教育費シミュレーター', 'education-cost', 'simulator', '学資保険'),
        ('投資リターン計算機', 'investment-return', 'calculator', '証券口座'),
        ('複利計算シミュレーター', 'compound-interest', 'simulator', 'NISA口座'),
        ('積立NISAシミュレーター', 'nisa-simulator', 'simulator', 'NISA口座'),
        ('家賃vs購入比較', 'rent-vs-buy', 'simulator', '不動産査定'),
        ('不動産投資利回り計算機', 'real-estate-yield', 'calculator', '不動産投資'),
        ('ふるさと納税上限額計算機', 'furusato-tax', 'calculator', 'ふるさと納税'),
        ('確定申告要否チェッカー', 'tax-return-checker', 'checker', '確定申告ソフト'),
        ('扶養内パート収入シミュレーター', 'part-time-income', 'simulator', 'パート求人'),
        ('失業保険計算機', 'unemployment-benefit', 'calculator', '転職サイト'),
        ('育休給付金シミュレーター', 'childcare-leave', 'simulator', 'ベビー用品'),
        ('年金受給額シミュレーター', 'pension-calculator', 'simulator', '資産運用'),
        ('車維持費シミュレーター', 'car-cost', 'simulator', '自動車保険'),
        ('ガソリン代計算機', 'gas-cost', 'calculator', 'カーリース'),
        ('Wi-Fi速度チェッカー', 'wifi-speed-checker', 'checker', '光回線'),
        ('英語レベル診断', 'english-level-test', 'checker', '英語学習'),
        ('タイピング速度テスト', 'typing-speed-test', 'checker', 'パソコンスクール'),
        ('睡眠時間計算機', 'sleep-calculator', 'calculator', 'マットレス'),
        ('文字数カウンター', 'character-counter', 'checker', 'ライティングツール'),
        ('パスワード強度チェッカー', 'password-checker', 'checker', 'VPN'),
        ('QRコード生成器', 'qr-generator', 'generator', '名刺印刷'),
        ('画像リサイズツール', 'image-resizer', 'converter', '画像編集ソフト'),
        ('単位変換ツール', 'unit-converter', 'converter', 'なし'),
        ('和暦西暦変換', 'era-converter', 'converter', 'なし'),
        ('割引率計算機', 'discount-calculator', 'calculator', 'クーポンサイト'),
        ('割り勘計算機', 'split-bill', 'calculator', 'キャッシュレス'),
        ('出産費用シミュレーター', 'birth-cost', 'simulator', '保険'),
        ('ペット生涯費用シミュレーター', 'pet-cost', 'simulator', 'ペット保険'),
        ('結婚式費用シミュレーター', 'wedding-cost', 'simulator', 'ブライダル'),
        ('旅行予算シミュレーター', 'travel-budget', 'simulator', '旅行予約'),
        ('ダイエット期間シミュレーター', 'diet-period', 'simulator', 'ジム'),
        ('プロテイン摂取量計算機', 'protein-calculator', 'calculator', 'プロテイン'),
        ('ランニングペース計算機', 'running-pace', 'calculator', 'ランニングシューズ'),
        ('年齢計算ツール', 'age-calculator', 'calculator', 'なし'),
        ('日数計算ツール', 'date-calculator', 'calculator', 'なし'),
        ('時差計算ツール', 'timezone-converter', 'converter', '海外WiFi'),
        ('通貨換算ツール', 'currency-converter', 'converter', '海外送金'),
        ('固定費見直しチェッカー', 'fixed-cost-checker', 'checker', '家計相談'),
        ('水道光熱費シミュレーター', 'utility-cost', 'simulator', '電力ガス比較'),
        ('配当金利回り計算機', 'dividend-yield', 'calculator', '証券口座'),
        ('FX損益計算機', 'fx-calculator', 'calculator', 'FX口座'),
        ('BMI計算機', 'bmi-calculator', 'calculator', 'ジム'),
        ('住宅ローン計算機', 'loan-calculator', 'calculator', '住宅ローン比較'),
    ]

    for name, slug, category, affiliate_cat in tools_data:
        c.execute('''INSERT OR IGNORE INTO tools (name, slug, category, affiliate_category, deploy_status)
                      VALUES (?, ?, ?, ?, 'not_started')''',
                  (name, slug, category, affiliate_cat))

    conn.commit()

    # 確認
    for table in ['keywords', 'tools', 'comparison_data', 'social_posts', 'revenue', 'templates']:
        c.execute(f'SELECT COUNT(*) FROM {table}')
        count = c.fetchone()[0]
        print(f"  {table}: {count} records")

    conn.close()
    print(f"\nDB initialized: {os.path.abspath(DB_PATH)}")

if __name__ == '__main__':
    print("=== Money Machine DB Init ===")
    init_db()
    print("=== Done ===")
