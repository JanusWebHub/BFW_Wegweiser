import sys;sys.path.insert(0,'.')
from load import *
from check import zid,pid
import heapq,itertools
from collections import defaultdict
info,z,zel,p,lab,shell,J=load('m')
Z={zid(i):g for i,g in z.items()};P={pid(i):v for i,v in p.items()}
JZ=J['zones'];JP=J['portals'];upm=J['floors']['E']['units_per_meter']
def ends(i):
    parts=i.split('_')
    if parts[-1].isdigit() and len(parts)==3: parts=parts[:2]
    return parts
# components of crossable graph
adj=defaultdict(set)
for i in JP:
    a,b=ends(i);adj[a].add(b);adj[b].add(a)
def reach(start,blocked=set()):
    seen={start};st=[start]
    while st:
        u=st.pop()
        if u!=start and not JZ[u]['crossable']: continue
        for v in adj[u]:
            if v not in seen and v not in blocked: seen.add(v);st.append(v)
    return seen
R=reach('exterior')
print('unreachable from exterior (cross-only):',sorted(set(JZ)-R))
# crossable components ignoring exterior
cz=[i for i in JZ if JZ[i]['crossable'] and i!='exterior']
comp={};c=0
for i in cz:
    if i in comp: continue
    c+=1;st=[i];comp[i]=c
    while st:
        u=st.pop()
        for v in adj[u]:
            if v in cz and v not in comp: comp[v]=c;st.append(v)
groups=defaultdict(list)
for i,cc in comp.items(): groups[cc].append(i)
print('crossable components (no exterior):',len(groups))
for cc,g in groups.items(): print(' ',len(g),g if len(g)<15 else g[:6]+['...'])
# adjacent zone pairs w/o portal (shared boundary length>3) among circulation
def sharedlen(a,b):
    g=Z[a].boundary.intersection(Z[b].boundary)
    return g.length
from shapely.strtree import STRtree
names=list(Z);tree=STRtree([Z[n] for n in names])
pairs=[]
have=set(tuple(sorted(ends(i))) for i in JP)
for ia,a in enumerate(names):
    for j in tree.query(Z[a].buffer(0.8)):
        b=names[j]
        if j<=ia: continue
        L=sharedlen(a,b) if Z[a].buffer(0.8).intersects(Z[b]) else 0
        L=Z[a].buffer(0.5).boundary.intersection(Z[b].boundary).length/1.0
        if L>4: pairs.append((a,b,round(L,1),tuple(sorted((a,b))) in have))
print('circulation-circulation adjacent w/o portal (len>4):')
for a,b,L,h in sorted(pairs,key=lambda x:-x[2]):
    if not h and JZ[a]['crossable'] and JZ[b]['crossable']: print('  ',a,b,L)
print('crossable-nonc adjacent (both circ).. count no-portal pairs with room:',sum(1 for a,b,L,h in pairs if not h))
# room zones with one portal only
deg=defaultdict(int)
for i in JP:
    for e in ends(i): deg[e]+=1
print('non-crossable rooms with 0 non-exterior... degree1:',sorted(i for i in JZ if i!='exterior' and deg[i]==1 and not JZ[i]['crossable']))
print('degree1 crossable:',sorted(i for i in JZ if i!='exterior' and deg[i]==1 and JZ[i]['crossable']))
# rooms whose ONLY portals go to non-crossable rooms
print()
for cc,g in groups.items(): print(cc,sorted(g))
# which portals are known door-links missing: list candidate joins between the two components
c1=set(groups[1]);c2=set(groups[2])
cands=[]
for a in c1:
    for b in c2:
        if Z[a].distance(Z[b])<3: cands.append((a,b,round(Z[a].distance(Z[b]),2),round(Z[a].buffer(1).boundary.intersection(Z[b].boundary).length,1)))
print('nearby zone pairs across components:',cands)
