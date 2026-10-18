// JRE MALLチケットの商品ページ（a180-09: 観覧席 / a180-10: 駐車場）で、11/14 のプランごとの状態を読む。
// 戻り値: { read_at, plans: {プランID: 状態}, raw: {判定できなかったプラン: セルのHTML} }
// 状態 = available（〇）| few（△）| soldout（✕）| unknown
(async () => {
  for (let i = 0; i < 10 && !document.querySelector('[id^=plan-] [data-day="14"]'); i++) await new Promise(r => setTimeout(r, 1000));
  // 売り切れの✕アイコン（2026-10-18 の画面で確認した形）。これ以外の svg は判定しない
  const CROSS = 'M10.1210938,8l5.4394531';
  const plans = {}, raw = {};
  document.querySelectorAll('[id^=plan-]').forEach(p => {
    const id = p.id.replace('plan-', '');
    const d = p.querySelector('[data-day="14"]');
    let st = 'unknown';
    if (d) {
      const name = d.querySelector('.activity-spot-name');
      const path = name && name.querySelector('svg path');
      if (name && name.querySelector('i.js-reservation_available')) st = 'available';
      else if (name && name.querySelector('i.js-reservation_only_a_few')) st = 'few';
      else if (path && (path.getAttribute('d') || '').replace(/\s+/g, '').startsWith(CROSS)) st = 'soldout';
    }
    plans[id] = st;
    if (st === 'unknown') raw[id] = d ? d.outerHTML.replace(/\s+/g, ' ').slice(0, 600) : '(14日のセルが無い)';
  });
  if (!Object.keys(plans).length) return { error: 'プランが見つからない（待合室・エラー画面？）', url: location.href };
  return { read_at: new Date().toISOString(), url: location.href, plans, raw };
})()
