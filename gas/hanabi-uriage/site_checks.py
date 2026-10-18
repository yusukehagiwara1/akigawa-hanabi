# -*- coding: utf-8 -*-
"""
販売サイトの公開画面で、席種ごとに「いま買えるか」を確かめた結果をまとめる。

- アソビュー・KKday・JRE MALL・チケットぴあ … 毎朝の定期実行で Claude がブラウザで画面を開き、
  browser/*.js で読んだ結果を observed.json に保存する（待合室や bot 対策はすり抜けない。
  ふつうに画面を開くだけ）。from_observed() がそれを (席種, 販売サイト) に読み替える。
- 楽天トラベル … 画面の「予約へ進む」と同じ在庫確認を呼ぶ（check_rakuten()。ログイン不要・予約はしない）。

状態は 'available'（買える）/ 'few'（残りわずか）/ 'soldout'（売り切れ）。
読めなかったもの・自信がないものは入れない（＝シートの記号をそのまま使う）。
売り切れでないのに「売り切れ」と出すと販売を止めてしまうので、迷ったら入れない。
"""
import datetime, json, re, time, unicodedata, urllib.request

JST = datetime.timezone(datetime.timedelta(hours=9))
SITES = ('アソビュー', 'チケットぴあ', '楽天トラベル', 'KKday', 'JRE MALL')
RANK = {'available': 0, 'few': 1, 'soldout': 2}

SS, S, A, FREE = 'SS席', 'S席', 'A席（大人＋子ども）', 'フリーエリア'
P1, P2 = '駐車場①（会場隣接）', '駐車場②（プール側）'

# ---- アソビュー: 商品ID → {画面の席種名: ページの席種}。'*' は席種が1つだけの商品
ASOVIEW = {
    '15a2d40e-de69-49cb-aa22-3450dd5e17b3': {'SS席': SS, 'S席': S, 'A席': A},  # SS・S・A が1つの商品
    '4e015166-974c-4717-aa29-7ea7a902a8c8': {'*': S},    # ＜S席追加販売＞
    'eeb73892-7a4f-4cc6-aeb9-20d7980d5298': {'*': P1},
    'bcd564e0-361e-4a67-bdec-0a608cc54213': {'*': P2},
    '6dbcf060-4a33-4e3c-9348-551a867822d1': {'*': FREE},  # 別チャネル（西多摩在住者限定フリーエリア）
}
ASOVIEW_URL = {
    pid: 'https://machizukuricon.my.urakata.app/channels/%s/products/%s' % (
        'd58e8525-0f46-4109-9740-1c1b928b5aa0' if pid.startswith('6dbcf060') else 'debdd785-6f29-4fa5-827f-b8eb02f3a583', pid)
    for pid in ASOVIEW
}
# ---- KKday: プランID → 席種
KKDAY = {'2047519': [SS], '2047527': [S], '2047520': [A], '2047543': [P1], '2047562': [P2]}
# ---- JRE MALL: プランID → 席種（3737 は駐車場2種を1つのプランで売っている）
JRE = {'3734': [SS], '3735': [S], '3736': [A], '3737': [P1, P2]}
# ---- チケットぴあ: 券種名（NFKC で半角にそろえたもの）の席名・価格 → 席種、表示 → 状態
PIA_SEAT = [('SS席', '35,000円', SS), ('S席', '14,000円', S), ('A席(おとな)', '5,000円', A),
            ('駐車場(観覧会場隣接)', '1,500円', P1), ('駐車場(サマーランドプール側)', '1,000円', P2)]
PIA_STATE = {'発売中': 'available', '残りわずか': 'few', '予定枚数終了': 'soldout'}
PIA_IGNORE = ('ソファー席',)   # ページに載せていない券種


def _nfkc(s):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', s or '')).strip()


def _put(out, seat, site, st):
    if st not in RANK:
        return
    cur = out.get((seat, site))
    if cur is None or RANK[st] > RANK[cur]:
        out[(seat, site)] = st


def _today_read(r, today, name, notes):
    """その日（日本時間）に読んだ結果だけ使う。前日以前の observed.json を使ってしまったときの備え"""
    if not r:
        notes.append('%s: 結果が無い' % name)
        return None
    if r.get('error'):
        notes.append('%s: 読めなかった（%s）' % (name, r['error']))
        return None
    try:
        at = datetime.datetime.fromisoformat(str(r.get('read_at')).replace('Z', '+00:00')).astimezone(JST).date()
    except ValueError:
        at = None
    if at != today:
        notes.append('%s: 今日読んだ結果ではない（read_at=%s）' % (name, r.get('read_at')))
        return None
    return r


def from_observed(raw, today):
    """observed.json（ブラウザで読んだ結果）→ ({(席種, サイト): 状態}, 確認できたサイトの集合, メモ)
    today: 日本時間の今日。read_at がこの日でない結果は使わない。"""
    out, ok, notes = {}, set(), []

    # ---- アソビュー: 席種ごとに、その席種を売っている全商品の状態がそろったときだけ使う
    aso = raw.get('asoview') or {}
    by_seat, good = {}, 0
    for pid, seats in ASOVIEW.items():
        r = _today_read(aso.get(pid), today, 'アソビュー %s' % pid[:8], notes)
        got = (r or {}).get('seats') or {}
        vals = {}
        for name, seat in seats.items():
            if not r:
                st = None
            elif name == '*':
                st = list(got.values())[0] if len(got) == 1 else (r.get('date') if not got else None)
            else:
                st = got.get(name)
            vals[seat] = st if st in RANK else None
            by_seat.setdefault(seat, []).append(vals[seat])
        extra = sorted(set(got) - set(seats)) if '*' not in seats else []
        if extra:
            notes.append('アソビュー %s: 想定外の席種 %s' % (pid[:8], extra))
        if r and all(v is not None for v in vals.values()):
            good += 1
        elif r:
            notes.append('アソビュー %s: 席種の状態がそろわない %s' % (pid[:8], got or r.get('date')))
    for seat, sts in by_seat.items():
        if all(s is not None for s in sts):
            # 同じ席種を2つの商品で売っている（S席）ときは、どれかで買えれば買える（良い方をとる）
            _put(out, seat, 'アソビュー', min(sts, key=RANK.get))
    if good == len(ASOVIEW):
        ok.add('アソビュー')

    # ---- KKday
    r = _today_read(raw.get('kkday'), today, 'KKday', notes)
    kk = (r or {}).get('options') or {}
    for oid, seats in KKDAY.items():
        for seat in seats:
            _put(out, seat, 'KKday', kk.get(oid))
    if r and all(kk.get(o) in RANK for o in KKDAY):
        ok.add('KKday')
    elif r:
        notes.append('KKday: 状態がそろわない %s' % kk)

    # ---- JRE MALL
    plans = {}
    for page in ('jre09', 'jre10'):
        r = _today_read(raw.get(page), today, 'JRE %s' % page, notes)
        plans.update((r or {}).get('plans') or {})
    for pid, seats in JRE.items():
        for seat in seats:
            st = plans.get(pid)
            # 3737 は駐車場2種まとめてのプランなので、「残りわずか」はどちらのことか分からない → 売り切れだけ使う
            if pid == '3737' and st == 'few':
                st = None
            _put(out, seat, 'JRE MALL', st)
    if all(plans.get(p) in RANK for p in JRE):
        ok.add('JRE MALL')
    elif plans:
        notes.append('JRE MALL: 状態がそろわない %s' % plans)

    # ---- チケットぴあ: 席種ごとに、期待する券種（席名＋価格）がちょうど1行だけあるときに使う
    r = _today_read(raw.get('pia'), today, 'チケットぴあ', notes)
    pia = {_nfkc(k): v for k, v in ((r or {}).get('seats') or {}).items()}
    got = set()
    for head, price, seat in PIA_SEAT:
        lines = [(n, v) for n, v in pia.items() if n.startswith(head) and not any(
            n.startswith(h2) for h2, _, _ in PIA_SEAT if h2 != head and h2.startswith(head))]
        exact = [(n, v) for n, v in lines if n.startswith(head + ' ' + price)]
        if len(lines) == 1 and len(exact) == 1 and PIA_STATE.get(exact[0][1]):
            _put(out, seat, 'チケットぴあ', PIA_STATE[exact[0][1]])
            got.add(seat)
        elif r:
            notes.append('チケットぴあ %s: 券種が想定と違う %s' % (seat, lines))
    if len(got) == len(PIA_SEAT):
        ok.add('チケットぴあ')
    unknown = [n for n in pia if not any(n.startswith(h) for h, _, _ in PIA_SEAT) and not n.startswith(PIA_IGNORE)]
    if unknown:
        notes.append('チケットぴあ: 想定外の券種 %s' % unknown)
    return out, ok, notes


# ---- 楽天トラベル（画面の「予約へ進む」が最初に呼ぶ在庫確認と同じもの。予約・仮押さえはしない）
RAKUTEN_API = 'https://experiences.travel.rakuten.co.jp/api'
RAKUTEN_Q = 'language=ja&locale=ja_jp&displayCurrency=JPY'
RAKUTEN = {63097: SS, 63098: S, 63099: A, 63100: P1, 63101: P2}   # optionId → 席種
RAKUTEN_TITLE = {63097: 'SS席', 63098: 'S席', 63099: 'A席', 63100: '駐車場', 63101: '駐車場'}


def _rk(url, body=None):
    h = {'User-Agent': 'Mozilla/5.0 (akigawa-hanabi stock check; once a day)', 'Accept': 'application/json',
         'Referer': 'https://experiences.travel.rakuten.co.jp/experiences/62751',
         'Origin': 'https://experiences.travel.rakuten.co.jp'}
    data = None
    if body is not None:
        data = json.dumps(body).encode('utf-8')
        h['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=data, headers=h, method='POST' if body is not None else 'GET')
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))


def check_rakuten(date='2026-11-14'):
    opts = _rk('%s/experiences/options?experienceId=62751&page=0&startDate=%s&currency=JPY&%s'
               % (RAKUTEN_API, date, RAKUTEN_Q)).get('options') or []
    boxes = {}
    for o in opts:
        oid = int(o.get('optionId') or 0)   # API は文字列で返す
        if oid in RAKUTEN and (o.get('title') or '').strip().startswith(RAKUTEN_TITLE[oid]):
            tb = {p.get('ticketBoxId') for p in (o.get('prices') or []) if p.get('ticketBoxId')}
            if len(tb) == 1:
                boxes[oid] = tb.pop()
    if len(boxes) != len(RAKUTEN):
        raise ValueError('楽天の席種が想定と違う: %s' % sorted(boxes))

    def can(tb, n):
        time.sleep(2)
        v = _rk('%s/ticketbox/check-availability?%s' % (RAKUTEN_API, RAKUTEN_Q),
                {'schedule': date, 'options': [{'count': n, 'ticketBoxId': tb}], 'timeslot': ''}).get('canProceed')
        if not isinstance(v, bool):
            raise ValueError('楽天の在庫確認の応答が想定と違う')
        return v

    out = {}
    for oid, tb in boxes.items():
        if not can(tb, 1):
            out[RAKUTEN[oid]] = 'soldout'
        else:
            out[RAKUTEN[oid]] = 'available' if can(tb, 6) else 'few'   # 残り5以下は△（シートと同じ基準）
    # 全部「売り切れ」は API の仕様変更・ID違いの可能性が高い（存在しないIDでも false が返る）
    if out and all(v == 'soldout' for v in out.values()):
        raise ValueError('楽天が全席種売り切れと返した（仕様変更の疑い）')
    return out


def run_auto():
    """スクリプトだけで確かめられるもの（楽天）→ ({(席種, サイト): 状態}, 確認できたサイトの集合, メモ)"""
    out, ok, notes = {}, set(), []
    try:
        for seat, st in check_rakuten().items():
            _put(out, seat, '楽天トラベル', st)
        ok.add('楽天トラベル')
    except Exception as e:
        notes.append('楽天トラベル: 確認できなかった %s: %s' % (type(e).__name__, e))
    return out, ok, notes


def merge(*results):
    out, ok, notes = {}, set(), []
    for o, k, n in results:
        for (seat, site), st in o.items():
            _put(out, seat, site, st)
        ok |= k
        notes += n
    return out, ok, notes
