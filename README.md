# akigawa-hanabi — 秋川流域花火大会 公式サイト 運用リポジトリ

公式サイトは WordPress(https://machizukuri-con.or.jp/ 、ConoHa WING)で運用しています。
このリポジトリは、その WordPress を更新するための **本文HTML・外部JS・作業スクリプトの置き場** です。

## 現在の役割

| パス | 用途 |
|---|---|
| `wp-snippets/seat-quiz.js` | チケットページの「座席診断」JS。本番の /ticket/ が `https://akigawa-hanabi.pages.dev/wp-snippets/seat-quiz.js` を読み込んでいる(WP側のWAFが本文内の `<script` を拒否するため外部配信) |
| `wp-snippets/ticket-page-content.html` ほか | WordPress の各ページ本文(REST API / ブロックエディタで流し込む元データ) |
| `wp-snippets/drafts/` | 2026-09 のサイト改善で追加した固定ページ(②〜⑬)の本文、点検スクリプト、委員会向け判断案 |
| `wp-snippets/plan/` | 「サイト改善計画表」(xlsx)と生成スクリプト |
| `_redirects` / `_headers` | Cloudflare Pages 用。旧静的サイトのURLを WordPress へ 301 転送し、`wp-snippets/` をCORS付きで配信 |
| `sw.js` | 旧静的サイトの Service Worker を訪問者のブラウザから消すための自己破棄版 |

## Cloudflare Pages(akigawa-hanabi.pages.dev)について

- 旧静的サイトは 2026-07-04 に運用終了。すべてのページは WordPress へ 301 転送されます。
- **プロジェクトを削除しないでください**。本番チケットページが `wp-snippets/seat-quiz.js` を参照しています。
  廃止する場合は、先に WordPress 側で JS の配信元を変更してください。
- `main` に push すると自動デプロイされます(約30秒)。

## 旧静的サイトの保管場所

2026-05〜07 に構築した静的サイト(HTML/CSS/JS、画像、ドキュメント、ConoHa 移行用 GitHub Actions)は
`main` から削除し、以下に残しています。今後使う予定はありません。

- ブランチ: `archive/static-site`
- タグ: `static-site-final`

## 整理の記録(2026-09-20)

- GitHub Actions の ConoHa デプロイ用 Secrets(FTP情報)と ConoHa 側の FTP アカウント `ghdeploy` を削除
- GitHub Organization `machizukuri-consortium`(未使用)を削除
- microCMS(旧静的サイトのニュース/協賛/ギャラリー)はエクスポート後に削除(保存先: OneDrive `花火大会_作業ファイル/アーカイブ_microCMS_20260920`)
- Netlify の空プロジェクトを削除
- ConoHa ホーム直下の `_old-static-site-20260704` を削除
