import json,math,itertools
exec(open('fixed.py').read().split("# ================= validation")[0])
from shapely.geometry import LineString,Polygon,Point,MultiPolygon
from shapely.ops import unary_union,nearest_points
R=lambda v:round(v,1)
def pl(g):
    g=max(g.geoms,key=lambda x:x.area) if hasattr(g,'geoms') else g
    return [[R(x),R(y)] for x,y in list(g.exterior.coords)[:-1]]
def ln(a,b): return [[R(a[0]),R(a[1])],[R(b[0]),R(b[1])]]
nb={}
for i in PT:
    a,b=ends2(i); nb.setdefault(a,set()).add(b); nb.setdefault(b,set()).add(a)
SG=[]
def add(**k): k['id']='s%02d'%(len(SG)+1); SG.append(k)
# ---- hand-authored: evidence and connectivity
for z,txt in (('E.elt-vert-tr5','Elt vertical shaft'),('E.technik-tr5','technical room')):
    if z in G:
        ps=[i for i in PT if z in ends2(i)]
        add(cat='Evidence',prio=3,title=f'{z} ({txt}): block or keep the assumed door?',
         why='Same pattern as the Installationsschacht and the Lüftung: spaces you treated as inaccessible when no door is visible. This door was assumed in the Claude Design pass, not read from the plan.',
         act=f'Accept = make {z} a block and remove its door(s) {", ".join(ps)}. Reject = keep as is.',
         hl=[{'t':'poly','p':pl(G[z])}]+[{'t':'line','p':ln(LN[i][:2],LN[i][2:])} for i in ps],pr=[])
# ---- gaps
U=unary_union(list(G.values())); gp=sh.difference(U)
gs=sorted([g for g in getattr(gp,'geoms',[gp]) if g.area>=12],key=lambda g:-g.area)
for g in gs[:10]:
    best=None
    for n,zg in G.items():
        if n in BLOCKS: continue
        L=g.boundary.intersection(zg.buffer(0.3)).length
        sc=(1 if C.get(n) else 0,L)
        if L>0.5 and (best is None or sc>best[0]): best=(sc,n)
    if not best: continue
    n=best[1]; c=g.representative_point()
    add(cat='Coverage',prio=2,title=f'Gap of {round(g.area)} units² at ({round(c.x)},{round(c.y)})',
     why='Zones must cover the shell without gaps. Left over from the Claude Design merge.',
     act=f'Accept = give the gap to {n} (longest shared edge, crossable preferred).',
     hl=[{'t':'poly','p':pl(g),'k':'gap'}],pr=[{'t':'note','p':[R(c.x),R(c.y)],'x':'→ '+n}])
out=U.difference(sh)
for g in sorted([g for g in getattr(out,'geoms',[out]) if g.area>=5],key=lambda g:-g.area)[:4]:
    c=g.representative_point(); n=min(G,key=lambda z:G[z].distance(c))
    add(cat='Coverage',prio=2,title=f'{round(g.area)} units² of {n} sticks out of the shell',
     why='Zones must stay inside the shell.',act=f'Accept = clip {n} to the shell.',hl=[{'t':'poly','p':pl(g),'k':'out'}],pr=[])
# ---- doors off boundary (real doors only)
for i,l in LN.items():
    a,b=ends2(i)
    if 'exterior' in (a,b) or PT[i]['virtual'] or a not in G or b not in G: continue
    m=Point((l[0]+l[2])/2,(l[1]+l[3])/2); d=max(m.distance(G[a].boundary),m.distance(G[b].boundary))
    if d>0.6:
        sgs=G[a].boundary.intersection(G[b].buffer(2.0)); q=nearest_points(sgs,m)[0]
        add(cat='Doors',prio=3,title=f'{i}: {d:.1f} off the shared boundary',
         why='Doors sit on the zone outline (≤0.6).',act='Accept = snap the door onto the boundary.',
         hl=[{'t':'line','p':ln(l[:2],l[2:])}],pr=[{'t':'line','p':ln((l[0]+q.x-m.x,l[1]+q.y-m.y),(l[2]+q.x-m.x,l[3]+q.y-m.y))}])
# ---- wall dents from door-driven wall moves
for (i,gn,lo,st,off) in WALLS:
    if st.is_empty or off<2.0: continue
    l=LN[i]
    add(cat='Walls',prio=3,title=f'Wall dent at {i} ({off} units, {round(st.area)} units²)',
     why='I moved the wall onto your door. In a long straight wall that leaves a dent and an uneven corridor edge. Your rule allows either way (adapt wall to door, or door to wall).',
     act='Accept = straighten the wall again and snap the door to it (the door moves '+str(off)+' units). Reject = keep the dent, as now.',
     hl=[{'t':'poly','p':pl(st),'k':'dent'},{'t':'line','p':ln(l[:2],l[2:])}],pr=[])
# ---- convexity cuts
def cut_for(z):
    g=G[z]; co=list(g.exterior.coords)[:-1]
    # dedupe
    pts=[co[0]]
    for p in co[1:]:
        if math.dist(p,pts[-1])>0.3: pts.append(p)
    if len(pts)>2 and math.dist(pts[0],pts[-1])<=0.3: pts.pop()
    n=len(pts); ccw=Polygon(pts).exterior.is_ccw; best=None
    for k in range(n):
        p0,p1,p2=pts[k-1],pts[k],pts[(k+1)%n]
        cr=(p1[0]-p0[0])*(p2[1]-p1[1])-(p1[1]-p0[1])*(p2[0]-p1[0])
        refl = cr<-1 if ccw else cr>1
        if not refl: continue
        for d in ((p1[0]-p0[0],p1[1]-p0[1]),(p1[0]-p2[0],p1[1]-p2[1])):
            L=math.hypot(*d); 
            if L<1e-6: continue
            ux,uy=d[0]/L,d[1]/L; far=(p1[0]+ux*600,p1[1]+uy*600)
            seg=LineString([(p1[0]+ux*0.05,p1[1]+uy*0.05),far]).intersection(g.buffer(0.01))
            if seg.is_empty: continue
            seg=seg if seg.geom_type=='LineString' else max(seg.geoms,key=lambda s:s.length)
            q=list(seg.coords)[-1]
            cand=(math.hypot(q[0]-p1[0],q[1]-p1[1]),p1,q)
            if best is None or cand[0]<best[0]: best=cand
    return best
for z in G:
    if not C.get(z) or z in BLOCKS: continue
    ps=[i for i in PT if z in ends2(i)]; w=0;n=0
    for a,b in itertools.combinations(ps,2):
        o=LineString([PT[a]['point'],PT[b]['point']]).difference(G[z].buffer(0.8))
        if o.length>3: n+=1; w=max(w,o.length)
    if not n: continue
    c=cut_for(z)
    add(cat='Shape',prio=3,title=f'{z} is not convex: {n} route segment(s) leave it (worst {round(w)} units)',
     why='Zones are split so a straight line between any two portals stays inside (your convexity rule, as agreed for E.41 and E.52).',
     act='Accept = split along the proposed cut; the two halves get a virtual portal along it. Some of these may disappear once the gap and wall items above are settled.',
     hl=[{'t':'poly','p':pl(G[z])}],pr=([{'t':'line','p':ln(c[1],c[2]),'k':'cut'}] if c else []))
for s_ in SG:
    pts=[q for o in s_['hl']+s_['pr'] for q in (o['p'] if isinstance(o['p'][0],list) else [o['p']])]
    xs=[q[0] for q in pts]; ys=[q[1] for q in pts]; s_['bb']=[min(xs),min(ys),max(xs),max(ys)]
json.dump(SG,open('sugg.json','w'))
print(len(SG)); 
for s in SG: print(s['id'],s['cat'],s['prio'],s['title'][:90])
