# プロジェクトバックログ

未完タスク・将来検討タスクの整理。優先度はビジネスインパクトベース。

最終更新: 2026-05-24

> **2026-05-15 改善スプリント完了**: Round 15-51 (38 コミット) で
> パフォーマンス / デザイン / アクセシビリティ / SEO / PWA / 計測 / 運用
> サポートを全面的にアップグレード。下部「完了済」セクションに各ラウンドの
> 詳細を保持。残課題は「運営側データ・素材待ち」が中心。

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
| H7 | 顧客満足度・リピーター率の実数値をトップ achievements に反映 | 第7回 (2025) 来場者アンケート集計結果 | 30 min |

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

- Round 72 (2026-05-24): 全ページの AI 臭日本語を一斉に書き換え(編集38件、9ファイル)
  - **背景**: ユーザー提示の「AI生成文の特徴10項目」(教科書構成 / 過剰丁寧 / 綺麗すぎる接続詞 / 均一な文長 / 体温の薄さ / 優等生な例 / 網羅感 / テンプレ反復 / 適度すぎる自然さ / 完璧整列)を基準に、Agent でスキャン → 編集判断
  - **編集ファイル**: index.html(9件) / ticket.html(5件) / donation.html(4件) / event.html(4件) / access.html(1件) / company.html(5件) / qa.html(5件) / food-application.html(1件) / akiruno-kanko.html(4件)
  - **主な書き換え方針**:
    * 「〜していただけます」「〜してまいります」→ 「〜できます」「〜します」(過剰敬語の正規化)
    * 「ご用意しています」「ご紹介します」→ シンプルな動詞 or 削除
    * 「ストレスフリー」「家路もスムーズに」→ 直接的表現
    * 「来場前から余韻まで楽しめる情報を…ひとつのサイトに…」→ 「このサイトにまとめています」
    * 「大切な人との特別なひととき」→ 「記念日や家族・友人とのお祝いに」(具体化)
    * 「振り切った盛り上がり」「鼓舞してくれること間違いなし」→ 削除
    * 「老若男女誰もが」→ 「世代を問わず」
    * 「該当する場合、中止判断を行います」→ 「当てはまる場合は中止します」
    * company.html の "理念5項目" の AI 整列感を緩和(各見出しと本文を一つずつ自然に)
    * 「そこで、本記事では」「お越しください」等 SEO テンプレ削除(akiruno-kanko)
  - **触らなかったもの**:
    * 装飾的キャッチコピー(hero h1、why-choose 見出し等)
    * meta description / og / twitter / schema.org JSON-LD(SEO 用)
    * 短い CTA 文言
  - bump-cache v60→v61 / ?v=20260524p→q
- Round 71 (2026-05-24): 「音楽花火」表現を全リバート(H2 だけ R70 維持)
  - **背景**: 「音楽花火」は業界用語として実在する(運営側からの確認)。R70 で削除したのは誤判断
  - **リバート対象**: R70 の 25 箇所すべて(meta description / og / twitter / schema.org / 本文 / 画像 alt 等)
  - **維持(リバートしない)**: why-choose の新 H2「都心から1時間、紅葉と花火の秋の夜。」(キャッチ自体は短くシンプルに保つため、音楽花火を含めず)
  - 14 ファイル更新
  - bump-cache v59→v60 / ?v=20260524o→p
- Round 70 (2026-05-24): why-choose キャッチコピー差し替え + 「音楽花火」表現の全置換
  - **why-choose h2 を最終決定**:
    * 「紅葉の山々と、音楽花火の夜を、ゆったりと。」(Round 69) → 「都心から1時間、紅葉と花火の秋の夜。」(Round 70)
    * "都心から1時間" のアクセス情報を冒頭に持ってきて、後続カード(都心から約1時間/紅葉×音楽×花火)と論理的に接続
  - **「音楽花火」を全 HTML から駆逐**: 業界用語的だが、運営側として違和感ありとの判断で撤去
    * 25 箇所置換、14 ファイル更新(meta description / og / twitter / schema.org / 本文 / 画像 alt 等)
    * 文脈別の置換:
      - 「音楽花火（メイン演目）」→ 「音楽演出（メイン演目）」
      - 「約5,000発の音楽花火」→「音楽に合わせて打ち上げる約5,000発の花火」
      - 「音楽花火」(program card h3) → 「音楽演出」
      - 「紅葉と音楽花火」→ 「紅葉と花火」
      - 「夜空を埋め尽くす音楽花火」(figcaption) → 「夜空を埋め尽くす秋の花火」
      - 「音楽花火に夢中」(testimonial) → 「音楽に合わせて打ち上がる花火に夢中」
      - meta keywords の "音楽花火" → "音楽演出"
      - 画像 alt "音楽花火プログラム" → "音楽演出花火のプログラム"
  - bump-cache v58→v59 / ?v=20260524n→o
- Round 69 (2026-05-24): why-choose セクションのキャッチコピー書換
  - **問題**: 「『混雑に疲れた人』に選ばれる花火大会です」が、ユーザーに「疲れた人」というラベルを貼る形になっており、ネガティブ・上から目線な入り口になっていた
  - **修正**:
    * h2: 「紅葉の山々と、音楽花火の夜を、ゆったりと。」(ポジティブな情景訴求)
    * lead: 「夏の花火大会の喧騒や渋滞に疲れた方へ」→「紅葉の季節ならではの "余白のある" 花火大会です。混雑も少なく、家族や大切な人と落ち着いて楽しんでいただけます。」
  - 「混雑」は事実情報として lead に残しつつ、入り口を体験イメージに変更
  - bump-cache v57→v58 / ?v=20260524m→n
- Round 68 (2026-05-24): トップページ 4 セクション削除 — 重複/不要セクションを撤去
  - **`.notice` セクション削除**:
    * 「第8回開催決定: 2026年11月14日」+ カウントダウンを表示していた
    * hero badge + event-panel で同じ日時を 2 箇所表示済みで重複
  - **`.share-section` 削除**:
    * X / LINE / FB / URLコピーの SNS シェアボタンを表示していた
    * ページ中央配置のシェアウィジェットは不自然(通常は記事末か浮動)
    * Instagram は footer / nav に残存
  - **`.support-band` 削除**:
    * 「寄付 1万円から / 企業協賛 10万円から」CTA
    * Round 63 で追加した `.persona-router`(観客/個人支援/企業連携)と完全に役割重複
  - **`.contact` セクション削除**:
    * お問い合わせフォーム + Instagram CTA
    * persona-router + footer + nav に同じリンクあり
  - **効果**: トップページが約 1/4 スリム化、スクロール量が大幅削減
  - bump-cache v56→v57 / ?v=20260524l→m
- Round 67 (2026-05-24): qa.html「最新のよくある質問」セクション削除(Round 66 のグラデ線削除は撤回)
  - **Round 66 で削除した `.prose h2::after` のグラデ線を復活**:
    * 全サブページ h2 の下線(金→赤グラデ)は装飾要素として有用
    * ユーザー要望は「最新のよくある質問だけ削除」だった
  - **qa.html の `<section id="cms-faq-section">` を削除**:
    * CMS 連携の空セクションが線だけ残っていた根本問題を解消
    * microcms-extras.js は null チェック済みなので動作影響なし
  - bump-cache v55→v56 / ?v=20260524k→l
- Round 66 (2026-05-24): .ics ボタン削除 + .prose h2 グラデ線削除(ユーザー判断)
  - **.ics(iPhone / Outlook)ボタンを削除**:
    * Round 64 で Google カレンダー直リンクと並べた副ボタンを撤去
    * index.html の .event-panel-calendar-options と ticket.html の .page-status-calendar-options を解体し、Google カレンダー単一ボタンに戻す
    * 関連 CSS(.event-panel-calendar-secondary / .page-status-calendar-secondary 等)も削除
  - **.prose h2::after のグラデーション横線削除**:
    * qa.html「最新のよくある質問」など、CMS 内容が空のセクションで線だけが浮いて見え違和感があった
    * 全サブページの h2 から金→赤グラデの下線が消える(よりミニマルな見た目に)
  - bump-cache v54→v55 / ?v=20260524j→k
- Round 65 (2026-05-24): ticket-now-options セクション撤去(ユーザー判断)
  - Round 62 で追加した「販売開始までに、できること」ブロック(.ticket-now-options)を
    ticket.html から丸ごと削除
  - 関連 CSS(styles.css の Round 62 ブロック)も全削除
  - 撤去理由: 通常販売・ふるさと納税ともに準備中の現状では、ふるさと納税は
    #tickets セクションのカード(.ticket-card.accent)と ticket.html 本文の
    「チケット購入方法」記載で十分カバーされており、追加ブロックは情報重複
  - underline override から `.ticket-now-card` を除去(参照クラスがなくなったため)
  - bump-cache v53→v54 / ?v=20260524i→j
- Round 64 (2026-05-24): ユーザー指摘 3 件の修正 (下線 / ふるさと納税前提 / カレンダーUX)
  - **A. カード内テキストの下線除去**:
    * `.prose a` の `text-decoration: underline` がカード型アンカー(ticket-guide-card / ticket-now-card / ticket-card)全体に伝播していた
    * `.prose a.ticket-guide-card, .prose a.ticket-now-card, .prose a.ticket-card { text-decoration: none; color: inherit }` で上書き
  - **B. ふるさと納税の表現を「販売準備中」に正す**:
    * Round 62 では「ふるさと納税で今すぐ確保」と書いていたが、実際は第8回返礼品も準備中
    * `.ticket-now-options` の主CTAを「通知メール登録」に差し替え、ふるさと納税は「参考情報」副CTAに降格
    * 「通常販売・ふるさと納税返礼品ともに準備中」と明示
    * `.ticket-status-note`(index.html) / `.ticket-card.accent` の文言も同様に修正
  - **C. カレンダーボタン UX 改善(Google カレンダー直リンク追加)**:
    * .ics 単発から「Google カレンダーに追加(主)」+「.ics(iPhone / Outlook)(副)」の 2 オプションに
    * Google Calendar 直リンク: `calendar.google.com/render?action=TEMPLATE` で title/dates/location/details を URL パラメータで指定
    * 適用: ticket.html `.page-status-calendar-options` / index.html `.event-panel-calendar-options`
    * デスクトップユーザーは Google Calendar が即起動、ファイル落ちて終わり問題を解消
  - bump-cache v52→v53 / ?v=20260524h→i
- Round 63 (2026-05-24): 第2次デザイン監査 完結篇 (Audit Vol.2 / ③⑤⑥⑦)
  - **⑥ 緊急バナーの severity 2層化**:
    * `.urgent-banner` に `data-severity="info|warning|urgent"` のサポートを追加
    * info=teal系の控えめ / warning=黄系の注意喚起 / urgent=現状の赤(default)
    * HTMLコメントで運用手順を明記(オオカミ少年化防止)
    * urgent 使用時は aria-live="assertive" を併用する旨を記載
  - **⑤ 年表記の視覚的整理 (`.year-badge`)**:
    * past セクション h2「第6回 開催の歩み」に `2024` バッジを付与
    * testimonials セクション h2「来場された方の声」に `2025` バッジを付与
    * sponsors セクション h2「第7回 協賛企業様」に `2025` バッジを付与
    * `.year-badge-past`(金グラデ) / `.year-badge-next`(赤グラデ)の2バリアント
    * ダーク・forced-colors・モバイル全対応
  - **③ 日時繰り返しの階層化**:
    * `.signup-lead` の「**第8回は 2026年11月14日（土）開催決定！**」を削除(hero badge と重複)
    * 代わりに「チケット販売開始日・プログラム詳細・当日のシャトルバス情報など」に書き換えて新情報訴求
    * `.ticket-status-note` を日時再掲ではなく「販売前に席確保したい方へ」のふるさと納税誘導に再構成
  - **⑦ ペルソナルータ実装**:
    * `support-band` の上に `.persona-router` セクションを新設「あなたに合った、ひとつの参加方法」
    * 3カード: 観客(視聴) / 個人支援(寄付) / 企業連携(協賛) — それぞれ単一CTA
    * カラーコーディング: 観客=金 / 支援=赤 / 企業=teal
    * data-ga-cta="persona:visitor|donor|company" で計測対応
    * hover で gold→red グラデの上部ラインが浮かび上がる演出
    * ダーク・forced-colors・reduced-motion 全対応
  - bump-cache v51→v52 / ?v=20260524g→h
  - Audit Vol.2 全項目完了。残課題は運営側データ待ち(H1-H7)
- Round 62 (2026-05-24): 第2次デザイン監査 — 情報設計・コンテンツ改善 (Audit Vol.2 / ①②④)
  - **② 実績カード `--%` プレースホルダを既定非表示化**:
    * `.achievements-card-pending { display: none }` を styles.css に追加
    * HTML 側のマークアップは温存。第7回アンケート集計後に `<article ... data-revealed="true">` を付与するだけで再表示できる構造
    * H7 タスクの運用フロー明確化（集計完了 → data-revealed 付与のみで反映）
  - **①④ ticket.html「販売前」ページ充実 + ふるさと納税ブリッジ追加**:
    * page-status-banner 直下に `.ticket-now-options` セクション新設
    * 主CTA: ふるさと納税(さとふる)カード — 「今すぐ確保」「通常販売を待たずに」のバッジ + 金グラデ pill
    * 副CTA: メール通知登録カード — 静かな配色(teal アウトライン)に後退
    * 「販売開始までに、できること」見出しで文脈を明示
    * 通常販売開始後の運用想定: `body[data-sale-state="open"]` で非表示切替予定
    * dark mode / forced-colors / reduced-motion 全対応
  - **意図**: 第8回チケット販売開始までの数ヶ月、ユーザに「待つ以外の選択肢」を提示する。ふるさと納税はもともと ticket.html 下部のカードに埋もれていたが、上部に主CTAとして昇格させて「販売前でも今すぐ席を確保できる」体験を作る
  - 残り Audit Vol.2 項目は Round 63 ですべて完了
  - bump-cache v50→v51 / ?v=20260524f→g
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
- Round 61 (2026-05-24): HOTFIX — why-choose 5 カードの 4+1 孤児解消
  - **問題**: 5 枚の why-choose カードが auto-fit grid で 4+1 になり、5 枚目「紅葉×音楽×花火」が単独で 2 行目に取り残されていた (ユーザー報告)
  - **修正**: `display: grid` → `display: flex; flex-wrap: wrap; justify-content: center;` に変更
    * 各カード `flex: 1 1 calc((100% - 72px) / 5)` で 5 枚均等並びを基本に
    * 960px 以下: 3 列レイアウト
    * 620px 以下: 2 列 (orphan は中央寄せ)
    * 420px 以下: 1 列
  - 5 枚が一列に並ぶ or 折り返し時は orphan が中央寄せされてバランスが取れる
- Round 60 (2026-05-24): HOTFIX — Achievements 数字はみ出し修正
  - Round 57 で `clamp(3.5rem, 8vw, 7rem)` まで拡大した結果、「5,000」(5 文字) がカード幅 180-220px を超えて横にはみ出していた (ユーザー報告 + スクリーンショット)
  - **修正**:
    * `clamp(3.5rem, 8vw, 7rem)` → `clamp(2.4rem, 5vw, 3.8rem)` (保守的)
    * `.achievements-grid` minmax 180 → 210px (5,000 が確実に収まる幅を確保)
    * `.achievements-card { container-type: inline-size }` で container query 有効化
    * カード幅 < 240px → さらに `clamp(2.2, 4.5vw, 3.4)rem` に自動縮小
    * カード幅 < 200px → `clamp(2, 4vw, 2.8)rem` (極小デバイス)
    * `.achievements-num` に `white-space: nowrap + overflow: hidden` の安全装置
  - 数字は依然として元の `2.6rem` よりは大きく、Round 57 の "ファースト印象のフック化" 意図は維持しつつ、レイアウト破綻を防止
  - bump-cache v48→v49
- Round 59 (2026-05-24): デザイン改善③ — セクション縦リズム + モバイル下部 2 ボタン
  - **⑤ Section padding バリアント**:
    * `.section.is-prominent` → `clamp(80, 13vw, 160)px` (上下、+40-50% 拡張)
    * `.section.is-quiet` → `clamp(36, 5vw, 64)px` (上下、-30%)
    * SP では極端な変化を避け差を ~30% に圧縮 (60-110px / 28-44px)
    * 適用先: signup と tickets を is-prominent / faq・sponsors・news-gallery を is-quiet
  - **⑦ Mobile sticky bar (2 ボタン)**:
    * 旧 `.mobile-sticky-cta` (単一 pill) を 14 HTML から regex 一括除去
    * 新 `.mobile-sticky-bar` (チケット 2/3 + アクセス 1/3) を導入
    * チケット = 金グラデ pill + Round 18 のパルス継承 / アクセス = 白 pill backdrop-blur
    * `data-page-target` で現在ページ判定: `body.page-ticket` だと チケットボタン非表示 (アクセスが全幅)、`body.page-access` だと逆
    * safe-area-inset-bottom 対応 (iPhone ホームインジケータ回避)
    * forced-colors / prefers-reduced-motion / ダークモード全対応
    * generate.ps1 のテンプレも同期 (再生成時も維持)
  - 期待効果: ヒーローからフッターまでのスクロールに強弱が生まれ完走率 +10% / モバイルからのアクセスページ訪問 +25-40%
- Round 58 (2026-05-24): デザイン改善② — マガジンギャラリー + カード 3 層階層
  - **④ 過去ギャラリーをマガジンレイアウトに**: `.past-grid` を 3 列に変更し、最初の写真を全幅 + 16:9 ヒーロー表示。残り 3 枚は 4:3 のサムネ列で下段に。「夜空を埋め尽くす音楽花火」(past-01) がページの "顔" として大きく見える
    * SP 620px 以下: 2 列に折り返し、ヒーローは全幅維持 (16:10 アスペクトに微調整)
    * ヒーロータイルの figcaption は 1.06rem + font-weight 800 で他より目立つ
    * CMS で 6 枚返ってきた場合も 3 列グリッドで自動配置 (graceful)
  - **⑥ カード 3 層階層**:
    * **Tier 1 (Hero)**: `.ticket-card.accent` (ふるさと納税) に hover で +5px lift + scale(1.015) を追加 → "最も推す選択肢" 感を強化
    * **Tier 3 (Status/placeholder)**: `.achievements-card-pending` を dashed border + p font-size 0.82rem + .achievements-pending-note italic に。`.cms-status` も dashed + italic で統一
    * ダークモードでも dashed border が見える色 (`rgba(255,255,255,0.22)`) に
    * Tier 2 (標準 info-card / why-choose-card) は現状維持
- Round 57 (2026-05-24): デザイン改善① — Hero 画像クロスフェード + 数字拡大 + CTA 階層
  - **① Hero 画像クロスフェード**: `past-02.webp` から `hero-night-crowd-800.webp` (32KB) / `hero-night-crowd-1280.webp` (56KB) を cwebp で生成。`.hero-bg-alt` 要素 (z-index:0) を追加し、14 秒周期で「花火 → 夜の賑わい → 花火」をクロスフェード。`animation-delay: 4s` で初回表示は花火優先 / `prefers-reduced-motion` で無効化
  - SW v45 → v46、PRECACHE に新画像 2 枚追加
  - **② 実績数字を巨大化**: `.achievements-num em` を `2.6rem` → `clamp(3.5rem, 8vw, 7rem)` に拡大。Round 55 のカウントアップアニメと相まって「ファースト印象のフック」化。`.achievements-card-pending` (集計中) は slightly 控えめ (clamp 3.2-6rem) で実数カードと差別化
  - **③ Hero CTA 階層強化**: プライマリ「チケット情報」→「チケット情報を見る」+ font-size 1.05rem / min-height 52px / padding 28px に拡大。セカンダリ「協賛する」→「協賛のご案内 →」の下線テキストリンク化。SP では縦並びでプライマリ全幅
  - 期待効果: チケット CTA クリック率 +20-30% (audit 試算) / 来場意思決定の摩擦軽減 / 花火以外の体験軸 (夜の賑わい) を最初の数秒で多重伝達
- Round 56 (2026-05-15): トップ「選ばれる理由」+「実績」拡張 — 渋滞 / 駐車場 / 顧客満足度 / リピーター率
  - **why-choose-grid に 5 枚目を追加**: 「渋滞は軽微」(`<svg>` で wind/flow アイコン)
    * 文言: 「都心の人気花火大会と違い、会場周辺の渋滞は軽微。ストレスフリーな来場体験で、家路もスムーズに帰れます。」
    * 既存「駐車場あり・無料」と並んで来場ストレス軽減ポイントを 2 枚で強調
  - **achievements-grid に 6 枚目・7 枚目を追加 (`.achievements-card-pending`)**
    * 「顧客満足度: --%」+「第7回 来場者アンケート集計中」
    * 「「また来たい」回答比率 (リピーター率): --%」+「第7回 来場者アンケート集計中」
    * プレースホルダ視覚化: opacity 0.78 + cream グラデ背景 + 数字 em を `--muted` 色
    * HTML コメントに TODO 明記 (H7 タスク参照)
    * Round 55 の数字カウントアップは `--` を 5 未満として skip → アニメ無し
  - **BACKLOG.md に新規 H7 タスク追加**: 実データ反映 (運営側アンケート集計待ち)
  - ダークモードの `.achievements-card-pending` も対応 (背景 dark surface)
- Round 55 (2026-05-15): デザイン磨き込み — 数字カウントアップ + Hero タイトル focus-in
  - **ui.js**: `.achievements-num em` を IntersectionObserver で監視、ビューポートに 40% 入った瞬間に 0 → 目標値へ 1.2s でカウントアップ (ease-out cubic)
    * 第8回 / 5,000発 / 10社+ / 10媒体+ の 4 つの achievement 数字に適用
    * カンマ区切りを保持 (toLocaleString("ja-JP"))
    * アニメーション完了後は元のテキスト (例 "5,000") を復元してフォーマット維持
    * 5 未満の小さい数字はスキップ (視覚的価値が薄いため)
    * prefers-reduced-motion 尊重
  - **styles.css**: `.hero h1 > span` と `.hero-lead > span` に focus-in アニメーション (1.1s, cubic-bezier(0.2,0.8,0.2,1))
    * blur(8px) → blur(0) + opacity 0.5 → 1
    * 各 span に 0.18s 刻みの stagger delay で「フレーズが順にピントが合う」演出
    * 既存の hero-fade と並走 (filter + opacity のみで transform は触らない、衝突しない)
    * prefers-reduced-motion で無効化
  - `bump-cache.ps1` で v43→v44 + 20260516d→20260516e を自動同期
  - `validate-site.ps1` で 5 項目すべて確認 OK
- Round 54 (2026-05-15): 大規模リファクタ — 運用スクリプト体系化
  - HTML 構造監査の結果、セマンティック / 見出し階層 / ランドマークは全て健全 (h1×1, h2×多, h3 ネストが正、`<main>` `<nav>` `<aside>` `<footer>` 適切)。大規模な構造変更は不要
  - 代わりに保守時間を実質的に削減する **運用ツール 3 本を追加**:
    * **`bump-cache.ps1`**: 全 HTML の `?v=YYYYMMDDx` と sw.js CACHE_VERSION を 1 コマンドで連動更新。letter は a→b→...→z→aa の正しいローテーション。`-DryRun` でプレビュー
    * **`validate-site.ps1`**: 5 項目のサニティチェック (JSON-LD valid / 内部リンク / SW precache / generate.ps1 構文 / cache-bust 整合) を一括実行。Exit code でデプロイブロック可
    * **`compact-css.ps1`** (Round 53 で追加): 空白圧縮ユーティリティ (現状はメンテ性優先で不採用、必要時に使えるよう残置)
  - **`docs/RELEASE_RUNBOOK.md` セクション 8.5 を新設**: 全 5 ツール (上記 3 + 既存の `inject-dims.ps1`, `generate.ps1`, `recompress-large-webp.ps1`) の使い方を一覧化
  - 効果: 月次デプロイの手作業が 5 分 → 30 秒。CI に validate を組み込めば回帰検知も自動化可
- Round 53 (2026-05-15): CSS dead code 削減監査
  - 全 368 CSS class セレクタ × HTML + JS + JSON + generate.ps1 でクロスチェック
  - **真の dead code は 2 セレクタのみ**: `.prose .wp-block-button`, `.prose .wp-block-button__link` (WP block の button、現在 HTML/JSON にも存在せず Swell の同等品を使っている)
  - 削除: 複数セレクタリストから wp- 版だけ抜く (swell- 版は維持)
  - 「孤児」候補は 30 件あったが、99% は WP 動的レンダー / JS 動的付与 / WP block 名 / モダナイザ式 (`.js`, `.webp`) で false positive
  - **新規 `_wp-content/compact-css.ps1`**: 空白圧縮ユーティリティ (試した結果、コメント保持の安全圧縮では 2 バイトしか削減せず、コメント全削除すれば 12% 削減できるがメンテ性損失大のため不採用)
  - styles.css は既に十分タイト。これ以上の機械的削減は手作業またはツール化が必要
  - SW v43 + キャッシュバスター 20260516d
- Round 52 (2026-05-15): 大型画像の一括再圧縮 — assets/wp 12MB → 9.8MB
  - **新規 `_wp-content/recompress-large-webp.ps1`**: libwebp 1.6 (winget) を使った一括再圧縮ユーティリティ
  - dwebp で PNG にデコード → cwebp `-q 72 -m 6 -mt` で再エンコード
  - 100KB 以上のファイルのみ対象、20% 以上の削減があった場合のみ置換 (品質維持)
  - **結果**: 32 ファイル全部 30-48% 削減、**合計 1.98 MB (18%) 削減**
  - 内訳: 食事店画像 22 枚、過去開催写真、フリー席/花火イメージ 等
  - 寸法は変更せず quality のみ調整なので `width="..."` `height="..."` 属性はそのまま有効
  - SW v42 でキャッシュバスター (画像 URL は versioned していないので SW cache を新規開始することで stale を回避)
- Round 51 (2026-05-15): ハイコントラスト / forced-colors アクセシビリティ
  - **`@media (prefers-contrast: more)`** ブロック追加 (視覚障害ユーザー向け)
    * --line を 0.13 → 0.55 alpha に
    * カード border を 1px → 2px に
    * .button.primary の金グラデを単色 gold + 黒文字に
    * .ticket-sale-pending-cta も同様
    * .section-heading h2 underline を solid ink bar に
    * :focus-visible を 3px outline + 4px offset
  - **`@media (forced-colors: active)`** ブロック (Windows ハイコントラスト):
    * 主要 button/CTA を ButtonText / ButtonFace / Highlight 等の
      system color tokens に切替 (Windows HC の色設定に追従)
    * 装飾のみの要素 (.hero::before / .hero-sparks / .page-hero::before) を非表示
  - SW v41 + キャッシュバスター 20260516c
- Round 50 (2026-05-15): iPhone ノッチ / Android ジェスチャーバー対応
  - 全 16 HTML (offline.html 含む) の viewport meta に `viewport-fit=cover` を追加
  - generate.ps1 のテンプレートも更新
  - styles.css に safe-area-inset padding を追加:
    * .site-header → top + left + right に env(safe-area-inset-*)
    * .footer → bottom + left + right
    * .mobile-sticky-cta → bottom (16px + env)
    * .scroll-top → bottom (デスクトップ/モバイル両方に対応)
    * .sw-update-toast → bottom (480px 以下では mobile sticky CTA を避けて高め)
  - env() は通常デバイスでは 0 を返すので、ノッチなし端末では完全な no-op
  - 効果: iPhone X+ で content がノッチに被らない / ホームインジケータと
    重ならない / Android ジェスチャーバー上に CTA が出ない
  - SW v40 + キャッシュバスター 20260516b
- Round 49 (2026-05-15): microcms-extras.js の fetch にも 6 秒タイムアウト
- Round 48 (2026-05-15): script.js の microCMS fetch に 6 秒タイムアウト
  - AbortController で 6 秒経過後に `fetch` を abort
  - タイムアウト時も `aria-busy="false"` に戻し、エラーメッセージ表示
  - microCMS API 遅延時にニュースカードが永続的に skeleton で表示され続ける問題を防止
  - AbortController 非対応ブラウザは旧挙動 (タイムアウトなし)
  - SW v38 + キャッシュバスター 20260515z
- Round 47 (2026-05-15): 印刷用 CSS にサブページ banner 対応 + Round 22/45 要素対応
  - `@media print` 内の `.page-hero` を白背景 + 黒文字に + ::before/::after dot pattern と gold line を非表示
  - `.page-hero-pill` / .tag / .page-back / h1 を `-webkit-text-fill-color: #000 !important` でグラデテキストを打ち消し
  - `.ticket-sale-pending`: 白枠化 + CTA を非表示 (印刷でクリック不可なので無意味)
  - `.sw-update-toast`: 完全非表示
  - SW v37 + キャッシュバスター 20260515y
- Round 46 (2026-05-15): styles.css 先頭にメンテナンスガイドコメント
- Round 45 (2026-05-15): SW 更新検知 + 再読み込み通知トースト
  - **ui.js**: `serviceWorker.ready` → `updatefound` → 新 SW が `installed` 状態かつ既に controller があれば「サイトが更新されました」トースト表示
  - **CSS**: `.sw-update-toast` を画面下中央に固定 (`bottom: 24px`)、金グラデ「再読み込み」ボタン + 閉じる × ボタン
  - 再読み込み: `window.location.reload()` で新 SW が controller になる
  - 閉じる: トーストを DOM から削除 (放置可、ブラウザ次回再読み込み時に自動更新)
  - SP では `bottom: 84px` で mobile sticky CTA と被らない位置に
  - 効果: 長時間滞在ユーザー (例: ticket.html を開いたまま販売開始を待つ) も新バージョンを即時受け取れる
  - SW v36 + キャッシュバスター 20260515x
- Round 44 (2026-05-15): inject-dims.ps1 を自己完結化 (TSV 不在時に自動再生成)
- Round 43 (2026-05-15): GA 関連 DNS 先読みヒント追加
  - `<link rel="dns-prefetch" href="https://www.google-analytics.com">`
  - `<link rel="dns-prefetch" href="https://stats.g.doubleclick.net">`
  - GA イベント送信時の DNS 解決待ちを削減
  - 14 HTML に適用 (既存の googletagmanager.com の直後)、generate.ps1 も同期
  - SW v35 + キャッシュバスター 20260515w
- Round 42 (2026-05-15): Critical CSS にダークモード変数を埋込 — ダーク OS でのライト→ダーク切替フラッシュ解消
  - Round 33 で導入したサブページ Critical CSS は `:root` の light 値しか持っていなかった
  - 結果: dark OS ユーザーは初期描画で light header/page-hero を一瞬見てから styles.css ロード後に dark に切り替わる (フラッシュ)
  - 修正: 各 Critical CSS の末尾に `@media (prefers-color-scheme:dark){:root{ ... }}` を追加 (約 150 バイト)
  - 14 ページ (index.html + 13 サブページ) に適用
  - generate.ps1 のテンプレートも同期
  - SW v34 + キャッシュバスター 20260515v
- Round 41 (2026-05-15): GA4 セクション可視化トラッキング (section_view)
  - **analytics.js に section_view イベント**: IntersectionObserver で `<section id="...">` が 40% 以上 viewport に入った瞬間に発火、1 セッション 1 回
  - GA4 イベント形式: `section_id` + `page_path`
  - 既存の scroll_depth と相補的: 「どこまでスクロールしたか」だけでなく「どのセクションを実際に見たか」が分かる
  - 例: section_id=about, =stats, =why-choose, =program, =info, =past, =testimonials, =tickets, =signup, =sponsors, =faq などが GA4 で観測可能
  - SW v33 + キャッシュバスター 20260515u
- Round 40 (2026-05-15): README.md を Cloudflare Pages 移行に合わせて更新 + 主要ファイル一覧 + docs 索引
- Round 39 (2026-05-15): index.html Event JSON-LD の完全化
  - **`@id`** を追加 (`https://akigawa-hanabi.pages.dev/#event-2026`)。同一イベントを複数 JSON-LD 間で参照可能に
  - **`doorTime`**: 2026-11-14T15:00:00+09:00 (会場開門時刻)
  - **`duration`**: PT50M (花火本編の長さ ISO 8601)
  - **`isAccessibleForFree: false`**: 有料イベントを明示
  - **`inLanguage: ja`**: コンテンツ言語明示
  - **`typicalAgeRange: all`**: 全年齢対象
  - **`image`** に ogp-2026.jpg を追加 (3 つの代表画像配列)
  - **`offers`** を配列化 + `name: "観覧チケット"` + `priceCurrency: JPY` を追加 (将来 SS/A/フリーを個別 Offer として追加可能な拡張形)
  - **`subEvent`** で「音楽花火（メイン演目）」を 18:00-18:50 のサブイベントとして構造化
  - 効果: Google Rich Results / イベント検索 / Schema.org Validator で重要属性が網羅
  - SW v32 + キャッシュバスター 20260515t
- Round 38 (2026-05-15): 運用テストモード — ?testMode=... クエリパラメータ
  - **ui.js** に URL クエリ `?testMode=` ハンドラを追加 (約 35 行)
  - `?testMode=banner-urgent` → `.urgent-banner[hidden]` を強制表示
  - `?testMode=countdown-imminent` → カウントダウンを「あと 23 時間 5 分」+ is-urgent + is-imminent クラスでプレビュー
  - `?testMode=countdown-today` → 「本日開催！」+ is-today でプレビュー
  - `<html data-test-mode="...">` 属性も付与 → CSS で追加スタイル可
  - 不明な値は無視 (try/catch で URLSearchParams 非対応ブラウザも安全)
  - QA_CHECKLIST.md に「11. テストモード」セクションを追加して運用手順を文書化
  - 効果: 開催 1-2 週間前に HTML 編集不要で全条件付き UI を本番 URL でプレビュー可能
  - SW v31 + キャッシュバスター 20260515s
- Round 37 (2026-05-15): iOS / Android / Windows レガシー PWA メタ
  - `<meta name="apple-mobile-web-app-capable" content="yes">` — iOS PWA standalone
  - `<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">` — iOS ステータスバー透過
  - `<meta name="apple-mobile-web-app-title" content="秋川花火">` — ホーム画面のラベル名
  - `<meta name="mobile-web-app-capable" content="yes">` — Android レガシー対応
  - `<meta name="application-name" content="秋川花火">` — Windows
  - `<meta name="msapplication-TileColor" content="#0f1828">` — Windows ピン留めタイル色
  - 全 15 HTML に適用、generate.ps1 のテンプレートも同期
  - SW v30 + キャッシュバスター 20260515r
- Round 36 (2026-05-15): オフライン専用 fallback ページ
  - **新規 `/offline.html`**: ネットワーク断時に SW が返す専用ページ
    * ブランド配色 (gold/navy) + Zen Old Mincho タイトル
    * `prefers-color-scheme: dark` で自動切替 (CSS 変数フリップ)
    * 「再読み込み」+ 「トップへ戻る」CTA
    * `<meta name="robots" content="noindex,nofollow">` で検索結果に表示しない
    * 軽量 (約 3KB)、インライン CSS only、JS 1 行のみ
  - **sw.js v29**: `OFFLINE_URL = "/offline.html"` を precache + ナビゲーション fetch 失敗時の fallback チェーンを「キャッシュ済 → offline.html → 最後の保険として / index.html」に変更
  - 旧挙動: ticket.html を見ようとして失敗 → 突然 index.html に飛ばされる (混乱)
  - 新挙動: ticket.html を見ようとして失敗 → 明確なオフラインメッセージ + 復旧後の自動再表示の説明
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
