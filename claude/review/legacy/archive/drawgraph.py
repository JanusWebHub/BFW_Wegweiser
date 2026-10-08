exec(open('fixed.py').read().split("# ================= validation")[0])
exec("def ends(i): return ends2(i)\n")
exec(open('fixed.py').read().split("# ================= routing graph")[1].split("ROUTES=")[0].replace("os_=__import__('os'); os_.makedirs('review/routing',exist_ok=True)",""))
exec("ROUTES=[('E.01','E.52'),('E.72a','E.62'),('E.90','E.60a'),('E.34','E.41a'),('E.33a','E.02')]\n"+open('fixed.py').read().split("ROUTES=[('E.01','E.52'),('E.72a','E.62'),('E.90','E.60a'),('E.34','E.41a'),('E.33a','E.02')]")[1])
import io,cairosvg
from PIL import Image,ImageDraw,ImageFont
WARM={'corridor':'#e4dfd3','hall':'#ece3cf','stair':'#cfc6b6','room':'#fdfcf9','service':'#f1eee8'}
EXC={'E.41','E.68','E.66','E.74','E.82','E.83','E.33','E.58','E.52'}
def zclass(n):
    e=zel.get('zone-'+n); return e.get('class').split()[-1] if e is not None else 'corridor'
mainp=[i for i in PT if all((e=='exterior' or C[e]) for e in ends(i))]
def svg(bg,routes=False,S=1.5):
    W,H=1790,1000
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{int(W*S)}" height="{int(H*S)}"><style>text{{font-family:Helvetica,Arial,sans-serif;text-anchor:middle}}</style>']
    if bg=='zones':
        o.append('<rect width="100%" height="100%" fill="#faf9f6"/>')
        pts=' '.join(f'{x},{y}' for x,y in sh.exterior.coords); o.append(f'<polygon points="{pts}" fill="#faf9f6" stroke="#2f2b27" stroke-width="1.6"/>')
    for n,g in G.items():
        cls=zclass(n); cross=C[n]
        fill=WARM.get(cls,'#fdfcf9')
        if n in EXC: fill='#f0d9b5'
        if bg=='pdf': op=.55 if cross else .08
        else: op=1.0 if cross else .9
        if not cross and bg=='zones': fill='#fdfcf9'
        pts=' '.join(f'{x},{y}' for x,y in g.exterior.coords)
        o.append(f'<polygon points="{pts}" fill="{fill}" fill-opacity="{op}" stroke="#8f877b" stroke-width="{.6 if cross else .3}" stroke-opacity="{.9 if cross else .35}"/>')
    # segments of main graph
    for z,ps in zp.items():
        if not C[z]: continue
        mp=[p for p in sorted(ps) if p in mainp]
        for a,b in itertools.combinations(mp,2):
            pa,pb=PT[a]['point'],PT[b]['point']
            o.append(f'<line x1="{pa[0]}" y1="{pa[1]}" x2="{pb[0]}" y2="{pb[1]}" stroke="#0d6b63" stroke-width="{.9 if not routes else .6}" stroke-opacity="{.75 if not routes else .35}"/>')
    # room doors as faint spurs? only dots for room count skipped
    # portals
    for i in mainp:
        x,y=PT[i]['point']; ex='exterior' in ends(i); new=i in NEW
        if ex: o.append(f'<rect x="{x-3}" y="{y-3}" width="6" height="6" fill="#b4561f" stroke="#fff" stroke-width=".7" transform="rotate(45 {x} {y})"/>')
        elif PT[i]['virtual']: o.append(f'<circle cx="{x}" cy="{y}" r="2.4" fill="#fff" stroke="#0d6b63" stroke-width="1.1"/>')
        else: o.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#0d6b63" stroke="#fff" stroke-width=".7"/>')
        if new: o.append(f'<circle cx="{x}" cy="{y}" r="6.5" fill="none" stroke="#d62f1f" stroke-width="1.8"/>')
    # labels for circulation zones
    for n,g in G.items():
        if not C[n]: continue
        rp=g.representative_point(); t=n[2:] if n.startswith('E.') else n
        big=n in ('E.speisesaal','E.foyer','E.terrasse','E.52')
        fs=7 if big else 4.8; fw=600 if big else 600
        o.append(f'<text x="{rp.x:.1f}" y="{rp.y:.1f}" font-size="{fs}" fill="none" font-weight="{fw}" stroke="#fff" stroke-width="1.6" stroke-opacity=".85">{t}</text><text x="{rp.x:.1f}" y="{rp.y:.1f}" font-size="{fs}" fill="#2f2b27" font-weight="{fw}">{t}</text>')
    if routes:
        cols=['#d62f1f','#8a3ffc','#e08a00','#b0306a','#2f6bd6']
        for k,((s,t),(d,p)) in enumerate(RT.items()):
            pts=[]
            rp=G[s].representative_point(); pts.append((rp.x,rp.y))
            for z,pi in p[1:]:
                if pi: pts.append(tuple(PT[pi]['point']))
            rt=G[t].representative_point(); pts.append((rt.x,rt.y))
            pl=' '.join(f'{x},{y}' for x,y in pts)
            o.append(f'<polyline points="{pl}" fill="none" stroke="#fff" stroke-width="5.2" stroke-linejoin="round" stroke-linecap="round"/><polyline points="{pl}" fill="none" stroke="{cols[k]}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>')
            o.append(f'<circle cx="{pts[0][0]}" cy="{pts[0][1]}" r="4.5" fill="{cols[k]}" stroke="#fff" stroke-width="1"/><rect x="{pts[-1][0]-4}" y="{pts[-1][1]-4}" width="8" height="8" fill="{cols[k]}" stroke="#fff" stroke-width="1"/>')
            for (tx,ty,tt) in ((pts[0][0],pts[0][1]-7,s[2:]),(pts[-1][0],pts[-1][1]-7,t[2:])):
                o.append(f'<text x="{tx}" y="{ty}" font-size="8" font-weight="700" fill="none" stroke="#fff" stroke-width="2.4">{tt}</text><text x="{tx}" y="{ty}" font-size="8" font-weight="700" fill="{cols[k]}">{tt}</text>')
    o.append('</svg>'); return '\n'.join(o)
NEW={'E.flur-tr2-1_E.flur-tr7-3','E.flur-tr2-2_E.flur-tr2-4','E.flur-tr7-1_E.flur-tr9-3','E.48_exterior','E.37_E.flur-tr2-1','E.53.1_E.53.2'}
lp=Image.open('lp_half.png').convert('RGB').rotate(180)
def render(bg,routes,out,S=1.5,title='',legend=None):
    png=cairosvg.svg2png(bytestring=svg(bg,routes,S).encode())
    ov=Image.open(io.BytesIO(png)).convert('RGBA')
    if bg=='pdf':
        W,H=lp.size; can=Image.new('RGBA',(int(1790*S),int(1000*S)),(255,255,255,255))
        b=lp.resize((int(W*S),int(H*S)),Image.LANCZOS).convert('RGBA'); can.alpha_composite(b,(int(-40*S),int(-77*S)))
        # lighten the pdf
        veil=Image.new('RGBA',can.size,(255,255,255,90)); can.alpha_composite(veil); can.alpha_composite(ov); img=can.convert('RGB')
    else: img=ov.convert('RGB')
    # crop to building bbox
    minx,miny,maxx,maxy=sh.bounds; img=img.crop((int((minx-12)*S),int((miny-12)*S),int((maxx+12)*S),int((maxy+12)*S)))
    f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26); f2=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19)
    hh=40+27*len(legend or [])+14
    canvas=Image.new('RGB',(img.width,img.height+hh),'#f6f4ef'); canvas.paste(img,(0,hh)); d=ImageDraw.Draw(canvas)
    d.text((14,8),title,fill='#2f2b27',font=f)
    for k,l in enumerate(legend or []): d.text((14,44+27*k),l,fill='#4a453e',font=f2)
    canvas.save(out); print(out,canvas.size)
leg1=['Nodes = portals between circulation zones (teal dot = door, white ring = virtual, orange diamond = exit, red ring = new/changed in this review).','Edges = computed straight segments inside each crossable zone (room doors left out). Orange-tinted zones = rooms made crossable by exception.']
RN=[f'{s[2:]} -> {t[2:]}: {d:.0f} m' for (s,t),(d,p) in RT.items()]
leg2=['Sample shortest routes: '+'   '.join(RN[:3]),'   '.join(RN[3:])+'   (graph in teal, faint)']
render('pdf',False,'review/routing/routing-graph-on-pdf.png',1.5,'Routing graph (main connections) on the Lageplan',leg1)
render('zones',False,'review/routing/routing-graph-on-zones.png',1.5,'Routing graph (main connections) on the zone map',leg1)
render('pdf',True,'review/routing/routes-on-pdf.png',1.5,'Sample routes on the Lageplan',leg2)
render('zones',True,'review/routing/routes-on-zones.png',1.5,'Sample routes on the zone map',leg2)
