import sys;sys.path.insert(0,'.')
exec(open('graph.py').read().split("# components of crossable graph")[0])
from shapely.geometry import LineString
# convexity per crossable zone
print('non-convex crossable zones (area/hull<0.97):')
rows=[]
for i,v in JZ.items():
    if i=='exterior' or not v['crossable']: continue
    g=Z[i]; r=g.area/g.convex_hull.area
    if r<0.97: rows.append((round(r,3),i,round(g.area)))
for r in sorted(rows): print('  ',r)
# segments: per crossable zone, pairs of portals, check line inside zone
bad=[];tot=0;lens=[]
zp=defaultdict(list)
for i,v in JP.items():
    for e in ends(i):
        if e!='exterior': zp[e].append(i)
for zn,ps in zp.items():
    if not JZ[zn]['crossable']: continue
    for a,b in itertools.combinations(sorted(ps),2):
        tot+=1
        ln=LineString([JP[a]['point'],JP[b]['point']])
        out=ln.difference(Z[zn].buffer(0.6)).length
        if out>0.5: bad.append((zn,a,b,round(out,1),round(ln.length,1)))
print('segments',tot,'segments leaving zone by >0.5u:',len(bad))
by=defaultdict(list)
for x in bad: by[x[0]].append(x)
for zn,l in sorted(by.items(),key=lambda kv:-sum(x[3] for x in kv[1])): print('  ',zn,len(l),'segs, max out',max(x[3] for x in l),'of',len(zp[zn]),'portals')
