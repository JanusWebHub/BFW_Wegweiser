from pathlib import Path as _P
__file__ = str(_P(__file__).resolve().parent / "wing_merge_check.py")
src = _P(__file__).read_text(encoding="utf-8").split("# gaps:")[0]
exec(src.replace("print(","(lambda *a,**k:None)("))
wings = {e.get("id"): polys(e) for e in load_svg(D/"bfw-eg.svg")[1].iter() if (e.get("id") or "").startswith("wing-")}
from collections import Counter
for wid in ["wing-6","wing-5","wing-3"]:
    pl = wings[wid]; x0,y0,x1,y1 = bbox(pl); c = Counter(); x = x0+1
    while x<x1:
        y=y0+1
        while y<y1:
            if inside((x,y),pl) and not any(bbs[z][0]<=x<=bbs[z][2] and bbs[z][1]<=y<=bbs[z][3] and inside((x,y),v[1]) for z,v in zones.items()):
                c[(int(x//25)*25, int(y//25)*25)] += 4
            y+=2
        x+=2
    print(wid, "uncovered area (units2) per 25x25 cell:", sorted(c.items(), key=lambda kv:-kv[1])[:12])
