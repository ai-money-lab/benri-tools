# 家賃診断ツール デプロイガイド

## 1. Google Forms でデータ収集を設定する

### Step 1: Google Forms を作成
1. [Google Forms](https://forms.google.com) にアクセス
2. 「空白のフォーム」を新規作成
3. フォームタイトル: `家賃診断データ収集`

### Step 2: 以下の質問を追加（すべて「記述式」）
| 順番 | 質問テキスト | タイプ |
|------|-------------|--------|
| 1 | エリア | 記述式 |
| 2 | 家賃 | 記述式 |
| 3 | 年代 | 記述式 |
| 4 | 世帯年収 | 記述式 |
| 5 | 家族構成 | 記述式 |
| 6 | 満足度 | 記述式 |
| 7 | 重視ポイント | 記述式 |
| 8 | 診断スコア | 記述式 |
| 9 | 家賃比率 | 記述式 |

### Step 3: フォームURLとエントリIDを取得
1. フォームのプレビューを開く
2. ブラウザの「ページのソースを表示」
3. `entry.` で検索 → 各質問の `entry.XXXXXXXXX` をメモ
4. フォームURLの取得:
   - 編集画面のURL: `https://docs.google.com/forms/d/e/XXXXX/viewform`
   - 送信先URL: `https://docs.google.com/forms/d/e/XXXXX/formResponse`

### Step 4: diagnosis_tool に設定
`output/tools/rent-diagnosis/index.html` の以下の部分を編集:

```javascript
const GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/e/XXXXX/formResponse';
const ENTRY_IDS = {
  area: 'entry.123456789',
  rent: 'entry.234567890',
  age: 'entry.345678901',
  income: 'entry.456789012',
  family: 'entry.567890123',
  satisfaction: 'entry.678901234',
  priority: 'entry.789012345',
  score: 'entry.890123456',
  rentRatio: 'entry.901234567'
};
```

---

## 2. Cloudflare Pages にデプロイする

### 方法A: GitHub連携（推奨）
1. GitHubリポジトリに `output/tools/` をpush
2. [Cloudflare Dashboard](https://dash.cloudflare.com) → Pages
3. 「Create a project」→「Connect to Git」
4. リポジトリを選択
5. ビルド設定:
   - **ビルドコマンド**: なし（空欄）
   - **ビルド出力ディレクトリ**: `output/tools`
6. 「Save and Deploy」

### 方法B: ダイレクトアップロード
1. Cloudflare Dashboard → Pages → 「Create a project」
2. 「Direct Upload」を選択
3. `output/tools/` フォルダをドラッグ&ドロップ
4. プロジェクト名: `rockedge-tools`
5. デプロイ完了

### カスタムドメイン設定（任意）
1. Pages → プロジェクト → 「Custom domains」
2. サブドメイン例: `tools.rockedge.jp`

---

## 3. デプロイ後の確認チェックリスト

- [ ] フォームが正しく表示される
- [ ] 7問すべて回答できる
- [ ] 診断結果が即時表示される
- [ ] Xシェアボタンが動作する
- [ ] LINEシェアボタンが動作する
- [ ] コピーボタンが動作する
- [ ] Google Formsにデータが送信される
- [ ] スマホ表示が崩れない
- [ ] 関連ツールへのリンクが正しい

---

## 4. URL取得後のアクション

デプロイ完了後:
1. URLをコピー（例: `https://rockedge-tools.pages.dev/rent-diagnosis/`）
2. GitHub README.md に診断ツールへのリンクを追記
3. X/TikTok のプロフィールリンクに設定
