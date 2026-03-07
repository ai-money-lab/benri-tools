# Google Forms データ収集バックエンド セットアップ手順

## Step 1: Google Forms を作成

1. https://forms.google.com にアクセス
2. 「空白のフォーム」→ タイトル「家賃診断データ」
3. 以下の質問を **すべて「記述式（短文）」** で追加:

| # | 質問名 |
|---|--------|
| 1 | エリア |
| 2 | 家賃 |
| 3 | 年代 |
| 4 | 世帯年収 |
| 5 | 家族構成 |
| 6 | 満足度 |
| 7 | 重視ポイント |
| 8 | 診断スコア |
| 9 | 家賃比率 |

4. 回答を「スプレッドシートで表示」をONにする

## Step 2: entry ID を取得

1. フォームのプレビューを開く（目のアイコン）
2. `Ctrl+U`（ページのソース表示）
3. `entry.` で検索
4. 各質問に対応する `entry.XXXXXXXXX` を9個メモ

## Step 3: 診断ツールに設定

`output/tools/rent-diagnosis/index.html` 内の以下を書き換え:

```javascript
const GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/e/あなたのID/formResponse';
const ENTRY_IDS = {
  area: 'entry.XXXXXXXXX',       // エリア
  rent: 'entry.XXXXXXXXX',       // 家賃
  age: 'entry.XXXXXXXXX',        // 年代
  income: 'entry.XXXXXXXXX',     // 世帯年収
  family: 'entry.XXXXXXXXX',     // 家族構成
  satisfaction: 'entry.XXXXXXXXX',// 満足度
  priority: 'entry.XXXXXXXXX',   // 重視ポイント
  score: 'entry.XXXXXXXXX',      // 診断スコア
  rentRatio: 'entry.XXXXXXXXX'   // 家賃比率
};
```

## Step 4: Google Apps Script で JSON エクスポートを設定

1. 回答先スプレッドシートを開く
2. メニュー → 拡張機能 → Apps Script
3. `scripts/google_apps_script.js` の内容を貼り付け
4. トリガーを設定:
   - 関数: `exportToJSON`
   - イベントソース: 時間主導型
   - タイプ: 週ベース
   - 曜日: 月曜日
   - 時間: 午前6〜7時

## Step 5: GitHub Actions で自動取得

GitHub リポジトリの Settings → Secrets → Actions secrets に追加:
- `GSHEET_JSON_URL`: Apps Script で生成したJSON URL

ワークフロー `weekly-data-sync.yml` が毎週月曜に自動実行される。
