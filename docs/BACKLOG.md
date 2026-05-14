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
| M5 | sponsor.html を carousel から grid に統一 | デザイン整合 | 1 hour |

## 🟢 低優先（やれたらやる）

| ID | タスク | 効果 |
|---|---|---|
| L1 | 開催実績数値を CMS 化 | 運営側で更新できる |
| L2 | カウントダウンの「N時間」「N分」表示（直前期） | 緊張感UP |
| L3 | 動画埋め込み（過去開催の高画質映像） | エモーション |
| L4 | ふるさと納税の各プラン詳細を独立ページ化 | コンバージョン |
| L5 | カラーパレットのダークモード対応 | a11y |
| L6 | Lighthouse 実測・点数 95+ 目指す微調整 | パフォーマンス |

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
