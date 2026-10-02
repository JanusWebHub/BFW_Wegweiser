src=open('fixed.py').read().split("# ================= validation")[0]
exec(src)
bad=[]
for n,p in UP.items():
    if n not in G: continue
    g=G[n]; r=g.area/max(p.area,1e-6); hd=g.hausdorff_distance(p)
    if abs(r-1)>0.08 or hd>6: bad.append((n,round(p.area),round(g.area),round(hd,1)))
print('DEV',bad)
for z in ('E.82a','E.80','E.82','E.83','E.83a','E.84'):
    print('AREA',z,round(G[z].area),[round(v) for v in G[z].bounds])
