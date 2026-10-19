// 既存ページに、ミニ四駆大会のページ（/mini4wd/）への入口を足す。
// WordPress の管理画面（ログイン済み）で javascript として実行する。
//   window.__M4_APPLY = false のまま実行 → 変更点の確認だけ（書き込まない）
//   window.__M4_APPLY = true にして実行 → 書き込む
// 公開中の本文をその場で読み、決まった位置に差し込む。すでに /mini4wd/ が入っているページは飛ばす。
// チケットページ（1711）はリポジトリの ticket-page-content.html を丸ごと送る別手順（在庫表示と一緒に管理しているため）。
(async () => {
  const APPLY = !!window.__M4_APPLY;
  const nonce = (window.aioseo && window.aioseo.nonce) || (window.wpApiSettings && window.wpApiSettings.nonce);
  if (!nonce) return { error: 'nonce が無い（ログイン切れ？）' };
  const H = { 'X-WP-Nonce': nonce };
  const M4 = 'https://machizukuri-con.or.jp/mini4wd/';
  const KV = 'https://machizukuri-con.or.jp/wp-content/uploads/mini4wd-kv-1024x768.jpg';
  const KV_ALT = 'ミニ四駆☆TOKYO 秋川流域 GRAND PRIX 2026。11月14日（土）12:00〜17:30、東京サマーランド第2駐車場 イベントエリア。秋川流域花火大会とのコラボ開催。';

  // 関連ページのリスト: 「チケット情報」の次に1行足す
  const REL_ANCHOR = '<li><a href="https://machizukuri-con.or.jp/ticket/">チケット情報</a>（席の種類・購入方法）</li>\n<!-- /wp:list-item -->\n\n';
  const REL_ITEM = '<!-- wp:list-item -->\n<li><a href="' + M4 + '">ミニ四駆☆TOKYO 秋川流域 GRAND PRIX 2026</a>（花火大会とのコラボ企画・コラボチケット）</li>\n<!-- /wp:list-item -->\n\n';
  const related = s => {
    const i = s.lastIndexOf('関連ページ');
    const j = s.indexOf(REL_ANCHOR, i);
    if (i < 0 || j < 0) throw new Error('関連ページのリストが見つからない');
    return s.slice(0, j + REL_ANCHOR.length) + REL_ITEM + s.slice(j + REL_ANCHOR.length);
  };
  const insertAfter = (s, anchor, add) => {
    const n = s.split(anchor).length - 1;
    if (n !== 1) throw new Error('差し込み位置が ' + n + ' か所: ' + anchor.slice(0, 60));
    return s.replace(anchor, () => anchor + add);
  };
  const replaceOnce = (s, a, b) => {
    const n = s.split(a).length - 1;
    if (n !== 1) throw new Error('置き換え位置が ' + n + ' か所: ' + a.slice(0, 60));
    return s.replace(a, () => b);
  };

  const PATCHES = [
    // トップページ: 「チケット情報」節の「チケット情報を見る」ボタンの下
    { type: 'pages', id: 7, name: 'トップページ', fn: s => insertAfter(s,
      '<div class="swell-block-button green_ is-style-btn_shiny"><a href="https://machizukuri-con.or.jp/ticket/" class="swell-block-button__link"><span>チケット情報を見る</span></a></div>\n<!-- /wp:loos/button -->',
      '\n\n<!-- wp:paragraph {"align":"center","className":"u-mt-ctrl u-mt-40"} -->\n<p class="has-text-align-center u-mt-ctrl u-mt-40"><strong>花火大会の「A席」とミニ四駆の走行体験がセットになった、コラボチケットもあります。</strong></p>\n<!-- /wp:paragraph -->\n\n' +
      '<!-- wp:image {"id":4816,"width":"640px","sizeSlug":"large","linkDestination":"custom","align":"center"} -->\n<figure class="wp-block-image aligncenter size-large is-resized"><a href="' + M4 + '"><img src="' + KV + '" alt="' + KV_ALT + '" class="wp-image-4816" style="width:640px"/></a></figure>\n<!-- /wp:image -->\n\n' +
      '<!-- wp:loos/button {"hrefUrl":"' + M4 + '","color":"red","className":"is-style-btn_line"} -->\n<div class="swell-block-button red_ is-style-btn_line"><a href="' + M4 + '" class="swell-block-button__link"><span>ミニ四駆大会のページを見る</span></a></div>\n<!-- /wp:loos/button -->') },
    // イベント一覧: 冒頭の注記（第7回の記録）の直後に、第8回の新企画として1節
    { type: 'pages', id: 1702, name: 'イベント一覧', fn: s => insertAfter(s,
      '第8回大会（2026年11月14日）の内容は、決まり次第順次更新します。</p>\n<!-- /wp:paragraph -->',
      '\n\n<!-- wp:loos/full-wide {"bgColor":"#ffffff","contentSize":"container","pcPadding":"20","spPadding":"20","anchor":"mini4wd"} -->\n<div class="swell-block-fullWide pc-py-20 sp-py-20 alignfull" style="background-color:#ffffff" id="mini4wd"><div class="swell-block-fullWide__inner l-container"><!-- wp:heading {"className":"is-style-section_ttl"} -->\n<h2 class="wp-block-heading is-style-section_ttl">ミニ四駆（12:00～17:30）</h2>\n<!-- /wp:heading -->\n\n' +
      '<!-- wp:paragraph -->\n<p>第8回は新しく、花火大会とのコラボ企画「ミニ四駆☆TOKYO 秋川流域 GRAND PRIX 2026」を開催します。花火観覧エリアのとなりのイベントエリアで、5レーン公式模擬コースの走行体験会・ミニ四駆組み立て教室・物販コーナーを行います。花火大会の「A席」と走行体験がセットになったコラボチケットもあります。</p>\n<!-- /wp:paragraph -->\n\n' +
      '<!-- wp:image {"id":4816,"width":"640px","sizeSlug":"large","linkDestination":"custom","align":"center"} -->\n<figure class="wp-block-image aligncenter size-large is-resized"><a href="' + M4 + '"><img src="' + KV + '" alt="' + KV_ALT + '" class="wp-image-4816" style="width:640px"/></a></figure>\n<!-- /wp:image -->\n\n' +
      '<!-- wp:loos/button {"hrefUrl":"' + M4 + '","color":"blue","className":"is-style-btn_line"} -->\n<div class="swell-block-button blue_ is-style-btn_line"><a href="' + M4 + '" class="swell-block-button__link"><span><strong>くわしく見る</strong></span></a></div>\n<!-- /wp:loos/button --></div></div>\n<!-- /wp:loos/full-wide -->') },
    // 楽しみ方: 「子ども向けの遊び・体験」の「第8回は決まり次第お知らせします」をミニ四駆の案内に置き換える＋関連ページ
    { type: 'pages', id: 4556, name: '楽しみ方', fn: s => related(replaceOnce(s,
      '第8回の遊び・体験は決まり次第お知らせします。</p>',
      '第8回は、花火観覧エリアのとなりのイベントエリアで「<a href="' + M4 + '">ミニ四駆☆TOKYO 秋川流域 GRAND PRIX 2026</a>」（12:00〜17:30）を開催します。5レーン公式模擬コースの走行体験会や、ミニ四駆の組み立て教室があります。そのほかの遊び・体験は決まり次第お知らせします。</p>')) },
    { type: 'pages', id: 4558, name: '来場ガイド', fn: related },
    { type: 'pages', id: 4555, name: '秋川で過ごす一日', fn: related },
    { type: 'pages', id: 4559, name: '天候・開催情報', fn: related },
    { type: 'pages', id: 4557, name: 'もっと知る', fn: related },
    { type: 'pages', id: 4560, name: '花火師のご紹介', fn: related },
    { type: 'posts', id: 4572, name: 'お知らせ（音楽紹介）', fn: related },
  ];

  // ミニ四駆のページが公開されてからでないとリンク切れになるので、公開を確かめてから進む
  const m4 = await fetch('/wp-json/wp/v2/pages/4825?context=edit&_fields=status,slug', { headers: H }).then(r => r.json());
  if (APPLY && !(m4.status === 'publish' && m4.slug === 'mini4wd')) return { error: 'ミニ四駆のページが未公開（' + m4.status + '）。反映しない' };

  const out = [];
  for (const p of PATCHES) {
    try {
      const j = await fetch('/wp-json/wp/v2/' + p.type + '/' + p.id + '?context=edit&_fields=id,content,status,_links', { headers: H }).then(r => r.json());
      // <style> を含む本文を送り直すので、unfiltered_html 権限が無いアカウントでは書き込まない（見た目が崩れるため）
      if (APPLY && !(j._links && j._links['wp:action-unfiltered-html'])) { out.push([p.name, '権限なし（unfiltered_html）のため中止']); continue; }
      const raw = j.content.raw;
      if (raw.includes(M4)) { out.push([p.name, 'すでに入っている（飛ばした）']); continue; }
      const next = p.fn(raw);
      if (!APPLY) { out.push([p.name, '確認OK +' + (next.length - raw.length) + '文字']); continue; }
      const r = await fetch('/wp-json/wp/v2/' + p.type + '/' + p.id, { method: 'POST', headers: Object.assign({ 'Content-Type': 'application/json' }, H), body: JSON.stringify({ content: next }) });
      out.push([p.name, r.ok ? '更新した' : '失敗 ' + r.status]);
    } catch (e) { out.push([p.name, 'エラー: ' + e.message]); }
  }
  return out;
})()
