# -*- coding: utf-8 -*-
import io, html
SEATS=[
 ("リクライニング席（ペア）",["D"],{"アソビュー":75}),
 ("SS席",["E"],{"アソビュー":45,"チケットぴあ":0,"楽天トラベル":10,"KKday":5,"JRE MALL":5}),
 ("S席",["F"],{"アソビュー":130,"チケットぴあ":30,"楽天トラベル":10,"KKday":10,"JRE MALL":10}),
 ("A席（大人＋子ども）",["G","H"],{"アソビュー":1200,"チケットぴあ":1000,"楽天トラベル":600,"KKday":600,"JRE MALL":600}),
 ("フリーエリア",["I","J"],{"アソビュー":1000}),
 ("駐車場①（会場隣接）",["K"],{"アソビュー":300,"チケットぴあ":150,"楽天トラベル":100,"KKday":100,"JRE MALL":100}),
 ("駐車場②（プール側）",["L"],{"アソビュー":200,"チケットぴあ":200,"楽天トラベル":100,"KKday":100,"JRE MALL":100}),
]
SITES=["アソビュー","チケットぴあ","楽天トラベル","KKday","JRE MALL","さとふる"]
FEW=0.25
ROWS=59; COLS=6
BD="1px solid #cccccc"
grid=[[("","") for _ in range(COLS)] for _ in range(ROWS)]
span={}
def S(r,c,v,st=""): grid[r-1][c-1]=(v,st)
TITLE="font-size:14pt;font-weight:bold;padding:4px 2px"
NOTE="font-size:9pt;color:#666666;padding:2px"
BLK="font-size:11pt;font-weight:bold;padding:4px 2px"
HEAD="border:%s;background:#d9d9d9;font-weight:bold;text-align:center;padding:4px"%BD
def C(align="left",extra=""): return "border:%s;background:#ffffff;text-align:%s;padding:3px 6px;%s"%(BD,align,extra)

S(1,1,"在庫数（配分 − 販売数）",TITLE); span[(1,1)]=COLS
S(2,1,"集計シートを更新すると自動で変わります。配分を変えるときは②の「配分」列を直してください。",NOTE); span[(2,1)]=COLS
S(4,1,"① 席種ごと",BLK); span[(4,1)]=COLS
for i,h in enumerate(["席種","在庫","販売","残り","状況"]): S(5,i+1,h,HEAD)
for i,(name,cols,alloc) in enumerate(SEATS):
    r=6+i
    S(r,1,name,C())
    S(r,2,"=SUMIF($A$16:$A$57,$A%d,$C$16:$C$57)"%r,C("right"))
    S(r,3,"=SUMIF($A$16:$A$57,$A%d,$D$16:$D$57)"%r,C("right"))
    S(r,4,"=$B%d-$C%d"%(r,r),C("right","font-weight:bold"))
    S(r,5,'=IFS($D{0}<=0,"🔴 完売",IFERROR($D{0}/$B{0},1)<={1},"🟡 残りわずか",TRUE,"🟢 空席あり")'.format(r,FEW),C("center","font-weight:bold"))
S(14,1,"② 販売サイト別",BLK); span[(14,1)]=COLS
for i,h in enumerate(["席種","販売サイト","配分","販売","残り","記号"]): S(15,i+1,h,HEAD)
r=16
for si,(name,cols,alloc) in enumerate(SEATS):
    for sj,site in enumerate(SITES):
        top=("border-top:2px solid #999999;") if sj==0 else ""
        S(r,1,name,C("left",top+("" if sj==0 else "color:#999999;")))
        S(r,2,site,C("left",top))
        S(r,3,"" if site=="さとふる" else str(alloc.get(site,0)),C("right",top))
        key='SWITCH($B{0},"チケットぴあ","ぴあ","JRE MALL","JR MALL","さとふる","ふるさと納税",$B{0})'.format(r)
        m="IFERROR(MATCH({1},集計!$B$3:$B$8,0),MATCH({1},集計!$A$3:$A$8,0))".format(r,key)
        parts=["INDEX(集計!${0}$3:${0}$8,{1})".format(c,m) for c in cols]
        S(r,4,"=IFERROR(%s,0)"%("+".join(parts)),C("right",top))
        S(r,5,'=IF($C{0}="","",$C{0}-$D{0})'.format(r),C("right",top+"font-weight:bold"))
        S(r,6,'=IFS($C{0}="","―",$C{0}=0,"―",$E{0}<=0,"🔴",IFERROR($E{0}/$C{0},1)<={1},"🟡",IFERROR(VLOOKUP($A{0},$A$6:$D$12,4,FALSE)/VLOOKUP($A{0},$A$6:$B$12,2,FALSE),1)<={1},"🟡",TRUE,"🟢")'.format(r,FEW),C("center",top+"font-size:12pt;font-weight:bold"))
        r+=1
S(59,1,"※さとふるは按分の割当がないため販売数のみ。S席アソビューの配分130は座席番号の記載が80席分のみで要確認。",NOTE); span[(59,1)]=COLS

tsv="\n".join("\t".join(c[0] for c in row) for row in grid)
io.open('zaiko.tsv','w',encoding='utf-8',newline='').write(tsv)
out=['<meta charset="utf-8"><table style="border-collapse:collapse;font-family:Arial;font-size:10pt">']
for ri,row in enumerate(grid,1):
    out.append('<tr>'); ci=1
    while ci<=COLS:
        v,st=row[ci-1]; cs=span.get((ri,ci),1)
        out.append('<td%s style="%s">%s</td>'%((' colspan="%d"'%cs) if cs>1 else '',st,html.escape(v)))
        ci+=cs
    out.append('</tr>')
out.append('</table>')
io.open('zaiko.html','w',encoding='utf-8',newline='').write("".join(out))
print('ok tsv',len(tsv),'html',len("".join(out)))
