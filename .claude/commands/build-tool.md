---
description: 新しいWebツールを自動生成。引数なしなら高単価アフィリ紐づきを自動選択。
allowed-tools: Read, Write, Bash, Glob, Grep, Task
---

$ARGUMENTSが空または未指定の場合：
data/money_machine.db の tools テーブルから deploy_status='not_started' のツールを取得。
affiliate_category が高単価（住宅ローン比較、不動産投資、保険相談、証券口座、転職サイト、資産運用）のものを優先して1つ選ぶ。

$ARGUMENTSが指定されている場合：
そのslugのツールを生成する。

生成仕様：
1. output/tools/[slug]/index.html に1ファイル完結HTML
2. CSS/JS全てインライン、外部依存ゼロ
3. レスポンシブ対応（min-width:320px〜max-width:1200px）
4. リアルタイム計算（oninput/onchangeで即更新）
5. スライダー+数値入力のハイブリッドUI
6. グラフはCanvas描画（外部ライブラリ不使用）
7. アフィリエイトリンク枠 href="#" で設置
8. SEOメタタグ（title, meta description, og:title, og:description）
9. 注意文言「この計算は概算です。正確な情報は専門家にご相談ください。」
10. デザイン：白背景、モダン、カード型UI、box-shadow付き
11. カラー：金融系=グリーン/ネイビー、健康系=グリーン、生活系=ブルー

生成後の処理：
1. sqlite3でDBの当該ツールの deploy_status を 'draft' に UPDATE
2. file_path を実際のファイルパスに UPDATE
3. ファイルサイズとパスを報告
