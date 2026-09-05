# -*- coding: utf-8 -*-
"""
integrate.py - Build the new ticket page body (page 1711) from the raw block markup.

Steps
 1. Prepend two loos/full-wide sections (same attributes as the existing sections,
    see analysis_ticket.md section 4 / seat_quiz_spec.md section 6-1):
      - full-wide #1 (anchor akg-guide): block6.html (3 ways to get tickets)
      - full-wide #2 (anchor akg-quiz-sec): core/heading h2 + seat-quiz.html (seat quiz)
    Both html files are already wrapped in <!-- wp:html -->.
 2. Enable the core lightbox on link-less wp:image blocks (seat photos, parking maps,
    carousel photos) and give each of them an alt text (visually confirmed 2026-09-05).
    Images inside hidden blocks (blockVisibility:false) are skipped.
 2b. Give the 5 logo/banner images of the "販売サイト" section (#site) an alt text, because each
    purchase link contains nothing but that image (WCAG 1.1.1 / 2.4.4, F89).
 2c. In the sales-site table, replace the icon-only "available" cells (aria-hidden span, no text)
    with the text 〇 already used by one cell of the same table (WCAG 1.1.1 / 1.3.3).
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
# The quiz gets its own full-wide so that its h2 is the first child of the inner box
# (.post_content div>:first-child{margin-top:0!important}); a heading in the middle of a
# full-wide would get the theme's 4em top margin (.post_content h2{margin:4em 0 2em}).
# Adjacent full-wides overlap by 2em (.swell-block-fullWide+.swell-block-fullWide{margin-top:-2em}),
# which is the same rhythm as the existing sections.
QUIZ_ANCHOR = "akg-quiz-sec"
QUIZ_HEADING_TEXT = "どの席にしようか迷ったら"
QUIZ_HEADING = ('<!-- wp:heading {"className":"is-style-section_ttl"} -->\n'
                '<h2 class="wp-block-heading is-style-section_ttl"><span class="swl-fz u-fz-xl">%s</span></h2>\n'
                "<!-- /wp:heading -->" % QUIZ_HEADING_TEXT)
# Give the SS/S/A price paragraph the same "u-mb-ctrl u-mb-20" class the two existing
# button cards use (analysis section 2 / 6), so the button spacing is identical.
ADD_MB_CLASS_TO_PRICE = True

ASOVIEW_LIST_URL = ("https://machizukuricon.my.urakata.app/channels/"
                    "debdd785-6f29-4fa5-827f-b8eb02f3a583/products?salesProductTagCode=v4h0rdje5x")
BUTTON_LABEL = "アソビューで予約する"
OTHER_SITES_HTML = '<a href="#site">他の販売サイト（チケットぴあ・KKday・楽天トラベル・JRE MALL）で購入する</a>'
# class of that paragraph: u-fz-s (theme small font) + akg-sublink
# (seat-quiz.html <style> has `.post_content .akg-sublink a{display:inline-block;box-sizing:border-box;min-height:44px;padding:.65em 0}` -> ~45px tap height)
OTHER_SITES_CLASS = "u-fz-s akg-sublink"

# alt text for the 5 logo/banner images that are the only content of the purchase links in the
# "販売サイト" section (#site). id -> (alt, substring the link href must contain)
LOGO_ALT = {
    4247: ("楽天トラベルで購入する", "experiences.travel.rakuten.co.jp"),
    4246: ("JRE MALLで購入する", "event.jreast.co.jp"),
    4222: ("チケットぴあで購入する", "t.pia.jp"),
    4223: ("アソビューで購入する", "urakata.app"),
    4224: ("KKdayで購入する", "kkday.com"),
}
# "available" cells of the sales-site table: icon-only span (aria-hidden="true", a single space as text).
# Replaced by the text the アソビュー×フリーエリア cell of the same table already uses.
TABLE_ICON_RE = re.compile(r'<span [^>]*class="swl-inline-icon"[^>]*> </span>')
TABLE_MARK = "〇"
EXPECTED_TABLE_ICONS = 21

# Expected lightbox targets (analysis section 3): 5 seat photos + 2 parking maps + 7 carousel photos
EXPECTED_LIGHTBOX_IDS = {4435, 4277, 4278, 4279, 4495, 4251, 4252,
                         4298, 4305, 4301, 4295, 4293, 4297, 4296}
# alt text for every lightbox image (the core/image block keeps alt only in the <img> tag).
# Each image was opened in a browser and checked on 2026-09-05; the wording follows the seat
# names / prices on the same page and adds nothing that is not visible in the picture.
IMAGE_ALT = {
    4435: "リクライニングペアシート席から花火を観覧している写真",
    4277: "SS席（4名掛けのテーブル席）の写真",
    4278: "S席（2名掛けのテーブル席）の写真",
    4279: "A席（椅子席）の写真",
    4495: "西多摩在住者限定フリーエリアの案内画像",
    4251: "駐車場（観覧会場隣接）の案内図",
    4252: "駐車場（東京サマーランドプール側）の案内図",
    4298: "観覧席から見た花火の写真",
    4305: "キッチンカーの写真",
    4301: "紅葉の写真",
    4295: "会場に並ぶリクライニングシートの写真",
    4293: "SS席のテーブルとイスの写真",
    4297: "S席のテーブルとイスの写真",
    4296: "A席の椅子が並ぶ写真",
}
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
    quiz_blocks = QUIZ_HEADING + "\n\n" + quiz

    def fullwide(anchor, inner):
        attrs = {"bgColor": "#ffffff", "contentSize": "container", "pcPadding": "20",
                 "spPadding": "20", "anchor": anchor}
        return ("<!-- wp:loos/full-wide %s -->\n"
                '<div class="swell-block-fullWide pc-py-20 sp-py-20 alignfull" style="background-color:#ffffff" id="%s">'
                '<div class="swell-block-fullWide__inner l-container">%s</div></div>\n'
                "<!-- /wp:loos/full-wide -->"
                % (json.dumps(attrs, separators=(",", ":"), ensure_ascii=False), anchor, inner))

    if WRAP_IN_FULLWIDE:
        prefix = fullwide(FULLWIDE_ANCHOR, block6) + "\n\n" + fullwide(QUIZ_ANCHOR, quiz_blocks)
    else:
        prefix = block6 + "\n\n" + quiz_blocks
    edits.append((0, 0, prefix + "\n\n", "prefix"))

    # ---- 2. lightbox ---------------------------------------------------------
    lightbox_ids = []
    alt_ids = []
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
        # alt text: exactly one alt="" inside this image block
        body = raw[b["start"]:b["end"]]
        if body.count('alt=""') != 1:
            raise SystemExit("image %s: expected exactly one alt=\"\"" % a.get("id"))
        alt_text = IMAGE_ALT.get(a.get("id"))
        if not alt_text:
            raise SystemExit("no alt text defined for image %s" % a.get("id"))
        if '"' in alt_text or "<" in alt_text or "&" in alt_text:
            raise SystemExit("alt text for image %s contains a character that needs escaping" % a.get("id"))
        p = b["start"] + body.find('alt=""')
        edits.append((p, p + len('alt=""'), 'alt="%s"' % alt_text, "alt:%s" % a.get("id")))
        alt_ids.append(a.get("id"))

    if set(lightbox_ids) != EXPECTED_LIGHTBOX_IDS:
        raise SystemExit("lightbox targets differ from expectation: %s" % sorted(lightbox_ids))
    if alt_ids != lightbox_ids:
        raise SystemExit("alt targets differ from lightbox targets")

    # ---- 2b. logo / banner links in #site: alt = destination ---------------------
    logo_ids = []
    for b in blocks0:
        if b["name"] != "image" or b["hidden"]:
            continue
        a = json.loads(b["attrs"])
        if a.get("linkDestination") != "custom":
            continue
        img_id = a.get("id")
        if img_id not in LOGO_ALT:
            raise SystemExit("unexpected custom-link image %s" % img_id)
        alt_text, href_hint = LOGO_ALT[img_id]
        body = raw[b["start"]:b["end"]]
        if body.count('alt=""') != 1:
            raise SystemExit("logo image %s: expected exactly one alt=\"\"" % img_id)
        m = re.search(r'<a href="([^"]*)"', body)
        if not m or href_hint not in m.group(1):
            raise SystemExit("logo image %s: link does not point to %s" % (img_id, href_hint))
        if ('alt="%s" class="wp-image-%d"' % ("", img_id)) not in body:
            raise SystemExit("logo image %s: alt/class order differs" % img_id)
        p = b["start"] + body.find('alt=""')
        edits.append((p, p + len('alt=""'), 'alt="%s"' % alt_text, "logoalt:%s" % img_id))
        logo_ids.append(img_id)
    if set(logo_ids) != set(LOGO_ALT):
        raise SystemExit("logo targets differ from expectation: %s" % sorted(logo_ids))

    # ---- 2c. sales-site table: icon-only cells -> text -----------------------------
    tables = [b for b in blocks0 if b["name"] == "table"]
    if len(tables) != 1 or tables[0]["hidden"]:
        raise SystemExit("expected exactly one visible core/table block")
    tb = tables[0]
    tbody = raw[tb["start"]:tb["end"]]
    n_icon_edits = 0
    for m in TABLE_ICON_RE.finditer(tbody):
        edits.append((tb["start"] + m.start(), tb["start"] + m.end(), TABLE_MARK, "tableicon"))
        n_icon_edits += 1
    if n_icon_edits != EXPECTED_TABLE_ICONS or raw.count("swl-inline-icon") != EXPECTED_TABLE_ICONS:
        raise SystemExit("table icons: found %d, expected %d" % (n_icon_edits, EXPECTED_TABLE_ICONS))

    # ---- 3. buttons ----------------------------------------------------------
    button_block = (
        '<!-- wp:loos/button {"hrefUrl":"%s","btnAlign":"left","color":"red","className":"is-style-btn_line"} -->\n'
        '<div class="swell-block-button red_ is-style-btn_line" data-align="left">'
        '<a href="%s" class="swell-block-button__link"><span><strong>%s</strong></span></a></div>\n'
        "<!-- /wp:loos/button -->" % (ASOVIEW_LIST_URL, ASOVIEW_LIST_URL, BUTTON_LABEL))
    other_block = ('<!-- wp:paragraph {"className":"%s"} -->\n'
                   '<p class="%s">%s</p>\n'
                   "<!-- /wp:paragraph -->" % (OTHER_SITES_CLASS, OTHER_SITES_CLASS, OTHER_SITES_HTML))
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
    applied = []  # (new_start, new_end, raw_start, raw_end, replacement, tag)
    new_len = 0
    for s, e, rep, tag in edits:
        seg = raw[pos:s]
        out_parts.append(seg)
        kept_segments.append(seg)
        new_len += len(seg)
        applied.append((new_len, new_len + len(rep), s, e, rep, tag))
        out_parts.append(rep)
        new_len += len(rep)
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
    n_heading_new = counts1.get("heading", {}).get("open", 0) - counts0.get("heading", {}).get("open", 0)
    n_quiz_heading = new.count(QUIZ_HEADING)
    n_alt_set = sum(1 for i in lightbox_ids if ('alt="%s" class="wp-image-%d"' % (IMAGE_ALT[i], i)) in new)
    n_alt_empty0 = raw.count('alt=""')
    n_alt_empty1 = new.count('alt=""')
    n_lightbox_true = len(re.findall(r'<!-- wp:image \{"lightbox":\{"enabled":true\}', new))
    n_lightbox_false = len(re.findall(r'"lightbox":\{"enabled":false\}', new))
    n_other = new.count('<p class="%s">%s</p>' % (OTHER_SITES_CLASS, OTHER_SITES_HTML))
    n_logo_alt = sum(1 for i, (alt, _h) in LOGO_ALT.items() if ('alt="%s" class="wp-image-%d"' % (alt, i)) in new)
    n_icon0 = raw.count("swl-inline-icon")
    n_icon1 = new.count("swl-inline-icon")
    n_mark0 = raw.count(TABLE_MARK)
    n_mark1 = new.count(TABLE_MARK)
    n_sublink_css = quiz.count(".post_content .akg-sublink a{")
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
    # b2) exact reverse transform (position based, so repeated replacements such as 〇 are safe)
    rev = new
    reverse_ok = True
    for ns, ne, s, e, rep, tag in reversed(applied):
        if rev[ns:ne] != rep:
            reverse_ok = False
            break
        rev = rev[:ns] + raw[s:e] + rev[ne:]
    reverse_ok = reverse_ok and (rev == raw)

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

    expected_fullwide = 2 if WRAP_IN_FULLWIDE else 0
    all_ok = (ok1 and n_html_new == 2 and n_button_new == 3 and len(lightbox_ids) == 14 and n_lightbox_true == 14
              and n_lightbox_false == 5 and n_other == 3 and order_ok and reverse_ok and hidden_ok
              and n_hidden0 == n_hidden1 == 7 and btn_ok and verbatim_ok and enc_ok and skipped_hidden == [3268]
              and n_fullwide_new == expected_fullwide and n_heading_new == 1 and n_quiz_heading == 1
              and n_alt_set == 14 and n_alt_empty1 == n_alt_empty0 - 14 - len(LOGO_ALT)
              and n_logo_alt == len(LOGO_ALT) and n_icon0 == EXPECTED_TABLE_ICONS and n_icon1 == 0
              and n_mark1 == n_mark0 + EXPECTED_TABLE_ICONS and n_sublink_css == 1)

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
    report.append("| 先頭への `wp:html` ブロック挿入（block6.html、seat-quiz.html） | %d | 2 | %s |" % (n_html_new, mark(n_html_new == 2)))
    report.append("| 座席診断の見出し `core/heading`（h2「%s」、`is-style-section_ttl`） | %d | 1 | %s |" % (QUIZ_HEADING_TEXT, n_quiz_heading, mark(n_heading_new == 1 and n_quiz_heading == 1)))
    report.append("| ↑を包む `loos/full-wide`（既存セクションと同じ属性。anchor `%s` = block6、`%s` = 見出し＋診断） | %d | %d | %s |" % (FULLWIDE_ANCHOR, QUIZ_ANCHOR, n_fullwide_new, expected_fullwide, mark(n_fullwide_new == expected_fullwide)))
    report.append("| 画像の `\"lightbox\":{\"enabled\":true}` 追加 | %d | 14（席5＋駐車場2＋スクロール写真7） | %s |" % (len(lightbox_ids), mark(len(lightbox_ids) == 14 and n_lightbox_true == 14)))
    report.append("| 同じ14枚の `alt=\"\"` を説明文に置換 | %d | 14 | %s |" % (n_alt_set, mark(n_alt_set == 14)))
    report.append("| 販売サイト（`#site`）のロゴ／バナー5枚の `alt=\"\"` を「○○で購入する」に置換（画像だけのリンクの名前になる） | %d | 5 | %s |" % (n_logo_alt, mark(n_logo_alt == len(LOGO_ALT))))
    report.append("| `alt=\"\"` の残数（非表示ブロック内の画像1枚＋バナーリンクの背景画像1枚だけ） | %d → %d | 21 → 2 | %s |" % (n_alt_empty0, n_alt_empty1, mark(n_alt_empty1 == n_alt_empty0 - 14 - len(LOGO_ALT) == 2)))
    report.append("| 対応表の「販売あり」アイコン（`swl-inline-icon`、読み上げ不可）を文字「〇」に置換（`〇` %d → %d、`swl-inline-icon` %d → %d） | %d | 21 | %s |" % (n_mark0, n_mark1, n_icon0, n_icon1, n_icon0 - n_icon1, mark(n_icon1 == 0 and n_mark1 == n_mark0 + EXPECTED_TABLE_ICONS)))
    report.append("| SS/S/A席カードへの `loos/button`「%s」追加 | %d | 3 | %s |" % (BUTTON_LABEL, n_button_new, mark(n_button_new == 3)))
    report.append("| ボタン直下の小さめ段落（`%s`、`#site` へのリンク。タップ高さは seat-quiz.html の CSS で約45px） | %d | 3 | %s |" % (OTHER_SITES_CLASS, n_other, mark(n_other == 3 and n_sublink_css == 1)))
    report.append("| SS/S/A席の価格段落に `u-mb-ctrl u-mb-20` を付与（既存ボタン付きカードと同じ余白） | %d | 3 | %s |" % (n_mb_price, mark(n_mb_price == 3)))
    report.append("| ロゴ画像の `lightbox:false`（無変更のまま残る数） | %d | 5 | %s |" % (n_lightbox_false, mark(n_lightbox_false == 5)))
    report.append("| 非表示ブロック（`blockVisibility:false`）の数 | 元 %d → 新 %d | 7 → 7 | %s |" % (n_hidden0, n_hidden1, mark(n_hidden0 == n_hidden1 == 7)))
    report.append("")
    report.append("ライトボックス化した画像ID（`linkDestination:\"none\"` かつ表示中のブロック内、本文の出現順）: %s" % lb_rows)
    report.append("")
    report.append("ライトボックスの対象外: ロゴ／バナー5枚（4247, 4246, 4222, 4223, 4224 = `linkDestination:\"custom\"`、`lightbox:false` のまま。alt だけ下記のとおり追加）、"
                  "非表示ブロック内の画像 %s（触っていません）。`alt=\"\"` が残る2枚は、非表示ブロック内の 3268（フリー席.jpg）と `loos/banner-link` の背景画像（装飾）です。\n" % (skipped_hidden or "なし"))
    report.append("### 画像に入れた alt（拡大ボタンの読み上げ名になります。実画像を開いて確認済み）\n")
    report.append("| 画像ID | ファイル名の一部 | alt |")
    report.append("|---|---|---|")
    for i in lightbox_ids:
        m = re.search(r'wp-image-%d' % i, new)
        seg = new[max(0, m.start() - 400):m.start()] if m else ""
        fm = re.findall(r'/uploads/([^"]+)" alt=', seg)
        report.append("| %d | %s | %s |" % (i, fm[-1] if fm else "", IMAGE_ALT[i]))
    report.append("")

    report.append("## 2. ブロックの開閉対応（`<!-- wp:` と `<!-- /wp:`）\n")
    report.append("- 入れ子（スタック）検証: **%s**%s" % (mark(ok1), "" if ok1 else " → " + "; ".join(problems1)))
    report.append("- 挿入した2つの `wp:html` の内側に `<!-- wp:` / `<!-- /wp:` が無いこと: OK（スクリプトが事前に検査）")
    report.append("- 挿入した `wp:html` 2ブロックが元ファイル（block6.html / seat-quiz.html）と1文字も違わないこと: %s" % mark(verbatim_ok))
    report.append("- 座席診断の見出しブロックが1つだけ入っていること（`heading` の開閉数が元より1多い）: %s\n" % mark(n_heading_new == 1 and n_quiz_heading == 1))
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
    report.append("### 先頭に挿入したもの（full-wide 2つ）")
    report.append("```")
    fw1 = fullwide(FULLWIDE_ANCHOR, "…")
    fw2 = fullwide(QUIZ_ANCHOR, "…")
    report.append(fw1.split("\n")[0])
    report.append(fw1.split("\n")[1].split("…")[0] + "…")
    report.append("  （block6.html の中身そのまま）")
    report.append("<!-- /wp:html --></div></div>")
    report.append("<!-- /wp:loos/full-wide -->")
    report.append("")
    report.append(fw2.split("\n")[0])
    hl = QUIZ_HEADING.split("\n")
    report.append(fw2.split("\n")[1].split("…")[0] + hl[0])
    for line in hl[1:]:
        report.append(line)
    report.append("  空行1つ")
    report.append("  （seat-quiz.html の中身そのまま）")
    report.append("<!-- /wp:html --></div></div>")
    report.append("<!-- /wp:loos/full-wide -->")
    report.append("```")
    report.append("analysis_ticket.md §4 の結論どおり「本文の先頭（`#site` セクションの前・外側）」に置きました。"
                  "`#site` の着地点は変わりません。full-wide で包んだ理由: 本文カラムは最大900px、既存セクションは1200pxのため、"
                  "包まないとPCで新ブロックだけ狭く見えるため（§4「挿入時の注意」、チェックリスト1）。")
    report.append("見出し h2「%s」は seat_quiz_spec.md §5・§6-1 のとおり診断ブロックの外（`core/heading`）に置き、"
                  "既存の「販売サイト」見出しと同じ形式です（目次にも載ります）。診断を2つ目の full-wide に分けた理由: "
                  "見出しを full-wide の先頭に置くとテーマの `.post_content div>:first-child{margin-top:0!important}` で上余白が0になり、"
                  "full-wide 同士は `-2em` で重なるため、既存セクションと同じ余白リズムになります。"
                  "1つの full-wide の途中に h2 を挟むと `.post_content h2{margin:4em 0 2em}` の上余白（375px幅で80px超）が出るため避けました。"
                  "包まない形にしたい場合は `integrate.py` の `WRAP_IN_FULLWIDE = False` で再実行できます。\n" % QUIZ_HEADING_TEXT)
    report.append("### 画像ブロックの属性変更（例: SS席）")
    report.append("```")
    report.append('<!-- wp:image {"id":4277,"aspectRatio":"4/3","scale":"cover","sizeSlug":"full","linkDestination":"none"} -->')
    report.append("↓")
    report.append('<!-- wp:image {"lightbox":{"enabled":true},"id":4277,"aspectRatio":"4/3","scale":"cover","sizeSlug":"full","linkDestination":"none"} -->')
    report.append("```")
    report.append("JSONは `json.loads` → `\"lightbox\"` を先頭に追加（既存ロゴの属性順に合わせた） → `json.dumps`（空白なし）で書き戻し。"
                  "既存キーの順序と値はそのまま（書き戻し前に元の文字列と一致することを確認済み）。")
    report.append("HTML本体（`<figure>`）は `alt=\"\"` → `alt=\"SS席（4名掛けのテーブル席）の写真\"` の置換だけ（core/image の alt は `<img>` にしか保存されないため、ブロック属性の変更は不要）。"
                  "ライトボックス有効時は画像ごとに「拡大」ボタンが生成されるので、読み上げ環境で何の画像か分かるようにしました。\n")
    report.append("### 販売サイト（`#site`）のロゴ／バナーの alt")
    report.append("```")
    for i in (4247, 4246, 4222, 4223, 4224):
        report.append('<img … alt="" class="wp-image-%d"/>  →  <img … alt="%s" class="wp-image-%d"/>' % (i, LOGO_ALT[i][0], i))
    report.append("```")
    report.append("5つの購入リンクは画像だけを中身にしているため、alt が空だと読み上げでは「リンク」としか読まれません（WCAG 1.1.1 / 2.4.4、失敗例F89）。"
                  "座席診断の「他の販売サイトで購入する」と block6 の1枚目のカードがここへ誘導するので、行き先が分かる alt を入れました。"
                  "ブロック属性は変更していません（alt は `<img>` にしか保存されないため）。置換前に各リンクの href が対応するサイトを指していることをスクリプトが確認しています。\n")
    report.append("### 提携サイトの販売座席対応表（`core/table`）")
    report.append("```")
    report.append('<td><span style="--the-icon-svg: url(data:…)" data-icon="LsCircle" data-id="0" aria-hidden="true" class="swl-inline-icon"> </span></td>')
    report.append("↓")
    report.append("<td>〇</td>")
    report.append("```")
    report.append("「販売あり」の21セルが `aria-hidden` のアイコンだけで、読み上げでは空セル（「ー」と区別できない）でした。"
                  "同じ表の アソビュー×フリーエリア のセルがすでに文字「〇」なので、それに揃えました（見た目は丸のまま。SWELL のアイコン書式が外れるだけで、ブロックエディタで再保存しても壊れません）。"
                  "元に戻したい場合は `integrate.py` の `EXPECTED_TABLE_ICONS` まわり（2c）を外して再実行してください。\n")
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
    report.append("- 小さめ段落は `.u-fz-s{font-size:var(--swl-fz--small)!important}`（main.css）を利用。括弧は同じカード内の価格表記に合わせて全角にしています。"
                  "`akg-sublink` は seat-quiz.html の `<style>` 末尾 `.post_content .akg-sublink a{display:inline-block;box-sizing:border-box;min-height:44px;padding:.65em 0}` の受け皿で、リンクの高さを約26px→約45pxにしてタップしやすくしています（見た目はリンクの上下に少し余白が付くだけ）。\n")

    report.append("## 5. 手動で確認していただきたい点\n")
    report.append("- 本番でスマホSafariの「タップで拡大」「閉じる」が動くこと（analysis §3 の展開手順どおり、まず1枚で確認してもよい）。")
    report.append("- **投入前の権限確認（重要）**: `wp:html` 内の `<style>` `<script>` は、保存するユーザーに `unfiltered_html` 権限が無い（または wp-config.php に `DISALLOW_UNFILTERED_HTML` がある）と、エラーなしで丸ごと削除されます（診断が動かない・見た目が崩れる）。"
                  "PUT の前に同じ認証情報で `GET https://machizukuri-con.or.jp/wp-json/wp/v2/pages/1711?context=edit` を実行し、応答 JSON の `_links` に `\"wp:action-unfiltered-html\"` キーがあることを確認してください（この権限があるときだけ付きます）。無ければ管理者のアプリケーションパスワードで実行するか、投入を止めて相談してください。")
    report.append("- **投入後の一致確認**: `GET …/pages/1711?context=edit` の `content.raw` が page_1711_new.html と完全一致すること（`<script>` が1回・`<style>` が2回残っていること）。さらに公開ページのソース（表示側の HTML）で `<script>` の中身が page_1711_new.html と同じであることも確認してください"
                  "（WordPress の wptexturize 対策として、スクリプト内の比較は `i < n` ではなく `n > i` の向きで書いてあります。今後スクリプトを編集するときも、裸の `<` を書かないでください）。")
    report.append("- **GA4 の設定（コード変更は不要）**: 公開と同時に GA4 の「管理 > データの表示 > カスタム定義 > カスタムディメンションを作成」で、範囲＝イベント、イベントパラメータ名 `seat_type` `quiz_with` `quiz_priority` `quiz_area` `quiz_source` の5件を登録してください（登録前のデータはレポートで遡って見られません）。必要なら「管理 > イベント」で `seat_quiz_cta` をキーイベントにします。")
    report.append("- **赤ボタンの色（サイト全体の判断事項）**: 座席診断の予約ボタンだけは `#d40000`（白文字とのコントラスト 5.5:1、WCAG AA）にしています。席カードに追加した3つのボタンと既存のボタンはテーマの赤 `#ff0000`（4.0:1、AA 未満）のままです。"
                  "そろえたい場合は SWELL カスタマイザー（外観 > カスタマイズ > エディター設定 > ボタン）の「赤」を `#d40000` に変更してください（サイト全体の赤ボタンに影響します）。")
    report.append("- 画像の `alt`（上の表）は実画像を開いて付けましたが、席名の対応など気になる点があれば `<img alt=\"…\">` の文字だけ書き換えれば済みます。")
    report.append("- REST API で送るときは本文を必ず JSON エンコーダで包むこと（Python: `json.dumps({\"content\": text}, ensure_ascii=False)` / PowerShell: `@{content=$text} | ConvertTo-Json -Depth 3`）。"
                  "本文にはバックスラッシュを含む箇所（block6 の CSS `\\203A` は削除済みですが、非表示ブロックの `\\u0026` が4か所）があり、文字列を手組みすると 400 エラーや `&` の変化が起こります。"
                  "反映後に `GET /wp-json/wp/v2/pages/1711?context=edit` の `content.raw` を取得して page_1711_new.html と完全一致することを確認してください。")

    write_utf8(REPORT_PATH, "\n".join(report) + "\n")

    summary = {
        "all_ok": all_ok,
        "inserted_html_blocks": n_html_new,
        "fullwide_wrapper": n_fullwide_new,
        "quiz_heading": n_quiz_heading,
        "alt_set": n_alt_set,
        "alt_empty": [n_alt_empty0, n_alt_empty1],
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
