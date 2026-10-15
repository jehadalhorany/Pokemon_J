import gzip,json,pathlib,collections
ROOT=pathlib.Path('pokemon-j/public/data/original');p=ROOT/'config.json.gz';c=json.load(gzip.open(p));spawns={};regions={};entities={};neighbors=collections.defaultdict(set)
for file in ROOT.glob('*.json.gz'):
 if file.name=='config.json.gz':continue
 w=json.load(gzip.open(file));sid=w['id'];entities[sid]=w['entities']
 for r in w['entities'].get('2',[]):spawns[str(r['id'])]={'scene':sid,**r}
 for r in w['entities'].get('8',[]):regions[str(r['id'])]={'scene':sid,**r}
 for i,a in enumerate(w['entities'].get('8',[])):
  for b in w['entities'].get('8',[])[i+1:]:
   dx=abs(a['p'][0]-b['p'][0])/10-(a['size'][0]+b['size'][0])/2;dz=abs(a['p'][2]-b['p'][2])/10-(a['size'][2]+b['size'][2])/2
   if dx<=2 and dz<=2 and (abs(a['p'][0]-b['p'][0])+abs(a['p'][2]-b['p'][2])>1):neighbors[a['id']].add(b['id']);neighbors[b['id']].add(a['id'])
for n in c['npcs']:
 if n['BirthId'] and str(n['Id']) in spawns and str(n['BirthId']) in spawns:
  a=spawns[str(n['Id'])]['area'];b=spawns[str(n['BirthId'])]['area'];neighbors[a].add(b);neighbors[b].add(a)
c['spawns']=spawns;c['regions']=regions;c['neighbors']={str(k):sorted(v) for k,v in neighbors.items()};c['source']='Original MapArea, MapMini, MapPoint, Npc, Model and scene object configurations'
p.write_bytes(gzip.compress(json.dumps(c,separators=(',',':'),ensure_ascii=False).encode(),6));print('spawns',len(spawns),'regions',len(regions),'connections',sum(map(len,neighbors.values())))
