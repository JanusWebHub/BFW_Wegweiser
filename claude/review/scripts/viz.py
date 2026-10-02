import sys,hashlib
from PIL import Image,ImageDraw,ImageFont
src=open('fixed.py').read().split("# ================= validation")[0]
exec(src)
def viz(out,b,S=5,labels=True):
    x0,y0,x1,y1=b; W,H=int((x1-x0)*S),int((y1-y0)*S)
    im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im,'RGBA')
    f=ImageFont.load_default()
    T=lambda p:((p[0]-x0)*S,(p[1]-y0)*S)
    for n,g in G.items():
        if not g.intersects(__import__('shapely.geometry',fromlist=['box']).box(*b)): continue
        h=int(hashlib.md5(n.encode()).hexdigest()[:6],16); col=(100+h%120,100+(h>>8)%120,100+(h>>16)%120)
        for p in ([g] if g.geom_type=='Polygon' else g.geoms):
            d.polygon([T(q) for q in p.exterior.coords],fill=col+((150,) if C.get(n) else (90,)),outline=(20,20,120,255))
        c=g.representative_point()
        if labels and x0<c.x<x1 and y0<c.y<y1: d.text(T((c.x-8,c.y)),n.replace('E.',''),fill=(0,0,0,255),font=f)
    for i,l in LN.items():
        if min(l[0],l[2])>x1 or max(l[0],l[2])<x0 or min(l[1],l[3])>y1 or max(l[1],l[3])<y0: continue
        d.line([T(l[:2]),T(l[2:])],fill=(0,140,120,255) if not PT[i]['virtual'] else (230,120,0,255),width=3)
    im.save(out)
if __name__=='__main__':
    viz('review/doors/v-tr3.png',(395,570,585,860),S=4)
    viz('review/doors/v-hex.png',(90,420,300,700),S=5)
    viz('review/doors/v-tr2.png',(440,480,640,660),S=6)
