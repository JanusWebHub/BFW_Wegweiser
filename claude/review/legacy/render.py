import sys,re,io;sys.path.insert(0,'.')
from load import *
import cairosvg
from PIL import Image
def render(k,out,scale=1.0,labels=True,crop=None):
    s=raw(k); s=re.sub(r'<metadata>.*?</metadata>','',s,flags=re.S); s=s.replace(' xmlns:c2pa="http://c2pa.org/manifest"','')
    st=open(R+'step-8-and-merge/bfw-eg-style-8.txt').read()
    st=st.replace('.room{fill:#ffffff}','.room{fill:#ffffff;fill-opacity:.25}').replace('.service{fill:#e8e4dc}','.service{fill:#e8e4dc;fill-opacity:.3}').replace('.corridor{fill:#d5e2cb}','.corridor{fill:#4caf50;fill-opacity:.35}').replace('.stair{fill:#c3d5b8}','.stair{fill:#2e7d32;fill-opacity:.4}').replace('.hall{fill:#dde8d3}','.hall{fill:#8bc34a;fill-opacity:.35}').replace('.outline{fill:#f6f4ef;','.outline{fill:none;')
    s=re.sub(r'<defs>\s*</defs>',st,s)
    if not labels: s=re.sub(r'<g id="labels">.*?</g>\s*</svg>','</svg>',s,flags=re.S)
    png=cairosvg.svg2png(bytestring=s.encode(),output_width=int(1790*scale),output_height=int(1000*scale))
    ov=Image.open(io.BytesIO(png)).convert('RGBA')
    bg=Image.open('lp_half.png').convert('RGB').rotate(180)
    W,H=bg.size
    can=Image.new('RGBA',(int(W*scale),int(H*scale)),(255,255,255,255))
    can.paste(bg.resize((int(W*scale),int(H*scale))).convert('RGBA'),(0,0))
    can.alpha_composite(ov,(int(40*scale),int(77*scale)))
    if crop: can=can.crop([int(c*scale) for c in crop])
    can.convert('RGB').save(out)
if __name__=='__main__':
    render('m','ov_full.png',1.0,labels=False)
