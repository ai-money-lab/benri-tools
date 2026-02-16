#!/usr/bin/env python3
"""格安SIM料金データ収集スクリプト（フォールバック辞書優先）"""
import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'money_machine.db')

# 2025-2026年時点の主要格安SIM料金データ（税込）
FALLBACK_DATA = [
    # 楽天モバイル
    {"provider": "楽天モバイル", "plan_name": "Rakuten最強プラン 〜3GB", "price": 1078, "data_gb": 3.0,
     "data_json": json.dumps({"call": "Rakuten Link無料", "feature": "データ無制限可能、楽天ポイント還元"}, ensure_ascii=False)},
    {"provider": "楽天モバイル", "plan_name": "Rakuten最強プラン 3〜20GB", "price": 2178, "data_gb": 20.0,
     "data_json": json.dumps({"call": "Rakuten Link無料", "feature": "段階制料金、自動で最適プラン"}, ensure_ascii=False)},
    {"provider": "楽天モバイル", "plan_name": "Rakuten最強プラン 20GB〜無制限", "price": 3278, "data_gb": 999.0,
     "data_json": json.dumps({"call": "Rakuten Link無料", "feature": "データ無制限、テザリング無制限"}, ensure_ascii=False)},
    # ahamo
    {"provider": "ahamo", "plan_name": "ahamo 20GB", "price": 2970, "data_gb": 20.0,
     "data_json": json.dumps({"call": "5分かけ放題込み", "feature": "ドコモ回線、海外82カ国対応"}, ensure_ascii=False)},
    {"provider": "ahamo", "plan_name": "ahamo大盛り 100GB", "price": 4950, "data_gb": 100.0,
     "data_json": json.dumps({"call": "5分かけ放題込み", "feature": "大容量100GB、テザリング可"}, ensure_ascii=False)},
    # LINEMO
    {"provider": "LINEMO", "plan_name": "ミニプラン 3GB", "price": 990, "data_gb": 3.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "LINEギガフリー、ソフトバンク回線"}, ensure_ascii=False)},
    {"provider": "LINEMO", "plan_name": "スマホプラン 20GB", "price": 2728, "data_gb": 20.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "LINEギガフリー、ソフトバンク回線"}, ensure_ascii=False)},
    {"provider": "LINEMO", "plan_name": "ベストプラン 3GB", "price": 990, "data_gb": 3.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "2024年新プラン、段階制"}, ensure_ascii=False)},
    # povo
    {"provider": "povo", "plan_name": "povo2.0 基本料", "price": 0, "data_gb": 0.0,
     "data_json": json.dumps({"call": "別途トッピング", "feature": "基本料0円、必要な時だけトッピング"}, ensure_ascii=False)},
    {"provider": "povo", "plan_name": "povo2.0 3GB/30日", "price": 990, "data_gb": 3.0,
     "data_json": json.dumps({"call": "別途トッピング", "feature": "au回線、30日有効"}, ensure_ascii=False)},
    {"provider": "povo", "plan_name": "povo2.0 20GB/30日", "price": 2700, "data_gb": 20.0,
     "data_json": json.dumps({"call": "別途トッピング", "feature": "au回線、30日有効"}, ensure_ascii=False)},
    {"provider": "povo", "plan_name": "povo2.0 60GB/90日", "price": 6490, "data_gb": 60.0,
     "data_json": json.dumps({"call": "別途トッピング", "feature": "au回線、90日有効、月あたり約2163円"}, ensure_ascii=False)},
    # UQモバイル
    {"provider": "UQモバイル", "plan_name": "ミニミニプラン 4GB", "price": 2365, "data_gb": 4.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "au回線、節約モードあり"}, ensure_ascii=False)},
    {"provider": "UQモバイル", "plan_name": "トクトクプラン 15GB", "price": 3465, "data_gb": 15.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "au回線、1GB以下は割引"}, ensure_ascii=False)},
    {"provider": "UQモバイル", "plan_name": "コミコミプラン 20GB", "price": 3278, "data_gb": 20.0,
     "data_json": json.dumps({"call": "10分かけ放題込み", "feature": "au回線、通話込みでお得"}, ensure_ascii=False)},
    # ワイモバイル
    {"provider": "ワイモバイル", "plan_name": "シンプル2 S 4GB", "price": 2365, "data_gb": 4.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "ソフトバンク回線、家族割あり"}, ensure_ascii=False)},
    {"provider": "ワイモバイル", "plan_name": "シンプル2 M 20GB", "price": 4015, "data_gb": 20.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "ソフトバンク回線、データ繰越可"}, ensure_ascii=False)},
    {"provider": "ワイモバイル", "plan_name": "シンプル2 L 30GB", "price": 5115, "data_gb": 30.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "ソフトバンク回線、大容量"}, ensure_ascii=False)},
    # IIJmio
    {"provider": "IIJmio", "plan_name": "2ギガプラン", "price": 850, "data_gb": 2.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "ドコモ/au回線選択可、老舗MVNO"}, ensure_ascii=False)},
    {"provider": "IIJmio", "plan_name": "5ギガプラン", "price": 990, "data_gb": 5.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "データ繰越可、eSIM対応"}, ensure_ascii=False)},
    {"provider": "IIJmio", "plan_name": "10ギガプラン", "price": 1500, "data_gb": 10.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "データシェア可能"}, ensure_ascii=False)},
    {"provider": "IIJmio", "plan_name": "15ギガプラン", "price": 1800, "data_gb": 15.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "コスパ良好"}, ensure_ascii=False)},
    {"provider": "IIJmio", "plan_name": "20ギガプラン", "price": 2000, "data_gb": 20.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "大容量でも低価格"}, ensure_ascii=False)},
    # mineo
    {"provider": "mineo", "plan_name": "マイピタ 1GB", "price": 1298, "data_gb": 1.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "ドコモ/au/ソフトバンク回線"}, ensure_ascii=False)},
    {"provider": "mineo", "plan_name": "マイピタ 5GB", "price": 1518, "data_gb": 5.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "パケット放題Plus対応"}, ensure_ascii=False)},
    {"provider": "mineo", "plan_name": "マイピタ 10GB", "price": 1958, "data_gb": 10.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "フリータンク利用可"}, ensure_ascii=False)},
    {"provider": "mineo", "plan_name": "マイピタ 20GB", "price": 2178, "data_gb": 20.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "パケット放題Plus無料"}, ensure_ascii=False)},
    {"provider": "mineo", "plan_name": "マイそく スタンダード", "price": 990, "data_gb": 999.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "最大1.5Mbpsで使い放題"}, ensure_ascii=False)},
    # 日本通信SIM
    {"provider": "日本通信SIM", "plan_name": "合理的シンプル290 1GB", "price": 290, "data_gb": 1.0,
     "data_json": json.dumps({"call": "11円/30秒", "feature": "業界最安級、ドコモ回線"}, ensure_ascii=False)},
    {"provider": "日本通信SIM", "plan_name": "合理的みんなのプラン 10GB", "price": 1390, "data_gb": 10.0,
     "data_json": json.dumps({"call": "70分無料通話込み", "feature": "通話込みでお得"}, ensure_ascii=False)},
    {"provider": "日本通信SIM", "plan_name": "合理的30GBプラン", "price": 2178, "data_gb": 30.0,
     "data_json": json.dumps({"call": "70分無料通話込み", "feature": "大容量＋通話付き"}, ensure_ascii=False)},
    # NUROモバイル
    {"provider": "NUROモバイル", "plan_name": "VSプラン 3GB", "price": 792, "data_gb": 3.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "ソニー系、バリューデータフリー"}, ensure_ascii=False)},
    {"provider": "NUROモバイル", "plan_name": "VMプラン 5GB", "price": 990, "data_gb": 5.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "Gigaプラスで3ヶ月毎+3GB"}, ensure_ascii=False)},
    {"provider": "NUROモバイル", "plan_name": "VLプラン 10GB", "price": 1485, "data_gb": 10.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "Gigaプラスで3ヶ月毎+6GB"}, ensure_ascii=False)},
    {"provider": "NUROモバイル", "plan_name": "NEOプラン 20GB", "price": 2699, "data_gb": 20.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "NEOデータフリー、あげ放題"}, ensure_ascii=False)},
    {"provider": "NUROモバイル", "plan_name": "NEOプランW 40GB", "price": 3980, "data_gb": 40.0,
     "data_json": json.dumps({"call": "別途オプション", "feature": "大容量、NEOデータフリー"}, ensure_ascii=False)},
]

def run_scraper():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 既存データをis_current=0に
    c.execute("UPDATE comparison_data SET is_current = 0 WHERE category = 'sim'")

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    inserted = 0

    for plan in FALLBACK_DATA:
        c.execute('''INSERT INTO comparison_data
                     (category, provider, plan_name, price, data_gb, data_json, source_url, scraped_at, is_current)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)''',
                  ('sim', plan['provider'], plan['plan_name'], plan['price'],
                   plan['data_gb'], plan['data_json'], 'fallback_dictionary', now))
        inserted += 1

    conn.commit()

    # 確認
    c.execute("SELECT COUNT(*) FROM comparison_data WHERE is_current = 1 AND category = 'sim'")
    current = c.fetchone()[0]
    c.execute("SELECT COUNT(DISTINCT provider) FROM comparison_data WHERE is_current = 1 AND category = 'sim'")
    providers = c.fetchone()[0]

    conn.close()

    print(f"  Inserted: {inserted} plans")
    print(f"  Current active: {current} plans from {providers} providers")

if __name__ == '__main__':
    print("=== SIM Scraper (Fallback Data) ===")
    run_scraper()
    print("=== Done ===")
