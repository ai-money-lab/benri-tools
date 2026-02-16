---
name: data-scraper
description: Webスクレイピングでデータ収集しSQLiteに保存するスキル。料金比較データ収集時に自動適用。
---

データ収集時は以下を守る：
1. requests + BeautifulSoup使用
2. User-Agent設定必須
3. リクエスト間隔2秒以上
4. スクレイピング困難ならフォールバック辞書データ優先
5. data/money_machine.db に保存
6. 既存は is_current=0 → 新規 is_current=1
7. エラー時はスキップして続行
