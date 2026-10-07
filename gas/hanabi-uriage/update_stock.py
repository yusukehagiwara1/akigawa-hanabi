# -*- coding: utf-8 -*-
"""
花火売上集計の「在庫」シート（CSV）から、チケットページの在庫表示を更新する。

  python update_stock.py <zaiko.csv> <ticket-page-content.html> [--write]

- 席ごとの表示（比較カード・席の詳細）: ① 状況 〇/△/✕ → 空席あり/残りわずか/完売
- 販売サイトごとの記号（購入リンク）: ② 記号 〇/△/✕。配分0の「―」は ✕ として扱う
--write を付けないときは変更点を表示するだけ（ファイルは書き換えない）。
"""
import csv, io, re, sys

SEAT_ANCHOR = {
    'seat-rec': 'リクライニング席（ペア）',
    'seat-ss': 'SS席',
    'seat-s': 'S席',
    'seat-a': 'A席（大人＋子ども）',
    'seat-free': 'フリーエリア',
}
CARD_CLASS = {'rec': 'リクライニング席（ペア）', 'ss': 'SS席', 's': 'S席', 'a': 'A席（大人＋子ども）', 'free': 'フリーエリア'}
PARKING_TITLE = {'観覧会場隣接': '駐車場①（会場隣接）', 'プール側': '駐車場②（プール側）'}

# ✕ の行にはリンクが残らないので、在庫が戻ったときのためのURL
PIA = 'https://t.pia.jp/pia/ticketInformation.do?eventCd=2625008&amp;rlsCd=001'
RAKUTEN = 'https://experiences.travel.rakuten.co.jp/experiences/62751'
KK = 'https://www.kkday.com/ja/product/527261?cid=22567&amp;ud1=officialsite#optionItem'
ASO = 'https://machizukuricon.my.urakata.app/channels/debdd785-6f29-4fa5-827f-b8eb02f3a583/products/'
URLS = {
    ('SS席', 'アソビュー'): ASO + '15a2d40e-de69-49cb-aa22-3450dd5e17b3',
    ('SS席', 'チケットぴあ'): PIA,
    ('SS席', 'KKday'): KK + '2047519',
    ('SS席', '楽天トラベル'): RAKUTEN,
    ('SS席', 'JRE MALL'): 'https://event.jreast.co.jp/activity/detail/a180/a180-09#plan-3734',
    ('S席', 'アソビュー'): ASO + '4e015166-974c-4717-aa29-7ea7a902a8c8',
    ('S席', 'チケットぴあ'): PIA,
    ('S席', 'KKday'): KK + '2047527',
    ('S席', '楽天トラベル'): RAKUTEN,
    ('S席', 'JRE MALL'): 'https://event.jreast.co.jp/activity/detail/a180/a180-09#plan-3735',
}

STOCK = {'〇': ('ok', '空席あり'), '△': ('few', '残りわずか'), '✕': ('none', '完売')}

# 記号を手で決めている枠（シートの判定より優先）
FORCE_MARK = {
    ('SS席', 'チケットぴあ'): '△',  # 10/7 ぴあで販売再開。シートは割当15・残り15で〇になるが△で表示（萩原さん判断）
}

# 割当はあるが、販売サイト側でまだ売り出していない枠（売り出したら外す）
NOT_ON_SALE = {
    ('S席', 'チケットぴあ'),   # 10/5按分で5席追加、ぴあは「予定枚数終了」のまま（10/7確認）
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


def load_sheet(path):
    rows = list(csv.reader(io.open(path, encoding='utf-8')))
    seat, site = {}, {}
    # ① 席種ごと: 「席種,在庫,販売,残り,残率,状況」の下
    i = next(k for k, r in enumerate(rows) if r[:6] == ['席種', '在庫', '販売', '残り', '残率', '状況'])
    for r in rows[i + 1:]:
        if not r or not r[0]:
            break
        seat[r[0]] = r[5].strip()
    # ② 販売サイト別
    j = next(k for k, r in enumerate(rows) if r[:7] == ['席種', '販売サイト', '配分', '販売', '残り', '残率', '記号'])
    for r in rows[j + 1:]:
        if not r or not r[0]:
            break
        site[(r[0], r[1])] = r[6].strip()
    return seat, site


def main():
    csv_path, html_path = sys.argv[1], sys.argv[2]
    write = '--write' in sys.argv
    seat, site = load_sheet(csv_path)
    s = io.open(html_path, encoding='utf-8').read()
    changes = []
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
        marks = []

        def li(m):
            body = m.group(0)
            nm = re.search(r'akg-buylist__name">(.+?)で購入する<', body)
            if not nm:
                return body
            st = nm.group(1)
            mark = site.get((key, st), '')
            if mark in ('', '―') or (key, st) in NOT_ON_SALE:
                mark = '✕'
            mark = FORCE_MARK.get((key, st), mark)
            href = re.search(r'href="([^"]+)"', body)
            url = href.group(1) if href else URLS.get((key, st))
            if mark != '✕' and not url:
                changes.append('!! URL不明 %s / %s（✕のまま）' % (key, st))
                marks.append('✕')
                return body
            marks.append(mark)
            new = row_html(st, mark, url)
            if new != body:
                cur = re.search(r'aria-hidden="true">(.)<', body)
                changes.append('%s / %s: %s → %s' % (key, st, cur.group(1) if cur else '?', mark))
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

    print('\n'.join(changes) if changes else '変更なし')
    if write and changes:
        io.open(html_path, 'w', encoding='utf-8', newline='').write(s)
        print('書き込みました')


if __name__ == '__main__':
    main()
