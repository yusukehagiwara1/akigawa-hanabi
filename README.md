# 秋川流域花火大会サイト

## microCMS連携

`microcms-config.js` を編集すると、「最新情報と見どころ」のカードがmicroCMSの一覧APIから読み込まれます。

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

推奨フィールド:

- `title`: お知らせタイトル
- `publishedAt` または `date`: 日付
- `excerpt`、`description`、`body`: 本文の抜粋
- `url` または `link`: 任意のリンク先

ブラウザにAPIキーが見える構成なので、公開してよいGET専用キーを使ってください。キーを秘匿したい場合は、サーバー側でmicroCMSを呼び出す構成に変更してください。
