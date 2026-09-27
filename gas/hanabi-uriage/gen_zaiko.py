# -*- coding: utf-8 -*-
import io, html
SEATS=[
 ("リクライニング席（ペア）",["D"],{"アソビュー":75},"按分シートの150席＝75ペア"),
 ("SS席",["E"],{"アソビュー":45,"チケットぴあ":0,"楽天トラベル":10,"KKday":5,"JRE MALL":5},""),
 ("S席",["F"],{"アソビュー":130,"チケットぴあ":30,"楽天トラベル":10,"KKday":10,"JRE MALL":10},"按分シートは130だが座席番号は80席分のみ記載・要確認"),
 ("A席（大人＋子ども）",["G","H"],{"アソビュー":1200,"チケットぴあ":1000,"楽天トラベル":600,"KKday":600,"JRE MALL":600},""),
 ("フリーエリア",["I","J"],{"アソビュー":1000},"按分シート対象外。西多摩在住者限定1,000名で計算"),
 ("駐車場①（会場隣接）",["K"],{"アソビュー":300,"チケットぴあ":150,"楽天トラベル":100,"KKday":100,"JRE MALL":100},""),
 ("駐車場②（プール側）",["L"],{"アソビュー":200,"チケットぴあ":200,"楽天トラベル":100,"KKday":100,"JRE MALL":100},""),
]
SITES=[("アソビュー","アソビュー"),("チケットぴあ","ぴあ"),("楽天トラベル","楽天トラベル"),("KKday","KKday"),("JRE MALL","JR MALL"),("さとふる","ふるさと納税")]
FEW=0.25
NAVY="#1f3864"; ALT="#eef2f8"; BD="1px solid #b7c3d6"
grid=[[("","") for _ in range(8)] for _ in range(61)]   # (value, style)
def S(r,c,v,st=""): grid[r-1][c-1]=(v,st)
span={}  # (r,c) -> colspan

TITLE="padding:6px 8px;background:%s;color:#ffffff;font-size:16pt;font-weight:bold"%NAVY
DESC="padding:2px 8px;color:#555555;font-size:9pt"
BLK="padding:4px 8px;color:%s;font-size:12pt;font-weight:bold"%NAVY
def HD(): return "border:%s;background:%s;color:#ffffff;font-weight:bold;text-align:center;padding:4px"%(BD,NAVY)
def CELL(alt,align="left",extra=""):
    bg=("background:%s;"%ALT) if alt else "background:#ffffff;"
    return "border:%s;%stext-align:%s;padding:3px 6px;%s"%(BD,bg,align,extra)

S(1,1,"在庫数（自動計算）",TITLE); span[(1,1)]=8
S(2,1,"配分（各販売サイトへの割当）から、集計シートの販売数を引いて計算しています。集計シートを更新すれば、ここも自動で変わります。",DESC); span[(2,1)]=8
S(3,1,"配分が変わったときは、②の「配分」列だけを直してください。記号は 〇＝在庫あり ／ △＝残りわずか（そのサイトか席種全体の残りが25%以下）／ ✕＝完売 です。",DESC); span[(3,1)]=8
S(5,1,"① 席種ごと",BLK); span[(5,1)]=8
for i,h in enumerate(["席種","在庫数","販売数","残り","残率","表示","備考"]): S(6,i+1,h,HD())
for i,(name,cols,alloc,note) in enumerate(SEATS):
    r=7+i; a=(i%2==1)
    S(r,1,name,CELL(a))
    S(r,2,"=SUMIF($A$17:$A$58,$A%d,$C$17:$C$58)"%r,CELL(a,"right"))
    S(r,3,"=SUMIF($A$17:$A$58,$A%d,$D$17:$D$58)"%r,CELL(a,"right"))
    S(r,4,"=$B%d-$C%d"%(r,r),CELL(a,"right","font-weight:bold"))
    S(r,5,'=IFERROR(TEXT($D{0}/$B{0},"0%"),"")'.format(r),CELL(a,"right"))
    S(r,6,'=IFS($D{0}<=0,"✕ 完売",IFERROR($D{0}/$B{0},1)<={1},"△ 残りわずか",TRUE,"〇 空席あり")'.format(r,FEW),CELL(a,"center","font-weight:bold"))
    S(r,7,note,CELL(a,"left","font-size:8pt;color:#777777"))
S(15,1,"② 販売サイト別",BLK); span[(15,1)]=8
for i,h in enumerate(["席種","販売サイト","配分","販売数","残り","残率","記号","集計シートでの表記"]): S(16,i+1,h,HD())
r=17
for si,(name,cols,alloc,note) in enumerate(SEATS):
    for sj,(label,key) in enumerate(SITES):
        a=(si%2==1)
        top=("border-top:2px solid %s;"%NAVY) if sj==0 else ""
        S(r,1,name if sj==0 else "",CELL(a,"left",top+"font-weight:bold" if sj==0 else top))
        S(r,2,label,CELL(a,"left",top))
        S(r,3,"" if label=="さとふる" else str(alloc.get(label,0)),CELL(a,"right",top))
        m="IFERROR(MATCH($H{0},集計!$B$3:$B$8,0),MATCH($H{0},集計!$A$3:$A$8,0))".format(r)
        parts=["INDEX(集計!${0}$3:${0}$8,{1})".format(c,m) for c in cols]
        S(r,4,"=IFERROR(%s,0)"%("+".join(parts)),CELL(a,"right",top))
        S(r,5,'=IF($C{0}="","",$C{0}-$D{0})'.format(r),CELL(a,"right",top+"font-weight:bold"))
        S(r,6,'=IF(OR($C{0}="",$C{0}=0),"",IFERROR(TEXT($E{0}/$C{0},"0%"),""))'.format(r),CELL(a,"right",top))
        S(r,7,'=IFS($C{0}="","―",$C{0}=0,"―",$E{0}<=0,"✕",IFERROR($E{0}/$C{0},1)<={1},"△",IFERROR(VLOOKUP($A{2},$A$7:$D$13,4,FALSE)/VLOOKUP($A{2},$A$7:$B$13,2,FALSE),1)<={1},"△",TRUE,"〇")'.format(r,FEW,"$A$%d"%(17+si*6)),CELL(a,"center",top+"font-size:13pt;font-weight:bold"))
        S(r,8,key,CELL(a,"left",top+"font-size:8pt;color:#888888"))
        r+=1
S(60,1,"※さとふる（ふるさと納税）は座席按分シートに割当がないため、販売数だけを表示しています（①の残りには含めて計算）。",DESC); span[(60,1)]=8
S(61,1,"※配分の出どころ:「花火座席情報・座席按分」スプレッドシートの座席数按分シート。H列は集計シートと名前を照合するための列です。",DESC); span[(61,1)]=8

tsv="\n".join("\t".join(c[0] for c in row) for row in grid)
io.open('zaiko.tsv','w',encoding='utf-8',newline='').write(tsv)

out=['<meta charset="utf-8"><table style="border-collapse:collapse;font-family:Arial;font-size:10pt">']
for ri,row in enumerate(grid,1):
    out.append('<tr>')
    ci=1
    while ci<=8:
        v,st=row[ci-1]
        cs=span.get((ri,ci),1)
        out.append('<td%s style="%s">%s</td>'%((' colspan="%d"'%cs) if cs>1 else '', st, html.escape(v) if v else '&nbsp;'))
        ci+=cs
    out.append('</tr>')
out.append('</table>')
io.open('zaiko.html','w',encoding='utf-8',newline='').write("".join(out))
print('tsv',len(tsv),'html',len("".join(out)))
