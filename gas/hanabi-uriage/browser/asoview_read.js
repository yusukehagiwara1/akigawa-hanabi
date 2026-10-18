// アソビュー（urakata）の「公演予定」画面で、11/14 の席種ごとの状態を読む。
// 使い方: 商品ページで asoview_open.js（「公演予定を確認する」を押す）を実行して公演予定の画面に移ってから、これを実行する。
// 戻り値: { read_at, date: 日付の行の状態, seats: {席種名: 状態} }  状態 = available | few | soldout | unknown
// アイコンは画面の凡例（…発売中 など）と形を突き合わせて読む。凡例が区別できないときは error。
(async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const norm = s => (s || '').replace(/\s+/g, '');
  const MAP = { '…発売中': 'available', '…残りわずか': 'few', '…予定枚数終了': 'soldout', '…販売期間外': 'unknown' };
  const legend = {};
  for (const e of document.querySelectorAll('div,span,p,li')) {
    const t = (e.innerText || '').trim();
    const svg = e.querySelector('svg');
    if (!MAP[t] || !svg || e.children.length > 3) continue;
    const k = norm(svg.innerHTML);
    if (k in legend && legend[k] !== MAP[t]) return { error: '凡例のアイコンが区別できない', url: location.href };
    legend[k] = MAP[t];
  }
  const vals = Object.values(legend);
  if (!['available', 'few', 'soldout'].every(v => vals.includes(v))) return { error: '凡例が読めない（公演予定の画面ではない？）', url: location.href };
  const icon = el => { const s = el && el.querySelector('svg'); return s ? (legend[norm(s.innerHTML)] || 'unknown') : 'unknown'; };

  const sum = [...document.querySelectorAll('summary')].find(e => /2026\/11\/14/.test(e.innerText));
  if (!sum) return { error: '11/14 の行がない', url: location.href };
  const date = icon(sum);
  const det = sum.closest('details');
  if (det && !det.open) { sum.click(); await sleep(1500); }
  // 「開演時間 12:00」（中の details）を開く。席種が出てくる。開いているものは押さない（押すと閉じる）
  for (const d of (det ? det.querySelectorAll('details') : [])) {
    if (!d.open && d.querySelector('summary')) { d.querySelector('summary').click(); await sleep(2000); }
  }

  const seats = {};
  const isState = s => norm(s.innerHTML) in legend;
  (det || document).querySelectorAll('svg').forEach(s => {
    if (sum.contains(s) || !isState(s)) return;
    let st = legend[norm(s.innerHTML)];
    let p = s.parentElement;
    for (let i = 0; i < 4 && p && !(p.innerText || '').trim(); i++) p = p.parentElement;
    const name = ((p && p.innerText) || '').trim().split('\n')[0].trim();
    if (!name || /^2026/.test(name) || name in seats) return;
    // その席の行（状態アイコンを1つだけ含む一番外側の要素）。✕なのに購入ボタンがあれば判定しない
    let row = s.parentElement;
    while (row.parentElement && row.parentElement !== det && [...row.parentElement.querySelectorAll('svg')].filter(isState).length === 1) row = row.parentElement;
    const buy = [...row.querySelectorAll('button, a')].some(b => /購入|申込/.test(b.innerText || ''));
    if (st === 'soldout' && buy) st = 'unknown';
    seats[name] = st;
  });
  return { read_at: new Date().toISOString(), url: location.href, date, seats };
})()
