---
description: マネーマシン全体のステータスを表示
allowed-tools: Read, Bash, Glob, Grep
---

python scripts/status.py を実行して結果を表示。

status.py が存在しない場合は以下をPythonで直接実行して結果を表示：
1. python -c "import sqlite3; c=sqlite3.connect('data/money_machine.db').cursor(); c.execute('SELECT COUNT(*) FROM comparison_data WHERE is_current=1'); print(c.fetchone())"
2. python -c "import sqlite3; c=sqlite3.connect('data/money_machine.db').cursor(); c.execute('SELECT deploy_status, COUNT(*) FROM tools GROUP BY deploy_status'); print(c.fetchall())"
3. output/tools/ 以下のindex.htmlをGlobで一覧
4. output/social/ 以下の.pngをGlobで一覧
