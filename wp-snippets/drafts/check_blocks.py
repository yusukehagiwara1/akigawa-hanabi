"""WordPress ブロック本文の機械チェック。
使い方: python check_blocks.py <content.html> [--net]
  --net を付けると本文中の URL/画像に HEAD リクエストして 200 か確認する。
結果は JSON で標準出力。errors が空なら合格。warnings は目視判断。
"""
import sys, re, json, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

path = sys.argv[1]
net = "--net" in sys.argv
t = open(path, encoding="utf-8").read()
errors, warnings, info = [], [], {}

# 1. WAF
if "<script" in t.lower():
    errors.append("WAF: '<script' が本文にあります(禁止)")
if "/*" in t:
    errors.append("WAF: CSSコメント '/*' が本文にあります(禁止)")

# 1b. wp:embed(CONTEXT_C §C で許可)の中身は URL の生テキストのみ。iframe は禁止
for m in re.finditer(r"<!--\s*wp:embed.*?<!--\s*/wp:embed\s*-->", t, flags=re.S):
    if "<iframe" in m.group(0).lower():
        errors.append("wp:embed の中に <iframe> があります(URL の生テキストのみにする)")

# 2. ブロックコメントの対応
ALLOWED = {"heading","paragraph","list","list-item","image","columns","column","table","separator","spacer","group","video","shortcode","html","embed",
           "loos/full-wide","loos/columns","loos/column","loos/step","loos/step-item","loos/button","loos/banner-link"}
stack = []
blocks = []
for m in re.finditer(r"<!--\s*(/?)wp:([a-z0-9/-]+)(\s+(\{.*?\}))?\s*(/?)-->", t, flags=re.S):
    closing, name, _, attrs, selfclose = m.groups()
    if name not in ALLOWED:
        errors.append(f"許可外のブロック: wp:{name}")
    if attrs:
        try:
            a = json.loads(attrs)
        except Exception as e:
            errors.append(f"wp:{name} の属性JSONが不正: {attrs[:80]}… ({e})")
            a = {}
    else:
        a = {}
    if closing:
        if not stack or stack[-1][0] != name:
            errors.append(f"閉じタグの不一致: /wp:{name} (直前の開き: {stack[-1][0] if stack else 'なし'}) @{m.start()}")
            if stack: stack.pop()
        else:
            stack.pop()
    elif selfclose:
        blocks.append((name, a, m.start()))
    else:
        stack.append((name, m.start()))
        blocks.append((name, a, m.start()))
if stack:
    errors.append("閉じられていないブロック: " + ", ".join(f"wp:{n}" for n, _ in stack))
info["block_count"] = len(blocks)
info["block_types"] = sorted({b[0] for b in blocks})

# 3. heading level と h タグ
for name, a, pos in blocks:
    if name == "heading":
        lvl = a.get("level", 2)
        seg = t[pos:pos+400]
        if not re.search(rf"<h{lvl}\b", seg):
            errors.append(f"wp:heading level={lvl} に <h{lvl}> が続いていません @{pos}")
        if lvl == 1:
            errors.append(f"h1 は使わない(ページタイトルが h1) @{pos}")

# 4. 画像 alt
for m in re.finditer(r"<img\b[^>]*>", t):
    tag = m.group(0)
    alt = re.search(r'alt="([^"]*)"', tag)
    if not alt or not alt.group(1).strip():
        errors.append(f"alt の無い画像: {tag[:120]}")
    src = re.search(r'src="([^"]*)"', tag)
    if src and not src.group(1).startswith("https://machizukuri-con.or.jp/wp-content/uploads/"):
        errors.append(f"既存アップロード以外の画像: {src.group(1)}")

# 5. 外部リンク target/rel
for m in re.finditer(r"<a\b[^>]*href=\"(https?://[^\"]+)\"[^>]*>", t):
    tag = m.group(0); href = m.group(1)
    if "machizukuri-con.or.jp" not in href:
        if 'target="_blank"' not in tag or "noopener" not in tag:
            warnings.append(f"外部リンクに target=_blank/rel=noopener がありません: {href}")

# 6. CSS スコープ
for sm in re.finditer(r"<style[^>]*>(.*?)</style>", t, flags=re.S):
    css = sm.group(1)
    body = re.sub(r"@media[^{]*\{", "", css)
    for rule in re.finditer(r"([^{}]+)\{[^{}]*\}", body):
        sel = rule.group(1).strip()
        if not sel or sel.startswith("@"):
            continue
        parts = [p.strip() for p in sel.split(",")]
        for p in parts:
            if p and ".akg-" not in p:
                errors.append(f"接頭辞 .akg- でスコープされていないセレクタ: '{p}'")
    if "!important" in css:
        warnings.append(f"!important が {css.count('!important')} 回使われています")

# 7. 固定幅
for m in re.finditer(r"(?<![-(])\bwidth\s*:\s*(\d{3,})px", t):
    if int(m.group(1)) > 320 and "@media" not in t[max(0, m.start()-30):m.start()]:
        warnings.append(f"固定幅 {m.group(1)}px があります(320px端末で要確認): …{t[max(0,m.start()-40):m.end()]}")

# 8. akg-todo の定義
if "akg-todo" in t and ".akg-todo{" not in t.replace(" ", "") :
    errors.append(".akg-todo を使っていますが <style> に定義がありません")
info["todo_count"] = t.count('class="akg-todo"')

# 9. 先頭ブロックが段落か
first = re.search(r"<!--\s*wp:([a-z0-9/-]+)", t)
info["first_block"] = first.group(1) if first else None

# 10. URL チェック
urls = sorted(set(re.findall(r'(?:href|src)="(https?://[^"]+)"', t)))
info["url_count"] = len(urls)
if net:
    import urllib.request, urllib.parse
    bad = []
    for u in urls:
        try:
            q = urllib.parse.quote(u, safe=":/?&=%#+,;@!$'()*[]~")
            req = urllib.request.Request(q, method="HEAD", headers={"User-Agent": "Mozilla/5.0 (check)"})
            with urllib.request.urlopen(req, timeout=15) as r:
                code = r.status
        except Exception as e:
            code = getattr(e, "code", None) or str(e)
            if code == 405 or code == 403:
                try:
                    req = urllib.request.Request(q, method="GET", headers={"User-Agent": "Mozilla/5.0 (check)"})
                    with urllib.request.urlopen(req, timeout=20) as r:
                        code = r.status
                except Exception as e2:
                    code = getattr(e2, "code", None) or str(e2)
        if code != 200:
            bad.append({"url": u, "status": code})
    info["url_bad"] = bad
    for b in bad:
        if "machizukuri-con.or.jp" in b["url"]:
            errors.append(f"サイト内URLが200ではありません: {b['url']} → {b['status']}")
        else:
            warnings.append(f"外部URLが200ではありません: {b['url']} → {b['status']}")

info["chars"] = len(t)
print(json.dumps({"file": path, "ok": not errors, "errors": errors, "warnings": warnings, "info": info}, ensure_ascii=False, indent=1))
