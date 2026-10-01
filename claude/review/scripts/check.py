import sys;sys.path.insert(0,'.')
from load import *
from collections import defaultdict,Counter
import itertools
def zid(s): return s[len('zone-'):]
def pid(s): return s[len('portal-'):]
def run(k,verbose=True):
    info,z,zel,p,lab,shell,J=load(k)
    out=[]
    def rep(*a): out.append(' '.join(str(x) for x in a))
    Z={zid(i):g for i,g in z.items()}; P={pid(i):v for i,v in p.items()}
    JZ=J['zones'];JP=J['portals']
    rep('==',k,'zones',len(Z),'portals',len(P),'| json zones',len(JZ)-1,'+ext portals',len(JP),'prov',J['provenance'],'upm',J['floors']['E']['units_per_meter'],J['floors']['E']['view_box'],J['floors']['E']['svg'])
    # id matching
    rep('svg-not-json zones',sorted(set(Z)-set(JZ)),'json-not-svg',sorted(set(JZ)-set(Z)-{'exterior'}))
    rep('svg-not-json portals',sorted(set(P)-set(JP)),'json-not-svg',sorted(set(JP)-set(P)))
    # id rules
    bad=[i for i in JZ if '_' in i or i!=i.strip() or (i!='exterior' and not re.match(r'^(E\.|R\.)[A-Za-z0-9.\-]+$',i))]
    rep('bad zone ids',bad)
    low=[i for i in JZ if i!='exterior' and re.search(r'[A-Z]',i.split('.',1)[1]) and not re.match(r'^E\.(TR\d|\d)',i) and not re.match(r'^[ER]\.\d',i)]
    rep('uppercase in name ids',low)
    # portal ids
    for i,v in JP.items():
        m=re.match(r'^(.*?)(_(\d+))?$',i)
        parts=i.split('_')
        if parts[-1].isdigit() and len(parts)==3: parts=parts[:2]
        if len(parts)!=2: rep('BAD portal id parts',i);continue
        a,b=parts
        if a not in JZ or b not in JZ: rep('portal unknown zone',i,a,b)
        if a==b: rep('portal same zone',i)
        if sorted([a,b])!=[a,b]: rep('portal not sorted',i)
        if ('emergency_exit' in v or 'main_entrance' in v) and 'exterior' not in (a,b): rep('flag on non-exterior',i)
        if 'virtual' not in v: rep('no virtual flag',i)
        pt=v.get('point'); vb=J['floors']['E']['view_box']
        if not(0<=pt[0]<=vb[2] and 0<=pt[1]<=vb[3]): rep('point outside vb',i)
    # every zone has portal
    have=set()
    for i in JP:
        parts=i.split('_'); 
        if parts[-1].isdigit() and len(parts)==3: parts=parts[:2]
        have.update(parts)
    rep('zones without portal',sorted(set(JZ)-have))
    # svg vs json portal geometry
    dev=[]
    for i,v in JP.items():
        if i not in P: continue
        s=P[i]; c=s['c']; pt=v['point']
        d1=math.dist(c,pt); l=s['line']; mid=((l[0]+l[2])/2,(l[1]+l[3])/2); d2=math.dist(c,mid)
        if d1>0.06 or d2>0.06: dev.append((i,round(d1,2),round(d2,2)))
        vcls='virtual' in (s['cls'] or ''); 
        if vcls!=v['virtual']: rep('virtual class mismatch',i,s['cls'],v['virtual'])
    rep('portal point/circle/midpoint dev>0.06:',dev)
    # portal line on boundary of both zones
    off=[]
    for i,v in JP.items():
        if i not in P: continue
        parts=i.split('_')
        if parts[-1].isdigit() and len(parts)==3: parts=parts[:2]
        ln=LineString([P[i]['line'][:2],P[i]['line'][2:]])
        ds=[]
        for zz in parts:
            if zz=='exterior': ds.append(0 if not shell else min(ln.distance(shell['shell-outline'][1].exterior),0.0)); continue
            ds.append(ln.hausdorff_distance(Z[zz].boundary) if False else max(Point(c).distance(Z[zz].boundary) for c in [ln.coords[0],ln.coords[1],ln.interpolate(0.5,normalized=True).coords[0]]))
        if max(ds)>0.6: off.append((i,[round(d,2) for d in ds]))
    rep('portal lines off boundary >0.6:',off)
    # exit portals vs shell
    ex=[]
    sh=shell['shell-outline'][1]
    for i in JP:
        if 'exterior' in i.split('_') and i in P:
            ln=LineString([P[i]['line'][:2],P[i]['line'][2:]])
            ex.append((i,round(max(Point(c).distance(sh.exterior) for c in ln.coords),1)))
    rep('exit portal dist to shell outline',ex)
    # geometry
    inval=[i for i,g in Z.items() if not g.is_valid]; rep('invalid polys',inval)
    zs=list(Z.items())
    ov=[]
    from shapely.strtree import STRtree
    tree=STRtree([g for _,g in zs])
    for ia,(a,ga) in enumerate(zs):
        for j in tree.query(ga):
            b,gb=zs[j]
            if j<=ia: continue
            ar=ga.intersection(gb).area
            if ar>0.5: ov.append((a,b,round(ar,1)))
    rep('overlaps >0.5 u2:',ov)
    U=unary_union(list(Z.values()))
    gap=sh.difference(U)
    rep('shell area',round(sh.area),'zones area',round(U.area),'gap area',round(gap.area,1),'outside shell',round(U.difference(sh).area,1))
    return dict(info=info,Z=Z,P=P,J=J,shell=sh,out=out,gap=gap,ov=ov)
if __name__=='__main__':
    for k in SETS:
        r=run(k)
        print('\n'.join(r['out']))
