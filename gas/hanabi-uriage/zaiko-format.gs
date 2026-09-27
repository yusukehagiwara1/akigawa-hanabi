/**
 * 「在庫」シートの見た目を整える（中身の数式は触らない）。
 * Apps Script エディタでこのファイルを開き、zaikoFormat を実行する。
 */
function zaikoFormat() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName('在庫');
  if (!sh) throw new Error('「在庫」シートが見つかりません');

  var T1_TOP = 6, T1_BOT = 13;   // ① 席種ごと（6=見出し, 7-13=データ）
  var T2_TOP = 16, T2_BOT = 58;  // ② 販売サイト別（16=見出し, 17-58=データ）
  var NAVY = '#1f3864', LIGHT = '#eef2f8';
  var GREEN = '#1b7f3a', GREEN_BG = '#e6f4ea';
  var YELLOW = '#8a6300', YELLOW_BG = '#fff4cc';
  var RED = '#c62828', RED_BG = '#fdecea';
  var GRAY = '#999999';

  sh.clearConditionalFormatRules();
  sh.getRange(1, 1, sh.getMaxRows(), sh.getMaxColumns())
    .setBorder(false, false, false, false, false, false)
    .setBackground(null).setFontWeight('normal').setFontColor('#222222')
    .setFontSize(10).setHorizontalAlignment('left').setVerticalAlignment('middle');

  // ---- タイトルと説明 ----
  sh.getRange('A1:H1').merge();
  sh.getRange('A1').setValue('在庫数（自動計算）')
    .setFontSize(16).setFontWeight('bold').setFontColor('#ffffff')
    .setBackground(NAVY).setVerticalAlignment('middle');
  sh.setRowHeight(1, 40);
  sh.getRange('A2:H2').merge();
  sh.getRange('A3:H3').merge();
  sh.getRange('A2:H3').setFontSize(10).setFontColor('#555555').setWrap(true);
  sh.setRowHeight(2, 22);
  sh.setRowHeight(3, 22);

  // ---- ブロック見出し ----
  [5, 15].forEach(function (r) {
    sh.getRange(r, 1, 1, 8).merge();
    sh.getRange(r, 1).setFontSize(12).setFontWeight('bold').setFontColor(NAVY);
    sh.setRowHeight(r, 28);
  });

  // ---- 表の共通書式 ----
  function styleTable(top, bot, cols) {
    var head = sh.getRange(top, 1, 1, cols);
    head.setFontWeight('bold').setFontColor('#ffffff').setBackground(NAVY)
      .setHorizontalAlignment('center').setVerticalAlignment('middle');
    sh.setRowHeight(top, 30);
    var body = sh.getRange(top + 1, 1, bot - top, cols);
    body.setVerticalAlignment('middle');
    sh.getRange(top, 1, bot - top + 1, cols)
      .setBorder(true, true, true, true, true, true, '#b7c3d6', SpreadsheetApp.BorderStyle.SOLID);
    // 1行おきの薄い色
    for (var r = top + 1; r <= bot; r++) {
      if ((r - top) % 2 === 0) sh.getRange(r, 1, 1, cols).setBackground(LIGHT);
    }
  }
  styleTable(T1_TOP, T1_BOT, 7);
  styleTable(T2_TOP, T2_BOT, 8);

  // ---- 数値・配置 ----
  sh.getRange(T1_TOP + 1, 2, T1_BOT - T1_TOP, 3).setNumberFormat('#,##0').setHorizontalAlignment('right');
  sh.getRange(T1_TOP + 1, 5, T1_BOT - T1_TOP, 1).setHorizontalAlignment('right');
  sh.getRange(T1_TOP + 1, 6, T1_BOT - T1_TOP, 1).setHorizontalAlignment('center').setFontWeight('bold');
  sh.getRange(T1_TOP + 1, 7, T1_BOT - T1_TOP, 1).setFontSize(9).setFontColor('#777777').setWrap(true);

  sh.getRange(T2_TOP + 1, 3, T2_BOT - T2_TOP, 3).setNumberFormat('#,##0').setHorizontalAlignment('right');
  sh.getRange(T2_TOP + 1, 6, T2_BOT - T2_TOP, 1).setHorizontalAlignment('right');
  sh.getRange(T2_TOP + 1, 7, T2_BOT - T2_TOP, 1).setHorizontalAlignment('center').setFontSize(14).setFontWeight('bold');
  sh.getRange(T2_TOP + 1, 8, T2_BOT - T2_TOP, 1).setFontSize(9).setFontColor('#888888');

  // 席種が変わる行に太い区切り線（6サイトごと）
  for (var r = T2_TOP + 7; r <= T2_BOT; r += 6) {
    sh.getRange(r, 1, 1, 8).setBorder(true, null, null, null, null, null, NAVY, SpreadsheetApp.BorderStyle.SOLID_MEDIUM);
  }

  // ---- 色分け（条件付き書式）----
  var markRange = sh.getRange(T2_TOP + 1, 7, T2_BOT - T2_TOP, 1);
  var dispRange = sh.getRange(T1_TOP + 1, 6, T1_BOT - T1_TOP, 1);
  var rules = [];
  function rule(range, text, color, bg) {
    rules.push(SpreadsheetApp.newConditionalFormatRule()
      .whenTextEqualTo(text).setFontColor(color).setBackground(bg).setBold(true)
      .setRanges([range]).build());
  }
  rule(markRange, '〇', GREEN, GREEN_BG);
  rule(markRange, '△', YELLOW, YELLOW_BG);
  rule(markRange, '✕', RED, RED_BG);
  rule(markRange, '―', GRAY, '#f5f5f5');
  rule(dispRange, '空席あり', GREEN, GREEN_BG);
  rule(dispRange, '残りわずか', YELLOW, YELLOW_BG);
  rule(dispRange, '完売', RED, RED_BG);
  sh.setConditionalFormatRules(rules);

  // ---- 列幅・固定 ----
  sh.setColumnWidth(1, 220); // 席種
  sh.setColumnWidth(2, 110); // 在庫数 / 販売サイト
  sh.setColumnWidth(3, 80);
  sh.setColumnWidth(4, 80);
  sh.setColumnWidth(5, 80);
  sh.setColumnWidth(6, 90);
  sh.setColumnWidth(7, 90);
  sh.setColumnWidth(8, 150);
  sh.setFrozenRows(3);
  sh.setHiddenGridlines(true);

  // ---- 注記 ----
  sh.getRange(T2_BOT + 2, 1, 2, 8).setFontSize(9).setFontColor('#777777');
  sh.getRange(T2_BOT + 2, 1, 1, 8).merge();
  sh.getRange(T2_BOT + 3, 1, 1, 8).merge();

  ss.toast('在庫シートの書式を整えました', '在庫', 5);
}
