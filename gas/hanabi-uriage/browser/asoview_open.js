// アソビュー（urakata）の商品ページで「公演予定を確認する」を押す（ふつうの利用者と同じ操作。購入はしない）。
// 押したあと公演予定の画面に移ったら、asoview_read.js を実行する。
(async () => {
  for (let i = 0; i < 10; i++) {
    const b = [...document.querySelectorAll('button')].find(x => (x.innerText || '').trim() === '公演予定を確認する');
    if (b) { b.click(); await new Promise(r => setTimeout(r, 3500)); return { clicked: true, url: location.href }; }
    await new Promise(r => setTimeout(r, 1000));
  }
  return { clicked: false, url: location.href, text: (document.body.innerText || '').replace(/\s+/g, ' ').slice(0, 200) };
})()
