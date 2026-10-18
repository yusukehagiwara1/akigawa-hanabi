# -*- coding: utf-8 -*-
"""
チケットページの在庫表示を作り直す（毎朝の定期実行から呼ぶ。手で実行してもよい）。

  python gas/hanabi-uriage/build_stock_json.py --observed observed.json [--csv zaiko.csv] [--no-auto]

1. 「在庫」シートを CSV で読む（ログイン不要の export URL）
2. 販売サイトの画面で確かめた状態を重ねる（悪い方をとる。在庫を増やす方向には変えない）
   - observed.json … ブラウザで読んだアソビュー・KKday・JRE MALL・チケットぴあ（site_checks.from_observed）
   - 楽天トラベル … スクリプトで確認（site_checks.run_auto。--no-auto で省略）
3. wp-snippets/ticket-page-content.html を書き換え、購入リンク・カードの HTML を wp-snippets/stock.json に出す
   → push すると Cloudflare Pages に載り、チケットページの stock.js が表示を差し替える（WordPress の更新は不要）

「○月○日時点」の日付は、5サイトすべてを確かめられた日だけ今日にする。
1つでも確かめられなかった日は前の日付のまま（表示は確かめられた分だけ更新する）。
"""
import datetime, io, json, os, re, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import update_stock as us  # noqa: E402
import site_checks as sc  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
HTML = os.path.join(ROOT, 'wp-snippets', 'ticket-page-content.html')
JSON_PATH = os.path.join(ROOT, 'wp-snippets', 'stock.json')
CSV_URL = ('https://docs.google.com/spreadsheets/d/1456s7-6nzhmIskjOuwVhIiSQ6TOk7KuQKYWkO51YdWw'
           '/export?format=csv&gid=714662832')
JST = datetime.timezone(datetime.timedelta(hours=9))
LABEL = {'available': '買える', 'few': '残りわずか', 'soldout': '売り切れ'}


def fetch_csv():
    req = urllib.request.Request(CSV_URL, headers={'User-Agent': 'Mozilla/5.0 (akigawa-hanabi stock)'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8')


def extract(s):
    """購入リンクの枠（div.akg-buylist[data-stock]）の中身と、カードの在庫表示を取り出す"""
    buylists = {}
    for m in re.finditer(r'<div class="akg-buylist" data-stock="(\w+)">', s):
        depth, start = 1, m.end()
        for t in re.finditer(r'<div\b|</div>', s[start:]):   # 入れ子の div があっても対応する閉じタグまで
            depth += 1 if t.group(0) == '<div' else -1
            if depth == 0:
                buylists[m.group(1)] = s[start:start + t.start()]
                break
    cards = dict(re.findall(r'<li class="akg-sf--(rec|ss|s|a|free)">.*?'
                            r'(<span class="akg-sf__stock akg-sf__stock--\w+"><i></i>[^<]+</span>)', s, flags=re.S))
    assert sorted(buylists) == sorted(us.STOCK_ID.values()) and len(cards) == 5, (sorted(buylists), sorted(cards))
    for k, b in buylists.items():
        assert 'akg-buylist__list' in b and 'class="akg-asof"' in b, '購入リンクの枠 %s の中身が想定と違う' % k
    return buylists, cards


def main():
    args = sys.argv[1:]
    now = datetime.datetime.now(JST)
    csv_text = (io.open(args[args.index('--csv') + 1], encoding='utf-8').read() if '--csv' in args
                else fetch_csv())
    seat, site = us.parse_sheet(csv_text)

    raw = json.load(io.open(args[args.index('--observed') + 1], encoding='utf-8')) if '--observed' in args else {}
    results = [sc.from_observed(raw, now.date())]
    if '--no-auto' not in args:
        results.append(sc.run_auto())
    seen, ok, notes = sc.merge(*results)

    orig = io.open(HTML, encoding='utf-8').read()
    page_date = re.search(r'class="akg-asof" data-date="([\d-]+)"', orig)
    prev_date = datetime.date.fromisoformat(page_date.group(1)) if page_date else now.date()
    complete = set(sc.SITES) <= ok
    date = now.date() if complete else prev_date

    s, changes, rows = us.transform(orig, seat, site, date, lambda key, st, url: seen.get((key, st)))
    buylists, cards = extract(s)

    print('== 確かめられたサイト: %s' % ('・'.join(x for x in sc.SITES if x in ok) or 'なし'))
    missing = [x for x in sc.SITES if x not in ok]
    if missing:
        print('== 確かめられなかったサイト: %s（日付は %s のまま）' % ('・'.join(missing), us.asof_label(date)))
    for n in notes:
        print('  - ' + n)
    print('== 表示の変更')
    print('\n'.join('  ' + c for c in changes) if changes else '  なし')
    warn = [r for r in rows if r[3] in ('available', 'few') and r[4] == '✕']
    if warn:
        print('== 要確認（販売サイトでは買えるのに、ページは✕）')
        for key, st, sheet_mark, seen_st, _ in warn:
            print('  %s / %s（シート %s・販売サイト %s）' % (key, st, sheet_mark, LABEL[seen_st]))

    data = {
        'date': date.isoformat(),
        'asof': us.asof_label(date),
        'generated': now.isoformat(timespec='seconds'),
        'checked': [x for x in sc.SITES if x in ok],
        'buylists': buylists,
        'cards': cards,
    }
    if s != orig:
        io.open(HTML, 'w', encoding='utf-8', newline='').write(s)
    io.open(JSON_PATH, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
    print('== 時点: %s' % data['asof'])


if __name__ == '__main__':
    main()
