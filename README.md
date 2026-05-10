# 秋川流域花火大会 公式サイト

静的HTML/CSSで構築した秋川流域花火大会の公式サイトです。WordPress（machizukuri-con.or.jp）からコンテンツを移管し、Netlify上で運用しています。

- **公開URL**: https://akigawa-hanabi.pages.dev/
- **リポジトリ**: https://github.com/yusukehagiwara1/akigawa-hanabi
- **ホスティング**: Netlify（GitHub連携・自動デプロイ）

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
└── _wp-content/            WordPressから取得したJSONとビルドスクリプト
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

push後、Netlifyが自動的にビルドして数十秒〜1分でサイトに反映されます。

## サブページの再生成（WordPressコンテンツを再取得したい時）

`_wp-content/*.json` をWordPress REST APIから取り直して、サブページHTMLを生成し直します。

```powershell
cd _wp-content
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
