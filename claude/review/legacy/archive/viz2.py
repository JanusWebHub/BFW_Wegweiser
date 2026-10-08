import json,glob,os,sys
from PIL import Image,ImageDraw,ImageFont
exec(open('viz.py').read().split("if __name__")[0])
M=[]
for f in glob.glob('marks8/marks/*.json'):
    m=json.load(open(f))
    if m['kind'] in('add','move'): M.append(m)
def viz2(out,b,S=12):
    viz(out,b,S,labels=True)
    im=Image.open(out).convert('RGB'); d=ImageDraw.Draw(im,'RGBA'); x0,y0=b[0],b[1]
    T=lambda p:((p[0]-x0)*S,(p[1]-y0)*S)
    for n,p in UP.items():
        if p.intersects(__import__('shapely.geometry',fromlist=['box']).box(*b)):
            d.line([T(q) for q in p.exterior.coords],fill=(230,0,0,255),width=2)
    for m in M:
        if m['kind']=='add': d.line([T(m['pts'][0]),T(m['pts'][1])],fill=(255,150,0,255),width=5)
    im.save(out)
viz2('review/doors/y-east.png',(440,600,620,880),S=3.6)
