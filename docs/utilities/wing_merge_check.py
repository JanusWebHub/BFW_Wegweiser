import re
from pathlib import Path as _P
__file__ = str(_P(__file__).resolve().parent / "wing_check.py")
src = _P(__file__).read_text(encoding="utf-8").split("base = json")[0]
exec(src)
base = json.loads((D/"connectivity-graph.json").read_text(encoding="utf-8"))
_, _, bz, bp, bshell = load_svg(D/"bfw-eg.svg")
W = {3:"2.3-3.3",4:"2.4-3.4",5:"2.5-3.5",6:"2.6-3.6",7:"2.7-3.7"}
zones = {z: ("base", polys(e)) for z, e in bz.items()}
portals = {p: "base" for p in bp}
allj = dict(base["zones"]); allp = dict(base["portals"])
for w, t in W.items():
    F = D/f"steps-{t}"
    j = json.loads((F/f"connectivity-graph-{t}.json").read_text(encoding="utf-8"))
    _, _, sz, sp, _ = load_svg(F/f"bfw-eg-{t}.svg")
    for z in j["zones"]:
        if z not in base["zones"]:
            if z in zones: print("DUP zone", z, zones[z][0], w)
            zones[z] = (w, polys(sz[z])); allj[z] = j["zones"][z]
    for p in j["portals"]:
        if p not in base["portals"]:
            if p in portals: print("DUP portal", p, portals[p], w)
            portals[p] = w; allp[p] = j["portals"][p]
print("merged zones", len(allj), "portals", len(allp))
bbs = {z: bbox(v[1]) for z, v in zones.items()}
ov = {}
for z, (w, pl) in zones.items():
    if w == "base": continue
    x0,y0,x1,y1 = bbs[z]; x = x0+1
    while x < x1:
        y = y0+1
        while y < y1:
            if inside((x,y), pl):
                for o,(w2,opl) in zones.items():
                    if o != z and w2 != w and bbs[o][0]<=x<=bbs[o][2] and bbs[o][1]<=y<=bbs[o][3] and inside((x,y),opl):
                        k = tuple(sorted((z,o))); ov[k] = ov.get(k,0)+1
            y += 2
        x += 2
print("cross-wing overlaps:", {"|".join(k): v for k,v in ov.items()})
# zones without portals after merge, and connectivity
deg = {z:0 for z in allj}
adj = {z:set() for z in allj}
for p in allp:
    a,b = p.split("_")[:2]; deg[a]+=1; deg[b]+=1; adj[a].add(b); adj[b].add(a)
print("zones without portal after merge:", sorted(z for z,d in deg.items() if d==0))
seen=set(); comps=[]
for z in allj:
    if z in seen: continue
    st=[z]; c=set()
    while st:
        n=st.pop()
        if n in c: continue
        c.add(n); st+=list(adj[n]-c)
    seen|=c; comps.append(c)
print("connected components:", len(comps))
for c in sorted(comps, key=len)[:-1]: print("  small component:", sorted(c))
# gaps: uncovered samples inside wing shapes (wings 3-7)
wings = {e.get("id"): polys(e) for e in load_svg(D/"bfw-eg.svg")[1].iter() if (e.get("id") or "").startswith("wing-")}
for wid in ["wing-3","wing-4","wing-5","wing-6","wing-7"]:
    pl = wings[wid]; x0,y0,x1,y1 = bbox(pl); miss=0; tot=0; x=x0+1
    while x<x1:
        y=y0+1
        while y<y1:
            if inside((x,y),pl):
                tot+=1
                if not any(bbs[z][0]<=x<=bbs[z][2] and bbs[z][1]<=y<=bbs[z][3] and inside((x,y),v[1]) for z,v in zones.items()): miss+=1
            y+=2
        x+=2
    print(wid, "uncovered samples", miss, "of", tot, f"({100*miss/tot:.1f}%)")
