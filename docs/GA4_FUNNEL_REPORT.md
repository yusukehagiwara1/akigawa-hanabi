# GA4 ファネル分析 自動レポート

GA4 から日次・月次でファネル指標を取得し、Google スプレッドシートに自動出力する Apps Script です。

## 計測する指標

| ステップ | 指標 | GA4 イベント |
|---|---|---|
| ① 認知 | サイト訪問 UU / セッション | `session_start` / `first_visit` |
| ② 興味 | 主要ページ閲覧 | `page_view` (ticket / donation 等) |
| ③ 検討 | CTA クリック | `cta_click` |
| ④ 行動 | チケット購入クリック | `ticket_purchase_click` |
| ④' 寄付・協賛 | 寄付/協賛フォーム送信 | `donation_click` / `sponsor_click` |
| ④'' ふるさと納税 | satofull リンク | `furusato_click` |
| エラー | JS エラー数 | `js_error` |

## 1. 事前準備

### A. Google スプレッドシート作成
1. Google ドライブで新規スプレッドシート作成（例：「秋川花火 GA4 月次レポート」）
2. スプレッドシートを開いた状態で **拡張機能 → Apps Script**

### B. GA4 Data API を有効化
1. Apps Script エディタで左サイドバー「サービス」→ **追加**
2. 「Google Analytics Data API」を選択 → 識別子は `AnalyticsData` のまま → 追加

## 2. スクリプトをコピペ

下記コード全文を Apps Script の `Code.gs` に貼り付け：

```javascript
// === 設定 ===
const GA4_PROPERTY_ID = "536964506"; // GA4 プロパティID
const SHEET_NAME_MONTHLY = "月次レポート";
const SHEET_NAME_WEEKLY = "週次レポート";

// === メニュー追加（開いた時に実行）===
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("📊 GA4レポート")
    .addItem("月次レポートを更新", "generateMonthlyReport")
    .addItem("週次レポートを更新", "generateWeeklyReport")
    .addToUi();
}

// === 月次レポート ===
function generateMonthlyReport() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME_MONTHLY);
  if (!sheet) sheet = ss.insertSheet(SHEET_NAME_MONTHLY);
  sheet.clear();

  // ヘッダー
  sheet.getRange(1, 1, 1, 9).setValues([[
    "月",
    "セッション",
    "UU",
    "ページビュー",
    "CTAクリック",
    "チケット購入クリック",
    "寄付クリック",
    "協賛クリック",
    "ふるさと納税クリック"
  ]]).setFontWeight("bold").setBackground("#f7efe2");

  const now = new Date();
  const rows = [];

  // 過去12ヶ月分
  for (let i = 11; i >= 0; i--) {
    const start = new Date(now.getFullYear(), now.getMonth() - i, 1);
    const end = new Date(now.getFullYear(), now.getMonth() - i + 1, 0);
    const label = Utilities.formatDate(start, Session.getScriptTimeZone(), "yyyy-MM");

    const sessions = runReport(start, end, [{ name: "sessions" }]);
    const users = runReport(start, end, [{ name: "totalUsers" }]);
    const pv = runReport(start, end, [{ name: "screenPageViews" }]);
    const ctaClicks = runEventReport(start, end, "cta_click");
    const tickets = runEventReport(start, end, "ticket_purchase_click");
    const donations = runEventReport(start, end, "donation_click");
    const sponsors = runEventReport(start, end, "sponsor_click");
    const furusato = runEventReport(start, end, "furusato_click");

    rows.push([label, sessions, users, pv, ctaClicks, tickets, donations, sponsors, furusato]);
  }

  sheet.getRange(2, 1, rows.length, rows[0].length).setValues(rows);
  sheet.autoResizeColumns(1, 9);
  SpreadsheetApp.getUi().alert("月次レポートを更新しました");
}

// === 週次レポート ===
function generateWeeklyReport() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME_WEEKLY);
  if (!sheet) sheet = ss.insertSheet(SHEET_NAME_WEEKLY);
  sheet.clear();

  sheet.getRange(1, 1, 1, 7).setValues([[
    "週",
    "セッション",
    "UU",
    "CTAクリック",
    "チケット購入",
    "寄付/協賛",
    "JSエラー"
  ]]).setFontWeight("bold").setBackground("#f7efe2");

  const now = new Date();
  const rows = [];

  // 過去12週間分
  for (let i = 11; i >= 0; i--) {
    const end = new Date(now);
    end.setDate(end.getDate() - i * 7);
    const start = new Date(end);
    start.setDate(start.getDate() - 6);
    const label = Utilities.formatDate(start, Session.getScriptTimeZone(), "MM/dd") +
                  " - " +
                  Utilities.formatDate(end, Session.getScriptTimeZone(), "MM/dd");

    const sessions = runReport(start, end, [{ name: "sessions" }]);
    const users = runReport(start, end, [{ name: "totalUsers" }]);
    const ctaClicks = runEventReport(start, end, "cta_click");
    const tickets = runEventReport(start, end, "ticket_purchase_click");
    const donations = runEventReport(start, end, "donation_click") +
                      runEventReport(start, end, "sponsor_click");
    const errors = runEventReport(start, end, "js_error");

    rows.push([label, sessions, users, ctaClicks, tickets, donations, errors]);
  }

  sheet.getRange(2, 1, rows.length, rows[0].length).setValues(rows);
  sheet.autoResizeColumns(1, 7);
  SpreadsheetApp.getUi().alert("週次レポートを更新しました");
}

// === GA4 メトリクス取得 ===
function runReport(start, end, metrics) {
  const startStr = Utilities.formatDate(start, Session.getScriptTimeZone(), "yyyy-MM-dd");
  const endStr = Utilities.formatDate(end, Session.getScriptTimeZone(), "yyyy-MM-dd");
  try {
    const request = {
      dateRanges: [{ startDate: startStr, endDate: endStr }],
      metrics: metrics,
    };
    const response = AnalyticsData.Properties.runReport(request, "properties/" + GA4_PROPERTY_ID);
    if (response.rows && response.rows.length > 0) {
      return Number(response.rows[0].metricValues[0].value);
    }
    return 0;
  } catch (e) {
    console.error("runReport error:", e);
    return 0;
  }
}

// === GA4 イベント数取得 ===
function runEventReport(start, end, eventName) {
  const startStr = Utilities.formatDate(start, Session.getScriptTimeZone(), "yyyy-MM-dd");
  const endStr = Utilities.formatDate(end, Session.getScriptTimeZone(), "yyyy-MM-dd");
  try {
    const request = {
      dateRanges: [{ startDate: startStr, endDate: endStr }],
      dimensions: [{ name: "eventName" }],
      metrics: [{ name: "eventCount" }],
      dimensionFilter: {
        filter: {
          fieldName: "eventName",
          stringFilter: { value: eventName },
        },
      },
    };
    const response = AnalyticsData.Properties.runReport(request, "properties/" + GA4_PROPERTY_ID);
    if (response.rows && response.rows.length > 0) {
      return Number(response.rows[0].metricValues[0].value);
    }
    return 0;
  } catch (e) {
    console.error("runEventReport error:", e);
    return 0;
  }
}

// === 自動実行トリガー（毎週月曜の朝9時）===
function setupTriggers() {
  // 既存トリガーをすべて削除
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(function (t) { ScriptApp.deleteTrigger(t); });

  // 月次：毎月1日 朝9時
  ScriptApp.newTrigger("generateMonthlyReport")
    .timeBased()
    .onMonthDay(1)
    .atHour(9)
    .create();

  // 週次：毎週月曜 朝9時
  ScriptApp.newTrigger("generateWeeklyReport")
    .timeBased()
    .everyWeeks(1)
    .onWeekDay(ScriptApp.WeekDay.MONDAY)
    .atHour(9)
    .create();

  SpreadsheetApp.getUi().alert("自動トリガーを設定しました（毎週月曜9時に週次、毎月1日9時に月次）");
}
```

## 3. 実行

1. 一度メニューから「月次レポートを更新」を実行
2. 初回は権限承認画面が出るので承認
3. データがスプレッドシートに書き込まれることを確認

## 4. 自動化（任意）

エディタで関数 `setupTriggers` を1回だけ手動実行すると、以降は自動で：
- 毎週月曜 9:00 → 週次レポート更新
- 毎月 1 日 9:00 → 月次レポート更新

## 5. ファネル可視化

スプレッドシート上で：
1. 月次レポートのデータを範囲選択
2. 挿入 → グラフ → 折れ線グラフ or 漏斗グラフ
3. シートに貼り付けて目視確認

## 6. Looker Studio 連携（オプション）

更に高度な可視化が欲しい場合は Looker Studio（旧 Data Studio）で：
1. https://lookerstudio.google.com/ にアクセス
2. 「データに接続」→ GA4 → プロパティ選択
3. 既製テンプレートで自動的にダッシュボード生成

これで GAS 不要でリッチなダッシュボードが手に入ります。

## 7. アラート（オプション）

エラーが急増した時にメール通知する場合：

```javascript
function checkErrorAlert() {
  const now = new Date();
  const yesterday = new Date(now);
  yesterday.setDate(yesterday.getDate() - 1);
  const errors = runEventReport(yesterday, yesterday, "js_error");

  if (errors > 50) {  // 1日50件以上のエラーで通知
    MailApp.sendEmail({
      to: "hagiyu5912@gmail.com",
      subject: "[秋川花火] JSエラーが急増しています",
      body: "昨日のJSエラー数: " + errors + "件\n\nGAで詳細確認: https://analytics.google.com/"
    });
  }
}
```

これを毎朝のトリガーに追加すれば、エラー多発時にメール通知が来ます。

---

## トラブルシューティング

**Q. AnalyticsData が認識されない**
→ Apps Script の「サービス」で Google Analytics Data API を追加してください

**Q. データが 0 になる**
→ GA4 プロパティID が正しいか確認。データの反映には 24-48 時間かかる場合あり

**Q. 権限エラー**
→ スクリプトを実行する Google アカウントが GA4 プロパティの閲覧権限を持っているか確認
