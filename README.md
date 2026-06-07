# 秋川流域花火大会 公式サイト

静的HTML/CSSで構築した秋川流域花火大会の公式サイトです。WordPress（machizukuri-con.or.jp）からコンテンツを移管し、Cloudflare Pages 上で運用しています。

- **公開URL**: https://akigawa-hanabi.pages.dev/
- **リポジトリ**: https://github.com/yusukehagiwara1/akigawa-hanabi
- **ホスティング**: Cloudflare Pages（GitHub連携・自動デプロイ、無料枠で運用）
- **GA4 測定ID**: `G-GWF9DQCZQ3`
- **microCMS**: news / sponsors / gallery / testimonial / press / faq の各 API

## ディレクトリ構成

```
.
├── index.html              トップページ
├── *.html                  各サブページ（チケット/寄付/アクセス/FAQ/協賛企業 ほか計15ページ）
├── 404.html                Not Foundページ
├── styles.css              共通スタイル
├── analytics.js            Google Analytics 4 + クリック計測
├── microcms-config.js      microCMS連携設定（任意）
├── script.js               microCMSニュース取得スクリプト
├── sitemap.xml             検索エンジン向けサイトマップ
├── robots.txt
├── assets/
│   ├── hero-fireworks-real.jpg
│   ├── keyvisual.jpg
│   ├── past-*.jpg, sponsors/, wp/  などの画像・PDF
│   └── favicon.ico
└── _build/            WordPressから取得したJSONとビルドスクリプト
    ├── *.json              各ページのコンテンツソース
    └── generate.ps1        サブページHTMLの再生成スクリプト
```

## 編集とデプロイ

通常の編集は `index.html` 等を直接書き換え、git push で自動反映されます。

```powershell
git add .
git commit -m "変更内容"
git push
```

push後、Cloudflare Pages が自動的にビルドして約30秒でサイトに反映されます。

## サブページの再生成（WordPressコンテンツを再取得したい時）

`_build/*.json` をWordPress REST APIから取り直して、サブページHTMLを生成し直します。

```powershell
cd _build
.\generate.ps1
cd ..

git add .
git commit -m "Refresh sub-page content"
git push
```

## Google Analytics 4

- 測定ID: `analytics.js` 5行目に記述（`G-GWF9DQCZQ3`）
- カスタムイベント: `cta_click`（自動でCTAリンククリックを記録）
- カスタムディメンション: `cta_label` / `cta_area` / `cta_type` / `cta_destination`

## microCMS連携（任意）

`microcms-config.js` を編集すると、トップページの「最新情報と見どころ」がmicroCMSの一覧APIから読み込まれます。

```js
window.MICROCMS_CONFIG = {
  serviceDomain: "YOUR_SERVICE_DOMAIN",
  apiKey: "YOUR_GET_ONLY_API_KEY",
  endpoint: "news",
  limit: 3,
};
```

- `serviceDomain`: `https://example.microcms.io` の `example` 部分
- `apiKey`: コンテンツAPIのGETだけを許可したAPIキー
- `endpoint`: microCMSで作成したAPIのエンドポイント名

ブラウザにAPIキーが見える構成なので、公開してよいGET専用キーを使ってください。キーを秘匿したい場合は、サーバー側でmicroCMSを呼び出す構成に変更してください。

## 主要ファイル概要

| ファイル | 役割 |
|---|---|
| `_headers` | Cloudflare Pages 用 HTTP ヘッダー設定（セキュリティ・キャッシュ） |
| `sw.js` | Service Worker（オフライン対応・静的アセットキャッシュ） |
| `offline.html` | オフライン時の専用 fallback ページ |
| `ui.js` | ナビゲーション・ハンバーガー・カウントダウン・テストモード等 |
| `analytics.js` | GA4 + CTA トラッキング + Web Vitals + スクロール深度計測 |
| `microcms-extras.js` | microCMS の sponsors/gallery/testimonial/press/faq 取得 |

## 関連ドキュメント

詳細な運用手順は `docs/` ディレクトリ参照：

- `docs/BACKLOG.md` — 未完タスク + 完了済ラウンドの履歴
- `docs/RELEASE_RUNBOOK.md` — リリース手順
- `docs/QA_CHECKLIST.md` — 動作確認チェックリスト（テストモード `?testMode=...` も含む）
- `docs/INCIDENT_RUNBOOK.md` — 障害対応
- `docs/WEB_STRATEGY_2026.md` — 2026 年の Web 戦略
- `docs/LOOKER_STUDIO_SETUP.md` — GA4 ダッシュボード構築
- `docs/MONTHLY_REPORT_TEMPLATE.md` — 月次レポートテンプレ
