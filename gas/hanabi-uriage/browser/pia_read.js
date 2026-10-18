// チケットぴあの公演ページ（ticketInformation.do?eventCd=2625008&rlsCd=001）で、券種ごとの表示を読む。
// 戻り値: { read_at, seats: {券種名: 表示（発売中 / 予定枚数終了 など）} }
(() => {
  const seats = {};
  document.querySelectorAll('.ticketSelect__text').forEach(t => {
    const icon = t.parentElement && t.parentElement.querySelector('.ticketSelect__icon');
    const name = (t.innerText || '').trim();
    if (name && icon && !(name in seats)) seats[name] = (icon.innerText || '').trim();
  });
  if (!Object.keys(seats).length) return { error: '券種が見つからない（混雑・エラー画面？）', url: location.href };
  return { read_at: new Date().toISOString(), url: location.href, seats };
})()
