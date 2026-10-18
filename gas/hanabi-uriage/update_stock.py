# -*- coding: utf-8 -*-
"""
花火売上集計の「在庫」シート（CSV）から、チケットページの在庫表示を更新する。

  python update_stock.py <zaiko.csv> <ticket-page-content.html> [--write] [--date 2026-10-18]

- 席ごとの表示（比較カード・席の詳細）: ① 状況 〇/△/✕ → 空席あり/残りわずか/完売
- 販売サイトごとの記号（購入リンク）: ② 記号 〇/△/✕。配分0の「―」は ✕ として扱う
- 「○月○日時点」の日付（akg-asof）: --date を付けないときは今日の日付
--write を付けないときは変更点を表示するだけ（ファイルは書き換えない）。

毎日の自動更新（build_stock_json.py）もこのファイルの transform() を使う。
"""
import csv, datetime, io, re, sys

SEAT_ANCHOR = {
    'seat-rec': 'リクライニング席（ペア）',
    'seat-ss': 'SS席',
    'seat-s': 'S席',
    'seat-a': 'A席（大人＋子ども）',
    'seat-free': 'フリーエリア',
}
CARD_CLASS = {'rec': 'リクライニング席（ペア）', 'ss': 'SS席', 's': 'S席', 'a': 'A席（大人＋子ども）', 'free': 'フリーエリア'}
PARKING_TITLE = {'観覧会場隣接': '駐車場①（会場隣接）', 'プール側': '駐車場②（プール側）'}
# 購入リンクの枠（div.akg-buylist）に付ける data-stock。stock.js がこれで差し替え先を探す
STOCK_ID = {
    'リクライニング席（ペア）': 'rec', 'SS席': 'ss', 'S席': 's', 'A席（大人＋子ども）': 'a', 'フリーエリア': 'free',
    '駐車場①（会場隣接）': 'park1', '駐車場②（プール側）': 'park2',
}

# ✕ の行にはリンクが残らないので、在庫が戻ったときのためのURL（ページにある全行ぶん）
PIA = 'https://t.pia.jp/pia/ticketInformation.do?eventCd=2625008&amp;rlsCd=001'
RAKUTEN = 'https://experiences.travel.rakuten.co.jp/experiences/62751'
KK = 'https://www.kkday.com/ja/product/527261?cid=22567&amp;ud1=officialsite#optionItem'
ASO = 'https://machizukuricon.my.urakata.app/channels/debdd785-6f29-4fa5-827f-b8eb02f3a583/products/'
ASO_MAIN = ASO + '15a2d40e-de69-49cb-aa22-3450dd5e17b3'   # SS・S・A席がまとめて入っている商品
JRE09 = 'https://event.jreast.co.jp/activity/detail/a180/a180-09'
JRE10 = 'https://event.jreast.co.jp/activity/detail/a180/a180-10'
URLS = {
    ('リクライニング席（ペア）', 'アソビュー'): ASO + 'e42dce79-988e-4b5d-bc20-099dbaf02d1d',
    ('SS席', 'アソビュー'): ASO_MAIN,
    ('SS席', 'チケットぴあ'): PIA,
    ('SS席', 'KKday'): KK + '2047519',
    ('SS席', '楽天トラベル'): RAKUTEN,
    ('SS席', 'JRE MALL'): JRE09 + '#plan-3734',
    ('S席', 'アソビュー'): ASO_MAIN,
    ('S席', 'チケットぴあ'): PIA,
    ('S席', 'KKday'): KK + '2047527',
    ('S席', '楽天トラベル'): RAKUTEN,
    ('S席', 'JRE MALL'): JRE09 + '#plan-3735',
    ('A席（大人＋子ども）', 'アソビュー'): ASO_MAIN,
    ('A席（大人＋子ども）', 'チケットぴあ'): PIA,
    ('A席（大人＋子ども）', 'KKday'): KK + '2047520',
    ('A席（大人＋子ども）', '楽天トラベル'): RAKUTEN,
    ('A席（大人＋子ども）', 'JRE MALL'): JRE09 + '#plan-3736',
    ('フリーエリア', 'アソビュー'): ('https://machizukuricon.my.urakata.app/channels/d58e8525-0f46-4109-9740-1c1b928b5aa0'
                                  '/products/6dbcf060-4a33-4e3c-9348-551a867822d1'),
    ('駐車場①（会場隣接）', 'アソビュー'): ASO + 'eeb73892-7a4f-4cc6-aeb9-20d7980d5298',
    ('駐車場①（会場隣接）', 'チケットぴあ'): PIA,
    ('駐車場①（会場隣接）', 'KKday'): KK + '2047543',
    ('駐車場①（会場隣接）', '楽天トラベル'): RAKUTEN,
    ('駐車場①（会場隣接）', 'JRE MALL'): JRE10,
    ('駐車場②（プール側）', 'アソビュー'): ASO + 'bcd564e0-361e-4a67-bdec-0a608cc54213',
    ('駐車場②（プール側）', 'チケットぴあ'): PIA,
    ('駐車場②（プール側）', 'KKday'): KK + '2047562',
    ('駐車場②（プール側）', '楽天トラベル'): RAKUTEN,
    ('駐車場②（プール側）', 'JRE MALL'): JRE10,
}

STOCK = {'〇': ('ok', '空席あり'), '△': ('few', '残りわずか'), '✕': ('none', '完売')}
MARK_RANK = {'〇': 0, '△': 1, '✕': 2}
# シートの記号の表記ゆれ。これ以外（#VALUE! など）が来たら止める
MARK_NORM = {'〇': '〇', '○': '〇', '◯': '〇', '△': '△', '✕': '✕', '×': '✕', '―': '―', '': ''}
SHEET_SEATS = ('リクライニング席（ペア）', 'SS席', 'S席', 'A席（大人＋子ども）', 'フリーエリア',
               '駐車場①（会場隣接）', '駐車場②（プール側）')
SHEET_SITES = ('アソビュー', 'チケットぴあ', '楽天トラベル', 'KKday', 'JRE MALL', 'さとふる')

# 記号を手で決めている枠（シートの判定より優先）
FORCE_MARK = {
    ('SS席', 'チケットぴあ'): '△',  # 10/7 ぴあで販売再開。シートは割当15・残り15で〇になるが△で表示（萩原さん判断）
}

# 割当はあるが、販売サイト側でまだ売り出していない枠（売り出したら外す）
NOT_ON_SALE = {
    ('S席', 'チケットぴあ'),   # 10/5按分で5席追加、ぴあは「予定枚数終了」のまま（10/7確認）
}

# 販売サイトの画面で売り切れを確認した枠（集計より先に売り切れることがある）
SOLD_OUT = {
    ('S席', 'アソビュー'),  # 10/18 「予定枚数終了」を確認（シートは10/16集計で残り1）
    ('S席', 'JRE MALL'),    # 10/18 カレンダーの✕を確認（シートは10/16集計で残り2）
    ('SS席', '楽天トラベル'),  # 10/18 楽天の在庫確認で1枚も確保できないことを確認（シートは10/16集計で残り1）
}


def row_html(site, mark, url):
    name = '<span class="akg-buylist__name">%sで購入する</span>' % site
    if mark == '✕':
        return ('<li class="akg-buylist__item--out"><span class="akg-buylist__row">%s'
                '<span class="akg-buylist__mark akg-buylist__mark--out" aria-hidden="true">✕</span>'
                '<span class="akg-buylist__sr">この販売サイトでは売り切れです</span></span></li>') % name
    if mark == '△':
        m = ('<span class="akg-buylist__mark akg-buylist__mark--few" aria-hidden="true">△</span>'
             '<span class="akg-buylist__sr">残りわずか・新しいタブで開きます</span>')
    else:
        m = ('<span class="akg-buylist__mark" aria-hidden="true">〇</span>'
             '<span class="akg-buylist__sr">在庫あり・新しいタブで開きます</span>')
    return '<li><a href="%s" target="_blank" rel="noopener">%s%s</a></li>' % (url, name, m)


def parse_sheet(text):
    """在庫シートを読む。席種・サイトがそろっていない、記号が読めないときは ValueError（表示を変えずに止める）"""
    rows = list(csv.reader(io.StringIO(text)))
    seat, site = {}, {}
    # ① 席種ごと: 「席種,在庫,販売,残り,残率,状況」の下
    i = next(k for k, r in enumerate(rows) if r[:6] == ['席種', '在庫', '販売', '残り', '残率', '状況'])
    for r in rows[i + 1:]:
        if not r or not r[0]:
            break
        seat[r[0]] = r[5].strip()
    # ② 販売サイト別: 見出しの下から、注記（※）の行か最後まで。空行は読み飛ばす
    j = next(k for k, r in enumerate(rows) if r[:7] == ['席種', '販売サイト', '配分', '販売', '残り', '残率', '記号'])
    for r in rows[j + 1:]:
        if r and r[0].startswith('※'):
            break
        if not r or not any(c.strip() for c in r):
            continue
        site[(r[0], r[1])] = r[6].strip() if len(r) > 6 else ''
    want = {(a, b) for a in SHEET_SEATS for b in SHEET_SITES}
    if set(seat) != set(SHEET_SEATS) or set(site) != want:
        raise ValueError('在庫シートの席種・販売サイトが想定と違う: ①に無い %s ②に無い %s ②に余分 %s' % (
            sorted(set(SHEET_SEATS) - set(seat)), sorted(want - set(site)), sorted(set(site) - want)))
    return seat, site


def load_sheet(path):
    return parse_sheet(io.open(path, encoding='utf-8').read())


def asof_label(date):
    return '%d月%d日' % (date.month, date.day)


def combine(mark, public):
    """シートの記号に、販売サイトの画面で見た状態を重ねる（悪い方をとる。在庫を増やす方向には変えない）"""
    if public == 'soldout':
        return '✕'
    if public == 'few' and mark == '〇':
        return '△'
    return mark


def transform(s, seat, site, date, public=None):
    """ページHTMLの在庫表示を書き換える。

    public: 関数 (席種, 販売サイト名, URL) -> 'available' | 'few' | 'soldout' | None。
            販売サイトの画面で確認した状態。None は「確認していない／取れなかった」。
    戻り値: (新しいHTML, 変更点のリスト, 行ごとの判定 [(席種, サイト, シート, 画面, 表示)])
    """
    changes, rows = [], []
    # 席全体の状況は、ページに出す販売サイトの記号から決める
    # （〇が1つでもあれば空席あり／〇がなく△があれば残りわずか／全部✕なら完売）。
    # 未発売の枠を数えないので、実際に買える席数に沿った表示になる。
    status = {}

    # 席の詳細・駐車場ブロック
    parts = re.split(r'(?=<!-- wp:loos/step-item )', s)
    for n, blk in enumerate(parts):
        a = re.search(r'"anchor":"(seat-[a-z]+)"', blk)
        key = SEAT_ANCHOR.get(a.group(1)) if a else None
        if not key and '"stepLabel":"PARKING"' in blk:
            t = re.search(r'swell-block-step__title[^>]*>([^<]+)<', blk)
            key = next((v for k, v in PARKING_TITLE.items() if t and k in t.group(1)), None)
        if not key:
            continue
        blk = re.sub(r'<div class="akg-buylist"(?: data-stock="[^"]*")?>',
                     '<div class="akg-buylist" data-stock="%s">' % STOCK_ID[key], blk)
        marks = []

        def li(m):
            body = m.group(0)
            nm = re.search(r'akg-buylist__name">(.+?)で購入する<', body)
            if not nm:
                return body
            st = nm.group(1)
            if (key, st) not in site:
                raise ValueError('在庫シートに行が無い: %s / %s' % (key, st))
            sheet_mark = site[(key, st)]
            if (key, st) in NOT_ON_SALE or (key, st) in SOLD_OUT:
                mark = '✕'
            elif sheet_mark not in MARK_NORM:
                raise ValueError('在庫シートの記号が読めない: %s / %s = %r' % (key, st, sheet_mark))
            else:
                mark = MARK_NORM[sheet_mark]
                if mark in ('', '―'):
                    mark = '✕'
            # 手で決めた記号は、表示を悪い方へ寄せるときだけ使う（シートが✕なら✕のまま）
            force = FORCE_MARK.get((key, st))
            if force and MARK_RANK[force] > MARK_RANK[mark]:
                mark = force
            href = re.search(r'href="([^"]+)"', body)
            url = href.group(1) if href else URLS.get((key, st))
            if not url:
                raise ValueError('購入リンクのURLが分からない: %s / %s（URLS に足す）' % (key, st))
            seen = public(key, st, url) if public else None
            mark = combine(mark, seen)
            rows.append((key, st, sheet_mark or '―', seen or '', mark))
            marks.append(mark)
            new = row_html(st, mark, url)
            if new != body:
                cur = re.search(r'aria-hidden="true">(.)<', body)
                changes.append('%s / %s: %s → %s%s' % (key, st, cur.group(1) if cur else '?', mark,
                                                      '（販売サイトの画面: %s）' % seen if seen else ''))
            return new
        blk = re.sub(r'<li(?: class="akg-buylist__item--out")?>.*?</li>', li, blk, flags=re.S)

        if key in seat and marks:
            status[key] = '〇' if '〇' in marks else ('△' if '△' in marks else '✕')
            cls, label = STOCK[status[key]]
            new = '<p class="akg-buylist__stock akg-buylist__stock--%s"><i></i>%s</p>' % (cls, label)
            old = re.search(r'<p class="akg-buylist__stock akg-buylist__stock--\w+"><i></i>[^<]+</p>', blk)
            if old and old.group(0) != new:
                changes.append('詳細 %s: %s → %s' % (key, re.sub('<[^>]+>', '', old.group(0)), label))
                blk = blk.replace(old.group(0), new)
        parts[n] = blk
    s = ''.join(parts)

    # 比較カード（席の詳細と同じ判定）
    def card(m):
        key = CARD_CLASS[m.group(1)]
        cls, label = STOCK[status.get(key, seat[key])]
        new = '<span class="akg-sf__stock akg-sf__stock--%s"><i></i>%s</span>' % (cls, label)
        if m.group(2) != new:
            changes.append('カード %s: %s → %s' % (key, re.sub('<[^>]+>', '', m.group(2)), label))
        return m.group(0).replace(m.group(2), new)
    s = re.sub(r'<li class="akg-sf--(rec|ss|s|a|free)">.*?(<span class="akg-sf__stock akg-sf__stock--\w+"><i></i>[^<]+</span>)',
               card, s, flags=re.S)

    # 「○月○日時点」の日付（data-date は stock.js が新旧を比べるのに使う）
    span = '<span class="akg-asof" data-date="%s">%s</span>' % (date.isoformat(), asof_label(date))
    olds = set(re.findall(r'<span class="akg-asof"[^>]*>[^<]*</span>', s))
    if olds != {span}:
        changes.append('時点の日付: %s → %s' % ('・'.join(sorted(re.sub('<[^>]+>', '', o) for o in olds)) or 'なし',
                                              asof_label(date)))
        s = re.sub(r'<span class="akg-asof"[^>]*>[^<]*</span>', span, s)
    return s, changes, rows


def main():
    csv_path, html_path = sys.argv[1], sys.argv[2]
    write = '--write' in sys.argv
    date = (datetime.date.fromisoformat(sys.argv[sys.argv.index('--date') + 1]) if '--date' in sys.argv
            else datetime.date.today())
    seat, site = load_sheet(csv_path)
    orig = io.open(html_path, encoding='utf-8').read()
    s, changes, _ = transform(orig, seat, site, date)
    print('\n'.join(changes) if changes else '変更なし')
    if write and s != orig:
        io.open(html_path, 'w', encoding='utf-8', newline='').write(s)
        print('書き込みました')


if __name__ == '__main__':
    main()
