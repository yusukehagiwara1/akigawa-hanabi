# ファイル構成・依存関係ガイド

このサイトで「どのファイルを直すと、どこに反映されるか」をまとめたリファレンス。
Claude Code での修正時はこの依存関係を踏まえること。

---

## 最初に知っておく3点

1. **index.html だけが動的ページ** — microCMS（news / sponsors / gallery / testimonial / press / faq）と連動。残り15ページは静的。
2. **共通ファイルは全ページに波及** — `styles.css` / `ui.js` / `analytics.js` / `sponsor-urls.js` / `sw.js` の5つは全16ページが読み込む。1行直すと全ページに影響。
3. **サブページ本文は HTML を直接編集** — `_wp-content/*.json` や `generate.ps1` は初回生成用の道具。通常は使わない（後述）。

---

## フォルダ構成

```
ルート/
├ index.html              トップ（唯一の動的ページ・microCMS連動）
├ ticket / donation / event / access / company / qa / contact /
│  sponsor / pr / akiruno-kanko / food-application /
│  privacy-policy / 2024-hanabi .html   （13サブページ）
├ 404.html / offline.html  特殊ページ（generate対象外・手書き）
├ styles.css              全ページ共通スタイル
├ ui.js / analytics.js / sponsor-urls.js   全ページ共通JS
├ script.js / microcms-config.js / microcms-extras.js   index専用JS
├ sw.js                   Service Worker（CACHE_VERSION保持）
├ manifest.json / _headers / sitemap.xml / robots.txt
├ assets/                 共有画像（hero・logo・icon・past-NN 等）
│  ├ sponsors/            協賛ロゴ
│  └ wp/                  本文中の画像・PDF（130枚以上）
├ _wp-content/            ビルド資材（非公開）
│  ├ *.json (13本)        各サブページのソース
│  ├ generate.ps1         サブページHTML生成（※通常使わない）
│  ├ bump-cache.ps1       キャッシュ番号一括更新
│  ├ validate-site.ps1    公開前検証
│  └ _tools/              作業用バイナリ（.gitignore済み）
└ docs/                   運用ドキュメント
```

公開対象 = ルート直下のHTML/CSS/JS + assets。`_wp-content`・`docs` は非公開。

---

## 共有リソースの役割と影響範囲

| ファイル | 読込ページ | 役割 | 1行修正の影響 |
|---|---|---|---|
| `styles.css` | 全16 | 全ページ共通スタイル（サブページのcritical CSSはgenerate.ps1内に別途インライン） | 全ページの見た目 |
| `ui.js` | 全16 | ナビ開閉/SW更新トースト/カウントダウン/スクロール演出/数字カウントアップ/`?testMode=`プレビュー | 全ページの挙動 |
| `analytics.js` | 全16 | GA4（`G-GWF9DQCZQ3`）+ CTAクリック計測 + Web Vitals + スクロール深度 | 全ページの計測 |
| `sponsor-urls.js` | 全16 | 協賛ロゴ`<img>`をURL付きアンカーで包む（`SPONSOR_URL_MAP`） | index/sponsorで効く |
| `sw.js` | 全16 | Service Worker。HTML=network-first、静的=SWR。`CACHE_VERSION`保持 | 全ページのキャッシュ |
| `microcms-config.js` | index のみ | microCMS接続設定（serviceDomain/apiKey/endpoint） | トップの動的設定 |
| `script.js` | index のみ | microCMS `news` → トップ「最新情報」描画 | トップのnewsのみ |
| `microcms-extras.js` | index のみ | microCMS sponsors/gallery/testimonial/press/faq → トップ描画 | トップの該当部のみ |

---

## generate.ps1 と HTML直接編集（重要）

**現運用は「HTML直接編集」が正。`generate.ps1` は初回移行用で通常使わない。**

- 直近の全コミット（ラウンド群）が16HTMLを横断的に手編集している。
- `generate.ps1` の `$pages` 配列に **index / 404 / offline は含まれない**（＝手編集前提）。
- **`generate.ps1` を再実行すると13サブページがJSONから再構築され、手編集分が失われる。**
- 共通テンプレ（header/footer/CTA/サブページcritical CSS）を全サブページ一括変更したい場合のみ generate.ps1 のテンプレ編集が効率的だが、手編集分の喪失に注意。

### generate.ps1 の特殊変換関数（slug限定）
| 関数 | 対象 | 役割 |
|---|---|---|
| `Apply-TicketStaleGuard` | ticket | 旧予約リンク無効化→「販売準備中」通知へ |
| `Apply-AccessStaleGuard` | access | バス時刻表に前回情報の注記 |
| `Apply-SponsorAltFix` | sponsor | プレースホルダロゴのalt修正 |
| `Get-ContactBody` | contact | GoogleフォームCTA本文を差し込み |
| `Clean-Content` | 全13 | style/srcset除去・img遅延読込・wp URL→assets/wp/・jpg/png→webp・width/height注入 等 |

---

## 逆引きガイド「○○を変えたいとき」

| やりたいこと | 修正する場所 |
|---|---|
| 全ページの色・フォント・余白 | `styles.css`（＋サブページ初期表示はgenerate.ps1内インラインCSS） |
| 全ページのヘッダー/フッター/ナビ | 各HTML直接編集（または generate.ps1テンプレ） |
| トップの文言・構成 | `index.html` |
| サブページ本文 | その `<page>.html` を直接編集（JSON編集では反映されない） |
| お知らせ追加 | microCMS `news`（script.js経由でindexに自動反映） |
| 協賛ロゴ・URL・並び | microCMS `sponsors`。静的URLは `sponsor-urls.js` |
| 過去ギャラリー写真 | microCMS `gallery`（ローカル差替は microcms-extras.js の `GALLERY_IMAGE_OVERRIDES`） |
| 声/メディア/動的FAQ | microCMS `testimonial`/`press_release`/`faq_dynamic` |
| microCMS接続・件数 | `microcms-config.js` |
| GA4計測 | `analytics.js` |
| ナビ/カウントダウン挙動 | `ui.js`（全ページ） |
| カウントダウン目標日時 | 各HTMLの `data-countdown-target` 属性 |
| 共有画像 | `assets/` 直下（sw.jsのPRECACHE_URLSにも記載） |
| 本文中画像・PDF | `assets/wp/` |
| 協賛ロゴ画像 | `assets/sponsors/` |
| HTTPヘッダ | `_headers` |
| 旧キャッシュ破棄 | `_wp-content/bump-cache.ps1` 実行（全HTML `?v=` + sw.js `CACHE_VERSION`） |
| 公開前検証 | `_wp-content/validate-site.ps1` |

---

## 外部サービス依存（コード変更では変わらない）

- **microCMS**: `0k3w9bd30b.microcms.io`（news/sponsors/gallery/testimonial/press_release/faq_dynamic）
- **GA4**: `G-GWF9DQCZQ3`
- **お問い合わせ**: Googleフォーム（contact.html / Get-ContactBody 内にURL固定）
- **ホスティング(現行・暫定)**: Cloudflare Pages（GitHub `yusukehagiwara1/akigawa-hanabi` 連携・push自動デプロイ）
- **ホスティング(最終移行先)**: ConoHa（国内レンタルサーバー）。移行後は公開URLが独自ドメインに変わり、デプロイ手順も ConoHa 向けに変わる可能性がある（GitHub→自動公開が使えるとは限らない）。移行時はリダイレクト設定と microCMS 連携の動作確認が必要。
