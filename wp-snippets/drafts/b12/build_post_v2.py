# -*- coding: utf-8 -*-
"""⑫ 第8回の音楽紹介 お知らせ記事 v2（見た目を強化: 写真・プログラム風カード・動画・ボタン）
出力: post.v2.html（WordPress ブロック記法）。<script と /* は使わない（WAF）。<td> も使わない。"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
UP = "https://machizukuri-con.or.jp/wp-content/uploads/"

PARTS = [
    dict(tag="開演前", emoji="🎼", name="overture（開演前）", colors=[], amount="",
         songs=[("「VIVANT」オリジナル・サウンドトラック", "千住 明")],
         note="花火が始まる前の時間に流れる、ドラマ『VIVANT』の音楽です。"),
    dict(tag="1", emoji="🎇", name="オープニング", colors=["colorful"], amount="花火の数：多め",
         songs=[("Zoo", "Shakira（シャキーラ）")],
         note="映画『ズートピア2』の楽曲で幕開け。色とりどりの花火を数多く打ち上げる予定です。"),
    dict(tag="2", emoji="🎤", name="ヒットチャート", colors=["#ff6fae", "#ff9a3c", "#e53935"], amount="花火の数：多め",
         songs=[("爆裂愛してる", "M!LK"), ("風と町", "Mrs. GREEN APPLE"), ("見知らぬ糸", "スピッツ")],
         note="いま話題の3曲。ピンク・オレンジ・赤を基調にした花火を予定しています。"),
    dict(tag="3", emoji="🌸", name="My花火（前半）", colors=[], amount="",
         songs=[("HANABI", "Mr.Children")],
         note="Mr.Children「HANABI」に合わせて打ち上げます。"),
    dict(tag="4", emoji="🎶", name="懐メロ", colors=["#e53935"], amount="",
         songs=[("LOVE SONG", "CHAGE and ASKA"), ("メロディー", "玉置浩二")],
         note="幅広い世代に親しまれてきた2曲。赤を基調にした花火を予定しています。"),
    dict(tag="5", emoji="💫", name="My花火（中半）", colors=[], amount="",
         songs=[("Forever Love", "X JAPAN"), ("それを愛と呼ぶなら", "Uru"), ("月光", "鬼束ちひろ"),
                ("Always Remember Us This Way", "Lady Gaga（レディー・ガガ）"), ("I Will Always Love You", "Whitney Houston（ホイットニー・ヒューストン）")],
         note="静かに始まり、名曲のバラードが続くパートです。"),
    dict(tag="6", emoji="🎆", name="エンディング", colors=["colorful"], amount="花火の数：多め",
         songs=[("Jupiter", "平原綾香")],
         note="平原綾香「Jupiter」で締めくくり。オープニングと同じく、色とりどりの花火を数多く打ち上げる予定です。"),
]

CSS = """
.akg-music,.akg-music *{box-sizing:border-box}
.akg-music{margin:0 0 2em;padding:1.25em 1em 1em;border-radius:14px;background:linear-gradient(180deg,#0b1a3a 0%,#14264f 60%,#1d2f5c 100%);color:#fff;font-size:1rem;line-height:1.6}
.akg-music__head{margin:0 0 .25em;font-size:1.05em;font-weight:700;letter-spacing:.05em;color:#ffd166}
.akg-music__lead{margin:0 0 1em;font-size:.9em;color:#dbe4ff}
.akg-music__part{position:relative;margin:0 0 .75em;padding:.9em .9em .8em 1em;border-radius:10px;background:rgba(255,255,255,.07);border-left:5px solid #ffd166}
.akg-music__part:last-child{margin-bottom:0}
.akg-music__ttl{display:flex;flex-wrap:wrap;align-items:center;gap:.4em .6em;margin:0 0 .4em;font-weight:700;font-size:1.05em}
.akg-music__no{display:inline-block;min-width:1.9em;padding:.05em .45em;border-radius:999px;background:#ffd166;color:#0b1a3a;font-size:.8em;text-align:center}
.akg-music__meta{display:flex;flex-wrap:wrap;align-items:center;gap:.35em;margin:0 0 .45em;font-size:.8em;color:#dbe4ff}
.akg-music__dot{display:inline-block;width:.9em;height:.9em;border-radius:50%;border:1px solid rgba(255,255,255,.5)}
.akg-music__dot--colorful{background:conic-gradient(#ff6fae,#ffd166,#4dd0e1,#a5d6a7,#ff9a3c,#ff6fae)}
.akg-music__songs{list-style:none;margin:0 0 .35em;padding:0}
.akg-music__songs li{margin:0 0 .25em;padding-left:1.1em;text-indent:-1.1em}
.akg-music__songs li:before{content:"♪";display:inline-block;width:1.1em;text-indent:0;color:#ffd166}
.akg-music__song{font-weight:700}
.akg-music__artist{margin-left:.4em;font-size:.9em;color:#dbe4ff}
.akg-music__note{margin:0;font-size:.88em;color:#eef2ff}
.akg-music__foot{margin:1em 0 0;font-size:.8em;color:#dbe4ff}
@media (min-width:600px){.akg-music{padding:1.5em 1.5em 1.25em}.akg-music__part{padding:1em 1.1em .9em 1.2em}}
""".strip()

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def part_html(p):
    dots = ""
    for c in p["colors"]:
        if c == "colorful":
            dots += '<span class="akg-music__dot akg-music__dot--colorful" aria-label="色とりどり"></span>'
        else:
            dots += '<span class="akg-music__dot" style="background:%s"></span>' % c
    meta = ""
    if p["colors"] or p["amount"]:
        bits = []
        if p["colors"]:
            bits.append("花火の色：" + dots)
        if p["amount"]:
            bits.append(p["amount"])
        meta = '<p class="akg-music__meta">' + "　".join(bits) + "</p>"
    songs = "".join('<li><span class="akg-music__song">%s</span><span class="akg-music__artist">%s</span></li>' % (esc(s), esc(a)) for s, a in p["songs"])
    return ('<div class="akg-music__part">'
            '<p class="akg-music__ttl"><span class="akg-music__no">%s</span><span>%s %s</span></p>%s'
            '<ul class="akg-music__songs">%s</ul>'
            '<p class="akg-music__note">%s</p></div>') % (esc(p["tag"]), p["emoji"], esc(p["name"]), meta, songs, esc(p["note"]))

program = ('<div class="akg-music"><p class="akg-music__head">第8回 音楽プログラム（予定）</p>'
           '<p class="akg-music__lead">2026年9月13日時点の予定です。曲目・順番は変更になる場合があります。</p>'
           + "".join(part_html(p) for p in PARTS) +
           '<p class="akg-music__foot">花火は18:00〜19:00頃（約1時間・5,000発予定）。花火の色や量は演出の目安です。</p></div>')

blocks = []
def para(text, cls=None):
    attr = ' {"className":"%s"}' % cls if cls else ""
    c = ' class="%s"' % cls if cls else ""
    blocks.append("<!-- wp:paragraph%s -->\n<p%s>%s</p>\n<!-- /wp:paragraph -->" % (attr, c, text))
def h2(text):
    blocks.append('<!-- wp:heading -->\n<h2 class="wp-block-heading">%s</h2>\n<!-- /wp:heading -->' % text)

para("第8回秋川流域花火大会（2026年11月14日・土）で、花火とともに流れる予定の楽曲をパートごとにご紹介します。曲目は2026年9月13日時点の予定です。")
blocks.append('<!-- wp:image {"sizeSlug":"large","linkDestination":"none"} -->\n<figure class="wp-block-image size-large"><img src="%s花火_高画質-1024x576.jpg" alt="夜空いっぱいに広がる打ち上げ花火（秋川流域花火大会）"/></figure>\n<!-- /wp:image -->' % UP)
h2("音楽に合わせて打ち上がる、約1時間の花火")
para("花火は18時から19時頃まで、約1時間で5,000発を打ち上げる予定です。第7回（2025年）に続き、第8回（2026年）も音楽に合わせて花火が打ち上がります。")
para("開演前の音楽から、オープニング、ヒットチャート、My花火、懐メロ、エンディングまで、パートごとに楽曲が組まれています。映画『ズートピア2』の「Zoo」で幕を開け、平原綾香「Jupiter」で締めくくる予定です。")
h2("第8回のプログラム")
blocks.append("<!-- wp:html -->\n<style>\n%s\n</style>\n%s\n<!-- /wp:html -->" % (CSS, program))
h2("昨年（第7回）の花火を動画で見る")
para("音楽に合わせて打ち上がる第7回（2025年）の花火を、定点カメラで通して収録した映像です（YouTube・約1時間、再生すると音が出ます）。")
blocks.append('<!-- wp:embed {"url":"https://www.youtube.com/watch?v=RCETodLcJTA","type":"video","providerNameSlug":"youtube","responsive":true,"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"} -->\n<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper">\nhttps://www.youtube.com/watch?v=RCETodLcJTA\n</div></figure>\n<!-- /wp:embed -->')
h2("観覧にはチケットが必要です")
para("観覧席はすべて指定席で、当日券はありません。席の種類と購入方法は、チケット情報のページをご覧ください。")
blocks.append('<!-- wp:loos/button {"hrefUrl":"https://machizukuri-con.or.jp/ticket/","btnAlign":"left","color":"red","className":"is-style-btn_normal"} -->\n<div class="swell-block-button red_ is-style-btn_normal" data-align="left"><a href="https://machizukuri-con.or.jp/ticket/" class="swell-block-button__link"><span><strong>チケット情報を見る</strong></span></a></div>\n<!-- /wp:loos/button -->')
para('第7回（2025年）の曲目は、お知らせ「<a href="https://machizukuri-con.or.jp/news/3723/">第7回大会の音楽紹介</a>」をご覧ください。')

out = "\n\n".join(blocks) + "\n"
assert "<script" not in out and "/*" not in out and "<td" not in out
open(os.path.join(HERE, "post.v2.html"), "w", encoding="utf-8", newline="\n").write(out)
print("written", len(out))
