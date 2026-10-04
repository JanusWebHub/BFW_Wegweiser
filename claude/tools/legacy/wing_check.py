import json, re, sys, math, xml.etree.ElementTree as ET
from pathlib import Path
D = Path(__file__).resolve().parent.parent / "data"
NS = "{http://www.w3.org/2000/svg}"
def strip(t): return t.replace(NS, "")
def load_svg(p):
    txt = Path(p).read_text(encoding="utf-8")
    root = ET.fromstring(txt)
    zones, portals, shell = {}, {}, None
    for e in root.iter():
        i = e.get("id") or ""
        t = strip(e.tag)
        if i.startswith("zone-"): zones[i[5:]] = e
        elif i.startswith("portal-"): portals[i[7:]] = e
        elif i == "shell-outline": shell = e
    return txt, root, zones, portals, shell
def polys(e):
    t = strip(e.tag)
    if t == "polygon":
        nums = list(map(float, re.findall(r"-?\d+\.?\d*", e.get("points"))))
        return [list(zip(nums[0::2], nums[1::2]))]
    if t == "path":
        out = []
        for sub in re.split(r"[Mm]", e.get("d"))[1:]:
            nums = list(map(float, re.findall(r"-?\d+\.?\d*", sub)))
            out.append(list(zip(nums[0::2], nums[1::2])))
        return out
    return []
def inside(pt, pl):
    x, y = pt; c = False
    for ring in pl:
        n = len(ring)
        for i in range(n):
            x1, y1 = ring[i]; x2, y2 = ring[(i+1) % n]
            if (y1 > y) != (y2 > y) and x < (x2-x1)*(y-y1)/(y2-y1)+x1: c = not c
    return c
def dseg(p, a, b):
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx-ax, by-ay; L = dx*dx+dy*dy
    t = 0 if L == 0 else max(0, min(1, ((px-ax)*dx+(py-ay)*dy)/L))
    return math.hypot(px-ax-t*dx, py-ay-t*dy)
def dpoly(p, pl):
    return min(dseg(p, r[i], r[(i+1) % len(r)]) for r in pl for i in range(len(r)))
def bbox(pl):
    xs = [x for r in pl for x, _ in r]; ys = [y for r in pl for _, y in r]
    return min(xs), min(ys), max(xs), max(ys)

base = json.loads((D/"connectivity-graph.json").read_text(encoding="utf-8"))
_, _, bz, bp, bshell = load_svg(D/"bfw-eg.svg")
def run(folder, tag):
    print("="*20, folder)
    F = D/folder
    j = json.loads((F/f"connectivity-graph-{tag}.json").read_text(encoding="utf-8"))
    txt, root, sz, sp, shell = load_svg(F/f"bfw-eg-{tag}.svg")
    print("top-level keys diff:", {k for k in set(j)|set(base) if k not in ("zones","portals") and j.get(k)!=base.get(k)})
    bZ, bP, Z, P = base["zones"], base["portals"], j["zones"], j["portals"]
    rem = [z for z in bZ if z not in Z]; chg = [z for z in bZ if z in Z and Z[z]!=bZ[z]]
    prem = [p for p in bP if p not in P]; pchg = [p for p in bP if p in P and P[p]!=bP[p]]
    addz = [z for z in Z if z not in bZ]; addp = [p for p in P if p not in bP]
    print(f"base zones removed {rem} changed {chg}; portals removed {prem} changed {pchg}")
    print(f"added zones {len(addz)}, added portals {len(addp)}; total zones {len(Z)} portals {len(P)}")
    print("SVG metadata/c2pa:", bool(re.search(r"c2pa|manifest|<metadata", txt, re.I)), "| style elements:", len(re.findall(r"<style", txt)), "| ends with newline:", txt.endswith("\n"))
    print("SVG zones not in JSON:", sorted(set(sz)-set(Z)), "| JSON zones not in SVG:", sorted(set(Z)-set(sz)))
    print("SVG portals not in JSON:", sorted(set(sp)-set(P)), "| JSON portals not in SVG:", sorted(set(P)-set(sp)))
    # base svg geometry unchanged?
    dz = [z for z in bz if z in sz and (bz[z].get("points"), bz[z].get("d")) != (sz[z].get("points"), sz[z].get("d"))]
    dp = [p for p in bp if p in sp and ET.tostring(bp[p]) and [ (strip(c.tag), sorted(c.attrib.items())) for c in bp[p]] != [(strip(c.tag), sorted(c.attrib.items())) for c in sp[p]]]
    print("base zone geometry changed in SVG:", dz, "| base portal geometry changed:", dp)
    print("shell changed:", bshell.get("points") != shell.get("points"))
    # portal id rule and zone refs
    bad = []
    for pid, pv in P.items():
        m = re.fullmatch(r"(.+?)_(.+?)(?:_(\d+))?", pid)
        # zone ids contain no '_'
        parts = pid.split("_")
        zs = parts[:2]
        if len(parts) not in (2, 3) or zs != sorted(zs) or any(z not in Z for z in zs) or (len(parts)==3 and not parts[2].isdigit()):
            bad.append(pid)
    print("portal ids violating rule:", bad)
    ids_bad = [z for z in addz if "_" in z or not re.fullmatch(r"(E\.|1\.|R\.)[A-Za-z0-9.\-]+", z)]
    print("added zone ids odd:", ids_bad)
    print("added zone ids:", addz)
    flags = [p for p, v in P.items() if (v.get("emergency_exit") or v.get("main_entrance")) and "exterior" not in p]
    print("flags on non-exterior portals:", flags)
    # zone attributes
    print("zones missing floor/crossable:", [z for z,v in Z.items() if z!="exterior" and ("floor" not in v or "crossable" not in v)])
    # portals with no zones connected
    deg = {z: 0 for z in Z}
    for pid in P:
        for z in pid.split("_")[:2]: deg[z] += 1
    print("zones without portal:", sorted(z for z,d in deg.items() if d==0))
    # portal geometry
    zp = {z: polys(e) for z, e in sz.items()}; shp = polys(shell)
    prob = []
    for pid, e in sp.items():
        if pid not in P: continue
        ln = [c for c in e if strip(c.tag)=="line"]; ci = [c for c in e if strip(c.tag)=="circle"]
        if not ln or not ci: prob.append((pid,"no line/circle")); continue
        l = ln[0]; a = (float(l.get("x1")), float(l.get("y1"))); b = (float(l.get("x2")), float(l.get("y2")))
        mid = ((a[0]+b[0])/2, (a[1]+b[1])/2); c = (float(ci[0].get("cx")), float(ci[0].get("cy")))
        if abs(mid[0]-c[0])>0.15 or abs(mid[1]-c[1])>0.15: prob.append((pid,"circle!=mid"))
        if any(abs(x-y)>0.15 for x,y in zip(P[pid]["point"], c)): prob.append((pid,"json point!=circle"))
        cls = e.get("class","")
        if ("virtual" in cls) != bool(P[pid].get("virtual")): prob.append((pid,"virtual class mismatch"))
        z1, z2 = pid.split("_")[:2]
        for z in (z1, z2):
            pl = shp if z=="exterior" else zp.get(z)
            if pl is None: continue
            for q in (a, b):
                if dpoly(q, pl) > 0.8: prob.append((pid, f"end {q} off boundary of {z} ({dpoly(q,pl):.1f})")); break
    print("portal problems:", prob)
    # overlaps: sample new zones
    ov = {}
    allz = {z: (polys(e), None) for z, e in sz.items()}
    bbs = {z: bbox(p[0]) for z, p in allz.items() if p[0]}
    for z in addz:
        if z not in bbs: continue
        x0, y0, x1, y1 = bbs[z]; pl = allz[z][0]
        x = x0+1
        while x < x1:
            y = y0+1
            while y < y1:
                if inside((x, y), pl):
                    for o, (opl, _) in allz.items():
                        if o != z and opl:
                            b = bbs[o]
                            if b[0] <= x <= b[2] and b[1] <= y <= b[3] and inside((x, y), opl):
                                k = tuple(sorted((z, o))); ov[k] = ov.get(k, 0) + 1
                y += 2
            x += 2
    print("overlaps (pairs, samples of 2x2):", {"|".join(k): v for k, v in ov.items()})
    outside = []
    for z in addz:
        pl = zp.get(z)
        if not pl: continue
        cx, cy = [sum(v)/len(v) for v in zip(*pl[0])]
        # sample outside shell via vertices
        n_out = sum(1 for r in pl for q in r if not inside(q, shp) and dpoly(q, shp) > 1.5)
        if n_out: outside.append((z, n_out))
    print("added zones with vertices outside shell:", outside)
    return set(addz), set(addp), set(j["zones"]["exterior"].keys()) if "exterior" in j["zones"] else None

res = {}
for f, t in [("steps-2.3-3.3","2.3-3.3"),("steps-2.4-3.4","2.4-3.4"),("steps-2.5-3.5","2.5-3.5"),("steps-2.6-3.6","2.6-3.6"),("steps-2.7-3.7","2.7-3.7")]:
    try: res[t] = run(f, t)
    except Exception as ex: print("ERROR", f, repr(ex))
print("="*20, "cross-wing duplicates")
ks = list(res)
for i in range(len(ks)):
    for k in range(i+1, len(ks)):
        zz = res[ks[i]][0] & res[ks[k]][0]; pp = res[ks[i]][1] & res[ks[k]][1]
        if zz or pp: print(ks[i], ks[k], "zones", sorted(zz), "portals", sorted(pp))
