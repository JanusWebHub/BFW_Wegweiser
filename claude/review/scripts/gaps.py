import sys;sys.path.insert(0,'.')
exec(open('graph.py').read().split("# components of crossable graph")[0])
sh=shell['shell-outline'][1]
U=unary_union(list(Z.values()))
gap=sh.difference(U)
gs=[g for g in (gap.geoms if hasattr(gap,'geoms') else [gap])]
gs=sorted(gs,key=lambda g:-g.area)
print('gap pieces',len(gs),'total',round(gap.area,1))
for g in gs[:25]:
    c=g.centroid; b=g.bounds
    print(' area %.1f at (%.0f,%.0f) bbox w%.1f h%.1f'%(g.area,c.x,c.y,b[2]-b[0],b[3]-b[1]))
out=U.difference(sh)
os_=sorted([g for g in (out.geoms if hasattr(out,'geoms') else [out])],key=lambda g:-g.area)
print('outside shell pieces',len(os_),round(out.area,1))
for g in os_[:12]:
    c=g.centroid; print(' area %.1f at (%.0f,%.0f)'%(g.area,c.x,c.y), [n for n,zg in Z.items() if zg.intersection(g).area>g.area*0.5])
# also compare to wing shapes: uncovered inside wing polygons
for w,(cl,g) in shell.items():
    if w.startswith('wing'):
        u=g.difference(U); print(w,'area',round(g.area),'uncovered',round(u.area),'%.1f%%'%(100*u.area/g.area))
