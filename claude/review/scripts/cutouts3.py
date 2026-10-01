import sys,re,io,math;sys.path.insert(0,'.')
exec(open('graph.py').read().split("# components of crossable graph")[0])
import cairosvg
from PIL import Image,ImageDraw,ImageFont
from shapely.geometry import box
lp=Image.open('lp_full.png').convert('RGB').rotate(180)   # 3507x2480 = 2 px per half-px
WARM={'corridor':'#e4dfd3','hall':'#ece3cf','stair':'#cfc6b6','room':'#fdfcf9','service':'#f1eee8'}
S=7   # output px per SVG unit
# proposed portals: id -> (point, line, kind)
def seg_on(a,b,half=None):
    g=Z[a].boundary.intersection(Z[b].boundary)
    return g
def unit(p,q):
    d=math.dist(p,q); return ((q[0]-p[0])/d,(q[1]-p[1])/d)
prop={}
# 1 fire door
p0,p1=(610,545),(622,594); u=unit(p0,p1); m=(616,569.5)
prop['E.flur-tr2-1_E.flur-tr7-3']=dict(pt=m,line=[(m[0]-11*u[0],m[1]-11*u[1]),(m[0]+11*u[0],m[1]+11*u[1])],note='fire door; width to read')
prop['E.flur-tr2-3_E.flur-tr2-4']=dict(pt=(450,564.5),line=[(450,556),(450,573)],note='double door')
prop['E.flur-tr7-1_E.flur-tr9-3']=dict(pt=(1050,504),line=[(1050,493),(1050,515)],note='double door at x~1050')
# candidates: shared boundary shown, point to be read
def shared(a,b):
    g=Z[a].buffer(0.05).boundary.intersection(Z[b].buffer(0.05).boundary) if False else Z[a].boundary.intersection(Z[b].boundary)
    return g
cand={}
for a,b in [('E.TR2','E.flur-tr2-4'),('E.TR2','E.flur-tr3-1')]:
    g=shared(a,b); print(a,b,g.wkt[:150])
    cand['%s_%s'%tuple(sorted((a,b)))]=g
# E.53.1 / E.flur-tr5-2: use clipped boundary
g=Z['E.53.1'].boundary.intersection(Z['E.flur-tr5-2'].buffer(0.8)); print('53.1/tr5-2',g.wkt[:200], g.length)
cand['E.53.1_E.flur-tr5-2']=g
EXCL=set();SKIP=set();EXTRA=[];PROP={};CAND={}
def build_svg(cx0,cy0,cx1,cy1,hl_zones=(),show=()):
    W,H=cx1-cx0,cy1-cy0
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{cx0} {cy0} {W} {H}" width="{W*S}" height="{H*S}">']
    o.append('<style>text{font-family:Helvetica,Arial,sans-serif;text-anchor:middle}</style>')
    cb=box(cx0-1,cy0-1,cx1+1,cy1+1)
    for n,g in Z.items():
        if not g.intersects(cb): continue
        cls=zel[f'zone-{n}'].get('class').split()[-1]
        pts=' '.join(f'{x},{y}' for x,y in g.exterior.coords)
        cross=JZ[n]['crossable']
        o.append(f'<polygon points="{pts}" fill="{WARM.get(cls,"#fdfcf9")}" fill-opacity="{0.62 if cross else 0.38}" stroke="#8f877b" stroke-width="0.5" stroke-linejoin="round"/>')
    for n,g in Z.items():
        if not g.intersects(cb): continue
        ip=g.intersection(cb)
        if ip.is_empty or ip.area<20 or n in SKIP: continue
        rp=ip.representative_point() if ip.geom_type!='MultiPolygon' else max(ip.geoms,key=lambda x:x.area).representative_point()
        o.append(f'<text x="{rp.x:.1f}" y="{rp.y:.1f}" font-size="3.4" fill="#2f2b27" font-weight="600">{n}</text>')
    for i,v in P.items():
        if i in EXCL: continue
        l=v['line']
        if not (min(l[0],l[2])<cx1+2 and max(l[0],l[2])>cx0-2 and min(l[1],l[3])<cy1+2 and max(l[1],l[3])>cy0-2): continue
        virt=JP[i]['virtual']; ex='exterior' in ends(i)
        col='#b4561f' if ex else '#0d6b63'
        da=' stroke-dasharray="3 2"' if virt else ''
        o.append(f'<line x1="{l[0]}" y1="{l[1]}" x2="{l[2]}" y2="{l[3]}" stroke="{col}" stroke-width="1.5"{da}/><circle cx="{v["c"][0]}" cy="{v["c"][1]}" r="2.1" fill="{col}" stroke="#fff" stroke-width=".5"/>')
    for i,c in CAND.items():
        if not c.intersects(cb): continue
        gs=c.geoms if hasattr(c,'geoms') else [c]
        for s in gs:
            if s.geom_type=='LineString':
                pts=list(s.coords)
                o.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="none" stroke="#d62f1f" stroke-width="2" stroke-dasharray="2 1.5" opacity=".9"/>')
                mx=sum(x for x,y in pts)/len(pts); my=sum(y for x,y in pts)/len(pts)
    o.extend(EXTRA)
    for i,v in PROP.items():
        (x,y)=v['pt']
        if not(cx0-3<x<cx1+3 and cy0-3<y<cy1+3): continue
        (a,b),(c,d)=v['line']
        o.append(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="#fff" stroke-width="3.2" stroke-linecap="round" opacity=".8"/><line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="#d62f1f" stroke-width="1.8" stroke-linecap="round" opacity=".92"/><circle cx="{x}" cy="{y}" r="2.6" fill="#d62f1f" stroke="#fff" stroke-width="1"/>')
    o.append('</svg>')
    return '\n'.join(o)
def panel(title,box_,sub,name):
    cx0,cy0,cx1,cy1=box_
    svg=build_svg(*box_)
    ov=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert('RGBA')
    # lageplan crop (full-res px = 2*(svg+offset))
    X0,Y0,X1,Y1=[int(2*(v+o)) for v,o in ((cx0,40),(cy0,77),(cx1,40),(cy1,77))]
    bg=lp.crop((X0,Y0,X1,Y1)).resize(ov.size,Image.LANCZOS).convert('RGBA')
    bg.alpha_composite(ov)
    f=ImageFont.load_default()
    try: f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22); f2=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
    except: f2=f
    import textwrap
    W,H=bg.size; lines=textwrap.wrap(sub,max(20,int(W/9.5))); hh=44+22*len(lines)+8
    out=Image.new('RGB',(W,H+hh),'#f6f4ef'); out.paste(bg.convert('RGB'),(0,hh))
    d=ImageDraw.Draw(out); d.text((10,6),title,fill='#2f2b27',font=f)
    for k,l in enumerate(lines): d.text((10,40+22*k),l,fill='#6b645a',font=f2)
    out.save(name); return out



import os
from shapely.geometry import Polygon
from shapely.ops import unary_union as UU
os.makedirs('review/cutouts',exist_ok=True)
RED='#d62f1f'; GREY='#6b645a'; TEAL='#0d6b63'
def line(a,b,c=GREY,w=1.0,dash='2 1.5',op=.9): return f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{c}" stroke-width="{w}" stroke-dasharray="{dash}" opacity="{op}"/>'
def txt(x,y,t,sz=3,c=GREY,w=600): return f'<text x="{x}" y="{y}" font-size="{sz}" fill="{c}" font-weight="{w}">{t}</text>'
def PROPDOOR(a,b,pt): return {'pt':pt,'line':[a,b]}
def tealdoor(a,b,pt): return f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{TEAL}" stroke-width="1.5"/><circle cx="{pt[0]}" cy="{pt[1]}" r="2.1" fill="{TEAL}" stroke="#fff" stroke-width=".5"/>'
S=7
Z0=dict(Z)   # keep originals
def reset():
    global EXCL,SKIP,EXTRA,PROP,CAND
    Z.clear(); Z.update(Z0); EXCL=set();SKIP=set();EXTRA=[];PROP={};CAND={}
def halfplane_left(A,B,far=-2000):
    # polygon to the left (smaller x) of line through A,B (extended)
    dx,dy=B[0]-A[0],B[1]-A[1]
    A2=(A[0]-dx*3,A[1]-dy*3); B2=(B[0]+dx*3,B[1]+dy*3)
    return Polygon([A2,B2,(far,B2[1]),(far,A2[1])])
# ===== c1 fire door, corrected + re-cut + E.37 door moved left
reset()
dA,dB=(606.3,545.0),(632.9,594.0); dM=((dA[0]+dB[0])/2,(dA[1]+dB[1])/2)
U=UU([Z0['E.flur-tr2-1'],Z0['E.flur-tr7-3']]); Lh=halfplane_left(dA,dB)
Z['E.flur-tr2-1']=U.intersection(Lh).buffer(0); Z['E.flur-tr7-3']=U.difference(Lh).buffer(0)
for k in ('E.flur-tr2-1','E.flur-tr7-3'):
    if Z[k].geom_type!='Polygon': Z[k]=max(Z[k].geoms,key=lambda g:g.area)
PROP={'fire':PROPDOOR(dA,dB,dM)}
EXCL={'E.37_E.flur-tr7-3'}
EXTRA=[line((610,545),(622,594),GREY,.8,'2 1.5'),txt(598,583,'old split',2.6),
 tealdoor((616.5,594),(627.5,594),(622,594)),txt(606,589.5,'E.37 door (moved)',2.6,TEAL)]
A=panel('1  E.flur-tr2-1_E.flur-tr7-3  (fire door)',(560,525,680,615),f'zones re-cut along the door: line {dA}-{dB}, point ({dM[0]:.1f}, {dM[1]:.1f}). E.37 door moved to x 616.5-627.5 (point 622), so it now opens onto E.flur-tr2-1 (E.37_E.flur-tr2-1). Grey dashed = old split.','review/cutouts/c1-fire-door.png')
# ===== c2 TR2 junction, user geometry
reset()
rh=Polygon([(525,536),(557,586),(532,625),(502,580)])
oldTR2=Z0['E.TR2']
rest=oldTR2.difference(rh)           # left part of old TR2 -> passage
pas=UU([Z0['E.flur-tr2-2'],Z0['E.flur-tr2-3'],rest]).buffer(0.01).buffer(-0.01)
# flur-tr2-4 extended to x=463 (y 556-593)
f4=UU([Z0['E.flur-tr2-4'],Polygon([(450,556),(463,556),(463,593),(450,593)])])
# passage loses the strip x<463
pas=pas.difference(Polygon([(440,540),(463,540),(463,600),(440,600)]))
Z['E.TR2']=rh; Z['E.flur-tr2-2']=pas; del Z['E.flur-tr2-3']
Z['E.flur-tr2-4']=f4
for k in ('E.flur-tr2-2','E.flur-tr2-4'):
    if Z[k].geom_type!='Polygon': Z[k]=max(Z[k].geoms,key=lambda g:g.area)
EXCL={'E.flur-tr2-2_E.flur-tr2-3','E.TR2_E.flur-tr2-3','E.TR2_E.flur-tr2-6'}
SKIP={'E.flur-tr2-3'}
PROP={'tr2':PROPDOOR((463,556),(463,593),(463,574.5))}
EXTRA=[line((450,556),(450,593),GREY,.8,'2 1.5'),txt(437,553,'old split x=450',2.6),
 line((557,586),(532,625),GREY,1.2,'2 1.5'),txt(538,612,'no portal',2.8),
 tealdoor((466.5,593),(478.5,593),(472.5,593)),txt(500,604,'was E.TR2_E.flur-tr2-6',2.4,TEAL)]
B=panel('2  TR2 junction (your geometry)',(415,535,575,640),'E.TR2 = yellow rhombus only. E.flur-tr2-2 = old -2 + -3 + left part of old TR2, from the double door (x 463, wall to wall, y 556-593) to the hub; virtual portal to E.flur-tr2-1 unchanged. Removed: -2/-3 split, E.TR2_E.flur-tr2-3. E.TR2 | E.flur-tr3-1 has no portal.','review/cutouts/c2-tr2-junction.png')
# ===== c3 TR7/TR9: re-cut + little bit virtual
reset()
eA,eB=(1011.0,481.0),(1037.0,528.3); eM=((eA[0]+eB[0])/2,(eA[1]+eB[1])/2)
T=Polygon([(1010.5,480),(1050,480),(1050,528),(1037,528.3)])
Z['E.flur-tr9-3']=UU([Z0['E.flur-tr9-3'],T]).buffer(0.01).buffer(-0.01)
Z['E.flur-tr7-1']=Z0['E.flur-tr7-1'].difference(T)
for k in ('E.flur-tr9-3','E.flur-tr7-1'):
    if Z[k].geom_type!='Polygon': Z[k]=max(Z[k].geoms,key=lambda g:g.area)
vA,vB=(1037,528.3),(1050,528); vM=((vA[0]+vB[0])/2,(vA[1]+vB[1])/2)
PROP={'tr7':PROPDOOR(eA,eB,eM)}
EXTRA=[line((1050,480),(1050,528),GREY,.8,'2 1.5'),txt(1062,470,'old split x=1050',2.6),
 txt(1034,538,'wall',2.6,GREY)]
C=panel('3  E.flur-tr7-1_E.flur-tr9-3  (double door)',(1000,455,1100,545),f'door line {eA}-{eB}, point ({eM[0]:.1f}, {eM[1]:.1f}). Splits re-cut along the door. The short stretch from the door end (1037, 528.3) to the E.51 corner (1050, 528) is part of E.flur-tr9-3 (its south wall runs on to the door end); no portal there. Grey dashed = old split at x=1050.','review/cutouts/c3-tr7-tr9.png')
for im in (A,B,C): print(im.size)
