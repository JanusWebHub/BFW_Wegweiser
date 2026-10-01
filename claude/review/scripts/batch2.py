# ================= batch 2: user redline marks (kitchen doors, hub, WC block, E.52, TR7, east block)
import json as _json
from shapely.geometry import MultiPolygon
from shapely.ops import unary_union as _UU
M2=_json.load(open('marks_batch2.json')); MID={m['id']:m for m in M2}
BLOCKS=set(); USER=set(); LOG2=[]; DIRTY=[]
def _polys(g):
    if g.is_empty: return []
    return list(g.geoms) if hasattr(g,'geoms') else [g]
def _clean(pts):
    p=[tuple(q) for q in pts]
    if p[0]==p[-1] or math.dist(p[0],p[-1])<0.6: p=p[:-1]
    return p
# --- snap near-equal coordinates across all user polygons
UZ={k:_clean(MID[k]['pts']) for k in MID if MID[k]['kind']=='zone'}
def _cluster(vals,tol=0.8):
    vals=sorted(vals); groups=[[vals[0]]]
    for v in vals[1:]:
        (groups[-1].append(v) if v-groups[-1][-1]<=tol else groups.append([v]))
    out={}
    for g in groups:
        ints=[x for x in g if abs(x-round(x))<0.01]
        c=ints[0] if ints else round(sum(g)/len(g),1)
        for x in g: out[x]=c
    return out
_xs=_cluster([q[0] for p in UZ.values() for q in p]); _ys=_cluster([q[1] for p in UZ.values() for q in p])
UZ={k:[(_xs[q[0]],_ys[q[1]]) for q in p] for k,p in UZ.items()}
ZMAP={'zone_mupvs1bbpexb':'E.vorraum-e50','zone_mupvtdc9xa3q':'E.block-e50','zone_mupvv6c3sl5d':'E.50a','zone_mupvver7hxan':'E.wc-beh-e50a',
 'zone_mupvwvw2k26u':'E.vr-e50b','zone_mupvx798kw5r':'E.50b','zone_mupvxdj6xekl':'E.wc-beh-e50b','zone_mupvyjyaqyd8':'E.block-e52-a','zone_mupvzd0fkcb3':'E.block-e52-b',
 'zone_mupw2cngma0m':'E.59b','zone_mupw51dhwx7g':'E.TR9','zone_mupyovktnn49':'E.foyer','zone_mupylhe9hgwe':'E.flur-tr7-2','zone_mupyq4a73xko':'E.flur-tr7-1','zone_mupyon9wssp4':'E.terrasse','zone_mupyjiiafftn':'E.flur-tr7-5','zone_mupwhu0lwn0w':'E.aufzug-tr7'}
UP={ZMAP[k]:Polygon(UZ[k]).buffer(0) for k in ZMAP}
UP['E.terrasse']=one(_UU([G['E.terrasse'],UP['E.terrasse']]).buffer(0))
# nested rooms are cut out of the host (host stays, notch or hole)
UP['E.50a']=one(UP['E.50a'].difference(UP['E.wc-beh-e50a'])); UP['E.50b']=one(UP['E.50b'].difference(UP['E.wc-beh-e50b']))
BLOCKS|={'E.block-e50','E.block-e52-a','E.block-e52-b','E.lueftung-e41','E.schacht-tr8'}
# --- 1. door removals and moves by id (before any zone change)
for k,m in MID.items():
    if m['kind']=='remove' and m['target'] in PT: rmportal(m['target'])
    elif m['kind']=='remove': LOG2.append(('rm missing',m['target']))
for k,m in MID.items():
    if m['kind']=='move':
        t=m['target']
        if t in PT:
            p=m['pts']; LN[t]=(p[0][0],p[0][1],p[1][0],p[1][1]); PT[t]['point']=[round((p[0][0]+p[1][0])/2,1),round((p[0][1]+p[1][1])/2,1)]; USER.add(t)
        else: LOG2.append(('move missing',t))
PT['E.flur-tr7-2_E.speisesaal']['virtual']=False          # widened double door is a real door
ADDS=[(k,[tuple(q) for q in m['pts']],m.get('text','')) for k,m in MID.items() if m['kind']=='add' and 'e.59 - e.59a' not in m.get('text','')]
# drop all portals of the old hub continuum (re-created from geometry below)
for i in list(PT):
    a,b=ends2(i)
    if 'E.foyer' in (a,b) or {a,b}<= {'E.flur-tr7-1','E.flur-tr7-2'} or i=='E.flur-tr7-2_E.flur-tr7-3': rmportal(i)
# --- 2. zone geometry
HUBOLD=_UU([G[z] for z in ('E.foyer','E.flur-tr7-1','E.flur-tr7-2')])
for z in ('E.foyer','E.flur-tr7-1','E.flur-tr7-2'): DIRTY.append(G.pop(z)); C.pop(z,None)
OLDS={n:G[n] for n in ('E.vorraum-e50','E.50a','E.50b','E.vr-e50b','E.wc-beh-e50b','E.TR9','E.59b','E.aufzug-tr7','E.52','E.41b','E.flur-tr8-6') if n in G}
def apply_zone(n,poly):
    poly=one(poly.buffer(0))
    if n in G: DIRTY.append(G[n])
    DIRTY.append(poly)
    for o in list(G):
        if o==n or not G[o].intersects(poly): continue
        d=G[o].difference(poly)
        if d.is_empty: DIRTY.append(G.pop(o)); continue
        if G[o].intersection(poly).area>0.05: DIRTY.append(G[o]); G[o]=one(d)
    G[n]=poly
order=['E.terrasse','E.flur-tr7-5','E.flur-tr7-2','E.flur-tr7-1','E.foyer','E.TR9','E.59b','E.aufzug-tr7',
       'E.vorraum-e50','E.block-e50','E.50a','E.wc-beh-e50a','E.vr-e50b','E.50b','E.wc-beh-e50b','E.block-e52-a','E.block-e52-b']
for n in order: apply_zone(n,UP[n])
# E.flur-tr8-6 reaches x=1174 (the E.41b pocket starts there)
apply_zone('E.flur-tr8-6',Polygon([(959.7,948),(1174,948),(1174,963),(959.7,963)]).intersection(sh))
C.update({'E.flur-tr7-1':True,'E.flur-tr7-2':True,'E.flur-tr7-5':True,'E.foyer':True,'E.block-e50':False,'E.block-e52-a':False,'E.block-e52-b':False,'E.wc-beh-e50a':False,'E.50a':True,'E.50b':False,'E.lueftung-e41':False,'E.schacht-tr8':False})
for z in ('E.flur-tr7-5','E.wc-beh-e50a','E.block-e50','E.block-e52-a','E.block-e52-b'):
    zel['zone-'+z]=ET.Element('x',{'class':'zone '+('service' if z.startswith(('E.block','E.wc')) else 'corridor')})
zel['zone-E.foyer']=ET.Element('x',{'class':'zone hall'})
# --- 3. gap fill inside the touched area: leftovers go to the neighbour sharing the longest edge
_dirty=_UU([g.buffer(10) for g in DIRTY]).intersection(sh)
def _fill():
    U=_UU(list(G.values())); n_=0
    for frag in _polys(_dirty.difference(U)):
        if frag.area<0.05: continue
        best=None
        for n,g in G.items():
            if n in BLOCKS or (n in UP and not C.get(n,False)): continue
            L=frag.boundary.intersection(g.buffer(0.05)).length
            sc=(1 if C.get(n,False) else 0, L)
            if L>0.3 and (best is None or sc>best[0]): best=(sc,n)
        if best: G[best[1]]=one(_UU([G[best[1]],frag]).buffer(0.02).buffer(-0.02)); n_+=1
    return n_
LOG2.append(('gap fragments filled',_fill()+_fill()+_fill()))
# --- 4. portals follow the zones
def zone_at(pt):
    c=[(g.area,n) for n,g in G.items() if g.contains(Point(pt))]
    if c: return min(c)[1]
    return 'exterior' if not sh.contains(Point(pt)) else None
def pair_at(l,off=4.0):
    mx,my=(l[0]+l[2])/2,(l[1]+l[3])/2; dx,dy=l[2]-l[0],l[3]-l[1]; L=math.hypot(dx,dy) or 1; nx,ny=-dy/L,dx/L
    for o in (1.5,2.5,4.0,6.0):
        a=zone_at((mx+nx*o,my+ny*o)); b=zone_at((mx-nx*o,my-ny*o))
        if a and b and a!=b: return tuple(sorted((a,b)))
    return None
def newid(a,b):
    i=sortid(a,b); k_=2
    while i in PT: i=sortid(a,b,f'_{k_}'); k_+=1
    return i
for i in list(PT):
    a,b=ends2(i)
    if 'exterior' in (a,b):
        continue
    ok=a in G and b in G
    if ok:
        x1,y1,x2,y2=LN[i]; mid=Point((x1+x2)/2,(y1+y2)/2)
        ok=max(mid.distance(G[a].boundary),mid.distance(G[b].boundary))<=1.2
    if not ok:
        if PT[i]['virtual'] and not (a in G and b in G): rmportal(i); LOG2.append(('virtual dropped',i)); continue
        pr=pair_at(LN[i])
        if pr==tuple(sorted((a,b))): continue
        if pr and 'exterior' not in pr:
            u=i in USER; ni=newid(*pr); renameportal(i,ni); (USER.discard(i),USER.add(ni)) if u else None; LOG2.append(('reparent',i,ni))
        else: LOG2.append(('UNRESOLVED',i,pr))
# exits on the shell: re-id by zone at the inner side
for i in list(PT):
    a,b=ends2(i)
    if 'exterior' in (a,b):
        z=a if b=='exterior' else b
        if z not in G:
            x1,y1,x2,y2=LN[i]; mx,my=(x1+x2)/2,(y1+y2)/2
            cand=min(((Point(mx,my).distance(g.boundary),n) for n,g in G.items()))
            ni=sortid(cand[1],'exterior'); renameportal(i,ni); LOG2.append(('exit reparent',i,ni))
# --- 5. new doors
for k,l,t in ADDS:
    l=(l[0][0],l[0][1],l[1][0],l[1][1])
    if 'exterior' in t or 'emergency' in t:
        mx,my=(l[0]+l[2])/2,(l[1]+l[3])/2
        z=zone_at((mx+1.5,my)) if zone_at((mx+1.5,my)) not in (None,'exterior') else zone_at((mx-1.5,my))
        # snap to the shell
        ps=[nearest_points(sh.exterior,Point(l[0],l[1]))[0],nearest_points(sh.exterior,Point(l[2],l[3]))[0]]
        z=min(((Point((l[0]+l[2])/2,(l[1]+l[3])/2).distance(g.boundary),n) for n,g in G.items()))[1]
        addportal(sortid(z,'exterior'),False,(ps[0].x,ps[0].y),(ps[1].x,ps[1].y),emergency_exit=True); USER.add(sortid(z,'exterior')); continue
    pr=pair_at(l)
    if pr is None:
        mx,my=(l[0]+l[2])/2,(l[1]+l[3])/2
        d,z=min(((Point(mx,my).distance(g.boundary),n) for n,g in G.items()))
        if Point(mx,my).distance(sh.exterior)<1.5:
            ps=[nearest_points(sh.exterior,Point(l[0],l[1]))[0],nearest_points(sh.exterior,Point(l[2],l[3]))[0]]
            ni=sortid(z,'exterior'); addportal(ni,False,(ps[0].x,ps[0].y),(ps[1].x,ps[1].y),emergency_exit=('exit' in t or 'TR8' in z)); USER.add(ni); LOG2.append(('exit door',ni,t)); continue
        LOG2.append(('ADD UNRESOLVED',k,l,t)); continue
    ni=newid(*pr); vt_=(t=='virtual'); addportal(ni,vt_,(l[0],l[1]),(l[2],l[3])); (None if vt_ else USER.add(ni)); LOG2.append(('add',ni,t))
# TR8 west door = emergency exit
for i in list(PT):
    if i.endswith('_exterior') and 'E.TR8' in i: PT[i]['emergency_exit']=True
# --- 6. virtual portals between consecutive hub pieces and the corridor beside the Terrasse
HUB=['E.flur-tr7-1','E.flur-tr7-2','E.flur-tr7-5','E.flur-tr7-3','E.flur-tr7-4','E.flur-tr9-3']
have={tuple(sorted(ends2(i))) for i in PT}
for a_,b_ in itertools.combinations(HUB,2):
    if tuple(sorted((a_,b_))) in have: continue
    s_=G[a_].boundary.intersection(G[b_].buffer(0.9).boundary) if False else G[a_].boundary.intersection(G[b_].buffer(0.9))
    segs=[g for g in _polys(s_) if g.geom_type=='LineString' and g.length>=3]
    if segs:
        g=max(segs,key=lambda q:q.length); c=list(g.coords)
        addportal(sortid(a_,b_),True,c[0],c[-1]); LOG2.append(('virtual',sortid(a_,b_),round(g.length,1)))
for i in list(PT):
    a,b=ends2(i)
    if 'exterior' in (a,b) or a not in G or b not in G: continue
    x1,y1,x2,y2=LN[i]; mid=Point((x1+x2)/2,(y1+y2)/2)
    if max(mid.distance(G[a].boundary),mid.distance(G[b].boundary))>0.6: _dirty=_dirty.union(mid.buffer(9))
LOG2.append(('gap fragments filled',_fill()+_fill()))
# --- 7. doors to boundaries: user doors move the wall (<=3.6), other doors snap to the wall
def shared_seg(a,b,near):
    s_=G[a].boundary.intersection(G[b].buffer(4.6))
    segs=[g for g in _polys(s_) if g.geom_type=='LineString' and g.length>1]
    return min(segs,key=lambda g:g.distance(Point(near))) if segs else None
nadapt=0;nsnap2=0
for i in list(PT):
    a,b=ends2(i)
    if a=='exterior' or b=='exterior': continue
    x1,y1,x2,y2=LN[i]; mid=Point((x1+x2)/2,(y1+y2)/2)
    d=max(mid.distance(G[a].boundary),mid.distance(G[b].boundary))
    if d<=0.6: continue
    sg=shared_seg(a,b,mid)
    if sg is None: LOG2.append(('door off wall',i,round(d,1))); continue
    q=nearest_points(sg,mid)[0]; dx,dy=q.x-mid.x,q.y-mid.y
    if i in USER and 0.6<math.hypot(dx,dy)<=4.5 and not PT[i]['virtual']:
        # move the wall onto the door: strip between wall piece and the door's line
        L_=math.hypot(x2-x1,y2-y1) or 1; ux,uy=(x2-x1)/L_,(y2-y1)/L_
        e1=(x1-ux*1.5,y1-uy*1.5); e2=(x2+ux*1.5,y2+uy*1.5); sx,sy=dx*(1+0.4/ max(math.hypot(dx,dy),1e-6)),dy*(1+0.4/max(math.hypot(dx,dy),1e-6))
        strip=Polygon([e1,e2,(e2[0]+sx,e2[1]+sy),(e1[0]+sx,e1[1]+sy)]).buffer(0)
        loser,gainer=(a,b) if G[a].contains(mid) or G[a].distance(mid)<G[b].distance(mid) else (b,a)
        strip=strip.intersection(G[loser])
        if strip.area>0.05 and not (a in BLOCKS or b in BLOCKS):
            print('W',i,gainer,loser,round(strip.area,1))
            LOG2.append(('wall',i,gainer,loser,round(strip.area,1),round(math.hypot(dx,dy),1)))
            G[gainer]=one(_UU([G[gainer],strip]).buffer(0.02).buffer(-0.02)); G[loser]=one(G[loser].difference(strip)); nadapt+=1; continue
    LN[i]=(x1+dx,y1+dy,x2+dx,y2+dy); PT[i]['point']=[round((x1+x2)/2+dx,1),round((y1+y2)/2+dy,1)]; nsnap2+=1
# --- 7b. remaining off-boundary doors: snap to the nearest point of the shared boundary
for i in list(PT):
    a,b=ends2(i)
    if a=='exterior' or b=='exterior' or a not in G or b not in G: continue
    x1,y1,x2,y2=LN[i]; mid=Point((x1+x2)/2,(y1+y2)/2)
    if max(mid.distance(G[a].boundary),mid.distance(G[b].boundary))<=0.6: continue
    best=None
    for r_ in (3.7,6.5):
        s_=G[a].boundary.intersection(G[b].buffer(r_))
        segs=[g for g in _polys(s_) if g.geom_type=='LineString' and g.length>0.5]
        if segs: best=min(segs,key=lambda g:g.distance(mid)); break
    if best is None: continue
    q=nearest_points(best,mid)[0]; dx,dy=q.x-mid.x,q.y-mid.y
    LN[i]=(x1+dx,y1+dy,x2+dx,y2+dy); PT[i]['point']=[round(mid.x+dx,1),round(mid.y+dy,1)]
for i in list(PT):
    a,b=ends2(i)
    if 'exterior' in (a,b):
        x1,y1,x2,y2=LN[i]; ps=[nearest_points(sh.exterior,Point(x1,y1))[0],nearest_points(sh.exterior,Point(x2,y2))[0]]
        if Point((x1+x2)/2,(y1+y2)/2).distance(sh.exterior)>0.3:
            LN[i]=(ps[0].x,ps[0].y,ps[1].x,ps[1].y); PT[i]['point']=[round((ps[0].x+ps[1].x)/2,1),round((ps[0].y+ps[1].y)/2,1)]
LOG2.append(('gap fragments filled',_fill()+_fill()))
LOG2.append(('walls moved to doors',nadapt,'doors snapped to walls',nsnap2))
for l in LOG2:
    if l[0] in ('rm missing','move missing','UNRESOLVED','ADD UNRESOLVED','door off wall','walls moved to doors','gap fragments filled','exit reparent','exit door'): print('B2',l)
print('B2 reparents',[l[1:] for l in LOG2 if l[0]=='reparent'])
print('B2 adds',[l[1:] for l in LOG2 if l[0]=='add'])
print('B2 virtual',[l[1:] for l in LOG2 if l[0]=='virtual'])
