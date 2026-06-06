# ConoHa WING 本番移行 手順書

秋川流域花火大会サイトを **Cloudflare Pages → ConoHa WING** に移行し、
本番ドメイン `https://machizukuri-con.or.jp/` で公開するための手順。

現在 `machizukuri-con.or.jp` は WordPress が稼働中。これを静的サイトに切り替える。

---

## コード側の準備（実施済み）

- [x] サイト内URLを `akigawa-hanabi.pages.dev` → `machizukuri-con.or.jp` に一括更新
- [x] `.htaccess` 作成（HTTPS強制・旧URL 301リダイレクト・セキュリティヘッダー・キャッシュ）
- [x] GitHub Actions 自動デプロイ `.github/workflows/deploy-conoha.yml`（FTPSアップロード）

### 旧URL → 新URL リダイレクト一覧（.htaccess に設定済み）

| 旧（WordPress） | 新（静的サイト） |
|---|---|
| `/home/` | `/` |
| `/company-overview/` | `/company.html` |
| `/sponsor-2025/` | `/sponsor.html` |
| `/lost-item/` | `/`（過去大会の忘れ物・転送） |
| `/yahoo-news/` | `/pr.html`（メディア掲載へ統合） |
| `/access/`, `/contact/`, `/donation/`, `/event/`, `/food-application/`, `/pr/`, `/privacy-policy/`, `/qa/`, `/ticket/`, `/2024-hanabi/`, `/akiruno-kanko/` | 同名 `.html` |

---

## 移行作業の順番（安全策）

### STEP 1. ConoHa WING に独自ドメインを追加
- ConoHa WING 管理画面 > サイト管理 > ドメイン > ドメイン追加
- `machizukuri-con.or.jp` を追加
- 公開フォルダ（ドキュメントルート）のパスを控える
  - 例: `/home/cXXXXXXX/public_html/machizukuri-con.or.jp/`

### STEP 2. FTP 接続情報を準備
- ConoHa WING 管理画面 > サイト管理 > FTP
- FTPアカウントを作成（ユーザー名・パスワードを設定）
- 控える情報:
  - **FTPサーバー名（ホスト）**: 例 `www123.conoha.ne.jp`
  - **FTPユーザー名**
  - **FTPパスワード**
  - **公開フォルダのパス**（STEP 1 で確認したもの）

### STEP 3. GitHub に Secrets を登録
GitHub リポジトリ > Settings > Secrets and variables > Actions > New repository secret

| Secret 名 | 値 |
|---|---|
| `CONOHA_FTP_HOST` | FTPサーバー名（例 `www123.conoha.ne.jp`） |
| `CONOHA_FTP_USER` | FTPユーザー名 |
| `CONOHA_FTP_PASSWORD` | FTPパスワード |
| `CONOHA_SERVER_DIR` | 公開フォルダのパス（末尾スラッシュ必須。例 `/public_html/machizukuri-con.or.jp/`） |

### STEP 4. 初回デプロイ（ファイルをConoHaへ転送）
- `main` ブランチに push すると GitHub Actions が自動でファイルをアップロード
- GitHub の Actions タブで成功（緑チェック）を確認
- ConoHa のファイルマネージャーで public_html にファイルが入ったか確認

### STEP 5. DNS を ConoHa に切り替え（＝本番切替）
- ドメインの DNS / ネームサーバーを ConoHa に向ける
  - ConoHa でドメイン管理している場合: ネームサーバーを ConoHa のものに
  - 他社でDNS管理の場合: A レコードを ConoHa WING のIPに変更
- 反映まで数時間〜最大48時間（通常は数十分）

### STEP 6. 無料独自SSL を有効化
- DNS が ConoHa に向いた後、ConoHa WING 管理画面 > サイト管理 > サイトセキュリティ > 無料独自SSL > 利用する
- 証明書発行まで数十分待つ
- ※ `.htaccess` で HTTPS を強制しているため、SSL有効化までは https でアクセスできない。
  DNS切替後はSSLを速やかに有効化すること。

### STEP 7. 動作確認
- `https://machizukuri-con.or.jp/` が新サイトで表示されるか
- 各ページ・PDF・お知らせ（microCMS）・申込フォームが動くか
- 旧URL（例 `/donation/`）が新URL（`/donation.html`）に301転送されるか
- スマホ表示の確認

### STEP 8. 移行後のクリーンアップ
- 旧WordPressのバックアップを取得・保管
- Google Search Console にドメインを登録（machizukuri.consortium@gmail.com）
- sitemap.xml を Search Console から再送信
- 必要に応じて Cloudflare Pages 側を停止 or 旧 pages.dev → 新ドメインへリダイレクト

---

## 補足
- WordPress投稿（ニュース記事9件）は microCMS のお知らせに集約済み。個別の旧投稿URLは
  必要に応じて後から `.htaccess` にリダイレクトを追加できる。
- 自動デプロイが不要な場合は、FileZilla 等で public_html へ手動アップロードでも可。
