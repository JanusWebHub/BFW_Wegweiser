import sys;sys.path.insert(0,'.')
exec(open('graph.py').read().split("# components of crossable graph")[0])
def build(extra={}, cross_over={}):
    jp=dict(JP); jp.update(extra)
    jz={k:dict(v) for k,v in JZ.items()}
    for k,v in cross_over.items(): jz[k]['crossable']=v
    zp=defaultdict(list)
    for i in jp:
        for e in ends(i):
            if e!='exterior': zp[e].append(i)
    return jp,jz,zp
def route(s,t,jp,jz,zp):
    # states: (zone, portal-entered-through); Dijkstra over portals
    # node = (portal, zone_we_are_in_after_crossing)
    pq=[];best={}
    def pt(i): return jp[i]['point']
    # start: from s, pick any portal of s (start point = first portal crossing; cost of walking inside start zone unknown -> 0)
    for i in jp:
        e=ends(i)
        if s in e:
            o=e[0] if e[1]==s else e[1]
            heapq.heappush(pq,(0,(i,o),[s,o]))
    while pq:
        d,(pi,z),path=heapq.heappop(pq)
        if (pi,z) in best: continue
        best[(pi,z)]=d
        if z==t: return d/upm,path
        if not jz[z]['crossable'] and z!=t: continue
        for pj in zp.get(z,[]):
            if pj==pi: continue
            e=ends(pj); o=e[0] if e[1]==z else e[1]
            if o==s: continue
            L=math.dist(pt(pi),pt(pj)) if pi in jp else 0
            heapq.heappush(pq,(d+L,(pj,o),path+[o]))
        # exterior as target handled by loop
    return None,None
if __name__=='__main__':
    base=build()
    ex={'E.flur-tr2-1_E.flur-tr7-3':{'virtual':False,'point':[616,569.5]}}
    fixed=build(ex)
    fixed2=build({**ex,'E.flur-tr2-3_E.flur-tr2-4':{'virtual':False,'point':[450,564.5]},'E.flur-tr7-1_E.flur-tr9-3':{'virtual':False,'point':[1050,504]}},{'E.33':True})
    tests=[('E.72a','E.21'),('E.01','E.52'),('E.62','E.41a'),('E.90','E.60a'),('E.29','E.71'),('E.21','E.52'),('E.33a','E.02'),('E.57','E.49'),('E.53.1','E.62')]
    for s,t in tests:
        for name,g in [('as-delivered',base),('+fire door',fixed),('+door,+tr2 door,+tr7/9 door,E.33 crossable',fixed2)]:
            d,p=route(s,t,*g)
            print(s,'->',t,name,None if d is None else round(d,1),'' if p is None else ' > '.join(p) if len(p)<14 else ' > '.join(p[:14])+'...')
        print()
