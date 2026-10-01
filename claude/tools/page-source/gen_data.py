import json,os
os.chdir('/tmp/claude-0/-home-user-BFW-Wegweiser/255821fa-d462-5ea3-b45c-fe956299e386/scratchpad')
exec(open('fixed.py').read().split("# ================= validation")[0])
zones=[]
for n,g in G.items():
    e=zel.get('zone-'+n); cls=e.get('class').split()[-1] if e is not None else 'corridor'
    zones.append({'id':n,'c':1 if C[n] else 0,'b':1 if n in BLOCKS else 0,'k':cls,'p':[[round(x,1),round(y,1)] for x,y in list(g.exterior.coords)[:-1]]})
ports=[{'id':i,'l':[round(v,1) for v in l],'v':1 if PT[i]['virtual'] else 0,'x':1 if 'exterior' in ends2(i) else 0} for i,l in LN.items()]
shp=[[round(x,1),round(y,1)] for x,y in sh.exterior.coords][:-1]
json.dump({'zones':zones,'portals':ports,'shell':shp},open('mk/data.json','w'),separators=(',',':'))
print(len(zones),len(ports))
