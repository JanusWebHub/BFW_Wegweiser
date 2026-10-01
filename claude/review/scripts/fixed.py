import sys,json,math,heapq,itertools;sys.path.insert(0,'.')
exec(open('graph.py').read().split("# components of crossable graph")[0])
from shapely.geometry import Polygon,LineString,Point,box
from shapely.ops import unary_union as UU, nearest_points
from collections import defaultdict
G={n:g for n,g in Z.items()}                       # zone polygons
C={n:v['crossable'] for n,v in JZ.items()}         # crossability
PT={i:dict(v) for i,v in JP.items()}               # portal json attrs (virtual, point, flags)
LN={i:tuple(P[i]['line']) for i in JP}             # portal svg line
sh=shell['shell-outline'][1]
log=[]
def addportal(i,virtual,a,b,pt=None,**fl):
    pt=pt or ((a[0]+b[0])/2,(a[1]+b[1])/2)
    PT[i]=dict(virtual=virtual,point=[round(pt[0],1),round(pt[1],1)],**fl); LN[i]=(a[0],a[1],b[0],b[1])
def rmportal(i): PT.pop(i,None); LN.pop(i,None)
def renameportal(old,new):
    PT[new]=PT.pop(old); LN[new]=LN.pop(old)
def left_of(A,B,far=-3000):
    dx,dy=B[0]-A[0],B[1]-A[1]; A2=(A[0]-dx*3,A[1]-dy*3); B2=(B[0]+dx*3,B[1]+dy*3)
    return Polygon([A2,B2,(far,B2[1]),(far,A2[1])])
def one(g):
    g=g.buffer(0)
    return g if g.geom_type=='Polygon' else max(g.geoms,key=lambda x:x.area)
CH=set()
def ends2(i):
    parts=i.split('_')
    if parts[-1].isdigit() and len(parts)==3: parts=parts[:2]
    return parts
# ---- A fire door + re-cut + E.37 door
dA,dB=(606.3,545.0),(632.9,594.0)
U=UU([G['E.flur-tr2-1'],G['E.flur-tr7-3']]); Lh=left_of(dA,dB)
G['E.flur-tr2-1']=one(U.intersection(Lh)); G['E.flur-tr7-3']=one(U.difference(Lh)); CH|={'E.flur-tr2-1','E.flur-tr7-3'}
addportal('E.flur-tr2-1_E.flur-tr7-3',False,dA,dB)
rmportal('E.37_E.flur-tr7-3'); addportal('E.37_E.flur-tr2-1',False,(616.5,594),(627.5,594),(622,594))
# ---- B TR2 junction
rh=Polygon([(525,536),(557,586),(532,625),(502,580)])
rest=G['E.TR2'].difference(rh)
pas=UU([G['E.flur-tr2-2'],G['E.flur-tr2-3'],rest]).buffer(0.01).buffer(-0.01).difference(Polygon([(440,540),(463,540),(463,600),(440,600)]))
G['E.TR2']=rh; G['E.flur-tr2-2']=one(pas); del G['E.flur-tr2-3']; C.pop('E.flur-tr2-3')
G['E.flur-tr2-4']=one(UU([G['E.flur-tr2-4'],Polygon([(450,556),(463,556),(463,593),(450,593)])])); CH|={'E.TR2','E.flur-tr2-2','E.flur-tr2-4'}
rmportal('E.flur-tr2-2_E.flur-tr2-3'); rmportal('E.TR2_E.flur-tr2-3'); renameportal('E.TR2_E.flur-tr2-6','E.flur-tr2-2_E.flur-tr2-6')
addportal('E.flur-tr2-2_E.flur-tr2-4',False,(463,556),(463,593),(463,574.5))
# ---- C TR7/TR9
eA,eB=(1011.0,481.0),(1037.0,528.3)
T=Polygon([(1010.5,480),(1050,480),(1050,528),(1037,528.3)])
G['E.flur-tr9-3']=one(UU([G['E.flur-tr9-3'],T]).buffer(0.01).buffer(-0.01)); G['E.flur-tr7-1']=one(G['E.flur-tr7-1'].difference(T)); CH|={'E.flur-tr9-3','E.flur-tr7-1'}
addportal('E.flur-tr7-1_E.flur-tr9-3',False,eA,eB)
# ---- D content blockers
C['E.33']=True; C['E.flur-tr2-5']=False; C['E.flur-tr2-6']=False
b=G['E.53.1'].boundary.intersection(G['E.53.2'].boundary)
if b.geom_type=='LineString': a_,b_=b.coords[0],b.coords[-1]
else: ls=max(b.geoms,key=lambda g:g.length); a_,b_=ls.coords[0],ls.coords[-1]
addportal('E.53.1_E.53.2',True,a_,b_)
# E.48 exit: nearest shell edge direction
p=Point(646.4,668.7); q=nearest_points(sh.exterior,p)[0]
cs=list(sh.exterior.coords); best=None
for k in range(len(cs)-1):
    s=LineString([cs[k],cs[k+1]]); d=s.distance(p)
    if best is None or d<best[0]: best=(d,cs[k],cs[k+1])
ux,uy=best[2][0]-best[1][0],best[2][1]-best[1][1]; L=math.hypot(ux,uy); ux/=L; uy/=L
addportal('E.48_exterior',False,(q.x-5.5*ux,q.y-5.5*uy),(q.x+5.5*ux,q.y+5.5*uy),(q.x,q.y),emergency_exit=True)
# ---- E overlaps clipping
S8={'E.flur-tr2-5','E.flur-tr2-6','E.53.1','E.53.2','E.56a','E.48','E.49','E.speisesaal'}
for n in S8: G[n]=one(G[n].intersection(sh)); CH.add(n)
names=list(G)
for _ in range(2):
    from shapely.strtree import STRtree
    tr=STRtree([G[n] for n in names])
    for ia,a in enumerate(names):
        for j in tr.query(G[a]):
            bn=names[j]
            if j<=ia: continue
            ar=G[a].intersection(G[bn]).area
            if ar<0.05: continue
            if (a in S8)!=(bn in S8): lo=a if a in S8 else bn
            elif a in S8: lo=a if G[a].area>G[bn].area else bn
            else: lo=a if 'flur' in a else bn if 'flur' in bn else (a if G[a].area>G[bn].area else bn)
            hi=bn if lo==a else a
            G[lo]=one(G[lo].difference(G[hi])); CH.add(lo)
# ---- G E.62 has no door to R.58; rename R.58 -> E.58
rmportal('E.62_R.58')
def sortid(a,b,suf=''): x=sorted([a,b]); return x[0]+'_'+x[1]+suf
for i in list(PT):
    a,b=ends2(i)
    if 'R.58' in (a,b):
        o=b if a=='R.58' else a; suf=i[len(a)+1+len(b):]
        renameportal(i,sortid('E.58',o,suf))
G['E.58']=G.pop('R.58'); C['E.58']=C.pop('R.58'); CH.add('E.58')
zel['zone-E.58']=zel['zone-R.58']
# ---- F re-snap portals of changed zones
nsnap=0
for i in list(PT):
    a,b=ends2(i)
    if a=='exterior' or b=='exterior': continue
    if a not in CH and b not in CH: continue
    x1,y1,x2,y2=LN[i]; mid=Point((x1+x2)/2,(y1+y2)/2)
    d=max(mid.distance(G[a].boundary),mid.distance(G[b].boundary))
    if d>0.6:
        cand=G[a].boundary.intersection(G[b].buffer(1.5))
        if cand.is_empty: continue
        q=nearest_points(cand,mid)[0]; dx,dy=q.x-mid.x,q.y-mid.y
        LN[i]=(x1+dx,y1+dy,x2+dx,y2+dy); PT[i]['point']=[round(q.x,1),round(q.y,1)]; nsnap+=1
print('snapped',nsnap)

# ================= validation of the fixed graph
def ends(i): return ends2(i)
adj=defaultdict(set)
for i in PT:
    a,b=ends(i); adj[a].add(b); adj[b].add(a)
def reach_from(s):
    seen={s};st=[s]
    while st:
        u=st.pop()
        if u!=s and not C[u]: continue
        for v in adj[u]:
            if v not in seen: seen.add(v);st.append(v)
    return seen
zones_all=[z for z in G]+['exterior']
cz=[z for z in G if C[z]]
comp={};k=0
for z in cz:
    if z in comp: continue
    k+=1;st=[z];comp[z]=k
    while st:
        u=st.pop()
        for v in adj[u]:
            if v in C and C[v] and v not in comp and v!='exterior': comp[v]=k;st.append(v)
print('crossable components (no exterior):',k)
for s in ['E.52','E.01','E.72a']:
    r=reach_from(s); print(s,'unreachable:',sorted(set(zones_all)-r))
rows=[]
nm=list(G); tr=STRtree([G[n] for n in nm])
ov=0
for ia,a in enumerate(nm):
    for j in tr.query(G[a]):
        if j<=ia: continue
        ar=G[a].intersection(G[nm[j]]).area
        if ar>0.5: ov+=ar; rows.append((nm[ia],nm[j],round(ar,1)))
print('overlaps>0.5:',rows,'total',round(ov,1))
U=UU(list(G.values())); print('gap',round(sh.difference(U).area),'outside shell',round(U.difference(sh).area))
off=[]
for i in PT:
    a,b=ends(i)
    if a=='exterior' or b=='exterior': continue
    x1,y1,x2,y2=LN[i]; ln=LineString([(x1,y1),(x2,y2)])
    d=max(max(Point(c).distance(G[z].boundary) for c in [(x1,y1),(x2,y2),((x1+x2)/2,(y1+y2)/2)]) for z in (a,b))
    if d>0.6: off.append((i,round(d,2)))
print('portals off boundary >0.6:',off)
print('zones',len(G),'portals',len(PT),'virtual',sum(1 for v in PT.values() if v['virtual']),'exits',sum(1 for i in PT if 'exterior' in ends(i)))

# ================= routing graph
os_=__import__('os'); os_.makedirs('review/routing',exist_ok=True)
zp=defaultdict(list)
for i in PT:
    for e in ends(i):
        if e!='exterior': zp[e].append(i)
SEG={}
for z,ps in zp.items():
    if not C[z]: SEG[z]=[]; continue
    SEG[z]=[]
    for a,b in itertools.combinations(sorted(ps),2):
        pa,pb=PT[a]['point'],PT[b]['point']
        SEG[z].append({'portals':[a,b],'geometry':[pa,pb],'distance_m':round(math.dist(pa,pb)/upm,2)})
nseg=sum(len(v) for v in SEG.values()); print('segments',nseg)
cg={'format':'wegweiser-connectivity-graph','version':1,'provenance':'unverified',
 'floors':J['floors'],
 'zones':{'exterior':{'crossable':False},**{z:{'floor':'E','crossable':C[z]} for z in G}},
 'portals':PT}
json.dump(cg,open('review/routing/connectivity-graph-fixed.json','w'),indent=1)
json.dump({**{k:v for k,v in cg.items() if k!='portals'} ,'format':'wegweiser-routing-graph','portals':PT,'segments':SEG,'state_costs':{},'segment_costs':{},'variants':{'standard':[]}},open('review/routing/routing-graph-fixed.json','w'),indent=1)
def route(s,t):
    pq=[];best={}
    for i in PT:
        e=ends(i)
        if s in e:
            o=e[0] if e[1]==s else e[1]
            heapq.heappush(pq,(0,(i,o),[(s,None),(o,i)]))
    while pq:
        d,(pi,z),path=heapq.heappop(pq)
        if (pi,z) in best: continue
        best[(pi,z)]=d
        if z==t: return d/upm,path
        if not C.get(z,False): continue
        for pj in zp.get(z,[]):
            if pj==pi: continue
            e=ends(pj); o=e[0] if e[1]==z else e[1]
            if o==s: continue
            heapq.heappush(pq,(d+math.dist(PT[pi]['point'],PT[pj]['point']),(pj,o),path+[(o,pj)]))
    return None,None
ROUTES=[('E.01','E.52'),('E.72a','E.62'),('E.90','E.60a'),('E.34','E.41a'),('E.33a','E.02')]
RT={}
for s,t in ROUTES:
    d,p=route(s,t); RT[(s,t)]=(d,p)
    print(s,'->',t,None if d is None else round(d,1),'m ',' > '.join(z for z,_ in p))
