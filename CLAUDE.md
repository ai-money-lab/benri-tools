# Money Machine OS v2.0

## Mission
人間の専門知識ゼロ・介入ゼロで自動収益を生むシステム。
Claude Code Agentが自律的にデータ収集→ツール生成→公開→改善を回す。

## 鉄則
1. 記事を書くな、データを作れ（事実の集積=一次情報）
2. 文章を売るな、ツールを売れ（便利さ=価値）
3. Google依存するな（X/YouTube/LINE分散集客）
4. AI記事量産しない（ペナルティ回避）
5. データとツールを蓄積（複利で増大）

## 技術スタック
- DB: SQLite (data/money_machine.db)
- ツール: HTML+CSS+JS 単一ファイル（output/tools/[slug]/index.html）
- スクレイピング: Python (scrapers/)
- 自動実行: cron + scripts/daily_run.sh
- Agent: サブエージェント + スラッシュコマンド + Hooks

## エージェント構成
- /daily-run → 日次自動運用（データ収集→HTML更新→画像生成）
- /build-tool → 新ツール自動生成
- /status → 全体ステータス確認
- /add-tool [slug] → 指定ツールを生成してDB登録

## サブエージェント
- data-harvester: データ収集特化
- tool-builder: Webツール生成特化
- social-poster: SNSコンテンツ生成特化
- optimizer: 分析・改善提案特化

## ファイル命名規則
- ツール: output/tools/[slug]/index.html
- 画像: output/social/YYYY-MM-DD_[type].png
- ログ: logs/daily_YYYY-MM-DD.log
- テンプレ: output/templates/notion/[name].md
