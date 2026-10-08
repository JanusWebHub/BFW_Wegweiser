exec(open('fixed.py').read().split("# ================= validation")[0])
import io,cairosvg,textwrap
from PIL import Image,ImageDraw,ImageFont
from shapely.geometry import box
lp=Image.open('lp_full.png').convert('RGB').rotate(180)
WARM={'corridor':'#e4dfd3','hall':'#ece3cf','stair':'#cfc6b6','room':'#fdfcf9','service':'#f1eee8'}
def zclass(n):
    e=zel.get('zone-'+n); return e.get('class').split()[-1] if e is not None else 'corridor'
DASH=' stroke-dasharray="3 2"'
def short(i): return i.replace('E.','').replace('exterior','ext')
def panel(name,title,b,S=6,labels=True,mark=None,extra=''):
    x0,y0,x1,y1=b; W,H=x1-x0,y1-y0; cb=box(x0-2,y0-2,x1+2,y1+2)
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {W} {H}" width="{W*S}" height="{H*S}"><style>text{{font-family:Helvetica,Arial,sans-serif;text-anchor:middle}}</style>']
    for n,g in G.items():
        if not g.intersects(cb): continue
        cr=C[n]; pts=' '.join(f'{x},{y}' for x,y in g.exterior.coords)
        o.append(f'<polygon points="{pts}" fill="{WARM.get(zclass(n),"#fdfcf9")}" fill-opacity="{.5 if cr else .12}" stroke="#8f877b" stroke-width=".45" stroke-opacity="{.9 if cr else .4}"/>')
    for n,g in G.items():
        ip=g.intersection(cb)
        if ip.is_empty or ip.area<60: continue
        rp=(ip if ip.geom_type=='Polygon' else max(ip.geoms,key=lambda q:q.area)).representative_point()
        o.append(f'<text x="{rp.x:.1f}" y="{rp.y:.1f}" font-size="3.4" fill="#2f2b27" font-weight="700" stroke="#fff" stroke-width=".9" stroke-opacity=".7">{n[2:] if n.startswith("E.") else n}</text><text x="{rp.x:.1f}" y="{rp.y:.1f}" font-size="3.4" fill="#2f2b27" font-weight="700">{n[2:] if n.startswith("E.") else n}</text>')
    for i,l in LN.items():
        pt=PT[i]['point']
        if not(x0-3<pt[0]<x1+3 and y0-3<pt[1]<y1+3): continue
        ex='exterior' in ends2(i); v=PT[i]['virtual']
        col='#b4561f' if ex else '#0d6b63'
        o.append(f'<line x1="{l[0]}" y1="{l[1]}" x2="{l[2]}" y2="{l[3]}" stroke="{col}" stroke-width="1.4"{DASH if v else ""}/><circle cx="{pt[0]}" cy="{pt[1]}" r="2" fill="{col}" stroke="#fff" stroke-width=".5"/>')
        if labels: o.append(f'<text x="{pt[0]}" y="{pt[1]-3.2}" font-size="2.5" fill="{col}" font-weight="700" stroke="#fff" stroke-width=".7" stroke-opacity=".8">{short(i)}</text><text x="{pt[0]}" y="{pt[1]-3.2}" font-size="2.5" fill="{col}" font-weight="700">{short(i)}</text>')
    o.append(extra); o.append('</svg>')
    ov=Image.open(io.BytesIO(cairosvg.svg2png(bytestring='\n'.join(o).encode()))).convert('RGBA')
    X0,Y0,X1,Y1=[int(2*(v+off)) for v,off in ((x0,40),(y0,77),(x1,40),(y1,77))]
    bg=lp.crop((X0,Y0,X1,Y1)).resize(ov.size,Image.LANCZOS).convert('RGBA'); bg.alpha_composite(ov)
    f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
    out=Image.new('RGB',(bg.width,bg.height+38),'#f6f4ef'); out.paste(bg.convert('RGB'),(0,38)); ImageDraw.Draw(out).text((10,6),title,fill='#2f2b27',font=f)
    out.save(name); print(name,out.size)
import os; os.makedirs('review/doors',exist_ok=True)
AREAS={'a-foyer-hub':('A  Foyer / E.flur-tr7-1 / E.flur-tr7-2',(855,470,1065,610)),
 'b-flur-tr7-3':('B  E.flur-tr7-3, Terrasse, TR7, E.37/E.48',(600,535,860,715)),
 'c-entrance':('C  E.52 / Wachdienst / Speisesaal east',(1060,520,1260,640)),
 'd-nw-junction':('D  Durchgang / NW wing junction / E.flur-tr7-4',(1040,240,1200,340)),
 'e-kitchen':('E  Kitchen entrance: TR8, flur-tr8-1/2, E.41',(820,780,1010,970)),
 'f-east-block':('F  East block: TR9, flur-tr9-1/2/3',(1240,455,1440,600))}
if __name__=='__main__':
    for k,(t,b) in AREAS.items(): panel(f'review/doors/{k}.png',t,b,S=6 if (b[2]-b[0])<=210 else 5)
