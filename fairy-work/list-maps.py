import json
from convert import Env,ROOT
from map_decode import decode,placements,vector
rows=json.load(open(ROOT/'inventory.json'));out=[]
for r in rows:
 if not any('MapConfig/' in p and p.endswith('.bytes') and not any(x in p for x in ['navmesh','object']) for p in r['paths']):continue
 try:
  e=Env();e.load_file((ROOT/'raw'/r['file']).read_bytes())
  for f in list(e.cabs.values()):
   if not hasattr(f,'objects'):continue
   for o in list(f.objects.values()):
    if o.type.name!='TextAsset':continue
    a=o.read()
    if not a.m_Name.isdigit():continue
    b=a.m_Script.encode('utf-8','surrogateescape') if isinstance(a.m_Script,str) else a.m_Script
    d=decode(b);models=placements(d);floors=[]
    for v in d.get(8,[]):
     q=decode(v);floors.append({'name':q[1][0].decode(),'p':vector(q.get(2,[b''])[0])})
    extras=[decode(v)[1][0].decode() for v in d.get(7,[])];out.append({'extras':extras,'id':a.m_Name,'bundle':r['file'],'floors':floors,'models':sorted({m['name'] for m in models}),'count':len(models)})
 except Exception as ex:print('ERROR',r['file'],str(ex),flush=True)
(ROOT/'maps-index.json').write_text(json.dumps(out));print('MAPS',len(out),flush=True)
for x in out:
 if any('bed' in n or 'yjs' in n or 'research' in n for n in x['models']):print(x,flush=True)
