# QA チェックリスト

大きな変更を本番に流す前 / 開催 1 ヶ月前 / 開催前日 に確認するチェック項目。

## 1. 主要 5 ページの動作確認

### 対象ページ
- [ ] トップ (/)
- [ ] チケット (/ticket.html)
- [ ] アクセス (/access.html)
- [ ] よくある質問 (/qa.html)
- [ ] 寄付協賛 (/donation.html)

### チェック観点
- [ ] ページが正常に表示される
- [ ] ヒーロー画像が見える
- [ ] 第8回の日付 "2026.11.14" が見える
- [ ] 「あと N 日」カウントダウンが正しい
- [ ] ヘッダーの "チケットを見る" が動く
- [ ] フッターのリンクが全部生きてる
- [ ] スマホで縦長メニュー（ハンバーガー）が動く

## 2. SNS シェアプレビュー

各ページの URL を以下にコピペしてプレビューを確認：
- X (Twitter) Card Validator: https://cards-dev.twitter.com/validator
- Facebook Debugger: https://developers.facebook.com/tools/debug/
- LINE Preview: 実際に LINE で共有してみる

### 観点
- [ ] OGP 画像（日付入り `ogp-2026.jpg`）が表示される
- [ ] タイトルが「秋川流域花火大会【公式】」になっている
- [ ] 説明文が読みやすい

## 3. モバイル表示確認（必須）

### 対象端末
- [ ] iPhone Safari（最新）
- [ ] Android Chrome（最新）
- [ ] 小型スマホ（375px 幅）

### チェック観点
- [ ] ハンバーガーメニューが開閉できる
- [ ] ヒーローのバッジ「第8回 開催決定」がはみ出してない
- [ ] event-panel（右下の白いボックス）がはみ出してない
- [ ] テキストが折り返してOK
- [ ] スクロール時に固定 CTA「チケットを見る」が出る
- [ ] フォントが読みやすいサイズ

## 4. クロスブラウザ確認

### 対象
- [ ] Chrome（最新）
- [ ] Safari（最新）
- [ ] Edge（最新）
- [ ] Firefox（最新）

### 観点
- [ ] スタイル崩れがない
- [ ] アニメーションが動く
- [ ] フォーム外部リンク (Google Forms) が新タブで開く

## 5. アクセシビリティ確認

### キーボードのみで操作
- [ ] Tab キーで全てのリンク・ボタンに到達できる
- [ ] フォーカスリング（黄色枠）が見える
- [ ] Esc キーでハンバーガーメニューが閉じる
- [ ] スキップリンク（Tab を最初に押すと出る）が機能する

### スクリーンリーダー（VoiceOver / NVDA）で
- [ ] 各セクションのタイトルが読み上げられる
- [ ] 画像の alt が適切
- [ ] フォームのラベルが読み上げられる

## 6. パフォーマンス確認

### Lighthouse（Chrome DevTools）
1. Chrome で対象ページを開く
2. F12 で DevTools 起動
3. "Lighthouse" タブ → "Mobile" → "Analyze page load"

### 目安スコア
- [ ] Performance: 80+
- [ ] Accessibility: 95+
- [ ] Best Practices: 90+
- [ ] SEO: 95+
- [ ] PWA: Installable ✓

## 7. 機能の動作確認（重要な順）

- [ ] 「カレンダーに追加」ボタンで .ics ファイルがダウンロードできる
- [ ] 「住所をコピー」で住所がクリップボードに入る（access.html）
- [ ] 「Google マップでルート案内」で Maps が開く
- [ ] シェアボタン（X / LINE / Facebook）で各プラットフォームが開く
- [ ] お問い合わせフォーム → Google フォームへ遷移できる
- [ ] チケット予約ボタン → 各販売サイトへ新タブで遷移
- [ ] Service Worker が登録されている（DevTools → Application → Service Workers）

## 8. SEO 観点の確認

- [ ] Google で `site:akigawa-hanabi.pages.dev` で検索 → 全 15 ページがインデックスされている
- [ ] Search Console でエラーゼロ
- [ ] sitemap.xml の lastmod が最新

## 9. リリース直前（開催 1 週間前など）チェック

- [ ] 「あと N 日」が正しい数字（手動計算と一致）
- [ ] チケット販売 URL が生きている（販売中の場合）
- [ ] 天気予報リンクが正しい場所を指している
- [ ] 駐車場情報・シャトルバス時刻が最新

## 10. 開催当日チェック

- [ ] 「あと N 日」表示が「本日開催！」に切り替わっている
- [ ] 雨天時の中止判断は QA ページに反映されている
- [ ] 緊急告知が必要なら notice 部分を即更新できる体制

## 11. テストモード（事前プレビュー用）

開催 1〜2 週間前に、本番 URL に `?testMode=...` を付けるだけで
条件付き UI が事前確認できる。HTML 編集不要。

| クエリ | 効果 |
|---|---|
| `?testMode=banner-urgent` | `.urgent-banner` を強制表示。デフォルト文言で見え方確認 |
| `?testMode=countdown-imminent` | カウントダウンを「あと 23 時間 5 分」+ 金赤グラデ + 強パルスでプレビュー |
| `?testMode=countdown-today` | 「本日開催！」+ 当日演出でプレビュー |

例: https://akigawa-hanabi.pages.dev/?testMode=banner-urgent

不明な値は無視される。`<html data-test-mode="...">` 属性が付与されるので、CSS で追加スタイルを差し込みたい場合のフックにも使える。

