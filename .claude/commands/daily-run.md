---
description: 日次自動運用。データ収集→HTML更新→画像生成→ステータス確認。
allowed-tools: Read, Write, Bash, Glob, Grep, Task
---

python scripts/daily_run.py を実行して結果を報告して。

daily_run.py が存在しない場合は以下を順番に実行（各ステップが失敗しても次に進む）：
1. python scrapers/sim_scraper.py
2. python generators/comparison_generator.py
3. python generators/social_image_generator.py
4. python scripts/generate_site_index.py
5. python scripts/status.py

全ステップの結果をまとめて報告して。
