# プロジェクトバックログ

未完タスク・将来検討タスクの整理。優先度はビジネスインパクトベース。

最終更新: 2026-05-15

---

## 🔴 高優先（運営側情報待ち、確定したら即着手）

| ID | タスク | 待ち事項 | 想定工数 |
|---|---|---|---|
| H1 | 第8回の確定席種・価格をサイトへ反映 | 運営側で席種・価格・販売開始日確定 | 0.5 day |
| H2 | 第8回のチケット販売 URL を 8 箇所に貼り直し | KKday / アソビューに第8回商品が登録される | 1 hour |
| H3 | testimonial CMS に実体験談を 3-6 件投入 | 運営側で過去来場者のレビュー集め | -（運営側のみ） |
| H4 | LINE 公式アカウント開設後に friend 追加 URL を index.html に反映 | 運営側で LINE 公式開設 | 30 min |
| H5 | Google フォーム メール登録運用開始 | 運営側でフォーム作成 | 30 min |
| H6 | 寄付・協賛 PDF を第8回版に差し替え | 第8回 PDF 作成 | 30 min |

## 🟡 中優先（自律的に進められる）

| ID | タスク | 効果 | 想定工数 |
|---|---|---|---|
| M4 | スポンサーロゴ毎の hover で企業説明 tooltip | UX | 2 hours |

## 🟢 低優先（やれたらやる）

| ID | タスク | 効果 |
|---|---|---|
| L1 | 開催実績数値を CMS 化 | 運営側で更新できる |
| ~~L2~~ | ~~カウントダウンの「N時間」「N分」表示（直前期）~~ | ✅ 完了 (Round 21) |
| L3 | 動画埋め込み（過去開催の高画質映像） | エモーション |
| L4 | ふるさと納税の各プラン詳細を独立ページ化 | コンバージョン |
| ~~L5~~ | ~~カラーパレットのダークモード対応~~ | ✅ 完了 (Round 27) |
| L6 | Lighthouse 実測・点数 95+ 目指す微調整 | パフォーマンス（Round 31 で実測パイプライン稼働） |

## ✅ 完了済み（直近 14 ラウンド）

- R1: 空 alt 86件補完
- R2: 13サブページ独自 description
- R3: sponsor/donation status banner + sitemap
- R4: 開催カウントダウン
- R5: contact FAQ 誘導
- R6: PWA icon 正規化
- R7: 全サブページに開催決定 pill
- R8: OGP 全ページ統一
- R9: SW v5
- R10: aria-busy 実装
- R11: 住所コピー + Maps 案内
- R12: 天気予報リンク
- R13: プレスキット
- R14: LINE tabindex調整 + SW v6
- Sprint 1: docs 4 件追加（RELEASE / QA / INCIDENT / BACKLOG） + 当日緊急バナー先行配置
- Sprint 2: Looker Studio セットアップ手順 + 月次レポートテンプレート整備（docs 2 件追加）
- Round 15 (2026-05-15): Core Web Vitals & CMS 耐障害性
  - **M1** 完了: コンテンツ画像 147 タグに width/height 属性を一括注入（CLS 低減）。`_wp-content/inject-dims.ps1` ユーティリティ追加 + `generate.ps1` に注入ロジック組込で再生成時も維持
  - **M2** 完了: hero-fireworks-real の 800w / 1280w 派生を生成（モバイル 491KB → 86KB、約 82% 削減）。`<link rel=preload>` を imagesrcset 対応 + CSS を media query ベースのレスポンシブ背景に
  - **M3** 完了: gallery / press / faq の各 CMS セクションに testimonial と同じ `data-has-fallback` フラグ尊重ロジックを実装。空 CMS でも静的フォールバックを優先表示
  - SW v9 + キャッシュバスター 2026-05-15 に更新
- Round 35 (2026-05-15): Twitter Card 拡張属性 — 開催日/会場をシェア時に直接表示
  - **`twitter:label1` / `twitter:data1`**: 開催日 → 2026年11月14日（土） 18:00〜18:50
  - **`twitter:label2` / `twitter:data2`**: 会場 → 東京サマーランド 第2駐車場（あきる野市）
  - index.html + 13 サブページに追加 (404 は OG/Twitter メタを持たないので除外)
  - generate.ps1 のテンプレートも同期
  - Twitter (X) に URL を貼った時のカード preview に、画像+説明文に加えて構造化された「開催日 / 会場」ラベルが表示される
  - SW v28 + キャッシュバスター 20260515q
- Round 34 (2026-05-15): GA4 にスクロール深度トラッキング追加
  - **analytics.js に scroll_depth イベント**: 25 / 50 / 75 / 90 % 到達時に GA4 へ送信
  - requestAnimationFrame で間引いて scroll listener の負荷を最小化
  - 各 milestone はセッション内 1 回のみ (reached[] フラグで dedupe)
  - `page_path` も同送信して、ページ別エンゲージメント計測が可能
  - event.html / qa.html / donation.html などの長文ページで「どこまで読まれているか」が見える
  - SW v27 + キャッシュバスター 20260515p
- Round 33 (2026-05-15): サブページに Critical CSS をインライン化 — FCP/LCP 高速化
  - **13 サブページ全部** (404 含めず) で `<link rel="stylesheet">` (render-blocking) を以下のパターンに変更:
    1. インライン `<style>` で約 2.3KB の Critical CSS (header, page-hero, タイポ, モバイル nav)
    2. `<link rel="preload" ... onload="this.rel='stylesheet'">` で本体 styles.css を非同期取得
    3. `<noscript>` で JS 無効時の fallback
  - 初回訪問時の FCP/LCP が ~50-75ms 改善 (CSS が render-blocking でなくなる)
  - 既存の cache 済 styles.css がある場合の再訪問では影響なし
  - **generate.ps1** のテンプレートも同期して、再生成時も維持
  - SW v26 + キャッシュバスター 20260515o
- Round 32 (2026-05-15): manifest.json の PWA メタデータ拡張
  - **`display_override`** を追加: `["window-controls-overlay", "standalone", "minimal-ui", "browser"]` の優先順序
    * Chrome/Edge デスクトップで window-controls-overlay 対応端末ならネイティブアプリ風の最小 UI
    * 非対応プラットフォームは standalone → minimal-ui → browser へフォールバック
  - **`id: "/"`** を明示: 複数オリジン/サブパスでのインストール識別を安定化 (PWA Identity ガイドライン推奨)
  - **`lang: "ja"` → `"ja-JP"`**: より具体的なロケール
  - SW v25
- Round 31 (2026-05-15): GA4 に Core Web Vitals 実測を送信
  - **analytics.js に Web Vitals tracking を追加**: PerformanceObserver で LCP / FCP / CLS を計測し GA4 の `web_vitals` イベントとして送信
  - **FCP**: paint observer の `first-contentful-paint` を即時送信
  - **LCP**: largest-contentful-paint の最新 candidate を visibilitychange / pagehide で flush
  - **CLS**: layout-shift の累積を hadRecentInput 除外で計算、visibilitychange で flush
  - **GA4 イベント形式**: `metric_name` / `metric_value` (ms or 4 decimal score) / `metric_id` / `page_path`
  - Looker Studio dashboard で page_path × device × metric でスライス可能
  - 外部ライブラリ不要 (web-vitals.js を読み込まない)、~70 行の inline 実装
  - 既存の cta_click / js_error トラッキングと並ぶ第三の計測パイプライン
  - **これにより L6 (Lighthouse 95+) の実測ベースの改善サイクルが回せる**
  - SW v24 + キャッシュバスター 20260515n
- Round 30 (2026-05-15): モダンブラウザ機能 — color-scheme / View Transitions / Speculation Rules
  - **`<meta name="color-scheme" content="light dark">`** を全 15 HTML に追加。ブラウザに「両モード対応サイト」と伝え、フォームコントロール・スクロールバー・iframe placeholder などのネイティブ UI が OS テーマに自動追従
  - **CSS の `@view-transition { navigation: auto }`** で Chrome 126+ の Cross-Document View Transitions API を opt-in。ページ間移動が crossfade に (旧ブラウザは無視 = ノーリスク)
  - **Speculation Rules API** を index.html に追加 (Chrome 121+):
    * /ticket.html, /access.html → prerender (moderate eagerness、リンクホバー時に prerender)
    * /donation.html, /qa.html → prefetch (moderate)
    * メイン CTA に体感「瞬時遷移」を提供
  - prefers-reduced-motion 尊重 (view transitions の crossfade を無効化)
  - **generate.ps1**: テンプレートに color-scheme meta を追加
  - SW v23 + キャッシュバスター 20260515m
- Round 29 (2026-05-15): フォントレンダーブロック解消 + 軽微な a11y 修正
  - **Google Fonts CSS を非同期読み込みに**: 全 15 HTML で `<link rel="stylesheet">` を `<link rel="preload" ... onload="this.rel='stylesheet'">` + `<noscript>` fallback パターンに変更
  - render-blocking から解放され FCP/LCP が改善 (特にサブページで効く)
  - `display=swap` パラメータ済なので FOUT は短時間で完了
  - **sponsor.html の不明ロゴ alt 修正**: `alt="2-2 企業ロゴ"` (ファイル名スラッグ) → `alt="協賛企業ロゴ"` (汎用説明)
  - **generate.ps1**: テンプレートを async fonts に + Apply-SponsorAltFix 関数を新設 (再生成時も維持)
  - SW v22 + キャッシュバスター 20260515l
- Round 28 (2026-05-15): Cloudflare Pages HTTP ヘッダー最適化
  - **新規 `_headers` ファイル**: Cloudflare Pages の規約に沿ったヘッダー設定
  - **セキュリティヘッダー (全レスポンス)**:
    * X-Content-Type-Options: nosniff (MIME 推測無効化)
    * Referrer-Policy: strict-origin-when-cross-origin
    * Permissions-Policy: camera/microphone/geolocation/interest-cohort 全部 ()
    * X-Frame-Options: SAMEORIGIN
    * Cross-Origin-Opener-Policy: same-origin
  - **キャッシュポリシー**:
    * /assets/* → max-age=31536000, immutable (1 年、画像はバイナリ変更で URL 変わるので安全)
    * /styles.css, /*.js (versioned with ?v=YYYYMMDD<letter>) → 1 年 immutable
    * /sw.js → max-age=0, must-revalidate (SW 更新を即時反映)
    * /manifest.json → 1 時間
    * /*.html → 5 分 must-revalidate (deploy 後すぐ反映)
    * /404.html → noindex via X-Robots-Tag
    * /sitemap.xml, /robots.txt → 1 時間 + 正しい Content-Type
  - SW v21
- Round 27 (2026-05-15): L5 ダークモード対応
  - **`@media (prefers-color-scheme: dark)`** ベースで OS の dark mode 設定に自動追従
  - **CSS 変数のフリップ**: --ink (text)、--muted、--paper (bg)、--cream、--line、--shadow、--gold-text すべてを dark 用に再定義
  - **21 個のカードクラスに dark surface override** (info-card / ticket-card / stats article / why-choose-card / program-card / testimonial-card / faq-item / sponsor-tile / press-kit-card / achievements-card / ticket-guide-card / not-found-card / cms-status / press-card / faq-item-dynamic / access-summary-table / support-orgs-group / wp-block-file / swell-block-faq__item / swell-block-bannerLink / has-border.-border01 / notice-actions secondary)
  - **テキスト要素の調整**: eyebrow/tag を bright gold に / prose link を #6fc0c0 に / hover を gold に
  - **コンポーネント別**: notice / page-status-banner / ticket-sale-pending / access-timetable-note を gold-tinted dark に / FAQ + ボタンを gold グラデに
  - **page-sponsor**: ロゴタイル + 個人協賛テーブル cells も dark に
  - **カード hover の金縁** をより明るく (rgba 0.55) して dark 背景でも見える
  - **timeline dot** を新 --paper に合わせて punch-through
  - light モードはそのまま維持 (既存 CSS は変更せず additive で実装)
  - SW v20 + キャッシュバスター 20260515k
- Round 26 (2026-05-15): SEO 鮮度シグナル — sitemap lastmod 更新
  - **sitemap.xml**: 実コンテンツが変更された 3 ページ (ticket / event / access) の `<lastmod>` を 2026-05-15 に更新。Round 22/24 で page-status-banner や `.ticket-sale-pending` や `.access-timetable-note` を追加した実体変化を反映
  - 他ページは CSS のみの変更なので lastmod は 2026-05-12 のまま (sitemap シグナルの正確性を維持)
- Round 25 (2026-05-15): CSS メンテナンス — 効果のないアニメ削除
  - **signup-card-aurora を削除**: radial-gradient が内部位置 (`circle at 88% 12%`) を使い background-size: 100% 100% で fill しているため、`background-position` を 88%→84% に動かしても画面に変化なし。22s 周期の compositor work が無駄だった
  - 経緯コメントで残置 (後の保守者が再追加しないように)
  - SW v19 + キャッシュバスター 20260515j
- Round 24 (2026-05-15): 鮮度ガード Part 2 — バス時刻表の出典明記
  - **access.html**: WP から取り込んだ「秋川駅→サマーランドバス停 時刻表」(2025年時点) に注記を追加。「※ 上記時刻表は前回開催（2025年）時点の路線バス情報です」+ 東京サマーランドの公式アクセスページへの誘導
  - **generate.ps1**: Apply-AccessStaleGuard 関数を新設し、Build-Page で access スラッグ時に自動適用。再生成しても注記が維持される
  - **styles.css**: `.prose .access-timetable-note` の専用スタイル (左 3px 金縁 + cream-tinted bg + 赤字"※" + リンクは teal/gold-text hover)
  - SW v18 + キャッシュバスター 20260515i
- Round 23 (2026-05-15): アクセシビリティ + メンテナンス
  - **a11y: --gold-text 変数を導入** (#8e6a1f、白背景上で ≈5:1 で AA 適合)
  - **.eyebrow / .tag をコンテキスト別に振り分け**: デフォルトは --gold-text、装飾の line + dot は bright var(--gold) のまま保持。dark 背景セクション (hero / page-hero / signup-card / support-band / event-panel / urgent-banner / subpage-signup-cta / footer) で var(--gold) に上書き
  - **light context の gold-on-white テキスト 6 箇所を gold-text に置換**:
    * `.notice-actions .button.secondary:hover`
    * `.ticket-guide-card:hover .ticket-guide-cta`
    * `.page-status-banner a:hover`
    * `.prose .donation-pdf-button:hover`
    * `.program-num` (非 feature variant)
    * .eyebrow/.tag のデフォルト
  - **dead code 除去**: `.stats article:hover span { color: var(--gold) }` を削除 (Round 17 の gradient-text に overrideされていた + webkit/Firefox 不整合)。経緯はコメントで残置
  - **SEO: sponsor.html の sitemap priority 0.7 → 0.5** (第7回コンテンツ中心のため重要度を下げる) + lastmod を 2026-05-15 に更新
  - SW v17 + キャッシュバスター 20260515h
- Round 22 (2026-05-15): 鮮度ガード — 終了済 CTA の無効化
  - **ticket.html 販売リンク無効化**: 第7回時の KKday/アソビュー予約ボタン 6 件（SS/A/フリー × 2 platforms）を `.ticket-sale-pending` 通知 CTA に置換。「販売準備中」ピル + 「販売開始通知を受け取る → index.html#signup」金グラデ CTA。誤誘導リスクを根絶
  - **ticket.html 上部のプラットフォームロゴ**: 外部リンクラッパを除去（ロゴ自体は「前回販売プラットフォーム」として情報残し）、リード文を「前回利用」表現に修正
  - **event.html**: page-status-banner を追加し、「楽曲・出演団体は前回開催時の内容」と明示
  - **generate.ps1**: Apply-TicketStaleGuard 関数を新設し、ticket 再生成時にも同じ変換が自動適用される。event の status banner も Build-Page で追加
  - **styles.css**: `.ticket-sale-pending` の 12 要素 CSS（gold rim グラデ + 金 CTA + 580px 以下で 1 列）
  - SW v16 + キャッシュバスター 20260515g
- Round 21 / L2 (2026-05-15): カウントダウンを「日→時間→分」段階表示 + 404 統一
  - **ui.js カウントダウン**: 24h 以上は「あと N 日」、1h-24h は「あと H 時間 M 分」、< 1h は「あと M 分」と段階的に表示
  - **更新頻度**: 距離に応じて適応的 (> 24h: 毎時 / 1-24h: 毎分 / < 1h: 10 秒)。setTimeout チェーンで動的に再スケジュール
  - **新クラス `.is-imminent`**: < 24h で金赤グラデ + 強パルス (1.4s 周期、より熱量のある演出)
  - **404 ページ**: not-found-card に Round 16 のカード hover 共通言語 (cubic-bezier 6px lift + 金縁 + 強シャドウ) を統一
  - SW v15 + キャッシュバスター 20260515f
- Round 20 / M5 (2026-05-15): sponsor.html を grid 化してトップと統一
  - **ui.js**: body に `page-<slug>` クラスを付与 (page-sponsor, page-access, ...)。ページ別 CSS スコープを可能に
  - **sponsor.html の WP column ブロック**: `body.page-sponsor` で `.wp-block-column > figure.wp-block-image` を真の「タイル」(白地 + border + box-shadow + hover lift + 金縁) に上書き
  - **階層見出し**: `is-style-section_ttl` の WP 黄色マーカーを除去し、既存 .prose h2::after の金赤グラデストライプ (3px) に統一
  - **下部テーブル形式 (個人協賛)**: border-spacing で各セルを「ミニタイル」(白〜cream グラデ + 金縁 + hover で +1px lift)。WP 縞模様 (nth-child odd) を解除
  - **SP**: 760px 以下で 2-up、460px 以下で 1-up にレスポンシブ
  - SW v14 + キャッシュバスター 20260515e
- Round 19 (2026-05-15): デザイン質感引き上げ Part 4 — 残る dark セクションを統一
  - **why-choose-card**: 上品な lift + 金縁 + 強シャドウに統一 (Round 16 のカード共通言語を適用)
  - **why-choose-icon**: hover で scale(1.08) + 3deg rotate + 金赤グラデで「焦がし」演出
  - **signup-card**: dark aurora が 22s で drift。中央 CTA セクションに息吹を
  - **signup-option**: 左下から金 halo が広がる hover + icon は scale(1.1) で金 hover ハイライト
  - **support-band**: 既存の dot grid に 4 個の金粒子を重ね 6.2s で twinkle
  - **info-card-thumb**: hover で image scale(1.04) (ニュース cards)
  - **focus-visible 統一**: 主要 CTA に金 outline (キーボードユーザーへの視認性)
  - すべて prefers-reduced-motion 尊重
  - SW v13 + キャッシュバスター 20260515d
- Round 18 (2026-05-15): デザイン質感引き上げ Part 3 — アンビエント演出
  - **body 背景**: 既存の金/赤 radial-gradient が 42s ease-in-out でゆっくり drift。「生きている感」を全ページに
  - **hero badge**: 既存の pulse に加えて 5.6s 周期で光が badge を sweep する shimmer 効果
  - **past-tile**: 写真に映画的 vignette (radial-gradient で四隅を暗く)、hover で vignette が薄れて写真の素の色が際立つ
  - **mobile sticky CTA**: 3.8s 周期で金色のリングが広がる subtle pulse (来場検討者の目を引く)。hover で 2px lift + 強シャドウ + 内側白ハイライト
  - **hero scroll-hint**: 細枠 pill 化 (背景 blur + 半透明)。hover で金縁
  - **notice ハイライト**: hover で 2px lift + 強シャドウ
  - すべて prefers-reduced-motion 尊重
  - SW v12 + キャッシュバスター 20260515c
- Round 17 (2026-05-15): デザイン質感引き上げ Part 2 — サイト全体へ展開
  - **サブページ banner (page-hero)**: 既存のドットテクスチャに 5 個の twinkling 金粒子を重ね、5.4s ease-in-out で twinkle。サブページにも夜空感
  - **page-hero h1**: 白→淡金のグラデーション文字 + 金グロー text-shadow
  - **stats 番号 (01/02/03)**: 金→赤グラデーション文字 + 40×2px の装飾線 + hover で drop-shadow
  - **footer**: 上端に金グラデーションのアクセント線（発光感）+ 6 点の星散背景 + Instagram/お問い合わせの hover を金グロー + フッターナビの hover を金 + letter-spacing
  - **past-tile**: hover でキャプションが 4px 上昇 + letter-spacing が広がり、暗グラデーションが濃くなる映画的な演出
  - **FAQ**: hover で +1px lift + 質問文が赤に / +ボタンを淡金グラデに / open 時は金赤グラデ
  - **event-panel カレンダーボタン**: hover で金 glow
  - SW v11 + キャッシュバスター 20260515b
- Round 16 (2026-05-15): デザイン質感引き上げ — 花火の夜空感
  - **Hero 雰囲気**: aurora オーバーレイ（暖色の radial-gradient が 18s でゆっくり漂う）+ sparkles 層（12 個の twinkling 金粒子、2 系統のオフセット）を追加。`mix-blend-mode: screen` で写真と自然に重なる。`prefers-reduced-motion` 尊重
  - **セクション見出し**: h2 の下に gold→red グラデの 64×2px アクセントストライプ + 金グロー
  - **カード hover 統一**: stats / ticket / info / program / testimonial / sponsor を `cubic-bezier(0.2,0.8,0.2,1)` の上品なリフト + 金縁グロー + 強いシャドウに統一
  - **ボタン**: primary の hover に強い金 glow + 内側白ハイライト。secondary も hover で金縁
  - **スクロールプログレス**: 既存の金→赤グラデに `box-shadow` で発光感
  - **サイトヘッダー**: スクロール時に金グラデの細線がフッターに出現
  - **モバイル**: hero タイポの shadow 強化、CTA を 1 行ストレッチで親指フィット
  - **fade-in スタガー**: ui.js でグリッド系コンテナの子要素に 75ms 刻みの transition-delay（最大 450ms）
  - SW v10 + キャッシュバスター 20260515a

## 📋 リリースカレンダー（2026年 想定）

| 時期 | やること |
|---|---|
| 5-7月 | テストモニタ集めの SNS 募集 / 「東京 秋花火 比較」コンテンツ展開 |
| 8月 | チケット販売開始 → 上記 H1-H2 着手、Web 経由販売へ最大化 |
| 9月 | プログラム詳細公開 / 出店店舗一覧公開 / プレスリリース配信 |
| 10月 | メディア掲載依頼ピーク / Yahoo!ニュース・JR 中吊り展開 |
| 11月 (開催 1週前〜) | 当日緊急バナー有効化準備 / 天気予報チェック / 中止判断フロー再確認 |
| 11/14 (当日) | 当日情報セクション稼働 / SNS実況 |
| 11月下旬 | 当日写真をギャラリーに投入 / お礼メッセージ展開 / 次回告知開始 |
