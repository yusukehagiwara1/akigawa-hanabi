# 秋川流域花火大会 サイト編集マニュアル

このサイトは「Cloudflare Pages + GitHub + microCMS」の構成で動いています。
編集者は **microCMS** だけで主要なコンテンツを更新できます。

---

## 1. 編集ツール早見表

| 種類 | 編集場所 | URL |
|---|---|---|
| お知らせ・ニュース | microCMS の `news` API | https://0k3w9bd30b.microcms.io/ |
| 協賛企業ロゴ・URL | microCMS の `sponsors` API | 同上 |
| 過去の写真ギャラリー | microCMS の `gallery` API | 同上 |
| サイト全般のテキスト・画像 | GitHub のコード | https://github.com/yusukehagiwara1/akigawa-hanabi |
| ホスティング・ドメイン | Cloudflare Pages | https://dash.cloudflare.com/ |
| アクセス解析 | Google Analytics 4 (G-GWF9DQCZQ3) | https://analytics.google.com/ |

---

## 2. microCMS でお知らせを投稿する

### 手順

1. https://0k3w9bd30b.microcms.io/ にログイン
2. 左メニュー「news」を選択
3. 「追加」ボタン → 入力フォームへ
4. 各項目を入力：

| フィールド | 内容 | 例 |
|---|---|---|
| **title** | お知らせのタイトル（30字以内推奨） | 「第8回開催決定！日程公開」 |
| **excerpt** | 一覧で表示される短い説明（80字以内） | 「2026年11月14日（土）開催決定。チケット先行販売は7月開始予定。」 |
| **body** | 本文 HTML（リッチエディタで入力） | 文章＋画像を自由に組み合わせ |
| **url**（任意） | 詳細ページや外部リンクへのジャンプ先 | https://www.instagram.com/p/.../ |
| **publishedAt** | 公開日時 | 通常は「今」 |

5. 「公開」ボタンを押す → 数秒〜数十秒でサイトに反映

### 画像の使い方

- 本文に画像を貼るとき、microCMS のメディアにアップロード後にリッチエディタから挿入
- 推奨サイズ: **横 1200px、縦 800px**（16:10）
- 形式: **WebP** か **JPEG**（5MB 以下）

### 投稿頻度の目安

- 月 2-3 件を目標に
- 投稿例：開催決定告知 / プレスリリース / スポンサー紹介 / 過去開催レポート / Instagram 連動

---

## 3. 協賛企業（sponsors）の追加・更新

### 手順

1. microCMS の左メニュー「sponsors」を選択
2. 「追加」ボタン
3. 各項目を入力：

| フィールド | 内容 | 必須 |
|---|---|---|
| **name** | 企業名 | ✓ |
| **logo** | 企業ロゴ画像（横長 1024x341 推奨） | ✓ |
| **url** | 企業ホームページの URL | 任意（あれば必ず入れる） |
| **order** | 表示順（小さいほど上） | 任意 |

4. 「公開」 → ホームページ・スポンサーページに自動反映

### 重要

- ロゴ画像は**白背景**＋**横長 3:1 程度**で統一
- 企業 HP が **404 / SSL証明書エラー** の場合は **url を空欄** にすること（クリックして 404 になる事態を防ぐ）

---

## 4. 過去ギャラリー（gallery）の差し替え

### 手順

1. microCMS の左メニュー「gallery」を選択
2. 「追加」または既存レコードを編集
3. 各項目：

| フィールド | 内容 |
|---|---|
| **caption** | 写真のキャプション（例: 「夜空を埋め尽くす音楽花火」） |
| **image** | 写真（16:10 or 4:5 縦長、WebP 推奨） |
| **year** | 撮影年（例: 2025） |
| **order** | 表示順 |

### 注意

- 「Coming Soon」のプレースホルダー画像が混じっている場合は、必ず実写真に差し替え
- captiton と内容（写真）が一致するように

---

## 5. GitHub でサイトコードを編集する

軽微な修正（テキスト・画像差し替え等）であれば GitHub 上で直接編集できます。

### 手順

1. https://github.com/yusukehagiwara1/akigawa-hanabi にアクセス（ログイン必要）
2. 該当ファイル（例: `index.html`）を開く
3. 鉛筆アイコン（Edit this file）をクリック
4. 編集 → 下部の「Commit changes」
5. コミットメッセージを記入して「Commit changes」ボタン
6. 自動で Cloudflare Pages がデプロイ（1〜2分で反映）

### 推奨

- 大きな変更は **Pull Request** 経由で他の人がレビューしてから merge
- 「main」ブランチに直接 push すると即本番反映なので注意

---

## 6. 画像ガイドライン

| 用途 | 推奨サイズ | アスペクト比 | 形式 |
|---|---|---|---|
| お知らせ本文画像 | 横 1200px | 16:10 | WebP |
| 協賛ロゴ | 横 1024px | 3:1 | WebP（白背景） |
| ギャラリー写真 | 横 1200px | 16:10 or 4:5 | WebP |
| ヒーロー画像 | 横 1920px | 16:9 | WebP（dark） |

### 圧縮

- WebP に変換するツール：[Squoosh](https://squoosh.app/) など
- 1 ファイル **500KB 以下** を目安に
- alt 属性は必ず入力（アクセシビリティ・SEO 用）

---

## 7. 更新後のチェックリスト

公開後に以下を確認：

- [ ] PC でサイトを開いて確認（[https://akigawa-hanabi.pages.dev/](https://akigawa-hanabi.pages.dev/)）
- [ ] スマホ（実機）でも確認
- [ ] 画像が崩れていないか
- [ ] リンクが正しく開くか
- [ ] 文字の誤字脱字
- [ ] 公開日時が意図通りか

---

## 8. トラブルシューティング

### 投稿しても反映されない
- microCMS の「公開」ボタンを押したか確認
- Cloudflare Pages のキャッシュが残っている可能性 → 数分後に再確認
- それでもダメなら開発者（Web 構築担当）に連絡

### サイトが見られない
- Cloudflare Pages 側で障害の可能性 → https://www.cloudflarestatus.com/ で確認
- ドメイン関連 → DNS 設定の確認

### お問い合わせ

- 技術的トラブル → Web 構築担当
- コンテンツ表現の相談 → 編集チーム
- スポンサー関連 → 広報

---

## 9. 参考：microCMS スキーマ拡張提案

将来的に追加すると編集の幅が広がるスキーマ：

| スキーマ名 | 用途 | フィールド例 |
|---|---|---|
| `press_release` | プレスリリース・メディア掲載 | title / outlet / date / url / summary / logo |
| `testimonial` | 来場者の声・口コミ | name / age / role / comment / year |
| `faq_dynamic` | よくある質問の動的管理 | question / answer / category / order |
| `vendor` | 出店店舗情報 | name / category / image / description / area |
| `staff_voice` | スタッフ・運営者の声 | name / role / message / image |

これらを追加すると、編集者が直接更新できる範囲が大きく広がります。
追加希望は Web 構築担当へ依頼してください。
