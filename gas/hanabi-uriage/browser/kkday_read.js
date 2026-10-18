// KKday 商品ページ（https://www.kkday.com/ja/product/527261）で、プランごとの状態を読む。
// 戻り値: { read_at, options: {プランID: 状態} }  状態 = available | soldout | unknown
// 「直近の利用可能日」があれば available、末尾が「完売」なら soldout。
// どのプランにも「直近の利用可能日」が無いときは画面の作りが変わったとみなして全部 unknown。
(async () => {
  for (let i = 0; i < 10 && !document.querySelector('[id^=optionItem]'); i++) await new Promise(r => setTimeout(r, 1000));
  const items = [...document.querySelectorAll('[id^=optionItem]')];
  if (!items.length) return { error: 'プランが見つからない', url: location.href };
  const options = {};
  items.forEach(e => {
    const t = (e.innerText || '').replace(/\s+/g, ' ').trim();
    const avail = /直近の利用可能日/.test(t), out = /完売$/.test(t);
    options[e.id.replace('optionItem', '')] = avail && !out ? 'available' : (out && !avail ? 'soldout' : 'unknown');
  });
  if (!Object.values(options).includes('available')) Object.keys(options).forEach(k => { options[k] = 'unknown'; });
  return { read_at: new Date().toISOString(), url: location.href, options };
})()
