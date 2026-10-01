import re, json, math
import xml.etree.ElementTree as ET
from shapely.geometry import Polygon, MultiPolygon, LineString, Point
from shapely.ops import unary_union
R='/home/user/BFW_Wegweiser/docs/data/'
SETS={
 'base':('steps-2.1-to-3.2.md/bfw-eg.svg','steps-2.1-to-3.2.md/connectivity-graph.json'),
 'w3':('steps-2.3-3.3/bfw-eg-2.3-3.3.svg','steps-2.3-3.3/connectivity-graph-2.3-3.3.json'),
 'w4':('steps-2.4-3.4/bfw-eg-2.4-3.4.svg','steps-2.4-3.4/connectivity-graph-2.4-3.4.json'),
 'w5':('steps-2.5-3.5/bfw-eg-2.5-3.5.svg','steps-2.5-3.5/connectivity-graph-2.5-3.5.json'),
 'w6':('steps-2.6-3.6/bfw-eg-2.6-3.6.svg','steps-2.6-3.6/connectivity-graph-2.6-3.6.json'),
 'w7':('steps-2.7-3.7/bfw-eg-2.7-3.7.svg','steps-2.7-3.7/connectivity-graph-2.7-3.7.json'),
 'm':('step-8-and-merge/bfw-eg-8.svg','step-8-and-merge/connectivity-graph-8.json'),
}
NS='{http://www.w3.org/2000/svg}'
def raw(k): return open(R+SETS[k][0]).read()
def parse_path(d):
    rings=[];cur=[]
    for m in re.finditer(r'([MLZmlz])\s*([-\d.,\s]*)',d):
        c,a=m.group(1),m.group(2)
        nums=[float(x) for x in re.findall(r'-?\d+\.?\d*',a)]
        if c in 'ML':
            if c=='M' and cur: rings.append(cur);cur=[]
            for i in range(0,len(nums),2): cur.append((nums[i],nums[i+1]))
        elif c in 'Zz':
            if cur: rings.append(cur);cur=[]
        else: raise Exception('rel cmd '+c)
    if cur: rings.append(cur)
    return rings
def poly_from(el):
    t=el.tag.replace(NS,'')
    if t=='polygon':
        n=[float(x) for x in re.findall(r'-?\d+\.?\d*',el.get('points'))]
        return Polygon(list(zip(n[0::2],n[1::2])))
    if t=='rect':
        x,y,w,h=[float(el.get(k)) for k in('x','y','width','height')]
        return Polygon([(x,y),(x+w,y),(x+w,y+h),(x,y+h)])
    if t=='path':
        rings=parse_path(el.get('d'))
        polys=[Polygon(r) for r in rings]
        # even-odd: sym diff
        g=polys[0]
        for p in polys[1:]: g=g.symmetric_difference(p)
        return g
    raise Exception(t)
def load(k):
    s=raw(k)
    info={'raw_len':len(s),'c2pa':'c2pa' in s,'has_style':'<style' in s,'nstyle':s.count('<style'),'transform':'transform' in s}
    root=ET.fromstring(s)
    groups=[g for g in root if g.tag==NS+'g']
    info['top']=[c.tag.replace(NS,'')+':'+str(c.get('id')) for c in root]
    z={};p={};lab=[];shell=None;zel={}
    for g in groups:
        gid=g.get('id')
        if gid=='zones':
            for e in g:
                i=e.get('id'); z[i]=poly_from(e); zel[i]=e
        elif gid=='portals':
            for e in g:
                i=e.get('id'); ln=e.find(NS+'line'); ci=e.find(NS+'circle')
                p[i]={'cls':e.get('class'),'line':[float(ln.get(a)) for a in('x1','y1','x2','y2')],'c':[float(ci.get('cx')),float(ci.get('cy'))],'r':ci.get('r'),'n':len(list(e))}
        elif gid=='labels':
            lab=[(e.text,float(e.get('x')),float(e.get('y')),e.get('class')) for e in g]
        elif gid=='shell':
            shell={}
            for e in g:
                shell[e.get('id')]=(e.get('class'),poly_from(e))
    J=json.load(open(R+SETS[k][1]))
    return info,z,zel,p,lab,shell,J
