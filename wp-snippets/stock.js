/*
 * チケットページの在庫表示（〇△✕・空席あり/残りわずか/完売・○月○日時点）を、
 * 毎朝作る stock.json の内容に差し替える。
 * stock.json は毎朝の定期実行が gas/hanabi-uriage/build_stock_json.py で作る
 * （手順は gas/hanabi-uriage/STOCK_DAILY.md）。HTMLもそのスクリプトが作るので、
 * ここでは中身を入れ替えるだけ（判定のロジックは持たない）。
 * 読み込めないとき・ページの方が新しいときは何もしない（ページに書いてある表示のまま）。
 */
(function () {
  'use strict';
  var SRC = 'https://akigawa-hanabi.pages.dev/wp-snippets/stock.json';

  function pageDate() {
    var e = document.querySelector('.akg-asof[data-date]');
    return e ? e.getAttribute('data-date') : '';
  }

  function apply(d) {
    if (!d || typeof d.date !== 'string' || !d.buylists || !d.cards) return;
    if (d.date < pageDate()) return;
    Object.keys(d.buylists).forEach(function (k) {
      var el = document.querySelector('.akg-buylist[data-stock="' + k + '"]');
      if (el) el.innerHTML = d.buylists[k];
    });
    Object.keys(d.cards).forEach(function (k) {
      var el = document.querySelector('.akg-sf--' + k + ' .akg-sf__stock');
      if (el) el.outerHTML = d.cards[k];
    });
    Array.prototype.forEach.call(document.querySelectorAll('.akg-asof'), function (e) {
      e.textContent = d.asof;
      e.setAttribute('data-date', d.date);
    });
  }

  function run() {
    if (!window.fetch || !document.querySelector('.akg-buylist[data-stock]')) return;
    fetch(SRC, { cache: 'no-cache' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(apply)
      .catch(function () {});
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
})();
