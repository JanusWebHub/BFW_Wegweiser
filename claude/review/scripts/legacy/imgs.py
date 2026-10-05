import os,math
exec(open('fixed.py').read().split("# ================= validation")[0])
exec("# ================= routing graph"+open('fixed.py').read().split("# ================= routing graph",1)[1].split("ROUTES=")[0])
from PIL import Image,ImageDraw,ImageFont
from shapely.geometry import box
OUT='review/images'; os.makedirs(OUT,exist_ok=True)
S=2; W,H=1790,1000
try: F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',11); FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
except: F=FB=ImageFont.load_default()
lp=Image.open('lp_half.png').convert('L').rotate(180)
def under(op):
    cv=Image.new('L',(W,H),255); cv.paste(lp,(-40,-77)); im=cv.resize((W*S,H*S)).convert('RGB')
    return Image.blend(Image.new('RGB',im.size,'white'),im,op)
T=lambda p:(p[0]*S,p[1]*S)
def kind(n):
    if n in BLOCKS: return 'block'
    e=zel.get('zone-'+n); cls=e.get('class','') if e is not None else ''
    if any(k in n for k in('treppe','aufzug')) : return 'vert'
    if n.startswith('E.flur') or 'durchgang' in n or 'corridor' in cls: return 'circ'
    return 'cross' if C[n] else 'room'
COL={'circ':(222,200,150),'vert':(176,160,140),'cross':(238,225,196),'room':(250,246,236),'block':(215,215,215)}
def polys(g): return [g] if g.geom_type=="Polygon" else [x for x in getattr(g,"geoms",[]) if x.geom_type=="Polygon"]
class Im(Image.Image): pass
def base(op=0.0,fill=True,alpha=235,lab=True,outline=(47,63,168),title=None,dim=1.0):
    im=under(op) if op else Image.new('RGB',(W*S,H*S),'white')
    d=ImageDraw.Draw(im,'RGBA')
    for n,g in G.items():
        k=kind(n)
        for p in polys(g):
            pts=[T(q) for q in p.exterior.coords]
            if fill: d.polygon(pts,fill=COL[k]+(int(alpha*dim),))
            if k=='block':
                x0,y0,x1,y1=p.bounds
                for t in range(int(x0-(y1-y0)),int(x1),4):
                    seg=[(t,y1),(t+(y1-y0),y0)]
                    from shapely.geometry import LineString
                    c=p.intersection(LineString(seg))
                    for l in ([c] if c.geom_type=='LineString' else [x for x in getattr(c,'geoms',[]) if x.geom_type=='LineString']):
                        d.line([T(q) for q in l.coords],fill=(150,150,150,255),width=1)
            d.line(pts,fill=outline+(255,),width=2)
    if lab:
        for n,g in G.items():
            if n in BLOCKS or g.area<60: continue
            c=g.representative_point(); t=n.replace('E.','').replace('flur-','f-')
            d.text(T((c.x-len(t)*2.6,c.y-4)),t,fill=(30,30,30,255),font=F)
    im.title=title
    return im
def save(im,name):
    t=getattr(im,'title',None); items=LEG.pop(id(im),None); b=sh.bounds
    c=im.crop((int(b[0]*S)-20,int(b[1]*S)-20,int(b[2]*S)+20,int(b[3]*S)+20))
    im=Image.new('RGB',(c.size[0],c.size[1]+60),'white'); im.paste(c,(0,60))
    ImageDraw.Draw(im).text((24,14),t or '',fill=(20,20,20),font=FB)
    if items: _legend(im,items)
    im.save(f'{OUT}/{name}.png'); print(name,im.size)
def ctr(n): c=G[n].representative_point(); return (c.x,c.y)
LEG={}
def legend(im,items): LEG[id(im)]=items
def _legend(im,items):
    d=ImageDraw.Draw(im,'RGBA'); x,y=24,im.size[1]-30*len(items)-24
    d.rectangle([x-8,y-8,x+330,y+30*len(items)],fill=(255,255,255,235),outline=(120,120,120,255))
    for i,(c,t,sh_) in enumerate(items):
        yy=y+i*30
        if sh_=='line': d.line([x,yy+10,x+30,yy+10],fill=c,width=5)
        elif sh_=='dot': d.ellipse([x+8,yy+3,x+22,yy+17],fill=c)
        else: d.rectangle([x,yy+2,x+30,yy+18],fill=c,outline=(47,63,168,255))
        d.text((x+40,yy+3),t,fill=(0,0,0,255),font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14))
def kindleg(): return [(COL['circ']+(255,),'circulation (corridors)','r'),(COL['vert']+(255,),'stairs and lifts','r'),(COL['cross']+(255,),'crossable rooms','r'),(COL['room']+(255,),'other rooms','r'),(COL['block']+(255,),'block (inaccessible, hatched)','r')]
# 1 semantic plan
im=base(title='1  Semantic plan: zone kinds (EG)'); legend(im,kindleg()); save(im,'01-semantic-plan')
# 2 over Lageplan
im=base(op=0.45,alpha=120,title='2  Zones over the Lageplan'); legend(im,kindleg()); save(im,'02-zones-on-lageplan')
im=base(op=0.7,fill=False,lab=False,title='3  Outlines only over the Lageplan (check of fit)'); save(im,'03-outlines-on-lageplan')
# portals
def pcol(i):
    if 'exterior' in ends2(i): return (214,40,40,255)
    if PT[i]['virtual']: return (240,140,20,255)
    return (0,140,120,255)
def portal_img(op,title,name):
    im=base(op=op,alpha=150,lab=False,title=title); d=ImageDraw.Draw(im,'RGBA')
    for i,l in LN.items(): d.line([T(l[:2]),T(l[2:])],fill=pcol(i),width=5)
    legend(im,[((0,140,120,255),'door (%d)'%sum(1 for i in LN if pcol(i)[0]==0),'line'),((240,140,20,255),'virtual portal (%d)'%sum(1 for i in LN if pcol(i)[0]==240),'line'),((214,40,40,255),'exit to outside (%d)'%sum(1 for i in LN if pcol(i)[0]==214),'line')]+kindleg()[:0]); save(im,name)
portal_img(0,'4  Portals: doors, virtual portals, exits','04-portals')
portal_img(0.45,'5  Portals over the Lageplan','05-portals-on-lageplan')
# connectivity graph
im=base(alpha=110,lab=False,title='6  Connectivity graph: zones = nodes, portals = edges'); d=ImageDraw.Draw(im,'RGBA')
for i in PT:
    e=ends2(i)
    if 'exterior' in e: continue
    a,b=e; d.line([T(PT[i]['point'] if False else ctr(a)),T(ctr(b))],fill=(60,60,60,200),width=2)
for n in G:
    c=ctr(n); r=5 if n not in BLOCKS else 3
    d.ellipse([T(c)[0]-r,T(c)[1]-r,T(c)[0]+r,T(c)[1]+r],fill=((47,63,168,255) if C[n] else (214,120,40,255)) if n not in BLOCKS else (150,150,150,255))
legend(im,[((47,63,168,255),'crossable zone','dot'),((214,120,40,255),'non-crossable zone','dot'),((150,150,150,255),'block (no portal)','dot'),((60,60,60,200),'portal (edge)','line')]); save(im,'06-connectivity-graph')
# routing graph
im=base(alpha=90,lab=False,title='7  Routing graph: portals and straight segments in crossable zones'); d=ImageDraw.Draw(im,'RGBA')
for z,sl in SEG.items():
    for s in sl: d.line([T(s['geometry'][0]),T(s['geometry'][1])],fill=(40,90,200,110),width=1)
for i,l in LN.items(): c=PT[i]['point']; d.ellipse([T(c)[0]-3,T(c)[1]-3,T(c)[0]+3,T(c)[1]+3],fill=pcol(i))
legend(im,[((40,90,200,200),'segment (%d)'%nseg,'line'),((0,140,120,255),'portal','dot')]); save(im,'07-routing-graph')
# crossable map
im=base(alpha=0,fill=False,lab=False,title='8  Where a route may pass (crossable) and where it may not'); d=ImageDraw.Draw(im,'RGBA')
for n,g in G.items():
    c=(70,170,90,150) if C[n] else ((190,190,190,200) if n in BLOCKS else (230,150,60,120))
    for p in polys(g): d.polygon([T(q) for q in p.exterior.coords],fill=c,outline=(47,63,168,255))
legend(im,[((70,170,90,255),'crossable','r'),((230,150,60,255),'room (destination only)','r'),((190,190,190,255),'block','r')]); save(im,'08-crossable-map')
# routes
RC=[(220,40,40),(40,120,220),(40,160,70),(170,60,200),(230,140,20)]
ROUTES=[('E.01','E.52'),('E.72a','E.62'),('E.90','E.60a'),('E.34','E.41a'),('E.33a','E.02')]
def path_pts(s,t,p):
    pts=[ctr(s)]
    for z,i in p[1:]:
        if i: pts.append(PT[i]['point'])
    pts.append(ctr(t)); return pts
def draw_route(d,pts,col,w=6):
    d.line([T(q) for q in pts],fill=col+(255,),width=w,joint='curve')
def endpoints(d,s,t,col):
    for n,l in ((s,'start'),(t,'target')):
        c=T(ctr(n)); d.ellipse([c[0]-10,c[1]-10,c[0]+10,c[1]+10],fill=col+(255,),outline=(255,255,255,255),width=3); d.text((c[0]+13,c[1]-8),n.replace('E.','')+' '+l,fill=(0,0,0,255),font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',15))
allr=[]
for k,(s,t) in enumerate(ROUTES):
    dist,p=route(s,t); pts=path_pts(s,t,p); allr.append((s,t,dist,pts))
    im=base(alpha=100,lab=False,title='%d  Route %s to %s: %.1f m, %d zones'%(9+k,s.replace('E.',''),t.replace('E.',''),dist,len(p))); d=ImageDraw.Draw(im,'RGBA')
    for z,_ in p:
        for q in polys(G[z]): d.polygon([T(x) for x in q.exterior.coords],fill=RC[k]+(60,))
    draw_route(d,pts,RC[k]); endpoints(d,s,t,RC[k]); save(im,'%02d-route-%s-%s'%(9+k,s.replace('E.',''),t.replace('E.','')))
im=base(op=0.45,alpha=70,lab=False,title='14  All five sample routes over the Lageplan'); d=ImageDraw.Draw(im,'RGBA')
for k,(s,t,dist,pts) in enumerate(allr): draw_route(d,pts,RC[k],6); endpoints(d,s,t,RC[k])
legend(im,[(RC[k]+(255,),'%s to %s  %.1f m'%(s.replace('E.',''),t.replace('E.',''),dist),'line') for k,(s,t,dist,pts) in enumerate(allr)]); save(im,'14-routes-all-on-lageplan')
# reachability from E.52 (distance heat)
import heapq
def dist_from(s):
    D={}
    for z in G:
        if z==s or z in BLOCKS: continue
        d_,_p=route(s,z)
        if d_ is not None: D[z]=d_
    D[s]=0; return D
D=dist_from('E.52'); mx=max(D.values())
im=base(alpha=0,fill=False,lab=False,title='15  Walking distance from E.52 to every zone (max %.0f m)'%mx); d=ImageDraw.Draw(im,'RGBA')
for n,g in G.items():
    if n in D: t=D[n]/mx; c=(int(255*t),int(200*(1-abs(t-.5)*1.2)),int(255*(1-t)),170)
    else: c=(200,200,200,200)
    for p in polys(g): d.polygon([T(q) for q in p.exterior.coords],fill=c,outline=(47,63,168,255))
d.rectangle([20,im.size[1]-90,360,im.size[1]-30],fill=(255,255,255,235))
for x in range(300): t=x/300; d.line([(30+x,im.size[1]-80),(30+x,im.size[1]-60)],fill=(int(255*t),int(200*(1-abs(t-.5)*1.2)),int(255*(1-t)),255))
d.text((30,im.size[1]-55),'0 m',fill=(0,0,0,255),font=F); d.text((300,im.size[1]-55),'%.0f m'%mx,fill=(0,0,0,255),font=F); save(im,'15-distance-from-E52')
# validation
im=base(alpha=110,lab=False,title='16  Validation: gaps, outside shell, doors off the wall'); d=ImageDraw.Draw(im,'RGBA')
from shapely.ops import unary_union
cov=unary_union(list(G.values())); gaps=sh.difference(cov); out_=cov.difference(sh)
for g_,c in ((gaps,(230,0,0,200)),(out_,(230,0,200,200))):
    for p in polys(g_) if not g_.is_empty else []: d.polygon([T(q) for q in p.exterior.coords],fill=c)
for i,l in LN.items():
    e=ends2(i)
    if 'exterior' in e: continue
    a,b=G[e[0]],G[e[1]]; pt=Point(PT[i]['point']); dd=min(pt.distance(a.boundary),pt.distance(b.boundary))
    if dd>0.6: c=T(PT[i]['point']); d.ellipse([c[0]-14,c[1]-14,c[0]+14,c[1]+14],outline=(230,0,0,255),width=4)
legend(im,[((230,0,0,200),'gap (%.0f units2)'%gaps.area,'r'),((230,0,200,200),'outside shell (%.0f units2)'%out_.area,'r'),((230,0,0,255),'door more than 0.6 off the wall','dot')]); save(im,'16-validation')
