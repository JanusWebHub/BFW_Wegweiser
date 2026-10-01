import sys;sys.path.insert(0,'.')
from load import *
from check import zid,pid
D={k:load(k) for k in SETS}
def zp(k):
    info,z,zel,p,lab,shell,J=D[k]
    return {zid(i):g for i,g in z.items()},{pid(i):v for i,v in p.items()},J,lab,shell
B=zp('base')
def same(a,b,tol=1e-6): return a.symmetric_difference(b).area<=tol
# base vs each
for k in ['w3','w4','w5','w6','w7','m']:
    Z,P,J,lab,shell=zp(k)
    chg=[i for i in B[0] if i not in Z or not same(B[0][i],Z[i])]
    pchg=[i for i in B[1] if i not in P or B[1][i]['line']!=P[i]['line'] or B[1][i]['c']!=P[i]['c']]
    jchg=[i for i,v in B[2]['portals'].items() if J['portals'].get(i)!=v]
    zj=[i for i,v in B[2]['zones'].items() if J['zones'].get(i)!=v]
    shchg=[i for i in B[4] if not same(B[4][i][1],shell[i][1])]
    print(k,'base zone geom changed',chg,'portal svg changed',pchg,'json portal changed',jchg,'json zone changed',zj,'shell changed',shchg)
# union of wings vs merge
M=zp('m')
allz={};allp={}
wid={}
for k in ['w3','w4','w5','w6','w7']:
    Z,P,J,lab,shell=zp(k)
    for i in Z:
        if i in B[0]: continue
        if i in allz: print('dup zone across wings',i)
        allz[i]=Z[i];wid[i]=k
    for i in P:
        if i in B[1]: continue
        if i in allp: print('dup portal across wings',i)
        allp[i]=(P[i],k)
extra_z=[i for i in M[0] if i not in B[0] and i not in allz]
print('zones in merge not in base/wings:',extra_z)
print('wing zones missing/changed in merge:',[i for i in allz if i not in M[0] or not same(allz[i],M[0][i])])
print('wing zones count',len(allz),'portals',len(allp))
mp=[i for i in M[1] if i not in B[1] and i not in allp]
print('portals in merge not in base/wings (%d):'%len(mp))
for i in mp: print('  ',i,M[2]['portals'][i])
print('wing portals missing/changed in merge:',[i for i in allp if i not in M[1] or allp[i][0]['line']!=M[1][i]['line']])
# JSON flags differences
print('json zone attr diff for wings:',[i for i in allz if M[2]['zones'][i]!=D[wid[i]][6]['zones'][i]])
# json base zone attr in merged
print('crossable in merge:',sorted(i for i,v in M[2]['zones'].items() if v['crossable']))
