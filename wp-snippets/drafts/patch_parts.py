"""patch_parts.py — 部品ファイル(b12/section, b13/embed-*)を差し込み先の「コピー」に適用し、check_blocks.py で検証する。
原本(out/b3, out/b5, out/b11, out/b12)は変更しない。出力は out/_patched/。

使い方(S = scratchpad フォルダ):
  python S/patch_parts.py                      # 記事URL未確定の状態で b3/b5 に部品を差し込み、模擬トップページで embed-top を試す
  python S/patch_parts.py --net                # 上記 + URL の接続確認
  python S/patch_parts.py --news-url https://machizukuri-con.or.jp/news/NNNN/      # ⑫記事公開後: b3(部品内リンク)・b5(楽曲の一文)・b11(お知らせリンク)を記事URLへ
  python S/patch_parts.py --hanabishi-url https://machizukuri-con.or.jp/hanabishi/ # ⑪公開後: b12/post 末尾に案内を追加、b5 に花火師リンクを追加
  python S/patch_parts.py --top-raw page7.raw.html   # 本番トップ(page 7)の content.raw を保存したファイルに embed-top を差し込む → out/_patched/top_content.patched.html

アンカーが 1 件でなければ中断する(差し込み先が変わっている合図)。
"""
import argparse, io, json, os, subprocess, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
S = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(S, "out")
P = os.path.join(OUT, "_patched")
os.makedirs(P, exist_ok=True)


def rd(rel):
    return open(os.path.join(OUT, rel), encoding="utf-8").read()


def wr(name, t):
    path = os.path.join(P, name)
    open(path, "w", encoding="utf-8", newline="\n").write(t)
    return path


def replace_once(t, old, new, label):
    n = t.count(old)
    if n != 1:
        raise SystemExit(f"[{label}] アンカーが {n} 件です(1 件であること): {old[:70]!r}")
    return t.replace(old, new)


STYLE_HDR = (
    "<!-- wp:html -->\n<style>\n"
    ".akg-todo{background:#fff6cc;border:2px dashed #d9a400;padding:.75em 1em;border-radius:6px}\n"
    "</style>\n<!-- /wp:html -->\n\n"
)

# ---- アンカー(差し込み先の実際の文字列) ----
B3_PARA = (
    "<!-- wp:paragraph -->\n"
    "<p>花火は18時から19時頃まで、約1時間で5,000発を打ち上げる予定です。音楽に合わせて打ち上がる演出が特徴で、"
    "第7回（2025年）は米津玄師「IRIS OUT」に合わせたオープニングと、映画音楽に合わせたパートが予告されました。"
    "第8回の楽曲は、決まり次第お知らせします。</p>\n"
    "<!-- /wp:paragraph -->"
)
B3_TODO = (
    '<!-- wp:paragraph {"className":"akg-todo"} -->\n'
    '<p class="akg-todo">【委員会確認】ここに第8回の花火演出の見どころ（楽曲・構成など）が入ります。確定後に差し替えます。</p>\n'
    "<!-- /wp:paragraph -->"
)
B3_H3_MEDIA = '<!-- wp:heading {"level":3} -->\n<h3 class="wp-block-heading">メディアでも紹介されました</h3>'
B5_H3_MUSIC = '<!-- wp:heading {"level":3} -->\n<h3 class="wp-block-heading">音楽とシンクロする花火</h3>'
B5_MUSIC_SENT = "第8回（2026年）の楽曲は未定です。</p>"
B11_NEWS_LINK = '<a href="https://machizukuri-con.or.jp/categry/news/">お知らせ</a>でご紹介します。</p>'
B12_SEC_LINK = 'href="https://machizukuri-con.or.jp/categry/news/"'
B12_POST_LAST = "第7回大会の音楽紹介</a>」をご覧ください。</p>\n<!-- /wp:paragraph -->"
TOP_VIDEO_SRC = "ショートムービー.mp4"
TOP_VIDEO_END = "<!-- /wp:video -->"

MOCK_TOP_RAW = (
    '<!-- wp:loos/full-wide {"bgColor":"#ffffff","contentSize":"container","pcPadding":"20","spPadding":"20"} -->\n'
    '<div class="swell-block-fullWide pc-py-20 sp-py-20 alignfull" style="background-color:#ffffff">'
    '<div class="swell-block-fullWide__inner l-container"><!-- wp:heading {"className":"is-style-section_ttl"} -->\n'
    '<h2 class="wp-block-heading is-style-section_ttl"><span class="swl-fz u-fz-xl">ギャラリー</span></h2>\n'
    "<!-- /wp:heading -->\n\n"
    '<!-- wp:heading {"level":4} -->\n<h4 class="wp-block-heading">第7回秋川流域花火大会ドキュメント</h4>\n<!-- /wp:heading -->\n\n'
    "<!-- wp:paragraph -->\n<p>準備、当日の様子に加え、花火大会に向けた私たちの想いを動画にしました。ぜひご覧ください。</p>\n<!-- /wp:paragraph -->\n\n"
    '<!-- wp:video {"id":0} -->\n'
    '<figure class="wp-block-video"><video controls src="https://machizukuri-con.or.jp/wp-content/uploads/第7回秋川流域花火大会-ショートムービー.mp4"></video></figure>\n'
    "<!-- /wp:video --></div></div>\n"
    "<!-- /wp:loos/full-wide -->\n"
)


def patch_b3(news_url):
    t = rd("b3/content.html")
    sec = rd("b12/section.html")
    if sec.startswith(STYLE_HDR):  # b3 には .akg-todo の定義が既にあるので部品先頭の style は省く
        sec = sec[len(STYLE_HDR):]
    sec = sec.strip("\n")
    if news_url:
        sec = replace_once(sec, B12_SEC_LINK, f'href="{news_url}"', "b12/section 記事リンク")
    t = replace_once(t, B3_PARA, sec, "b3 楽曲段落 → b12/section")
    todo_full = B3_TODO + "\n\n"
    t = replace_once(t, todo_full if t.count(todo_full) == 1 else B3_TODO, "", "b3 見どころ枠の削除")
    enjoy = rd("b13/embed-enjoy.html").strip("\n")
    t = replace_once(t, B3_H3_MEDIA, enjoy + "\n\n" + B3_H3_MEDIA, "b3 embed-enjoy 挿入")
    return wr("b3_content.patched.html", t)


def patch_b5(news_url, hanabishi_url):
    t = rd("b5/content.html")
    more = rd("b13/embed-more.html").strip("\n")
    t = replace_once(t, B5_H3_MUSIC, more + "\n\n" + B5_H3_MUSIC, "b5 embed-more 挿入")
    sent = B5_MUSIC_SENT
    if news_url:
        new = (
            f'第8回（2026年）の楽曲は、お知らせ「<a href="{news_url}">第8回大会の音楽紹介</a>」でご紹介しています'
            "（2026年9月13日時点の予定です）。</p>"
        )
        t = replace_once(t, sent, new, "b5 楽曲の一文")
        sent = new
    if hanabishi_url:
        new = sent[:-4] + f'花火を打ち上げる<a href="{hanabishi_url}">花火師のご紹介</a>もご覧ください。</p>'
        t = replace_once(t, sent, new, "b5 花火師リンク")
    return wr("b5_content.patched.html", t)


def patch_b11(news_url):
    t = rd("b11/content.html")
    t = replace_once(
        t, B11_NEWS_LINK, f'お知らせ「<a href="{news_url}">第8回大会の音楽紹介</a>」でご紹介しています。</p>', "b11 お知らせリンク"
    )
    return wr("b11_content.patched.html", t)


def patch_b12_post(hanabishi_url):
    t = rd("b12/post.html")
    add = (
        "\n\n<!-- wp:paragraph -->\n"
        f'<p>花火を打ち上げる花火師については、「<a href="{hanabishi_url}">花火を打ち上げる花火師（株式会社ホソヤエンタープライズ）</a>」のページをご覧ください。</p>\n'
        "<!-- /wp:paragraph -->"
    )
    t = replace_once(t, B12_POST_LAST, B12_POST_LAST + add, "b12/post 末尾に⑪の案内")
    return wr("b12_post.patched.html", t)


def patch_top(raw, name):
    top = rd("b13/embed-top.html").strip("\n")
    i = raw.find(TOP_VIDEO_SRC)
    if i < 0:
        raise SystemExit("トップ: ショートムービーの wp:video が見つかりません")
    j = raw.find(TOP_VIDEO_END, i)
    if j < 0:
        raise SystemExit("トップ: <!-- /wp:video --> が見つかりません(content.raw ではなく rendered を渡していませんか)")
    k = j + len(TOP_VIDEO_END)
    if raw.count(TOP_VIDEO_SRC) != 1:
        raise SystemExit("トップ: ショートムービーの参照が複数あります")
    return wr(name, raw[:k] + "\n\n" + top + raw[k:])


def check(path, net):
    cmd = [sys.executable, os.path.join(S, "check_blocks.py"), path] + (["--net"] if net else [])
    r = subprocess.run(cmd, capture_output=True)
    d = json.loads(r.stdout.decode("utf-8", "replace"))
    print(f"  {os.path.basename(path)}: ok={d['ok']} errors={d['errors']} warnings={d['warnings']} "
          f"blocks={d['info'].get('block_count')} todo={d['info'].get('todo_count')}")
    return d["ok"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--news-url")
    ap.add_argument("--hanabishi-url")
    ap.add_argument("--top-raw")
    ap.add_argument("--net", action="store_true")
    a = ap.parse_args()
    outs = [patch_b3(a.news_url), patch_b5(a.news_url, a.hanabishi_url)]
    if a.news_url:
        outs.append(patch_b11(a.news_url))
    if a.hanabishi_url:
        outs.append(patch_b12_post(a.hanabishi_url))
    if a.top_raw:
        outs.append(patch_top(open(a.top_raw, encoding="utf-8").read(), "top_content.patched.html"))
    else:
        outs.append(patch_top(MOCK_TOP_RAW, "top_mock.patched.html"))
    print("出力:", P)
    ok = all([check(p, a.net) for p in outs])
    print("RESULT:", "OK" if ok else "NG")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
