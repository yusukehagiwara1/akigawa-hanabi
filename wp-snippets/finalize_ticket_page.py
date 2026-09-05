# -*- coding: utf-8 -*-
"""ConoHa WING の WAF 対策の最終整形。
   out/page_1711_new.html -> out/page_1711_final.html
   (1) <style> 内の CSS コメント /* ... */ を除去(WAFがSQLコメント扱いで403にする)
   (2) <script src=...> タグを本文末尾の独立した wp:html ブロックへ移動(WAFは本文先頭付近を検査するため)
   (3) 整合性チェック: ブロック開閉、script/style 数、lightbox 数、ボタン数
"""
import re, io, os, sys, json
S = r"C:\Users\hagiy\AppData\Local\Temp\claude\C--Users-hagiy\369bb84d-a425-40de-9910-583a13db931a\scratchpad"
src = io.open(os.path.join(S, "out", "page_1711_new.html"), encoding="utf-8").read()
orig = src
# (1) strip CSS comments inside <style> blocks only
def strip_style(m):
    inner = re.sub(r"/\*.*?\*/", "", m.group(2), flags=re.S)
    inner = re.sub(r"\n{3,}", "\n\n", inner)
    return m.group(1) + inner + m.group(3)
src = re.sub(r"(<style[^>]*>)(.*?)(</style>)", strip_style, src, flags=re.S)
assert "/*" not in src, "CSS comment remains outside style?"
# (2) move script tag to the end as its own wp:html block
tags = re.findall(r"<script[^>]*src=[^>]*>\s*</script>", src)
assert len(tags) == 1, tags
tag = tags[0]
src = src.replace(tag, "").replace("\n\n\n<!-- /wp:html -->", "\n<!-- /wp:html -->")
src = re.sub(r"\n+<!-- /wp:html -->", "\n<!-- /wp:html -->", src)
src = src.rstrip("\n") + "\n\n<!-- wp:html -->\n" + tag + "\n<!-- /wp:html -->\n"
# (3) checks
opens = re.findall(r"<!-- wp:([a-z0-9\-/]+)", src); closes = re.findall(r"<!-- /wp:([a-z0-9\-/]+)", src)
from collections import Counter
co, cc = Counter(opens), Counter(closes)
# self-closing blocks (no closer) are not used here; every block should pair
bad = {k: (co[k], cc[k]) for k in set(co) | set(cc) if co[k] != cc[k]}
checks = {
    "block_pairs_ok": not bad, "bad": bad,
    "script_tags": len(re.findall(r"<script", src)),
    "style_tags": len(re.findall(r"<style", src)),
    "html_blocks": co.get("html", 0),
    "lightbox_true": src.count('"lightbox":{"enabled":true}'),
    "asoview_buttons": src.count("アソビューで予約する"),
    "css_comments": src.count("/*"),
    "chars": len(src), "bytes": len(src.encode("utf-8")),
}
io.open(os.path.join(S, "out", "page_1711_final.html"), "w", encoding="utf-8", newline="\n").write(src)
print(json.dumps(checks, ensure_ascii=False, indent=1))
assert checks["block_pairs_ok"] and checks["script_tags"] == 1 and checks["css_comments"] == 0 and checks["html_blocks"] == 3
print("OK -> out/page_1711_final.html")
