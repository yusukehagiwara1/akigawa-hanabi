/**
 * 「花火売上集計」スプレッドシートに『在庫』シートを作成／更新する。
 *
 * 配分（各販売サイトへの割当）− 販売数（集計シート）＝ 残り
 * 残りと記号は関数（数式）で入れるので、集計シートが更新されれば自動で変わる。
 * 配分が変わったときだけ、在庫シートの「配分」列を手で直す。
 *
 * 使い方: スプレッドシートを開く → メニュー「在庫」→「在庫シートを作り直す」
 */

var ZAIKO_SHEET = '在庫';
var SHUKEI_SHEET = '集計';

/** 席種の定義。shukeiCols は集計シートの列（複数あれば合算） */
var SEATS = [
  { name: 'リクライニング席（ペア）', cols: ['D'], alloc: { 'アソビュー': 75 }, note: '按分シートの150席＝75ペア' },
  { name: 'SS席',                     cols: ['E'], alloc: { 'アソビュー': 45, 'チケットぴあ': 0, '楽天トラベル': 10, 'KKday': 5, 'JRE MALL': 5 } },
  { name: 'S席',                      cols: ['F'], alloc: { 'アソビュー': 130, 'チケットぴあ': 30, '楽天トラベル': 10, 'KKday': 10, 'JRE MALL': 10 }, note: '按分シートは130だが座席番号は80席分のみ記載・要確認' },
  { name: 'A席（大人＋子ども）',       cols: ['G', 'H'], alloc: { 'アソビュー': 1200, 'チケットぴあ': 1000, '楽天トラベル': 600, 'KKday': 600, 'JRE MALL': 600 } },
  { name: 'フリーエリア',             cols: ['I', 'J'], alloc: { 'アソビュー': 1000 }, note: '按分シート対象外。西多摩在住者限定1,000名で計算' },
  { name: '駐車場①（会場隣接）',      cols: ['K'], alloc: { 'アソビュー': 300, 'チケットぴあ': 150, '楽天トラベル': 100, 'KKday': 100, 'JRE MALL': 100 } },
  { name: '駐車場②（プール側）',      cols: ['L'], alloc: { 'アソビュー': 200, 'チケットぴあ': 200, '楽天トラベル': 100, 'KKday': 100, 'JRE MALL': 100 } }
];

/** 在庫シートでのサイト名 → 集計シートでの呼び名 */
var SITES = [
  { label: 'アソビュー',   key: 'アソビュー' },
  { label: 'チケットぴあ', key: 'ぴあ' },
  { label: '楽天トラベル', key: '楽天トラベル' },
  { label: 'KKday',        key: 'KKday' },
  { label: 'JRE MALL',     key: 'JR MALL' },
  { label: 'さとふる',     key: 'ふるさと納税' }
];

var FEW_RATIO = 0.25; // 残りがこの割合以下なら △（残りわずか）

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('在庫')
    .addItem('在庫シートを作り直す', 'zaikoSheetRebuild')
    .addToUi();
}

function zaikoSheetRebuild() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(ZAIKO_SHEET);
  if (sh) {
    sh.clear();
    sh.clearNotes();
  } else {
    sh = ss.insertSheet(ZAIKO_SHEET, ss.getSheets().length);
  }

  // 集計シートの行を引く式（サイト名は区分2、ふるさと納税だけ区分1にある）
  var rowMatch = function (siteCell) {
    return 'IFERROR(MATCH(' + siteCell + ",'" + SHUKEI_SHEET + "'!$B$3:$B$8,0),MATCH(" +
      siteCell + ",'" + SHUKEI_SHEET + "'!$A$3:$A$8,0))";
  };
  var soldFormula = function (cols, siteCell) {
    var parts = cols.map(function (c) {
      return "INDEX('" + SHUKEI_SHEET + "'!$" + c + '$3:$' + c + '$8,' + rowMatch(siteCell) + ')';
    });
    return '=IFERROR(' + parts.join('+') + ',0)';
  };

  var r = 1;
  sh.getRange(r, 1).setValue('在庫数（自動計算）').setFontSize(14).setFontWeight('bold');
  r += 1;
  sh.getRange(r, 1).setValue('配分（各販売サイトへの割当）から、集計シートの販売数を引いて算出しています。集計シートが更新されれば自動で変わります。');
  r += 1;
  sh.getRange(r, 1).setValue('配分が変わったときは、下の表の「配分」列を直してください。記号は 〇＝在庫あり／△＝残りわずか（残り' +
    Math.round(FEW_RATIO * 100) + '%以下）／✕＝完売 です。');
  r += 2;

  // ---- 表1 席種ごとの合計 ----
  var t1Top = r;
  sh.getRange(r, 1).setValue('① 席種ごと').setFontWeight('bold');
  r += 1;
  var head1 = ['席種', '在庫数', '販売数', '残り', '残率', '表示', '備考'];
  sh.getRange(r, 1, 1, head1.length).setValues([head1]).setFontWeight('bold').setBackground('#efefef');
  var h1 = r;
  r += 1;
  var t1First = r;
  SEATS.forEach(function (seat) {
    sh.getRange(r, 1).setValue(seat.name);
    r += 1;
  });
  var t1Last = r - 1;
  r += 1;

  // ---- 表2 販売サイト別 ----
  sh.getRange(r, 1).setValue('② 販売サイト別').setFontWeight('bold');
  r += 1;
  var head2 = ['席種', '販売サイト', '配分', '販売数', '残り', '残率', '記号'];
  sh.getRange(r, 1, 1, head2.length).setValues([head2]).setFontWeight('bold').setBackground('#efefef');
  r += 1;
  var t2First = r;
  var rows2 = [];
  SEATS.forEach(function (seat) {
    SITES.forEach(function (site) {
      rows2.push({ seat: seat, site: site, row: r });
      r += 1;
    });
  });
  var t2Last = r - 1;

  // 表2の中身
  rows2.forEach(function (x) {
    var row = x.row;
    var alloc = x.seat.alloc[x.site.label];
    sh.getRange(row, 1).setValue(x.seat.name);
    sh.getRange(row, 2).setValue(x.site.label);
    if (x.site.label === 'さとふる') {
      sh.getRange(row, 3).setValue(''); // 按分シート対象外
    } else {
      sh.getRange(row, 3).setValue(alloc === undefined ? 0 : alloc);
    }
    sh.getRange(row, 4).setFormula(soldFormula(x.seat.cols, '$B' + row));
    sh.getRange(row, 5).setFormula('=IF($C' + row + '="","",$C' + row + '-$D' + row + ')');
    sh.getRange(row, 6).setFormula('=IF(OR($C' + row + '="",$C' + row + '=0),"",$E' + row + '/$C' + row + ')');
    sh.getRange(row, 7).setFormula(
      '=IFS($C' + row + '="","―（按分対象外）",' +
      '$C' + row + '=0,"―（取扱なし）",' +
      '$E' + row + '<=0,"✕",' +
      '$F' + row + '<=' + FEW_RATIO + ',"△",' +
      'TRUE,"〇")'
    );
  });

  // 表1の中身（表2を集計）
  var seatCol2 = "$A$" + t2First + ":$A$" + t2Last;
  SEATS.forEach(function (seat, i) {
    var row = t1First + i;
    sh.getRange(row, 2).setFormula('=SUMIF(' + seatCol2 + ',$A' + row + ',$C$' + t2First + ':$C$' + t2Last + ')');
    sh.getRange(row, 3).setFormula('=SUMIF(' + seatCol2 + ',$A' + row + ',$D$' + t2First + ':$D$' + t2Last + ')');
    sh.getRange(row, 4).setFormula('=$B' + row + '-$C' + row);
    sh.getRange(row, 5).setFormula('=IF($B' + row + '=0,"",$D' + row + '/$B' + row + ')');
    sh.getRange(row, 6).setFormula(
      '=IFS($D' + row + '<=0,"完売",$E' + row + '<=' + FEW_RATIO + ',"残りわずか",TRUE,"空席あり")'
    );
    if (seat.note) sh.getRange(row, 7).setValue(seat.note);
  });

  // ---- 見た目 ----
  sh.getRange(t1First, 2, SEATS.length, 3).setNumberFormat('#,##0');
  sh.getRange(t1First, 5, SEATS.length, 1).setNumberFormat('0%');
  sh.getRange(t2First, 3, rows2.length, 3).setNumberFormat('#,##0');
  sh.getRange(t2First, 6, rows2.length, 1).setNumberFormat('0%');
  sh.getRange(h1, 1, t1Last - h1 + 1, 7).setBorder(true, true, true, true, true, true);
  sh.getRange(t2First - 1, 1, rows2.length + 1, 7).setBorder(true, true, true, true, true, true);
  sh.setColumnWidth(1, 200);
  sh.setColumnWidth(2, 120);
  sh.setColumnWidth(7, 340);
  sh.setFrozenRows(t1Top + 1);

  // 記号の色分け（〇＝青／△＝緑／✕＝赤）※サイトページの表示に合わせています
  var markRange = sh.getRange(t2First, 7, rows2.length, 1);
  var rules = [
    { text: '〇', color: '#1b7f3a' },
    { text: '△', color: '#b38000' },
    { text: '✕', color: '#c62828' }
  ].map(function (o) {
    return SpreadsheetApp.newConditionalFormatRule()
      .whenTextEqualTo(o.text)
      .setFontColor(o.color)
      .setBold(true)
      .setRanges([markRange])
      .build();
  });
  var dispRange = sh.getRange(t1First, 6, SEATS.length, 1);
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('完売')
    .setFontColor('#c62828').setBold(true).setRanges([dispRange]).build());
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('残りわずか')
    .setFontColor('#b38000').setBold(true).setRanges([dispRange]).build());
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('空席あり')
    .setFontColor('#1b7f3a').setBold(true).setRanges([dispRange]).build());
  sh.setConditionalFormatRules(rules);

  sh.getRange(t2Last + 2, 1).setValue(
    '※さとふる（ふるさと納税）は座席按分シートに割当がないため、販売数だけを表示しています。席種ごとの残りには含めて計算しています。'
  );
  sh.getRange(t2Last + 3, 1).setValue('※配分の出どころ: 「花火座席情報・座席按分」スプレッドシートの座席数按分シート');

  SpreadsheetApp.getActiveSpreadsheet().toast('在庫シートを更新しました', '在庫', 5);
}
