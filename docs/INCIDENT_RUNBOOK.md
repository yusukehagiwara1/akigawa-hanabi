# インシデント対応フロー（INCIDENT_RUNBOOK）

サイトに問題が起きた時の対応手順。レベル別に対応方法を整理。

## レベル定義

| Lv | 状況 | 例 | 対応速度 |
|---|---|---|---|
| **P0** | サイト全体ダウン | 表示されない／500/502/CF エラー | 即時（5 分以内） |
| **P1** | 主要機能ダウン | チケット予約リンクが死んでる／フォームが送れない | 1 時間以内 |
| **P2** | UX 不具合 | デザイン崩れ・誤字・スマホで崩れる | 24 時間以内 |
| **P3** | 軽微な改善 | 細部の調整・SEO 最適化 | 計画的に |

---

## P0 対応：サイト全体ダウン

### 症状の例
- `https://akigawa-hanabi.pages.dev/` を開いて表示されない
- "ERR_FAILED" や CF エラーページが出る
- 全ページ 500/502

### 即時対応（5 分以内）

1. **Cloudflare Pages ダッシュボードを確認**
   - https://dash.cloudflare.com/ にログイン
   - Pages → akigawa-hanabi → Deployments
   - 最新デプロイの Status を確認
2. **直近のデプロイが Failed の場合**
   - 直前の Successful デプロイを開く
   - "Rollback to this deployment" をクリック
   - 1-2 分後に復活確認
3. **Successful だがダウンしている場合**
   - Cloudflare 全体障害の可能性 → https://www.cloudflarestatus.com/ で確認
   - 復旧待ち（自社で対応不可）

### 公式 SNS で告知（並行）

> 「現在、公式サイト（akigawa-hanabi.pages.dev）へのアクセスが不安定になっております。復旧次第ご案内いたします。」

Instagram で投稿。

---

## P1 対応：主要機能ダウン

### よくあるケース

#### ケース A: チケット予約リンクが死んでる
- 該当箇所: `ticket.html` 内の KKday / アソビュー リンク
- 確認: 各リンクを開いて 404 が出ないか
- 修正: 該当 URL を新しいものに差し替え → コミット

#### ケース B: お問い合わせフォームが開かない
- 確認: `contact.html` の Google フォーム URL
- 修正: 運営側で Google フォームの権限設定を確認
- 暫定: フォーム URL を一時的にコメントアウトし、メール直送を案内

#### ケース C: microCMS からデータが取れない
- 影響: お知らせ・体験談・スポンサーロゴが表示されない
- 確認: ブラウザ DevTools (F12) → Console で `microcms` エラー
- 暫定: ユーザー側はフォールバック content（来場者の声 3 件）が表示されるので致命的ではない
- 恒久: microCMS の API キー期限切れ・サービス障害 → microCMS サポートへ

---

## P2 対応：UX 不具合

### デザイン崩れ
1. 何の変更が原因か特定（git log で最近のコミットを確認）
2. 該当コミットを Revert（GitHub の Revert ボタン）
3. または直接 CSS を修正してコミット

### 誤字・脱字
1. 該当 .html ファイルを GitHub Web 画面で編集
2. Commit → 2 分後に反映

### スマホ表示崩れ
1. 開発者ツールでスマホサイズに切替て再現
2. styles.css の `@media (max-width: 620px)` あたりを調整

---

## P3 対応：計画的改善

`docs/BACKLOG.md` に追加して、優先度別にスプリント単位で消化。

---

## 連絡フロー

```
問題発覚
 ↓
運営側で対応可能か判断（Pages ダッシュボード / GitHub アクセス権あり）
 ↓
YES → 上記手順で対応
NO  → Web 担当（萩原）に連絡 → 復旧依頼
```

## 復旧後の振り返り

P0/P1 が発生した場合は事後対応：
1. 原因をメモ（git log や Cloudflare ログを参照）
2. 同じことが起きないように予防策をコード or 手順書に反映
3. `docs/BACKLOG.md` の "改善済み" 欄に記録

---

## よく使うURL

| 用途 | URL |
|---|---|
| 本番サイト | https://akigawa-hanabi.pages.dev/ |
| GitHub リポジトリ | https://github.com/yusukehagiwara1/akigawa-hanabi |
| Cloudflare Pages | https://dash.cloudflare.com/ |
| GA4 | https://analytics.google.com/ |
| Search Console | https://search.google.com/search-console |
| microCMS | https://0k3w9bd30b.microcms.io/ |
| 公式 Instagram | https://www.instagram.com/akigawa_hanabitaikai/ |
| 統合連絡先 | お問い合わせフォーム（contact.html 経由） |
