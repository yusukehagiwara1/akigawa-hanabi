(function () {
  'use strict';
  // NOTE: WordPress (wptexturize) treats a bare less-than sign in this script as the start of an HTML tag
  // and rewrites any ampersand up to the next greater-than sign into an entity. Never write a bare
  // less-than sign here: write comparisons as "n > i", not the reversed form.
  var root = document.getElementById('akg-quiz');
  if (!root) { return; }
  if (root.getAttribute('data-akg-init') === '1') { return; } // already initialised (duplicate script)
  root.setAttribute('data-akg-init', '1');
  var panel = root.querySelector('[data-akg="panel"]');
  var stepEl = root.querySelector('[data-akg="step"]');
  var barEl = root.querySelector('[data-akg="bar"]');
  var noteEl = root.querySelector('[data-akg="note"]');
  var statusEl = root.querySelector('[data-akg="status"]');
  if (!panel) { return; }

  // Asoview (urakata) list page: SS / S / A seats are bought from this list
  var LIST_URL = 'https://machizukuricon.my.urakata.app/channels/debdd785-6f29-4fa5-827f-b8eb02f3a583/products?salesProductTagCode=v4h0rdje5x';
  var UP = 'https://machizukuri-con.or.jp/wp-content/uploads/';

  // Seat facts (price, spec, photo, purchase URL). Same as the seat cards on the ticket page.
  var SEATS = {
    recliner: { name: 'リクライニングペアシート席', catchcopy: '夜空を見上げる、くつろぎの体験', price: '1組 30,000円（2席）',
      spec: ['指定席。リクライニングシート付き。', 'アソビューだけで販売しています。'],
      img: UP + 'リクライニングシート_画像1-1024x768.jpg', alt: 'リクライニングペアシート席の写真',
      url: 'https://machizukuricon.my.urakata.app/channels/debdd785-6f29-4fa5-827f-b8eb02f3a583/products/e42dce79-988e-4b5d-bc20-099dbaf02d1d',
      only: true, hint: 'アソビューの予約ページが新しいタブで開きます。',
      why: 'ふたり並んで背もたれを倒し、夜空を見上げながら花火を観覧できる席です。1組2席・30,000円で、アソビューだけで販売しています。' },
    ss: { name: 'SS席', catchcopy: '家族で最高の思い出を', price: '1テーブル 35,000円（4名掛けのテーブル席）',
      spec: ['指定席。カフェチェア、カフェテーブル付き。', '第7回と異なりテントはありません。', 'お席は購入時に自動で決まります（ご自身で選ぶことはできません）。'],
      img: UP + '2026_SS席-1024x768.jpg', alt: 'SS席の写真', url: LIST_URL,
      only: false, hint: 'アソビューの一覧が新しいタブで開きます。「SS席」を選んでお進みください。',
      why: '4名掛けのテーブル席に、カフェチェアとカフェテーブルが付いています。家族やグループでテーブルを囲んで、食事と花火を楽しめます。4名なら1人あたり8,750円の計算です。※テントはありません。' },
    s: { name: 'S席', catchcopy: '特別な人と観る花火', price: '1テーブル 14,000円（2名掛けのテーブル席）',
      spec: ['指定席。テーブル、イス付き。'],
      img: UP + '2026_S席-1024x768.jpg', alt: 'S席の写真', url: LIST_URL,
      only: false, hint: 'アソビューの一覧が新しいタブで開きます。「S席」を選んでお進みください。',
      why: '2名掛けのテーブル席で、テーブルとイスが付いています。デートや記念日など、大切な時間にどうぞ。2名なら1人あたり7,000円の計算です。' },
    a: { name: 'A席', catchcopy: '迷ったらこれ！快適に楽しむ特等席', price: '大人 5,000円／子ども 2,000円（椅子席）',
      spec: ['指定席。テーブルなし。', 'お席は購入時に自動で決まります（ご自身で選ぶことはできません）。', '小さなお子さまの膝上観覧は無料です。'],
      img: UP + '2026_A席-1024x768.jpg', alt: 'A席の写真', url: LIST_URL,
      only: false, hint: 'アソビューの一覧が新しいタブで開きます。「A席」を選んでお進みください。',
      why: '大人5,000円・子ども2,000円の椅子席（テーブルなし）です。はじめての方に最も選ばれているスタンダードで、指定席なので場所取りの心配がありません。' },
    free: { name: 'フリーエリア', catchcopy: '西多摩在住者限定！フリーエリア', price: 'おとな 2,000円（13歳以上）／こども 1,000円（3歳～12歳）／2歳以下 無料',
      spec: ['限定1,000名。予定枚数に達し次第、販売を終了します。', '対象地域：青梅市・福生市・羽村市・あきる野市・瑞穂町・日の出町・檜原村・奥多摩町', 'エリア内の好きな場所で観覧できます。立ち見はできません。', '小さな折りたたみイス（背もたれなし・30cm程度）と人数分のレジャーシートは持ち込めます。', 'アソビューだけで販売しています。'],
      img: UP + 'フリーエリアチケット-1024x768.jpg', alt: 'フリーエリアの写真',
      url: 'https://machizukuricon.my.urakata.app/channels/d58e8525-0f46-4109-9740-1c1b928b5aa0/products/6dbcf060-4a33-4e3c-9348-551a867822d1',
      only: true, hint: 'アソビューの予約ページが新しいタブで開きます。',
      why: '西多摩にお住まいの方だけが買えるチケットです。おとな2,000円・こども1,000円・2歳以下無料。エリア内の好きな場所で観覧できます（立ち見はできません）。限定1,000名です。' }
  };

  // Questions. Q3 (area) is asked only when Q2 = price.
  var QUESTIONS = {
    with: { text: 'どなたと観覧しますか？', hint: '', col1: false, opts: [
      { v: 'family', main: '家族で', sub: 'お子さま連れ、ご両親とご一緒の方も' },
      { v: 'friends', main: '友人・グループで', sub: 'お仲間や同僚と' },
      { v: 'couple', main: 'カップル・ご夫婦で', sub: 'ふたりで' },
      { v: 'solo', main: 'おひとりで', sub: '1名でゆっくり' } ] },
    priority: { text: 'いちばん大切にしたいことは？', hint: '', col1: false, opts: [
      { v: 'relax', main: 'ゆったり過ごしたい', sub: '席でゆっくりくつろぎたい' },
      { v: 'focus', main: '花火に集中して楽しみたい', sub: 'テーブルはなくても、花火をしっかり観たい' },
      { v: 'price', main: '料金を抑えたい', sub: '気軽に楽しみたい' },
      { v: 'special', main: '特別な時間にしたい', sub: '記念日やごほうびに' } ] },
    area: { text: '西多摩にお住まいですか？', hint: '西多摩にお住まいの方だけが買える「フリーエリアチケット」があります。', col1: true, opts: [
      { v: 'yes', main: 'はい、住んでいます', sub: '青梅市・福生市・羽村市・あきる野市・瑞穂町・日の出町・檜原村・奥多摩町' },
      { v: 'no', main: 'いいえ', sub: 'それ以外の地域' } ] }
  };

  // Result table (all 20 combinations).
  // Key: with|priority  or  with|price|area
  // seat = first choice, alt = second choice, altHint = one line on the second-choice card, why = reason shown for the first choice
  // To change a recommendation, edit only the matching line here (seat / alt must be one of: recliner, ss, s, a, free).
  var RULES = {
    'family|relax':      { seat: 'ss', alt: 'a', altHint: '人数分をそろえやすい椅子席。子ども料金（2,000円）があります', why: '4名掛けのテーブル席に、カフェチェアとカフェテーブルが付いています。飲食ブースの食事をテーブルに広げて、昼からゆっくり過ごせます。4名なら1人あたり8,750円の計算です。※テントはありません。' },
    'family|focus':      { seat: 'a', alt: 'ss', altHint: '4名でテーブルを囲みたいときに', why: '指定席なので場所取りの心配がなく、18時頃からの約1時間、5,000発の花火に集中できます。子ども料金（2,000円）があり、小さなお子さまの膝上観覧は無料です。' },
    'family|price|yes':  { seat: 'free', alt: 'a', altHint: '売り切れのときや、椅子でゆっくり座りたいときに', why: 'おとな2,000円・こども1,000円・2歳以下は無料と、いちばんお手頃です。エリア内の好きな場所で、人数分のレジャーシートや小さな折りたたみイスを使えます（立ち見はできません）。限定1,000名です。' },
    'family|price|no':   { seat: 'a', alt: 's', altHint: '大人2人なら、あと4,000円でテーブル・イス付きの2名掛け席に', why: '大人5,000円・子ども2,000円の椅子席で、西多摩以外にお住まいの方が選べる席の中ではいちばんお手頃です。指定席なので、場所取りの心配がありません。小さなお子さまの膝上観覧は無料です。' },
    'family|special':    { seat: 'ss', alt: 's', altHint: '大人2人で観覧するなら、2名掛けのテーブル席', why: '「家族で最高の思い出を」のテーブル席です。カフェチェアとカフェテーブルを家族みんなで囲んで、食事と花火を楽しめます。※テントはありません。' },
    'friends|relax':     { seat: 'ss', alt: 's', altHint: '2人ずつなら、2名掛けのテーブル席', why: '4名掛けのテーブル席に、カフェチェアとカフェテーブルが付いています。12時からのキッチンカーや、午後からのパフォーマンス、18時頃の花火まで、ゆっくり滞在できます。4名なら1人あたり8,750円の計算です。※テントはありません。' },
    'friends|focus':     { seat: 'a', alt: 'ss', altHint: '4名でテーブルを囲むなら', why: '大人1人5,000円の指定席で、人数分をそろえやすい席です。はじめての方に最も選ばれているスタンダードで、場所取りの心配なく花火に集中できます。' },
    'friends|price|yes': { seat: 'free', alt: 'a', altHint: '売り切れのときや、椅子に座りたいときに', why: 'おとな2,000円（13歳以上）で、いちばんお手頃です。エリア内の好きな場所で、人数分のレジャーシートや小さな折りたたみイスを使えます（立ち見はできません）。限定1,000名です。' },
    'friends|price|no':  { seat: 'a', alt: 's', altHint: '2人でテーブルがほしいなら、1テーブル14,000円（1人あたり7,000円の計算）', why: '大人1人5,000円の椅子席で、西多摩以外にお住まいの方が選べる席の中ではいちばんお手頃です。指定席なので、場所取りの心配がありません。' },
    'friends|special':   { seat: 'ss', alt: 's', altHint: '2人ずつなら、2名掛けのテーブル席', why: '4名掛けのテーブル席に、カフェチェアとカフェテーブルが付いています。音楽とシンクロした花火を、テーブルを囲んで楽しめます。※テントはありません。' },
    'couple|relax':      { seat: 'recliner', alt: 's', altHint: 'テーブル付きで食事も楽しむなら', why: 'ふたり並んで背もたれを倒し、夜空を見上げながら花火を観覧できる席です。1組2席・30,000円で、アソビューだけで販売しています。' },
    'couple|focus':      { seat: 's', alt: 'a', altHint: 'テーブルがなくてよければ、おふたりで10,000円の椅子席', why: '2名掛けのテーブル席で、テーブルとイスが付いています。指定席なので場所取りの心配がなく、18時頃からの約1時間、5,000発の花火に集中できます。' },
    'couple|price|yes':  { seat: 'free', alt: 'a', altHint: '売り切れのときや、椅子に座りたいときに（おふたりで10,000円）', why: 'おとな2,000円で、おふたりなら4,000円といちばんお手頃です。エリア内の好きな場所で、ふたり分のレジャーシートや小さな折りたたみイスを使えます（立ち見はできません）。限定1,000名です。' },
    'couple|price|no':   { seat: 'a', alt: 's', altHint: 'あと4,000円でテーブル・イス付きの2名掛け席に', why: '大人5,000円の椅子席で、おふたりで10,000円です。西多摩以外にお住まいの方が選べる席の中ではいちばんお手頃です。指定席なので、場所取りの心配がありません。' },
    'couple|special':    { seat: 'recliner', alt: 's', altHint: '「特別な人と観る花火」のテーブル席', why: 'ふたり並んでリクライニングシートに身をあずけ、夜空を見上げながら花火を観覧できる、記念日にもぴったりの席です。アソビューだけで販売しています。' },
    'solo|relax':        { seat: 'a', alt: 's', altHint: 'テーブルがほしい場合は、2名掛けのテーブルをひとりで', why: '1名から買える椅子席です。指定席なので場所取りの心配がなく、ゆっくり座って観覧できます。はじめての方に最も選ばれているスタンダードです。' },
    'solo|focus':        { seat: 'a', alt: 's', altHint: 'テーブル付きでゆっくりするなら', why: '大人1人5,000円の指定席です。場所取りの心配がなく、18時頃からの約1時間、5,000発の花火に集中できます。' },
    'solo|price|yes':    { seat: 'free', alt: 'a', altHint: '売り切れのときや、椅子に座りたいときに', why: 'おとな2,000円で、いちばんお手頃です。エリア内の好きな場所で、レジャーシートや小さな折りたたみイスを使えます（立ち見はできません）。限定1,000名です。' },
    'solo|price|no':     { seat: 'a', alt: 's', altHint: 'テーブル付きにするなら', why: '大人1人5,000円の椅子席で、西多摩以外にお住まいの方が選べる席の中ではいちばんお手頃です。指定席なので場所取りは不要です。' },
    'solo|special':      { seat: 's', alt: 'a', altHint: '気軽に楽しむなら、大人1人5,000円の椅子席', why: '2名掛けのテーブル席を、ひとりでゆったり使えます。テーブルとイス付きで、自分のペースで花火を楽しめます。' }
  };

  // Labels used to repeat the chosen answers on the result screen
  var LABELS = { family: '家族で', friends: '友人・グループで', couple: 'カップル・ご夫婦で', solo: 'おひとりで',
    relax: 'ゆったり過ごしたい', focus: '花火に集中して楽しみたい', price: '料金を抑えたい', special: '特別な時間にしたい',
    yes: '西多摩にお住まい', no: '西多摩以外' };

  var state = { with: null, priority: null, area: null, step: 'with', started: false, source: '', lastSent: '' };
  var lockUntil = 0; // clicks are ignored for a moment after each render (double-tap guard)

  function track(name, params) {
    try { if (typeof gtag === 'function') { gtag('event', name, params || {}); } } catch (e) {}
  }

  // Move focus without scrolling the page. Uses focus({preventScroll:true}) where supported,
  // otherwise restores the scroll position right after focusing.
  var canPreventScroll = false;
  try { document.createElement('div').focus({ get preventScroll() { canPreventScroll = true; return true; } }); } catch (e) {}
  function focusEl(el) {
    if (!el) { return; }
    if (canPreventScroll) { try { el.focus({ preventScroll: true }); } catch (e) {} return; }
    var x = window.pageXOffset, y = window.pageYOffset;
    try { el.focus(); } catch (e) {}
    try { window.scrollTo(x, y); } catch (e) {}
  }

  function setProgress(text, pct) {
    if (stepEl) { stepEl.textContent = text; }
    if (barEl) { barEl.style.width = pct + '%'; }
    if (statusEl) { statusEl.textContent = text; }
  }

  // The photo is created with createElement so that the theme's lazy-load rewrite never touches it.
  function makeImg(s) {
    var img = document.createElement('img');
    img.src = s.img;
    img.alt = s.alt;
    img.setAttribute('width', '1024');
    img.setAttribute('height', '768');
    img.setAttribute('loading', 'lazy');
    img.setAttribute('decoding', 'async');
    return img;
  }

  function renderQuestion(key, skipFocus) {
    var q = QUESTIONS[key];
    var html = '<p class="akg-quiz__q" id="akg-quiz-q" tabindex="-1">' + q.text + '</p>';
    if (q.hint) { html += '<p class="akg-quiz__hint">' + q.hint + '</p>'; }
    html += '<div class="akg-quiz__opts' + (q.col1 ? ' -col1' : '') + '" role="group" aria-labelledby="akg-quiz-q">';
    for (var i = 0; q.opts.length > i; i++) {
      var o = q.opts[i];
      html += '<button type="button" class="akg-quiz__opt" data-q="' + key + '" data-v="' + o.v + '">' +
        '<span class="akg-quiz__opt-main">' + o.main + '</span><span class="akg-quiz__opt-sub">' + o.sub + '</span></button>';
    }
    html += '</div>';
    if (key !== 'with') { html += '<button type="button" class="akg-quiz__back" data-act="back"><span aria-hidden="true">← </span>前の質問に戻る</button>'; }
    panel.innerHTML = html;
    lockUntil = Date.now() + 350;
    if (key === 'with') { setProgress('質問 1 / 2', 33); }
    else if (key === 'priority') { setProgress('質問 2 / 2', 66); }
    else { setProgress('あと1問だけ 3 / 3', 85); }
    if (noteEl) { noteEl.hidden = false; }
    state.step = key;
    state.source = '';
    if (!skipFocus) { focusEl(panel.querySelector('.akg-quiz__q')); }
  }

  function ruleKey() {
    return state.with + '|' + state.priority + (state.priority === 'price' ? '|' + state.area : '');
  }

  function renderResult(seatKey, altKey, why, altHint, source) {
    var s = SEATS[seatKey], alt = SEATS[altKey];
    var picked = LABELS[state.with] + '／' + LABELS[state.priority] + (state.priority === 'price' ? '／' + LABELS[state.area] : '');
    var html = '<div class="akg-quiz__result">';
    html += '<p class="akg-quiz__picked">' + picked + '</p>';
    html += '<p class="akg-quiz__label">' + (source === 'second' ? '第2候補' : 'あなたにおすすめの席') + '</p>';
    html += '<p class="akg-quiz__seat" id="akg-quiz-result-title" role="heading" aria-level="3" tabindex="-1"><span class="akg-quiz__sr">' + (source === 'second' ? '第2候補：' : 'おすすめの席：') + '</span>' + s.name + '</p>';
    html += '<p class="akg-quiz__catch">' + s.catchcopy + '</p>';
    html += '<div class="akg-quiz__body"><figure class="akg-quiz__fig" data-akg="fig"></figure>';
    html += '<div><p class="akg-quiz__price">' + s.price + '</p><ul class="akg-quiz__spec">';
    for (var i = 0; s.spec.length > i; i++) { html += '<li>' + s.spec[i] + '</li>'; }
    html += '</ul><p class="akg-quiz__why">' + why + '</p></div></div>';
    html += '<div class="swell-block-button red_ -size-l is-style-btn_normal"><a href="' + s.url + '" target="_blank" rel="noopener" class="swell-block-button__link" data-akg-cta="' + seatKey + '">' +
      '<span><strong>この席をアソビューで予約する</strong><span class="akg-quiz__sr">（新しいタブで開きます）</span></span></a></div>';
    html += '<p class="akg-quiz__cta-hint">' + s.hint + '</p>';
    if (s.only) {
      html += '<p class="akg-quiz__sub">この席はアソビューだけで販売しています。<a href="#site">販売サイトの一覧を見る</a></p>';
    } else {
      html += '<p class="akg-quiz__sub"><a href="#site">他の販売サイトで購入する</a>（チケットぴあ・KKday・楽天トラベル・JRE MALLでも販売しています）</p>';
    }
    html += '<div class="akg-quiz__alt"><p class="akg-quiz__alt-label">' + (source === 'second' ? '最初のおすすめ' : '第2候補') + '</p>';
    html += '<button type="button" class="akg-quiz__alt-btn" data-act="alt" data-seat="' + altKey + '" data-prev="' + seatKey + '">' +
      '<span class="akg-quiz__opt-main">' + alt.name + '　' + alt.price + '</span>' +
      '<span class="akg-quiz__opt-sub">' + altHint + '<span aria-hidden="true"> →</span> この席を見る</span></button></div>';
    html += '<p class="akg-quiz__note">※おすすめは目安です。席の詳しい説明は、このページ下の「観覧席」をご覧ください。</p>';
    html += '<p class="akg-quiz__foot"><button type="button" class="akg-quiz__again" data-act="reset">もう一度診断する</button></p>';
    html += '</div>';
    panel.innerHTML = html;
    lockUntil = Date.now() + 350;
    var fig = panel.querySelector('[data-akg="fig"]');
    if (fig) { fig.appendChild(makeImg(s)); }
    setProgress('診断結果', 100);
    if (statusEl) { statusEl.textContent = '診断結果。' + (source === 'second' ? '第2候補' : 'あなたにおすすめの席') + 'は' + s.name + 'です。'; }
    if (noteEl) { noteEl.hidden = true; }
    state.step = 'result';
    state.source = source;
    focusEl(panel.querySelector('#akg-quiz-result-title'));
    var sendKey = [seatKey, state.with, state.priority, state.area || 'na', source].join('|');
    if (sendKey !== state.lastSent) {
      state.lastSent = sendKey;
      track('seat_quiz_result', { seat_type: seatKey, quiz_with: state.with, quiz_priority: state.priority, quiz_area: state.area || 'na', quiz_source: source });
    }
  }

  function showPrimary() {
    var r = RULES[ruleKey()];
    if (!r) { renderQuestion('with'); return; }
    renderResult(r.seat, r.alt, r.why, r.altHint, 'primary');
  }

  function next() {
    if (!state.with) { renderQuestion('with'); return; }
    if (!state.priority) { renderQuestion('priority'); return; }
    if (state.priority === 'price' && !state.area) { renderQuestion('area'); return; }
    showPrimary();
  }

  function closestAttr(el, attr) {
    while (el && el !== root) {
      if (el.getAttribute && el.getAttribute(attr) !== null) { return el; }
      el = el.parentNode;
    }
    return null;
  }

  root.addEventListener('click', function (e) {
    var cta = closestAttr(e.target, 'data-akg-cta');
    if (cta) {
      track('seat_quiz_cta', { seat_type: cta.getAttribute('data-akg-cta'), quiz_source: state.source || 'primary', transport_type: 'beacon' });
      return; // plain link: let the browser open it
    }
    if (lockUntil > Date.now()) { return; } // double-tap guard: the new buttons sit where the old ones were
    var btn = closestAttr(e.target, 'data-q') || closestAttr(e.target, 'data-act');
    if (!btn) { return; }
    var q = btn.getAttribute('data-q');
    var act = btn.getAttribute('data-act');
    if (q) {
      state[q] = btn.getAttribute('data-v');
      if (q === 'with') { state.priority = null; state.area = null; }
      if (q === 'priority') { state.area = null; }
      if (!state.started) { state.started = true; track('seat_quiz_start', {}); }
      next();
    } else if (act === 'back') {
      if (state.step === 'area') { state.area = null; state.priority = null; renderQuestion('priority'); }
      else if (state.step === 'priority') { state.priority = null; state.with = null; renderQuestion('with'); }
    } else if (act === 'alt') {
      var seatKey = btn.getAttribute('data-seat');
      var r = RULES[ruleKey()];
      if (!r || !SEATS[seatKey]) { return; }
      if (seatKey === r.seat) { showPrimary(); }
      else { renderResult(seatKey, r.seat, SEATS[seatKey].why, '最初におすすめした席', 'second'); }
    } else if (act === 'reset') {
      state.with = null; state.priority = null; state.area = null; state.lastSent = '';
      track('seat_quiz_restart', {});
      renderQuestion('with');
    }
  });

  // Self-check: run AKG_QUIZ.check() in the browser console after editing RULES. Expect {rules:20, missing:[], bad:[]}.
  window.AKG_QUIZ = { seats: SEATS, rules: RULES, check: function () {
    var bad = [], missing = [], keys = Object.keys(RULES), i, j, k, key;
    var W = ['family', 'friends', 'couple', 'solo'], P = ['relax', 'focus', 'price', 'special'], A = ['yes', 'no'];
    for (i = 0; W.length > i; i++) {
      for (j = 0; P.length > j; j++) {
        if (P[j] === 'price') {
          for (k = 0; A.length > k; k++) { key = W[i] + '|price|' + A[k]; if (!RULES[key]) { missing.push(key); } }
        } else {
          key = W[i] + '|' + P[j]; if (!RULES[key]) { missing.push(key); }
        }
      }
    }
    for (i = 0; keys.length > i; i++) {
      var r = RULES[keys[i]];
      if (!SEATS[r.seat] || !SEATS[r.alt] || r.seat === r.alt || !r.why || !r.altHint) { bad.push(keys[i]); }
    }
    return { rules: keys.length, missing: missing, bad: bad };
  } };

  renderQuestion('with', true);
})();
