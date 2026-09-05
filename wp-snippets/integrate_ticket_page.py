# -*- coding: utf-8 -*-
"""
integrate.py - Build the new ticket page body (page 1711) from the raw block markup.

Steps
 1. Prepend block6.html (3 ways to get tickets) and seat-quiz.html (seat quiz),
    both already wrapped in <!-- wp:html -->, inside ONE loos/full-wide wrapper
    (same attributes as the existing sections, see analysis_ticket.md section 4).
 2. Enable the core lightbox on link-less wp:image blocks (seat photos, parking maps,
    carousel photos). Images inside hidden blocks (blockVisibility:false) are skipped.
 3. Add an "アソビューで予約する" loos/button (same form as the existing recliner button)
    plus a small "other sales sites" paragraph after the price paragraph of SS/S/A cards.
 4. Never touch hidden blocks.
 5. Verify and write integrate_report.md.
"""
import json
import os
import re
import sys

BASE = r"C:\Users\hagiy\AppData\Local\Temp\claude\C--Users-hagiy\369bb84d-a425-40de-9910-583a13db931a\scratchpad"
RAW_PATH = os.path.join(BASE, "wp", "page_1711_raw.html")
BLOCK6_PATH = os.path.join(BASE, "out", "block6.html")
QUIZ_PATH = os.path.join(BASE, "out", "seat-quiz.html")
OUT_PATH = os.path.join(BASE, "out", "page_1711_new.html")
REPORT_PATH = os.path.join(BASE, "out", "integrate_report.md")

# ---- switches -----------------------------------------------------------------
# Wrap the two wp:html blocks in a loos/full-wide (analysis section 4 / checklist 1).
# Without it the new section is limited to the 900px article width on PC while the
# neighbouring sections are 1200px wide.
WRAP_IN_FULLWIDE = True
FULLWIDE_ANCHOR = "akg-guide"
# Give the SS/S/A price paragraph the same "u-mb-ctrl u-mb-20" class the two existing
# button cards use (analysis section 2 / 6), so the button spacing is identical.
ADD_MB_CLASS_TO_PRICE = True

ASOVIEW_LIST_URL = ("https://machizukuricon.my.urakata.app/channels/"
                    "debdd785-6f29-4fa5-827f-b8eb02f3a583/products?salesProductTagCode=v4h0rdje5x")
BUTTON_LABEL = "アソビューで予約する"
OTHER_SITES_HTML = '<a href="#site">他の販売サイト（ぴあ・KKday・楽天トラベル・JRE MALL）で購入</a>'

# Expected lightbox targets (analysis section 3): 5 seat photos + 2 parking maps + 7 carousel photos
EXPECTED_LIGHTBOX_IDS = {4435, 4277, 4278, 4279, 4495, 4251, 4252,
                         4298, 4305, 4301, 4295, 4293, 4297, 4296}
# Price paragraphs that get a button (exact text from raw)
PRICE_PARAGRAPHS = {
    "SS席": "1テーブル 35,000円（4名掛けのテーブル席）<br>※指定席。カフェチェア、カフェテーブル付き。<br>※第7回と異なりテントはありません。",
    "S席": "1テーブル 14,000円（2名掛けのテーブル席）<br>※指定席。テーブル、イス付き。",
    "A席": "大人 5,000円／子ども 2,000円（椅子席）<br>※指定席。テーブルなし。",
}


def read_utf8(path):
    with open(path, "rb") as f:
        data = f.read()
    if data.startswith(b"\xef\xbb\xbf"):
        raise SystemExit("BOM found in %s" % path)
    if b"\r" in data:
        raise SystemExit("CR found in %s" % path)
    return data.decode("utf-8")


def write_utf8(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


# ---- block delimiter parsing --------------------------------------------------
DELIM_RE = re.compile(r"<!--\s+(/)?wp:([a-z][a-z0-9_-]*(?:/[a-z][a-z0-9_-]*)?)(?:\s+(\{.*?\}))?\s+(/)?-->",
                      re.DOTALL)


def parse_delims(text):
    """Return list of dicts: kind(open/close/void), name, attrs(str|None), start, end."""
    out = []
    for m in DELIM_RE.finditer(text):
        closing, name, attrs, void = m.group(1), m.group(2), m.group(3), m.group(4)
        kind = "close" if closing else ("void" if void else "open")
        out.append({"kind": kind, "name": name, "attrs": attrs, "start": m.start(), "end": m.end(),
                    "attrs_span": (m.start(3), m.end(3)) if attrs else None})
    return out


def check_balance(text):
    """Stack-based matching. Returns (ok, per-name counts, problems, blocks)."""
    delims = parse_delims(text)
    stack = []
    problems = []
    counts = {}
    blocks = []
    for d in delims:
        c = counts.setdefault(d["name"], {"open": 0, "close": 0, "void": 0})
        c[d["kind"]] += 1
        if d["kind"] == "open":
            hidden = False
            if d["attrs"]:
                try:
                    a = json.loads(d["attrs"])
                    hidden = (a.get("metadata") or {}).get("blockVisibility") is False
                except Exception as e:  # noqa
                    problems.append("JSON parse error at %d (%s): %s" % (d["start"], d["name"], e))
            inherited = any(s["hidden"] for s in stack)
            stack.append({"d": d, "hidden": hidden or inherited, "self_hidden": hidden})
        elif d["kind"] == "close":
            if not stack:
                problems.append("close without open: %s at %d" % (d["name"], d["start"]))
                continue
            top = stack.pop()
            if top["d"]["name"] != d["name"]:
                problems.append("mismatch: open %s at %d / close %s at %d" %
                                (top["d"]["name"], top["d"]["start"], d["name"], d["start"]))
            blocks.append({"name": d["name"], "start": top["d"]["start"], "end": d["end"],
                           "attrs": top["d"]["attrs"], "attrs_span": top["d"]["attrs_span"],
                           "depth": len(stack), "hidden": top["hidden"], "self_hidden": top["self_hidden"]})
    for s in stack:
        problems.append("unclosed: %s at %d" % (s["d"]["name"], s["d"]["start"]))
    ok = not problems and all(v["open"] == v["close"] for v in counts.values())
    return ok, counts, problems, blocks


def main():
    raw = read_utf8(RAW_PATH)
    block6 = read_utf8(BLOCK6_PATH).rstrip("\n")
    quiz = read_utf8(QUIZ_PATH).rstrip("\n")

    for label, html in (("block6.html", block6), ("seat-quiz.html", quiz)):
        if not (html.startswith("<!-- wp:html -->") and html.endswith("<!-- /wp:html -->")):
            raise SystemExit("%s is not wrapped in wp:html" % label)
        inner = html[len("<!-- wp:html -->"):-len("<!-- /wp:html -->")]
        if "<!-- wp:" in inner or "<!-- /wp:" in inner:
            raise SystemExit("%s contains block delimiters inside wp:html" % label)

    ok0, counts0, problems0, blocks0 = check_balance(raw)
    if not ok0:
        raise SystemExit("raw is not balanced: %s" % problems0)

    edits = []  # (start, end, replacement, tag)

    # ---- 1. prefix -----------------------------------------------------------
    inner_blocks = block6 + "\n\n" + quiz
    if WRAP_IN_FULLWIDE:
        attrs = {"bgColor": "#ffffff", "contentSize": "container", "pcPadding": "20",
                 "spPadding": "20", "anchor": FULLWIDE_ANCHOR}
        prefix = ("<!-- wp:loos/full-wide %s -->\n"
                  '<div class="swell-block-fullWide pc-py-20 sp-py-20 alignfull" style="background-color:#ffffff" id="%s">'
                  '<div class="swell-block-fullWide__inner l-container">%s</div></div>\n'
                  "<!-- /wp:loos/full-wide -->"
                  % (json.dumps(attrs, separators=(",", ":"), ensure_ascii=False), FULLWIDE_ANCHOR, inner_blocks))
    else:
        prefix = inner_blocks
    edits.append((0, 0, prefix + "\n\n", "prefix"))

    # ---- 2. lightbox ---------------------------------------------------------
    lightbox_ids = []
    skipped_hidden = []
    for b in blocks0:
        if b["name"] != "image":
            continue
        a = json.loads(b["attrs"])
        if a.get("linkDestination") != "none":
            continue  # logos with custom links: untouched
        if b["hidden"]:
            skipped_hidden.append(a.get("id"))
            continue
        if a.get("lightbox") == {"enabled": True}:
            continue
        # sanity: our serializer reproduces the original string exactly
        if json.dumps(a, separators=(",", ":"), ensure_ascii=False) != b["attrs"]:
            raise SystemExit("attrs round-trip mismatch for image %s" % a.get("id"))
        new_a = {"lightbox": {"enabled": True}}
        for k, v in a.items():
            if k != "lightbox":
                new_a[k] = v
        new_attrs = json.dumps(new_a, separators=(",", ":"), ensure_ascii=False)
        s, e = b["attrs_span"]
        edits.append((s, e, new_attrs, "lightbox:%s" % a.get("id")))
        lightbox_ids.append(a.get("id"))

    if set(lightbox_ids) != EXPECTED_LIGHTBOX_IDS:
        raise SystemExit("lightbox targets differ from expectation: %s" % sorted(lightbox_ids))

    # ---- 3. buttons ----------------------------------------------------------
    button_block = (
        '<!-- wp:loos/button {"hrefUrl":"%s","btnAlign":"left","color":"red","className":"is-style-btn_line"} -->\n'
        '<div class="swell-block-button red_ is-style-btn_line" data-align="left">'
        '<a href="%s" class="swell-block-button__link"><span><strong>%s</strong></span></a></div>\n'
        "<!-- /wp:loos/button -->" % (ASOVIEW_LIST_URL, ASOVIEW_LIST_URL, BUTTON_LABEL))
    other_block = ('<!-- wp:paragraph {"className":"u-fz-s"} -->\n'
                   '<p class="u-fz-s">%s</p>\n'
                   "<!-- /wp:paragraph -->" % OTHER_SITES_HTML)
    button_targets = []
    for seat, price in PRICE_PARAGRAPHS.items():
        old = "<!-- wp:paragraph -->\n<p>%s</p>\n<!-- /wp:paragraph -->" % price
        idx = raw.find(old)
        if idx < 0 or raw.find(old, idx + 1) >= 0:
            raise SystemExit("price paragraph for %s not found or not unique" % seat)
        # make sure the paragraph lives inside the step-item whose title is this seat
        title = '<div class="swell-block-step__title u-fz-l">%s' % seat
        t = raw.rfind(title, 0, idx)
        if t < 0:
            raise SystemExit("step title for %s not found before its price paragraph" % seat)
        if ADD_MB_CLASS_TO_PRICE:
            new_para = ('<!-- wp:paragraph {"className":"u-mb-ctrl u-mb-20"} -->\n'
                        '<p class="u-mb-ctrl u-mb-20">%s</p>\n<!-- /wp:paragraph -->' % price)
        else:
            new_para = old
        new = new_para + "\n\n" + button_block + "\n\n" + other_block
        edits.append((idx, idx + len(old), new, "button:%s" % seat))
        button_targets.append(seat)

    # ---- apply edits ---------------------------------------------------------
    edits.sort(key=lambda x: (x[0], x[1]))
    for i in range(1, len(edits)):
        if edits[i][0] < edits[i - 1][1]:
            raise SystemExit("overlapping edits")
    out_parts = []
    pos = 0
    kept_segments = []
    for s, e, rep, tag in edits:
        seg = raw[pos:s]
        out_parts.append(seg)
        kept_segments.append(seg)
        out_parts.append(rep)
        pos = e
    tail = raw[pos:]
    out_parts.append(tail)
    kept_segments.append(tail)
    new = "".join(out_parts)
    write_utf8(OUT_PATH, new)

    # ---- verification --------------------------------------------------------
    report = []
    ok1, counts1, problems1, blocks1 = check_balance(new)

    # a) counts
    n_html_new = counts1.get("html", {}).get("open", 0) - counts0.get("html", {}).get("open", 0)
    n_button_new = counts1.get("loos/button", {}).get("open", 0) - counts0.get("loos/button", {}).get("open", 0)
    n_fullwide_new = counts1.get("loos/full-wide", {}).get("open", 0) - counts0.get("loos/full-wide", {}).get("open", 0)
    n_lightbox_true = len(re.findall(r'<!-- wp:image \{"lightbox":\{"enabled":true\}', new))
    n_lightbox_false = len(re.findall(r'"lightbox":\{"enabled":false\}', new))
    n_other = new.count('<p class="u-fz-s">' + OTHER_SITES_HTML + "</p>")
    n_mb_price = sum(1 for p in PRICE_PARAGRAPHS.values()
                     if ('<p class="u-mb-ctrl u-mb-20">%s</p>' % p) in new)

    # b) kept segments appear in order in the new body (original preserved except edits)
    cursor = 0
    order_ok = True
    for seg in kept_segments:
        j = new.find(seg, cursor)
        if j < 0:
            order_ok = False
            break
        cursor = j + len(seg)
    # b2) exact reverse transform
    rev = new
    if rev.startswith(prefix + "\n\n"):
        rev = rev[len(prefix) + 2:]
    else:
        order_ok = False
    for s, e, rep, tag in edits:
        if tag == "prefix":
            continue
        if rev.count(rep) < 1:
            order_ok = False
        rev = rev.replace(rep, raw[s:e], 1)
    reverse_ok = (rev == raw)

    # c) hidden blocks untouched
    hidden_blocks0 = [raw[b["start"]:b["end"]] for b in blocks0 if b["self_hidden"]]
    hidden_ok = all(new.count(h) == raw.count(h) for h in hidden_blocks0)
    n_hidden0 = raw.count('"blockVisibility":false')
    n_hidden1 = new.count('"blockVisibility":false')

    # d) hrefUrl == href for every loos/button
    btn_ok = True
    btn_total = 0
    for b in blocks1:
        if b["name"] != "loos/button":
            continue
        btn_total += 1
        a = json.loads(b["attrs"])
        html = new[b["start"]:b["end"]]
        m = re.search(r'<a href="([^"]*)"', html)
        href = m.group(1).replace("&amp;", "&") if m else None
        if href != a.get("hrefUrl"):
            btn_ok = False

    # e) inserted wp:html blocks: verbatim and delimiter-free inside
    html_blocks = [new[b["start"]:b["end"]] for b in blocks1 if b["name"] == "html"]
    verbatim_ok = (block6 in new) and (quiz in new) and html_blocks == [block6, quiz]

    # f) encoding / newline
    data = new.encode("utf-8")
    enc_ok = (b"\r" not in data) and (not data.startswith(b"\xef\xbb\xbf"))

    n_chars = len(new)
    n_bytes = len(data)
    n_lines = new.count("\n") + 1

    all_ok = (ok1 and n_html_new == 2 and n_button_new == 3 and len(lightbox_ids) == 14 and n_lightbox_true == 14
              and n_lightbox_false == 5 and n_other == 3 and order_ok and reverse_ok and hidden_ok
              and n_hidden0 == n_hidden1 == 7 and btn_ok and verbatim_ok and enc_ok and skipped_hidden == [3268])

    def mark(v):
        return "OK" if v else "NG"

    per_name = "\n".join("| `%s` | %d | %d | %s |" % (k, v["open"], v["close"], mark(v["open"] == v["close"]))
                         for k, v in sorted(counts1.items()))
    lb_rows = ", ".join(str(i) for i in lightbox_ids)

    report.append("# 統合レポート（page 1711 `/ticket/` 本文）\n")
    report.append("- 入力: `wp/page_1711_raw.html`（%d文字 / %d行）" % (len(raw), raw.count("\n") + 1))
    report.append("- 出力: `out/page_1711_new.html`（**%d文字** / %d バイト / %d行、UTF-8 BOMなし・LF）" % (n_chars, n_bytes, n_lines))
    report.append("- 総合判定: **%s**\n" % ("すべてOK" if all_ok else "要確認（下記NG項目）"))

    report.append("## 1. 各処理の適用件数\n")
    report.append("| 処理 | 件数 | 期待値 | 判定 |")
    report.append("|---|---|---|---|")
    report.append("| 先頭への `wp:html` ブロック挿入（block6.html → seat-quiz.html、間は空行1つ） | %d | 2 | %s |" % (n_html_new, mark(n_html_new == 2)))
    report.append("| ↑を包む `loos/full-wide`（既存セクションと同じ属性、anchor `%s`） | %d | 1 | %s |" % (FULLWIDE_ANCHOR, n_fullwide_new, mark(n_fullwide_new == 1)))
    report.append("| 画像の `\"lightbox\":{\"enabled\":true}` 追加 | %d | 14（席5＋駐車場2＋スクロール写真7） | %s |" % (len(lightbox_ids), mark(len(lightbox_ids) == 14 and n_lightbox_true == 14)))
    report.append("| SS/S/A席カードへの `loos/button`「%s」追加 | %d | 3 | %s |" % (BUTTON_LABEL, n_button_new, mark(n_button_new == 3)))
    report.append("| ボタン直下の小さめ段落（`u-fz-s`、`#site` へのリンク） | %d | 3 | %s |" % (n_other, mark(n_other == 3)))
    report.append("| SS/S/A席の価格段落に `u-mb-ctrl u-mb-20` を付与（既存ボタン付きカードと同じ余白） | %d | 3 | %s |" % (n_mb_price, mark(n_mb_price == 3)))
    report.append("| ロゴ画像の `lightbox:false`（無変更のまま残る数） | %d | 5 | %s |" % (n_lightbox_false, mark(n_lightbox_false == 5)))
    report.append("| 非表示ブロック（`blockVisibility:false`）の数 | 元 %d → 新 %d | 7 → 7 | %s |" % (n_hidden0, n_hidden1, mark(n_hidden0 == n_hidden1 == 7)))
    report.append("")
    report.append("ライトボックス化した画像ID（`linkDestination:\"none\"` かつ表示中のブロック内、本文の出現順）: %s" % lb_rows)
    report.append("")
    report.append("対象外にした画像: ロゴ5枚（4247, 4246, 4222, 4223, 4224 = `linkDestination:\"custom\"`、`lightbox:false` のまま）、"
                  "非表示ブロック内の画像 %s（触っていません）。\n" % (skipped_hidden or "なし"))

    report.append("## 2. ブロックの開閉対応（`<!-- wp:` と `<!-- /wp:`）\n")
    report.append("- 入れ子（スタック）検証: **%s**%s" % (mark(ok1), "" if ok1 else " → " + "; ".join(problems1)))
    report.append("- 挿入した2つの `wp:html` の内側に `<!-- wp:` / `<!-- /wp:` が無いこと: OK（スクリプトが事前に検査）")
    report.append("- 挿入した `wp:html` 2ブロックが元ファイル（block6.html / seat-quiz.html）と1文字も違わないこと: %s\n" % mark(verbatim_ok))
    report.append("| ブロック名 | 開 | 閉 | 判定 |")
    report.append("|---|---|---|---|")
    report.append(per_name)
    report.append("")

    report.append("## 3. 元の本文がそのまま含まれているか\n")
    report.append("- 編集していない区間（%d区間）が新本文に同じ順序で出現: **%s**" % (len(kept_segments), mark(order_ok)))
    report.append("- 逆変換（先頭の挿入を外し、置換部分を元に戻す）で元の本文と完全一致: **%s**" % mark(reverse_ok))
    report.append("- 非表示ブロック7個が一字一句そのまま残っていること（出現回数も一致）: **%s**" % mark(hidden_ok))
    report.append("- `loos/button` 全%d個で属性 `hrefUrl` と HTML の `href` が一致: **%s**" % (btn_total, mark(btn_ok)))
    report.append("- UTF-8（BOMなし）・改行LF: **%s**\n" % mark(enc_ok))

    report.append("## 4. 置換内容の詳細\n")
    report.append("### 先頭に挿入したもの")
    report.append("```")
    report.append(prefix.split("\n")[0])
    report.append(prefix.split("\n")[1][:150] + "…")
    report.append("  （block6.html の中身そのまま）")
    report.append("  空行1つ")
    report.append("  （seat-quiz.html の中身そのまま）")
    report.append("<!-- /wp:html --></div></div>")
    report.append("<!-- /wp:loos/full-wide -->")
    report.append("```")
    report.append("analysis_ticket.md §4 の結論どおり「本文の先頭（`#site` セクションの前・外側）」に置きました。"
                  "`#site` の着地点は変わりません。full-wide で包んだ理由: 本文カラムは最大900px、既存セクションは1200pxのため、"
                  "包まないとPCで新ブロックだけ狭く見えるため（§4「挿入時の注意」、チェックリスト1）。包まない形にしたい場合は `integrate.py` の "
                  "`WRAP_IN_FULLWIDE = False` で再実行できます。\n")
    report.append("### 画像ブロックの属性変更（例: SS席）")
    report.append("```")
    report.append('<!-- wp:image {"id":4277,"aspectRatio":"4/3","scale":"cover","sizeSlug":"full","linkDestination":"none"} -->')
    report.append("↓")
    report.append('<!-- wp:image {"lightbox":{"enabled":true},"id":4277,"aspectRatio":"4/3","scale":"cover","sizeSlug":"full","linkDestination":"none"} -->')
    report.append("```")
    report.append("JSONは `json.loads` → `\"lightbox\"` を先頭に追加（既存ロゴの属性順に合わせた） → `json.dumps`（空白なし）で書き戻し。"
                  "既存キーの順序と値はそのまま（書き戻し前に元の文字列と一致することを確認済み）。HTML本体（`<figure>`）は無変更。\n")
    report.append("### SS席・S席・A席カードに追加したブロック（例: SS席）")
    report.append("```")
    report.append('<!-- wp:paragraph {"className":"u-mb-ctrl u-mb-20"} -->')
    report.append('<p class="u-mb-ctrl u-mb-20">%s</p>' % PRICE_PARAGRAPHS["SS席"])
    report.append("<!-- /wp:paragraph -->")
    report.append("")
    report.append(button_block)
    report.append("")
    report.append(other_block)
    report.append("```")
    report.append("- ボタンはリクライニング席（raw L138–140）と同一形式（`btnAlign:left`、`color:red`、`is-style-btn_line`、`<span><strong>` の太字）。"
                  "リンク先は facts_extracted.txt のアソビュー一覧URL（`&` を含まないためエスケープ不要）。")
    report.append("- 価格段落の `u-mb-ctrl u-mb-20` は analysis §2・§6 の指示（ボタン付きカードだけに付いているクラス）。文言は無変更。"
                  "不要なら `ADD_MB_CLASS_TO_PRICE = False` で再実行できます。")
    report.append("- 小さめ段落は `.u-fz-s{font-size:var(--swl-fz--small)!important}`（main.css）を利用。括弧は同じカード内の価格表記に合わせて全角にしています。\n")

    report.append("## 5. 手動で確認していただきたい点\n")
    report.append("- 本番でスマホSafariの「タップで拡大」「閉じる」が動くこと（analysis §3 の展開手順どおり、まず1枚で確認してもよい）。")
    report.append("- `wp:html` 内の `<script>` は管理者（unfiltered_html）権限で保存すること。")
    report.append("- 画像の `alt` は今回触っていません（拡大表示の説明文が空のまま）。席名を入れる場合は `<img alt=\"…\">` だけ書き換えれば済みます。")

    write_utf8(REPORT_PATH, "\n".join(report) + "\n")

    summary = {
        "all_ok": all_ok,
        "inserted_html_blocks": n_html_new,
        "fullwide_wrapper": n_fullwide_new,
        "lightbox_enabled": len(lightbox_ids),
        "lightbox_false_logos": n_lightbox_false,
        "buttons_added": n_button_new,
        "other_site_paragraphs": n_other,
        "price_mb_class": n_mb_price,
        "hidden_blocks": [n_hidden0, n_hidden1],
        "skipped_hidden_images": skipped_hidden,
        "balance_ok": ok1,
        "balance_problems": problems1,
        "kept_order_ok": order_ok,
        "reverse_ok": reverse_ok,
        "hidden_ok": hidden_ok,
        "button_href_ok": btn_ok,
        "verbatim_ok": verbatim_ok,
        "encoding_ok": enc_ok,
        "chars": n_chars,
        "bytes": n_bytes,
        "lines": n_lines,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
