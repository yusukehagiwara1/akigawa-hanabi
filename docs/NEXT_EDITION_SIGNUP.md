# 次回開催情報 メール通知フォーム セットアップ

ホームページの「次回開催情報をいち早く受け取る」セクションで、メールアドレス登録を受け付ける仕組みです。

## 構成

シンプル版：**Google フォーム + 既存サイト**

- 専用フォームを Google フォームで作成
- フォーム回答は Google スプレッドシートに自動蓄積
- 第8回開催情報が決まった時に、スプレッドシートからまとめてメール送信

## 1. Google フォーム作成

### A. フォームを新規作成

1. https://docs.google.com/forms/ にアクセス
2. 「+ 空白のフォーム」をクリック
3. 以下を入力：

**フォームタイトル**
```
秋川流域花火大会 次回開催情報 通知登録
```

**フォーム説明文**
```
第8回 秋川流域花火大会の開催情報・チケット販売開始のお知らせを、メールでお届けします。

ご登録いただいたメールアドレスは、本イベントの告知のみに使用し、第三者への提供はいたしません。
```

### B. 質問項目を追加

| 質問 | 種類 | 必須 |
|---|---|---|
| お名前 | 記述式（短文） | ◯ |
| メールアドレス | 記述式（短文）→ 回答の検証で「メール」 | ◯ |
| 興味のある情報 | チェックボックス（複数選択可） | 任意 |
| お住まいの地域 | プルダウン | 任意 |

**「興味のある情報」の選択肢例**：
- チケット販売情報
- プログラム・出演情報
- 出店店舗情報
- 協賛・寄付の機会
- ボランティア募集

**「お住まいの地域」の選択肢例**：
- あきる野市内
- 多摩地区（あきる野市以外）
- 23 区内
- 東京都外（神奈川・埼玉・千葉）
- その他

### C. プライバシー設定

- フォーム上部の「設定」タブ
- 「メールアドレスを収集する」を **オフ**（質問で明示的に取るため）
- 「回答を 1 回に制限する」は **オフ**（ログイン強制を避けるため）

### D. フォームを公開

1. 右上の「送信」ボタン
2. リンクアイコン → 「URL を短縮」にチェック → コピー
3. コピーした URL（例: `https://forms.gle/xxxxxxxx`）を控えておく

### E. 回答のスプレッドシート紐付け

1. フォーム編集画面の「回答」タブ
2. スプレッドシートアイコン → 「新しいスプレッドシートを作成」
3. 名前を「秋川花火 次回通知登録者リスト」等に設定

これで以降の登録は自動でスプレッドシートに蓄積されます。

## 2. サイト側に URL を反映

`index.html` の「次回開催情報を受け取る」セクションの **「メールでのお問い合わせ」** ボタンの href を、作成した Google フォーム URL に差し替えます。

### 該当箇所

```html
<a class="signup-option signup-email" href="contact.html" data-ga-cta="signup:email">
```

を

```html
<a class="signup-option signup-email" href="https://forms.gle/xxxxxxxx" target="_blank" rel="noopener" data-ga-cta="signup:email">
```

に変更（`xxxxxxxx` は実際のフォーム URL に置換）。

ラベルも以下に変更すると分かりやすいです：

```html
<strong>メールで通知を受け取る</strong>
<span>第8回情報・チケット販売開始のお知らせ</span>
```

## 3. LINE 公式アカウント（任意）

LINE 公式アカウントを開設する場合：

1. https://www.linebiz.com/jp/service/line-official-account/ で無料アカウント作成
2. 「友達追加 URL」を取得（例: `https://lin.ee/xxxxxxx`）
3. `index.html` の以下を差し替え：

```html
<a class="signup-option signup-line" href="https://line.me/" ... aria-disabled="true">
```

を

```html
<a class="signup-option signup-line" href="https://lin.ee/xxxxxxx" target="_blank" rel="noopener" data-ga-cta="signup:line">
```

`aria-disabled="true"` も削除（活性化）。

サブテキストも変更：
```html
<span>友達追加で最新情報をお届け</span>
```

## 4. 一斉通知の送信方法

### A. 単純な方法（少人数想定）

1. 回答スプレッドシートを開く
2. メールアドレス列をコピー
3. Gmail の「To」欄にペースト（または **BCC で送信して受信者を見えなくする**）
4. 件名・本文を作成して送信

**重要**: BCC で送信しないと、他の受信者のメールアドレスが見えてしまいます。

### B. 自動化（登録者多数の場合）

スプレッドシートで Apps Script を使った一斉送信：

```javascript
function sendBulkNotification() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  const emails = [];

  // ヘッダー行をスキップ。メール列が3列目と仮定（環境に応じて調整）
  for (let i = 1; i < data.length; i++) {
    const email = data[i][2];
    if (email && email.includes("@")) emails.push(email);
  }

  // 50件ずつに分割（Gmail一斉送信の制限対策）
  const subject = "【秋川流域花火大会】第8回 開催情報のお知らせ";
  const body = `ご登録いただいた皆様

第8回 秋川流域花火大会の開催情報が決定しましたのでお知らせします。

▼ 開催日時: 2026年11月14日（土）
▼ 会場: 東京サマーランド第2駐車場

詳細・チケット情報は公式サイトをご覧ください。
https://akigawa-hanabi.pages.dev/

----
配信停止をご希望の方は、本メールに「停止希望」と返信してください。
特定非営利活動法人まちづくりコンソーシアム
`;

  for (let i = 0; i < emails.length; i += 50) {
    const batch = emails.slice(i, i + 50);
    GmailApp.sendEmail("info@machizukuri-con.or.jp", subject, body, {
      bcc: batch.join(","),
    });
    Utilities.sleep(2000); // 2秒待機
  }

  SpreadsheetApp.getUi().alert("送信完了：" + emails.length + "件");
}
```

これをスプレッドシートの Apps Script に貼り付け → 実行で一斉送信。

## 5. プライバシーポリシーの追記（推奨）

メールアドレスを集める以上、プライバシーポリシーに以下のような記載を追加しておくと安心：

> 当サイトでは、次回開催情報の通知をご希望の方からメールアドレスを取得しております。取得した情報は本イベントの告知目的のみに利用し、第三者への提供は行いません。

---

## まとめ

| 項目 | 状態 |
|---|---|
| サイト側の受信導線 | ✅ 実装済（ホームページ「次回開催情報を受け取る」セクション） |
| Google フォーム | ⏳ 運営側で作成 |
| LINE 公式アカウント | ⏳ 任意で開設 |
| スプレッドシート蓄積 | ⏳ フォーム作成と同時に設定 |
| 一斉通知の送信 | ⏳ 第8回情報公開時に実施 |

Web 構築側でできる準備は完了しています。Google フォームと LINE が用意でき次第、index.html の URL を差し替えれば運用開始できます。
