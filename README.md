# ROCKEDGE AI-OS — Money Machine

自動でデータを集め、コンテンツを生成し、収益化する仕組み。

## 公開ツール

### 診断ツール
| ツール | 説明 | リンク |
|--------|------|--------|
| **家賃適正診断** | 7問で家賃の適正度を無料診断 | [診断する](output/tools/rent-diagnosis/index.html) |

### 計算機・シミュレーター（全22ツール）
| ツール | リンク |
|--------|--------|
| 年収手取り計算機 | [使う](output/tools/salary-calculator/index.html) |
| 持ち家vs賃貸シミュレーター | [使う](output/tools/rent-vs-buy/index.html) |
| 住宅ローン計算機 | [使う](output/tools/loan-calculator/index.html) |
| ふるさと納税上限額計算機 | [使う](output/tools/furusato-tax/index.html) |
| 副業税金シミュレーター | [使う](output/tools/tax-calculator/index.html) |
| 積立NISAシミュレーター | [使う](output/tools/nisa-simulator/index.html) |
| 不動産投資利回り計算機 | [使う](output/tools/real-estate-yield/index.html) |
| その他15ツール | [一覧を見る](output/tools/index.html) |

## システム構成

```
診断ツール → Google Forms → スプレッドシート
                                    ↓
                            Apps Script (JSON変換)
                                    ↓
                GitHub Actions (週次同期) → data/raw_data.json
                                    ↓
                            data/summary.json → コンテンツ生成
                                    ↓
                        TikTok / X / note → 収益化
```

## ファイル構成

```
money-machine/
├── output/tools/          # 公開ツール（22ツール）
│   ├── rent-diagnosis/    # 家賃適正診断（NEW）
│   └── ...
├── output/reports/        # noteレポート原稿
├── data/
│   ├── raw_data.json      # 診断データ（自動更新）
│   ├── summary.json       # サマリー（自動更新）
│   ├── kpi_history.json   # KPI履歴（自動更新）
│   ├── rent_x_posts.json  # X投稿キュー
│   ├── posting_calendar.md # 投稿カレンダー
│   └── latest_content.md  # TikTok台本
├── scripts/               # 自動化スクリプト
├── .github/workflows/     # CI/CD
│   ├── daily-deploy.yml   # 毎日デプロイ
│   └── weekly-data-sync.yml # 週次データ同期
├── docs/                  # ドキュメント
├── WEEKLY_SOP.md          # 週次オペレーション手順
└── CLAUDE.md              # AI-OS設定
```

## KPIロードマップ

| Phase | データ数 | 月間収益 | HIROKI作業 |
|-------|---------|---------|-----------|
| **1 (現在)** | 0-100 | ¥0 | 週5分 |
| 2 | 100-500 | ¥30K-150K | 週5分 |
| 3 | 500-2000 | ¥150K-500K | 月30分 |
| 4 | 2000+ | ¥500K+ | 月15分 |

---

Powered by ROCKEDGE AI-OS
