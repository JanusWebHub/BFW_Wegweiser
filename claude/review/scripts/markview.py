import json,glob,sys
exec(open('doors.py').read().split("import os; os.makedirs")[0])
M=[]
for f in glob.glob('marks/marks/*.json'):
    d=json.load(open(f)); m=d.get('data',d); m['id']=d.get('id',f.split('/')[-1][:-5])
    if not m.get('applied'): M.append(m)
M.sort(key=lambda m:m.get('at',0))
def marksvg(S):
    s=1/S; o=[]
    for n,m in enumerate(M,1):
        k=m['kind']; col='#d62f1f'; pts=m.get('pts',[])
        if k=='move' and m['target'] in LN:
            g=LN[m['target']]; o.append(f'<line x1="{g[0]}" y1="{g[1]}" x2="{g[2]}" y2="{g[3]}" stroke="#6b645a" stroke-width="{1.2*s}" stroke-dasharray="{3*s} {2*s}"/>')
            o.append(f'<line x1="{pts[0][0]}" y1="{pts[0][1]}" x2="{pts[1][0]}" y2="{pts[1][1]}" stroke="{col}" stroke-width="{2.4*s}"/><circle cx="{(pts[0][0]+pts[1][0])/2}" cy="{(pts[0][1]+pts[1][1])/2}" r="{3*s}" fill="{col}"/>')
        elif k=='add':
            o.append(f'<line x1="{pts[0][0]}" y1="{pts[0][1]}" x2="{pts[1][0]}" y2="{pts[1][1]}" stroke="#c07a00" stroke-width="{2.6*s}"/><circle cx="{(pts[0][0]+pts[1][0])/2}" cy="{(pts[0][1]+pts[1][1])/2}" r="{3.4*s}" fill="#c07a00"/>')
            if m.get('text'): o.append(f'<text x="{pts[0][0]}" y="{pts[0][1]-4*s}" font-size="{9*s}" fill="#c07a00" font-weight="700">{m["text"][:30]}</text>')
        elif k=='zone':
            pp=' '.join(f'{x},{y}' for x,y in pts); o.append(f'<polygon points="{pp}" fill="#1f5fd6" fill-opacity=".10" stroke="#1f5fd6" stroke-width="{1.8*s}" stroke-dasharray="{5*s} {3*s}"/>')
            cx=sum(p[0] for p in pts)/len(pts); cy=sum(p[1] for p in pts)/len(pts)
            o.append(f'<text x="{cx}" y="{cy}" font-size="{8.5*s}" text-anchor="middle" fill="#1f5fd6" font-weight="700" stroke="#fff" stroke-width="{2*s}" stroke-opacity=".8" paint-order="stroke">{m.get("text","")[:26]}</text>')
        elif k=='remove':
            t=m['target']
            if t in LN:
                g=LN[t]; cx,cy=(g[0]+g[2])/2,(g[1]+g[3])/2; r=5*s
                o.append(f'<path d="M{cx-r} {cy-r}L{cx+r} {cy+r}M{cx+r} {cy-r}L{cx-r} {cy+r}" stroke="{col}" stroke-width="{2.4*s}"/>')
    return ''.join(o)
def mp(name,title,b,S):
    panel(name,title,b,S=S,labels=False,extra=marksvg(S))
if __name__=='__main__':
    mp('review/doors/m-hub.png','Hub: marks',(790,465,1070,612),4.3)
    mp('review/doors/m-wc.png','WC block: marks',(880,545,1110,610),5.4)
    mp('review/doors/m-e52.png','E.52: marks',(1085,515,1260,665),6)
    mp('review/doors/m-kitchen.png','Kitchen: marks',(870,800,1235,968),3.3)
    mp('review/doors/m-lift.png','TR7 lift / E.48 / E.49: marks',(715,610,830,730),8)
