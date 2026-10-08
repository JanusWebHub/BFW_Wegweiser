# ================= batch 2: user redline marks (kitchen doors, hub, WC block, E.52, TR7, east block)
import json as _json
from shapely.geometry import MultiPolygon
from shapely.ops import unary_union as _UU, polygonize
M2=_json.load(open('marks_batch2.json')); MID={m['id']:m for m in M2}
PENDING=[]; WALLS=[]; BLOCKS=set(); USER=set(); LOG2=[]; DIRTY=[]
def _polys(g):
    if g.is_empty: return []
    return list(g.geoms) if hasattr(g,'geoms') else [g]
def _merge(*gs):
    m=_UU(list(gs))
    return m.buffer(0.005,join_style=2).buffer(-0.005,join_style=2)
def _faces(piece,nbrs):
    """split a leftover piece among its neighbours: nearest-neighbour regions, with straight separating cuts"""
    if len(nbrs)==1: return [(piece,nbrs[0])]
    from shapely.geometry import MultiPoint
    from shapely.ops import voronoi_diagram
    pts=[];own=[]
    for z in nbrs:
        sb=G[z].boundary.intersection(piece.buffer(0.4))
        for ls in _polys(sb):
            if ls.geom_type!='LineString': continue
            n_=max(2,int(ls.length/0.6))
            for k in range(n_+1):
                p=ls.interpolate(k/n_,normalized=True); pts.append((p.x,p.y)); own.append(z)
    if len({o for o in own})<2: return [(piece,(own or nbrs)[0])]
    vd=voronoi_diagram(MultiPoint(pts),envelope=piece.buffer(50))
    reg={z:[] for z in nbrs}
    from shapely.geometry import Point as _P
    from shapely.strtree import STRtree
    _sites=[_P(p) for p in pts]; _tree=STRtree(_sites)
    for cell in vd.geoms:
        idx=_tree.query(cell.buffer(1e-6),predicate='contains')
        if len(idx): reg[own[int(idx[0])]].append(cell)
    reg={z:_UU(v).intersection(piece) for z,v in reg.items() if v}
    out=[]
    for z,g in reg.items():
        for p in _polys(g):
            if p.geom_type=='Polygon' and p.area>0.02: out.append((p,z))
    return out
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
ZMAP.update({"zone_muqfn2wbz91y": "E.flur-tr4-2", "zone_muqfnsonlvv7": "E.flur-tr4-5", "zone_muqfonb0lxby": "E.83", "zone_muqfp215jc91": "E.83a", "zone_muqfpfv3cj6l": "E.82", "zone_muqfqa1mfjzr": "E.81", "zone_muqfqlfikjpc": "E.flur-tr4-6", "zone_muqfrolov2ig": "E.aufzug-tr4", "zone_muqfs1kl1lkq": "E.schacht-tr4", "zone_muqfsvg39n85": "E.block-tr4-a", "zone_muqft65pss5w": "E.putzmittel-tr4", "zone_muqfu7vyiz3a": "E.75", "zone_muqfurfqsmlb": "E.76", "zone_muqfv0j23yfd": "E.block-tr4-b", "zone_muqfwmoljyfc": "E.74a", "zone_muqfxn647ep0": "E.vr-e72c", "zone_muqfz5hb028o": "E.flur-tr4-4", "zone_muqfzji46045": "E.flur-tr4-7", "zone_muqg08j2hlth": "E.74", "zone_muqg19xioprq": "E.flur-tr4-1", "zone_muqg1p8kyp3o": "E.TR4", "zone_muqg55lyqgxw": "E.flur-tr4-3", "zone_muqg5od181qw": "E.flur-tr4-8", "zone_muqg6kvcx5jr": "E.vr-e84", "zone_muqg7hp6mwxi": "E.84", "zone_muqg7xugz40m": "E.80", "zone_muqg9gguvw8i": "E.TR3", "zone_muqg9zx684xi": "E.lager-tr3", "zone_muqgagzsl0ye": "E.aufzug-tr3", "zone_muqgc05gzctg": "E.flur-tr3-1", "zone_muqgcckdw1d9": "E.flur-tr3-2", "zone_muqgejoq11ux": "E.flur-tr2-2", "zone_muqgeqeqy5z4": "E.flur-tr2-3", "zone_muqgflsr02hr": "E.flur-tr1-3", "zone_muqgh00yiipl": "E.vr-e25b", "zone_muqgi07kikz9": "E.vr-e25", "zone_muqgifb5840x": "E.25b", "zone_muqgjlx5mw8x": "E.25a", "zone_muqgkxmywov3": "E.block-tr2", "zone_muqgl8zxg1hv": "E.aufzug-tr2-b", "zone_muqgliz9xgss": "E.37"})
ZMAP.update({"zone_muqkabihlukg": "E.schacht-e37", "zone_muqkf2qz7ydo": "E.49", "zone_muqkg178ht8f": "E.48", "zone_muqkimmxtouk": "E.kueche-ma", "zone_muqku29h0t36": "E.schacht-tr2", "zone_muqkv90ylali": "E.flur-tr1-1", "zone_muqkwbg7sfgc": "E.flur-tr2-3", "zone_muqkxqr8xw90": "E.flur-tr2-1", "zone_muqkyka51w9t": "E.flur-tr1-3", "zone_muql3icilfot": "E.72b", "zone_muql3ys9dima": "E.72a", "zone_muql70u1p5e6": "E.82a", "zone_muql7avky945": "E.82", "zone_muqldgku5l94": "E.flur-tr1-2", "zone_muqle8jxuir6": "E.03", "zone_muqlejt9ptvh": "E.vr-e03", "zone_muqlf9h7jihr": "E.vr-e01", "zone_muqlfvt80w1q": "E.01", "zone_muqlif8vg17e": "E.TR1", "zone_muqlixvhl57a": "E.block-tr1", "zone_muqlmz3ubqmk": "E.aufzug-tr2-b", "zone_muqlnd1eomk3": "E.37", "zone_muqlof3lisku": "E.block-tr2"})
for _k in ["zone_muqgflsr02hr", "zone_muqgeqeqy5z4", "zone_muqfpfv3cj6l", "zone_muqgl8zxg1hv", "zone_muqgliz9xgss", "zone_muqgkxmywov3"]: ZMAP.pop(_k,None)
UP={ZMAP[k]:Polygon(UZ[k]).buffer(0) for k in ZMAP}
UP['E.48']=one(UP['E.48'].union(Polygon(UZ['zone_muqllsjmskpd']).buffer(0)))   # 'absorb into e.48'
# your "boundary should be here" lines: vertices of drawn outlines near them move onto them
def _snap_to_line(ln):
    a,b=Point(ln[0]),Point(ln[1]); seg=LineString(ln)
    for n,p in list(UP.items()):
        if p.geom_type!='Polygon': continue
        new=[];ch=False
        for x,y in p.exterior.coords:
            q=Point(x,y)
            if q.distance(a)<3.0: nx,ny=ln[0]; ch=True
            elif q.distance(b)<3.0: nx,ny=ln[1]; ch=True
            elif q.distance(seg)<1.5: pp=nearest_points(seg,q)[0]; nx,ny=pp.x,pp.y; ch=True
            else: nx,ny=x,y
            new.append((nx,ny))
        if ch: UP[n]=one(Polygon(new).buffer(0))
for _id in ('zone_muql8fn4bkgv','line_muql8fn4bkgv','line_muqlouhttukv','line_muqlkp370yta','line_muqkq3efnkzq','line_muqkqi2vcs0p','line_muqkqqlrtakf'):
    if _id in MID and MID[_id]['kind']=='line': _snap_to_line([tuple(q) for q in MID[_id]['pts']])
# E.73: its east boundary is the straight line you drew (162,460.6)-(217.6,367.8)
UP['E.73']=one(Polygon([(98,366),(217.6,367.8),(162,460.6),(155.6,468.3),(146,484),(62.2,428)]).buffer(0))
def _adjust_G_to_line(ln):
    a,b=Point(ln[0]),Point(ln[1]); seg=LineString(ln)
    for n,g in list(G.items()):
        if n in UP or g.geom_type!='Polygon': continue
        new=[];ch=False
        for x,y in g.exterior.coords:
            q=Point(x,y)
            if q.distance(seg)<2.5 and q.distance(a)>0.01 and q.distance(b)>0.01: pp=nearest_points(seg,q)[0]; nx,ny=pp.x,pp.y; ch=True
            else: nx,ny=x,y
            new.append((nx,ny))
        if ch: G[n]=one(Polygon(new).buffer(0))
for _id in ('line_muqnf3c6dyxv','line_muqlkp370yta'):
    if _id in MID: _adjust_G_to_line([tuple(q) for q in MID[_id]['pts']])

UP['E.terrasse']=one(_UU([G['E.terrasse'],UP['E.terrasse']]).buffer(0))
BLOCKS.add('E.schacht-tr2')
if 'E.TR2_E.flur-tr2-1' in PT: rmportal('E.TR2_E.flur-tr2-1')
# nested rooms are cut out of the host (host stays, notch or hole)
UP['E.50a']=one(UP['E.50a'].difference(UP['E.wc-beh-e50a'])); UP['E.50b']=one(UP['E.50b'].difference(UP['E.wc-beh-e50b']))
BLOCKS|={'E.schacht-e37','E.block-tr1','E.schacht-tr4','E.block-tr4-a','E.block-tr4-b','E.block-tr2','E.block-e50','E.block-e52-a','E.block-e52-b','E.lueftung-e41','E.schacht-tr8'}
# --- 1. door removals and moves by id (before any zone change)
for k,m in MID.items():
    if m['kind']=='remove' and m['target'] in PT: rmportal(m['target'])
    elif m['kind']=='remove': PENDING.append(('rm',m['target'],None)); LOG2.append(('rm missing',m['target']))
for k,m in MID.items():
    if m['kind']=='move':
        t=m['target']
        if t in PT:
            p=m['pts']; LN[t]=(p[0][0],p[0][1],p[1][0],p[1][1]); PT[t]['point']=[round((p[0][0]+p[1][0])/2,1),round((p[0][1]+p[1][1])/2,1)]; USER.add(t)
        else: PENDING.append(('mv',t,m['pts'])); LOG2.append(('move missing',t))
PT['E.flur-tr7-2_E.speisesaal']['virtual']=False          # widened double door is a real door
ADDS=[(k,[tuple(q) for q in m['pts']],m.get('text','')) for k,m in MID.items() if m['kind']=='add' and 'e.59 - e.59a' not in m.get('text','')]
# drop all portals of the old hub continuum (re-created from geometry below)
for i in list(PT):
    a,b=ends2(i)
    if 'E.foyer' in (a,b) or {a,b}<= {'E.flur-tr7-1','E.flur-tr7-2'} or i=='E.flur-tr7-2_E.flur-tr7-3': rmportal(i)
# --- 2. zone geometry
HUBOLD=_UU([G[z] for z in ('E.foyer','E.flur-tr7-1','E.flur-tr7-2')])
for z in ('E.foyer','E.flur-tr7-1','E.flur-tr7-2'): DIRTY.append(G.pop(z)); C.pop(z,None)
# batch 3: zones the user removed or replaced; flur-tr2-6 is outside the building
sh=sh.difference(G['E.flur-tr2-6']).buffer(0)
# outer frame pulled back to the outer walls you drew: west edge of the IQ+UKM wing, E.33a bottom, TR3 and the E.34 tip
_cuts=[Polygon([(461,630),(473,631),(320,883)]),
       Polygon([(320,883),(372.7,883.6),(372.7,900),(320,900)]),
       Polygon([(459.3,866.6),(451,879.7),(456.7,888),(447.6,888.1),(447.6,891),(470,891),(470,866.6)]),
       Polygon([(372,886.2),(447.6,888.1),(447.6,891),(372,891)])]
sh=one(sh.difference(_UU(_cuts)).buffer(0))
_sh0=sh; _c=[(x,y) for x,y in sh.exterior.coords]; _o=[]
for x,y in _c:
    if abs(x-545)<1.5 and abs(y-713)<1.5: continue          # kink removed: the east wall is one straight line
    if abs(x-601)<1.5 and abs(y-623)<1.5: x,y=606.5,623.8
    _o.append((x,y))
sh=one(Polygon(_o).buffer(0))
DIRTY.append(sh.difference(_sh0).buffer(0.5))
for z in ('E.technik-tr4-a','E.technik-tr4-b','E.flur-tr2-5','E.flur-tr2-6','E.abstell-e37'):
    DIRTY.append(G.pop(z)); C.pop(z,None)
OLDS={n:G[n] for n in ('E.vorraum-e50','E.50a','E.50b','E.vr-e50b','E.wc-beh-e50b','E.TR9','E.59b','E.aufzug-tr7','E.52','E.41b','E.flur-tr8-6') if n in G}
def apply_zone(n,poly):
    poly=one(poly.buffer(0).intersection(sh))
    if n in G: DIRTY.append(G[n])
    DIRTY.append(poly)
    for o in list(G):
        if o==n or not G[o].intersects(poly): continue
        d=G[o].difference(poly)
        if d.is_empty: DIRTY.append(G.pop(o)); continue
        if G[o].intersection(poly).area>0.05: DIRTY.append(G[o]); G[o]=one(d)
    G[n]=poly
order=['E.terrasse','E.flur-tr7-5','E.flur-tr7-2','E.flur-tr7-1','E.foyer','E.TR9','E.59b','E.aufzug-tr7',
       'E.vorraum-e50','E.block-e50','E.50a','E.wc-beh-e50a','E.vr-e50b','E.50b','E.wc-beh-e50b','E.block-e52-a','E.block-e52-b','E.schacht-tr2','E.schacht-e37','E.block-tr1','E.kueche-ma','E.49','E.48','E.flur-tr1-1','E.flur-tr1-3','E.flur-tr2-1','E.flur-tr2-3','E.flur-tr1-2','E.01','E.vr-e01','E.03','E.vr-e03','E.TR1','E.72b','E.72a','E.82','E.82a','E.73',
       "E.flur-tr4-2", "E.flur-tr4-5", "E.83", "E.83a", "E.82", "E.81", "E.flur-tr4-6", "E.aufzug-tr4", "E.schacht-tr4", "E.block-tr4-a", "E.putzmittel-tr4", "E.75", "E.76", "E.block-tr4-b", "E.74a", "E.vr-e72c", "E.flur-tr4-4", "E.flur-tr4-7", "E.74", "E.flur-tr4-1", "E.TR4", "E.flur-tr4-3", "E.flur-tr4-8", "E.vr-e84", "E.84", "E.80", "E.TR3", "E.lager-tr3", "E.aufzug-tr3", "E.flur-tr3-1", "E.flur-tr3-2", "E.flur-tr2-2", "E.flur-tr2-3", "E.flur-tr1-3", "E.vr-e25b", "E.vr-e25", "E.25b", "E.25a", "E.block-tr2", "E.aufzug-tr2-b", "E.37"]
for n in order: apply_zone(n,UP[n])
# E.flur-tr8-6 reaches x=1174 (the E.41b pocket starts there)
apply_zone('E.flur-tr8-6',Polygon([(959.7,948),(1174,948),(1174,963),(959.7,963)]).intersection(sh))
C.update({'E.flur-tr7-1':True,'E.flur-tr7-2':True,'E.flur-tr7-5':True,'E.foyer':True,'E.block-e50':False,'E.block-e52-a':False,'E.block-e52-b':False,'E.wc-beh-e50a':False,'E.50a':True,'E.50b':False,'E.lueftung-e41':False,'E.schacht-tr8':False})
for z in ('E.flur-tr7-5','E.wc-beh-e50a','E.block-e50','E.block-e52-a','E.block-e52-b'):
    zel['zone-'+z]=ET.Element('x',{'class':'zone '+('service' if z.startswith(('E.block','E.wc')) else 'corridor')})
zel['zone-E.foyer']=ET.Element('x',{'class':'zone hall'})
# batch 3 flags and classes
for z in ('E.flur-tr4-5','E.flur-tr4-6','E.flur-tr4-7','E.flur-tr4-8','E.flur-tr3-2','E.flur-tr2-3','E.flur-tr1-3','E.vr-e72c','E.vr-e84','E.vr-e25b'): C[z]=True
for z in ('E.schacht-e37','E.block-tr1','E.kueche-ma','E.schacht-tr2','E.schacht-tr4','E.block-tr4-a','E.block-tr4-b','E.block-tr2','E.putzmittel-tr4','E.lager-tr3'): C[z]=False
C['E.49']=True
for z in ('E.flur-tr4-5','E.flur-tr4-6','E.flur-tr4-7','E.flur-tr4-8','E.flur-tr3-2','E.flur-tr2-3','E.flur-tr1-3'): zel['zone-'+z]=ET.Element('x',{'class':'zone corridor'})
for z in ('E.schacht-e37','E.block-tr1','E.kueche-ma','E.schacht-tr2','E.vr-e72c','E.vr-e84','E.vr-e25b','E.schacht-tr4','E.block-tr4-a','E.block-tr4-b','E.block-tr2','E.putzmittel-tr4','E.lager-tr3'): zel['zone-'+z]=ET.Element('x',{'class':'zone service'})
# --- 3. gap fill inside the touched area: leftovers go to the neighbour sharing the longest edge
_dirty=_UU([g.buffer(10) for g in DIRTY]).intersection(sh)
def _fill():
    U=_UU(list(G.values())); n_=0
    for frag in _polys(_dirty.difference(U)):
        if frag.area<0.05: continue
        near=[n for n in G if n not in BLOCKS and G[n].distance(frag)<0.4]
        if not near: continue
        shell_edge=frag.intersects(sh.exterior.buffer(0.5))
        pref=[n for n in near if n not in UP or shell_edge] or near      # drawn outlines do not grow into gaps
        fs=_faces(frag,pref)
        if False: print('FILL',round(frag.area),[round(v) for v in frag.bounds],'pref',pref,'faces',[(round(f.area),o) for f,o in fs])
        for f,o in fs: G[o]=one(_merge(G[o],f)); n_+=1
    return n_
LOG2.append(('gap fragments filled',_fill()+_fill()+_fill()))
# tidy: simplify touched zones, clip touched zones to the shell
for z in list(G):
    if G[z].intersects(_dirty):
        g=G[z].simplify(0)
        if g.difference(sh.buffer(0.3)).area>0.5: g=g.intersection(sh.buffer(0.01))
        if not g.is_empty: G[z]=one(g)
# E.flur-tr1-3 is the short corridor piece between E.flur-tr1-1 and E.flur-tr2-1: nothing of those two may run past its end edges
def _edges(poly):
    c=list(poly.exterior.coords); return [(c[k],c[k+1]) for k in range(len(c)-1)]
_t=UP['E.flur-tr1-3']; _ed=_edges(_t)
_top=min(_ed,key=lambda e:(e[0][1]+e[1][1])/2); _bot=max(_ed,key=lambda e:(e[0][1]+e[1][1])/2 if abs(e[0][1]-e[1][1])<3 else -1)
def _keep_side(zone,edge,keep_pt):
    (x1,y1),(x2,y2)=edge; dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy); ux,uy=dx/L,dy/L; nx,ny=-uy,ux
    sgn=1 if (keep_pt[0]-x1)*nx+(keep_pt[1]-y1)*ny>0 else -1
    big=400; hp=Polygon([(x1-ux*big,y1-uy*big),(x2+ux*big,y2+uy*big),(x2+ux*big+sgn*nx*big,y2+uy*big+sgn*ny*big),(x1-ux*big+sgn*nx*big,y1-uy*big+sgn*ny*big)])
    return hp
for _zn,_edge,_far in (('E.flur-tr1-1',_top,_t.centroid.coords[0]),('E.flur-tr2-1',_bot,_t.centroid.coords[0])):
    _tail=G[_zn].intersection(_keep_side(_zn,_edge,_far))          # the part on the tr1-3 side of the edge line
    _tail=_tail.difference(UP['E.flur-tr1-3'])
    if _tail.area<0.3: continue
    G[_zn]=one(G[_zn].difference(_tail))
    for _p in _polys(_tail):
        if _p.geom_type!='Polygon' or _p.area<0.05: continue
        _nb=[c for c in G if c not in (_zn,'E.flur-tr1-3','E.flur-tr1-1','E.flur-tr2-1','E.flur-tr2-3') and c not in BLOCKS and G[c].distance(_p)<0.4]
        if _nb:
            for f,o in _faces(_p,_nb): G[o]=one(_merge(G[o],f))
        else: G['E.flur-tr1-3']=one(_merge(G['E.flur-tr1-3'],_p)); UP['E.flur-tr1-3']=G['E.flur-tr1-3']
    LOG2.append(('trimmed junction tail',_zn,round(_tail.area,1)))
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
        _k=lambda z:(zel.get('zone-'+z).get('class').split()[-1] if zel.get('zone-'+z) is not None else 'room')
        room=[z for z in (a,b) if z in G and z not in BLOCKS and _k(z) not in ('corridor','stair') and (not C.get(z,False) or _k(z)=='room')]
        if room and (pr is None or all(C.get(z,False) for z in pr)) and room[0] not in (pr or ()):
            r=room[0]; x1,y1,x2,y2=LN[i]; mid=Point((x1+x2)/2,(y1+y2)/2); best=None
            for n,g in G.items():
                if n==r or not C.get(n,False) or n in BLOCKS: continue
                sg=G[r].boundary.intersection(g.buffer(0.4))
                if sg.is_empty or sg.length<3: continue
                d=sg.distance(mid)
                if best is None or d<best[0]: best=(d,n,sg)
            if best and best[0]<200:
                q=nearest_points(best[2],mid)[0]; dx,dy=q.x-mid.x,q.y-mid.y
                ni=i if tuple(sorted((r,best[1])))==tuple(sorted((a,b))) else newid(r,best[1]); u=i in USER
                LN[i]=(x1+dx,y1+dy,x2+dx,y2+dy); PT[i]['point']=[round(mid.x+dx,1),round(mid.y+dy,1)]
                if ni!=i: renameportal(i,ni)
                if u: USER.discard(i); USER.add(ni)
                LOG2.append(('relocated',i,ni,round(math.hypot(dx,dy),1))); continue
        if pr and 'exterior' not in pr:
            u=i in USER; ni=newid(*pr); renameportal(i,ni); (USER.discard(i),USER.add(ni)) if u else None; LOG2.append(('reparent',i,ni))
        elif a not in G or b not in G: rmportal(i); LOG2.append(('DROPPED',i,pr))
        elif C.get(a,False) and C.get(b,False) and pr is None: rmportal(i); LOG2.append(('DROPPED',i,'both crossable, no longer adjacent'))
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
    ni=newid(*pr); vt_=(t=='virtual'); addportal(ni,vt_,(l[0],l[1]),(l[2],l[3])); (None if vt_ else USER.add(ni))
    if 'exterior' in ni: PT[ni]['emergency_exit']=True; LOG2.append(('add',ni,t))
# a door you drew for a pair replaces the doors assumed earlier for the same pair
_pairs={}
for i in list(PT):
    a,b=ends2(i)
    if 'exterior' in (a,b) or PT[i]['virtual']: continue
    _pairs.setdefault(tuple(sorted((a,b))),[]).append(i)
for _k,_l in _pairs.items():
    _u=[i for i in _l if i in USER]
    if _u:
        for i in _l:
            if i not in USER: rmportal(i); LOG2.append(('superseded',i))
# assumed: the E.84 Vorraum opens to the corridor (no door was marked)
_sg=G['E.vr-e84'].boundary.intersection(G['E.flur-tr4-5'].buffer(0.4))
_ls=[g for g in _polys(_sg) if g.geom_type=='LineString']
if _ls:
    _g=max(_ls,key=lambda q:q.length); _m=_g.interpolate(0.5,normalized=True); _c=list(_g.coords); _dx,_dy=_c[-1][0]-_c[0][0],_c[-1][1]-_c[0][1]; _L=math.hypot(_dx,_dy) or 1; _h=min(5.5,_g.length/2)
    ni=newid('E.flur-tr4-5','E.vr-e84'); addportal(ni,False,(_m.x-_dx/_L*_h,_m.y-_dy/_L*_h),(_m.x+_dx/_L*_h,_m.y+_dy/_L*_h)); LOG2.append(('assumed door',ni))
# TR8 west door = emergency exit
for i in list(PT):
    if i.endswith('_exterior') and 'E.TR8' in i: PT[i]['emergency_exit']=True
# removals and moves aimed at doors that only exist after your door marks were resolved
for _kind,_t,_p in PENDING:
    if _t not in PT: continue
    if _kind=='rm': rmportal(_t); LOG2.append(('late removal',_t))
    elif not PT[_t]['virtual']:
        LN[_t]=(_p[0][0],_p[0][1],_p[1][0],_p[1][1]); PT[_t]['point']=[round((_p[0][0]+_p[1][0])/2,1),round((_p[0][1]+_p[1][1])/2,1)]; USER.add(_t); LOG2.append(('late move',_t))
# --- 6. virtual portals between consecutive hub pieces and the corridor beside the Terrasse
HUB=['E.flur-tr7-1','E.flur-tr7-2','E.flur-tr7-5','E.flur-tr7-3','E.flur-tr7-4','E.flur-tr9-3','E.flur-tr4-1','E.flur-tr4-2','E.flur-tr4-3','E.flur-tr4-4','E.flur-tr4-5','E.flur-tr4-6','E.flur-tr4-7','E.flur-tr4-8','E.flur-tr2-1','E.flur-tr2-2','E.flur-tr2-3','E.flur-tr2-4','E.flur-tr1-1','E.flur-tr1-2','E.flur-tr1-3','E.flur-tr3-1','E.flur-tr3-2']
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
# --- 6b. user-drawn outlines win: whatever a zone gained beyond its drawn polygon goes back to its neighbours
def _trim(n):
    ex=G[n].difference(UP[n])
    ex=_UU([p for p in _polys(ex) if p.area>0.3])
    if ex.is_empty or ex.area<4: return
    G[n]=one(G[n].intersection(UP[n]))
    for z in UP:                                   # neighbours whose own outline lost area take it back first
        if z==n or z not in G: continue
        t=ex.intersection(UP[z])
        if t.area>0.3:
            G[z]=one(_merge(G[z],t)); ex=ex.difference(t)
    for piece in _polys(ex):
        if piece.area<0.3: continue
        nbrs=[c for c in G if c!=n and c not in BLOCKS and G[c].distance(piece)<0.4]
        if not nbrs: continue
        for f,o in _faces(piece,nbrs): G[o]=one(_merge(G[o],f))
    LOG2.append(('trimmed',n,round(ex.area)))
for n in sorted([n for n in UP if n in G],key=lambda n:-G[n].difference(UP[n]).area):
    _trim(n)
for _a,_b in itertools.combinations(list(G),2):
    if G[_a].intersects(G[_b]) and G[_a].intersection(G[_b]).area>0.05:
        _lo=_b if (_b not in UP or _a in UP and G[_b].area>=G[_a].area) else _a
        _hi=_a if _lo==_b else _b
        G[_lo]=one(G[_lo].difference(G[_hi]))
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
            LOG2.append(('wall',i,gainer,loser,round(strip.area,1),round(math.hypot(dx,dy),1))); WALLS.append((i,gainer,loser,strip,round(math.hypot(dx,dy),1)))
            G[gainer]=one(_merge(G[gainer],strip)); G[loser]=one(G[loser].difference(strip)); nadapt+=1; continue
    LN[i]=(x1+dx,y1+dy,x2+dx,y2+dy); PT[i]['point']=[round((x1+x2)/2+dx,1),round((y1+y2)/2+dy,1)]; nsnap2+=1
# --- 7b. remaining off-boundary doors: snap to the nearest point of the shared boundary
for i in list(PT):
    a,b=ends2(i)
    if a=='exterior' or b=='exterior' or a not in G or b not in G: continue
    x1,y1,x2,y2=LN[i]; mid=Point((x1+x2)/2,(y1+y2)/2)
    if max(mid.distance(G[a].boundary),mid.distance(G[b].boundary))<=0.6: continue
    best=None
    for r_ in (3.7,6.5,10.0):
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
# virtual portals follow the final shared boundaries exactly
from shapely.ops import linemerge as _lm
def _shared(a,b):
    sb=G[a].boundary.intersection(G[b].buffer(0.05)); ls=[g for g in _polys(sb) if g.geom_type in ('LineString','MultiLineString')]
    segs=[]
    for g in ls: segs+= list(g.geoms) if hasattr(g,'geoms') else [g]
    if not segs: return None
    m=_lm(segs); m=list(m.geoms) if hasattr(m,'geoms') else [m]
    best=max(m,key=lambda q:q.length).simplify(0.3)
    c=list(best.coords); k=max(range(len(c)-1),key=lambda j:math.dist(c[j],c[j+1]))
    return LineString([c[k],c[k+1]])
for i in list(PT):
    a,b=ends2(i)
    if not PT[i]['virtual'] or 'exterior' in (a,b) or a not in G or b not in G: continue
    g=_shared(a,b)
    if g is not None and g.length>=1.5:
        c=list(g.coords); LN[i]=(c[0][0],c[0][1],c[-1][0],c[-1][1]); PT[i]['point']=[round((c[0][0]+c[-1][0])/2,1),round((c[0][1]+c[-1][1])/2,1)]
_have={tuple(sorted(ends2(i))) for i in PT}
for a_,b_ in itertools.combinations(HUB,2):
    if a_ not in G or b_ not in G or tuple(sorted((a_,b_))) in _have: continue
    g=_shared(a_,b_)
    if g is not None and g.length>=3:
        c=list(g.coords); addportal(sortid(a_,b_),True,c[0],c[-1]); LOG2.append(('virtual',sortid(a_,b_),round(g.length,1)))
# you removed every door between E.76 and E.flur-tr4-4
for _i in list(PT):
    if sorted(ends2(_i))==['E.76','E.flur-tr4-4']: rmportal(_i); LOG2.append(('late removal',_i))
# walls between neighbouring rooms along the TR3 corridor are straight (they came out of the gap split as gentle curves)
_row=['E.23','E.28','E.30','E.32','E.34','E.27','E.29','E.31','E.33','E.25b']
for _a,_b in itertools.combinations(_row,2):
    if _a not in G or _b not in G: continue
    _l=_shared(_a,_b) if False else None
    _sb=G[_a].boundary.intersection(G[_b].buffer(0.05)); _ls=[g for g in _polys(_sb) if g.geom_type in('LineString','MultiLineString')]
    _segs=[]
    for g in _ls: _segs+=list(g.geoms) if hasattr(g,'geoms') else [g]
    if not _segs: continue
    _m=_lm(_segs); _m=list(_m.geoms) if hasattr(_m,'geoms') else [_m]
    _L=max(_m,key=lambda q:q.length)
    if _L.length<6: continue
    _c=list(_L.coords); _ch=LineString([_c[0],_c[-1]])
    _dev=max(Point(q).distance(_ch) for q in _c)
    if _dev<0.2 or _dev>3.5: continue
    _lens=Polygon(_c).buffer(0)
    if _lens.is_empty or _lens.area<0.05: continue
    for _p in _polys(_lens):
        if _p.geom_type!='Polygon': continue
        _own=_a if G[_a].intersection(_p).area>=G[_b].intersection(_p).area else _b; _oth=_b if _own==_a else _a
        G[_own]=one(G[_own].difference(_p)); G[_oth]=one(_merge(G[_oth],_p))
# blocks have no doors; assumed doors that no longer sit on any shared wall are dropped (restored below only if a room would be cut off)
for i in list(PT):
    a,b=ends2(i)
    if a in BLOCKS or b in BLOCKS: rmportal(i); LOG2.append(('block door removed',i)); continue
    if 'exterior' in (a,b) or PT[i]['virtual'] or i in USER or a not in G or b not in G: continue
    x1,y1,x2,y2=LN[i]; mid=Point((x1+x2)/2,(y1+y2)/2)
    _sg=_shared(a,b)
    if max(mid.distance(G[a].boundary),mid.distance(G[b].boundary))>2.5 or _sg is None or _sg.length<1.5: rmportal(i); LOG2.append(('stale door dropped',i))
# the WC group beside TR2 is fully drawn by you: the doors assumed for it earlier are dropped
for i in list(PT):
    a,b=ends2(i)
    if i not in USER and not PT[i]['virtual'] and ({a,b}&{'E.25a','E.25b','E.vr-e25','E.vr-e25b'}) and 'exterior' not in (a,b): rmportal(i); LOG2.append(('stale door dropped',i))
# every room that touches circulation must be reachable: restore a dropped door where nothing else connects it
def _reach():
    adj={}
    for i in PT:
        a,b=ends2(i); adj.setdefault(a,set()).add(b); adj.setdefault(b,set()).add(a)
    seen={'E.01'}; st=['E.01']
    while st:
        u=st.pop()
        if u!='E.01' and not C.get(u,False) and u!='exterior': continue
        for v in adj.get(u,()):
            if v not in seen: seen.add(v); st.append(v)
    return seen
_keep=set()
for _z in sorted(G):
    if _z in BLOCKS or _z in _keep or _z in _reach(): continue
    nbs=[n for n in G if n!=_z and n not in BLOCKS and C.get(n,False) and n in _reach()]
    best=None
    for n in nbs:
        g=_shared(_z,n)
        if g is not None and g.length>=4 and (best is None or g.length>best[0].length): best=(g,n)
    if best:
        g,n=best; m=g.interpolate(0.5,normalized=True); c=list(g.coords); dx,dy=c[-1][0]-c[0][0],c[-1][1]-c[0][1]; L=math.hypot(dx,dy) or 1; h=min(5.5,g.length/2)
        ni=newid(_z,n); addportal(ni,False,(m.x-dx/L*h,m.y-dy/L*h),(m.x+dx/L*h,m.y+dy/L*h)); LOG2.append(('restored door',ni))
LOG2.append(('walls moved to doors',nadapt,'doors snapped to walls',nsnap2))
for l in LOG2:
    if l[0] in ('late removal','late move','UNRESOLVED','ADD UNRESOLVED','door off wall','block door removed','stale door dropped','restored door','superseded','trimmed junction tail','trimmed','assumed door','DROPPED','relocated','walls moved to doors','gap fragments filled','exit reparent','exit door'): print('B2',l)
print('B2 reparents',[l[1:] for l in LOG2 if l[0]=='reparent'])
print('B2 adds',[l[1:] for l in LOG2 if l[0]=='add'])
print('B2 virtual',[l[1:] for l in LOG2 if l[0]=='virtual'])
