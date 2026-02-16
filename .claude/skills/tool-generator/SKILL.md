---
name: tool-generator
description: Webツール（計算機・シミュレーター・チェッカー等）のHTML生成時に自動適用するスキル。
---

Webツール生成時は以下を必ず守る：
1. 1ファイル完結HTML（CSS+JSインライン）
2. レスポンシブ（320px〜1200px）
3. リアルタイム計算（oninput/onchange）
4. スライダー+数値入力
5. グラフはCanvas描画のみ
6. アフィリ枠 href="#"
7. SEOメタタグ
8. 注意文言
9. 白背景、モダンUI、カード型、shadow
10. 出力先：output/tools/[slug]/index.html
