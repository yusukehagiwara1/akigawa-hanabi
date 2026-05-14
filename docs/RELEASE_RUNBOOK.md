# デプロイ運用手順書（RELEASE_RUNBOOK）

Web担当が一時的に離れても、運営側で本サイトをメンテ・更新できるための手順書。

## 1. 全体構成

```
GitHub (yusukehagiwara1/akigawa-hanabi) ── main ブランチ
        ↓ 自動ビルド・デプロイ
Cloudflare Pages (akigawa-hanabi.pages.dev)
        ↓ 訪問者が見る
本番サイト
```

- 編集 → GitHub に push → 1-2 分後に本番反映
- 失敗してもロールバック可（後述）

## 2. よくある更新作業

### A. 既存ページの文言・画像を変更したい

1. **GitHub Web 画面で編集**（最も簡単）
   - https://github.com/yusukehagiwara1/akigawa-hanabi
   - 編集したいファイル（例: `ticket.html`）を開く
   - 鉛筆アイコン（Edit this file）→ 変更 → Commit changes
   - main に直接コミットしてもよい
2. **1-2 分後に本番に反映** されます
3. ブラウザで強制リロード（Ctrl+Shift+R）して確認

### B. 新しいお知らせ・体験談・スポンサーロゴを追加したい

→ サイト本体ではなく **microCMS** に追加します。
詳細は `docs/EDITING_GUIDE.md` を参照。

### C. 第8回の販売開始時にチケット情報を更新したい

1. `ticket.html` の **status banner** を「販売開始日」「販売 URL」に書き換え
2. 各席の価格を 第8回確定価格に書き換え（SS席 35,000円 / S席 14,000円 / A席 / フリーエリア / 駐車場 1,000円）
3. KKday / asoview の **第8回プロダクト URL** を 8 箇所の `href` に貼り直し
   - 検索キー: `kkday.com/product/527261` と `urakata.app/channels/.../products/`
4. `index.html` の Event JSON-LD `offers` 配列を席種・価格付きで復元（過去版あり、git log で参照）

## 3. ロールバック手順

「変更してから何かおかしくなった」時：

### 方法 1: GitHub で Revert（最も簡単）
1. https://github.com/yusukehagiwara1/akigawa-hanabi/commits/main を開く
2. 戻したいコミットを開く → 右上の "Revert" ボタン
3. "Create pull request" → Merge
4. 1-2 分後に本番反映

### 方法 2: 直前のコミットに戻す（緊急時）

Cloudflare Pages の管理画面でも「Rollback to this deployment」が可能：
1. https://dash.cloudflare.com/ にログイン
2. Pages → akigawa-hanabi
3. Deployments タブから直前の successful デプロイを選択
4. "Rollback to this deployment" をクリック

## 4. ホスティング設定

| 項目 | 値 |
|---|---|
| ドメイン | akigawa-hanabi.pages.dev |
| ホスティング | Cloudflare Pages（無料） |
| ビルドコマンド | なし（静的サイト） |
| 出力ディレクトリ | `/`（リポジトリルート） |
| 環境変数 | なし |
| ビルド時間 | 数秒〜30秒程度 |

## 5. Service Worker（オフライン対応）について

- 更新時は `sw.js` 内の `CACHE_VERSION` を `v6` → `v7` のように 1 つ上げると、ユーザーの古いキャッシュが破棄されます
- 大きな見た目変更を入れた時は必ずバンプしてください
- バンプしないと、ユーザーは古い見た目のままになることがあります

## 6. ドメイン関連

- 独自ドメイン未設定。`akigawa-hanabi.pages.dev` のみで運用
- 独自ドメイン化したい場合は Cloudflare Pages 管理画面 → Custom domains

## 7. Google Analytics 4（計測）

- 測定 ID: `G-GWF9DQCZQ3`（`analytics.js` に記載）
- 確認: https://analytics.google.com/ にログイン → リアルタイムで確認
- 月次の数値レポートは `docs/GA4_FUNNEL_REPORT.md` に従って Apps Script で生成

## 8. Google Search Console

- 登録 URL: `https://akigawa-hanabi.pages.dev/`
- 確認用メタ: `<meta name="google-site-verification" content="_SB5wUXCuqfQHGCTuY0_c6xVeaRyJ9jwoDLAwN-SYh0">`（index.html 内）
- sitemap.xml は登録済み

## 8.5. 開発ヘルパースクリプト（_wp-content/）

ローカル PowerShell で実行できる作業自動化スクリプト群。

### `_wp-content/bump-cache.ps1`

CSS/JS を更新したらキャッシュ識別子を 1 コマンドで全 HTML + SW に伝播。

```powershell
.\_wp-content\bump-cache.ps1            # 全 HTML の ?v=YYYYMMDDx を次へ + sw.js v++
.\_wp-content\bump-cache.ps1 -DryRun    # 変更内容のプレビューのみ
```

ルール:
- 今日の日付 > 現在の日付 → 今日 + `a` にリセット
- 今日の日付 == 現在の日付 → 末尾文字を進める（a→b→…→z→aa）
- 今日の日付 < 現在の日付 → 末尾文字だけ進める（日付は戻さない）

### `_wp-content/validate-site.ps1`

デプロイ前のサニティチェック。5 項目を一括確認:

```powershell
.\_wp-content\validate-site.ps1
```

チェック内容:
1. 全 HTML の JSON-LD が valid JSON か
2. 内部 HTML リンクの存在
3. SW の PRECACHE_URLS が実ファイルとして存在
4. generate.ps1 が PowerShell として構文 OK
5. キャッシュバスター ?v= の値が全 HTML で一致

失敗は exit code 1。CI に通すと安心。

### `_wp-content/inject-dims.ps1`

新しい画像を `assets/` に追加した後、HTML img タグに width/height を自動注入:

```powershell
.\_wp-content\inject-dims.ps1
```

`_image-dims.tsv` が無ければ自動生成（Round 44 で対応）。

### `_wp-content/recompress-large-webp.ps1`

100KB 超の WebP を quality 72 で再圧縮（30-48% 削減実績、Round 52 で 1.98MB 削減）:

```powershell
.\_wp-content\recompress-large-webp.ps1
```

20% 以上の削減がある場合のみ置換（品質劣化と引き換えに足りない節約は採用しない）。

### `_wp-content/generate.ps1`

WordPress REST API JSON からサブページ HTML を再生成（既存）。
新画像 / WP コンテンツ変更時のみ実行。

```powershell
cd _wp-content
.\generate.ps1
cd ..
.\_wp-content\bump-cache.ps1
.\_wp-content\validate-site.ps1
```

## 9. 微妙な更新が発生した時のチェックリスト

- [ ] 変更したいファイルをローカルまたは GitHub Web で編集
- [ ] 変更内容を確認（テキスト編集なら typo チェック）
- [ ] コミット
- [ ] 1-2 分待つ
- [ ] 本番サイトを Ctrl+Shift+R で強制リロードし反映確認
- [ ] スマホでも表示確認
- [ ] 大きな変更時は SW バージョンをバンプ

## 10. 困った時の連絡先

- Cloudflare Pages 不具合: dashboard.cloudflare.com から確認
- GitHub アクセス不能: GitHub support
- サイト全体ダウン: Cloudflare Pages → Deployments で履歴確認 → Rollback
