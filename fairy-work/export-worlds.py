from convert import Env,ROOT
from map_decode import decode,vector,placements,signed
import pathlib,json,gzip,struct,collections
OUT=ROOT.parent/'pokemon-j/public/data/original';OUT.mkdir(exist_ok=True,parents=True)
cat=json.load(open(ROOT.parent/'pokemon-j/public/assets/imported/catalog.json'));byName={x['name'].lower():x['id'] for x in cat['models']}
models={r['Id']:r for r in json.load(open(ROOT/'ModelConfig.json'))};npcs={r['Id']:r for r in json.load(open(ROOT/'NpcConfig.json'))};areas=json.load(open(ROOT/'MapAreaConfig.json'));lang=json.load(open(ROOT/'language-en.json'));meta={};missing=collections.Counter()
def match(name):
 name=name.split('/')[-1].removesuffix('.prefab').lower()
 return byName.get(name)
def nav(b):
 if len(b)<48:return []
 out=[];tiles=struct.unpack_from('<i',b,8)[0];ptr=40
 for tile in range(tiles):
  ref,size=struct.unpack_from('<II',b,ptr);ptr+=8;o=ptr;h=struct.unpack_from('<15I',b,o);polys,verts=h[6:8];v=[list(struct.unpack_from('<3f',b,o+100+i*12)) for i in range(verts)];start=o+100+verts*12
  for i in range(polys):
   p=start+i*32;ids=struct.unpack_from('<6H',b,p+4);n=b[p+30]
   if 3<=n<=6:out.append([[round(v[j][0],4),round(v[j][2],4),round(v[j][1],4)] for j in ids[:n]])
  ptr+=size
 return out
def objs(b):
 d=decode(b);out={}
 for k,values in d.items():
  if not isinstance(values[0],bytes):continue
  group=[]
  for v in values:
   q=decode(v)
   if k in [8,9,10,13]:
    group.append({'id':q.get(1,[0])[0],'size':vector(q.get(2,[b''])[0]),'p':vector(q.get(3,[b''])[0])})
   elif k==11:
    group.append({'id':q.get(1,[0])[0],'type':q.get(2,[0])[0],'p':vector(q.get(3,[b''])[0]),'area':q.get(4,[0])[0],'links':q.get(5,[])})
   else:
    group.append({'id':q.get(1,[0])[0],'type':q.get(2,[0])[0],'p':vector(q.get(4 if k==2 else 3,[b''])[0]),'area':q.get(5 if k==2 else 4,[0])[0],'face':q.get(3,[0])[0] if k==2 else 0})
  out[str(k)]=group
 return out
for row in json.load(open(ROOT/'maps-index.json')):
 try:
  e=Env();e.load_file((ROOT/'raw'/row['bundle']).read_bytes());assets={}
  for o in e.objects:
   if o.type.name=='TextAsset':
    a=o.read();assets[a.m_Name]=a.m_Script.encode('utf8','surrogateescape')
  id=row['id'];d=decode(assets[id]);placed=placements(d)
  for k in [7,8]:
   for b in d.get(k,[]):
    t=decode(b);name=t[1][0].decode();r={'name':name,'p':vector(t.get(2,[b''])[0]),'r':vector(t.get(3,[b''])[0]),'s':vector(t.get(4,[b''])[0],10),'environment':k==7,'floor':k==8 or 'floor' in name.lower()};placed.append(r)
  resolved=[]
  for r in placed:
   model=match(r['name'])
   if not model:missing[r['name']]+=1;continue
   r['model']=model;r.pop('fields',None);resolved.append(r)
  objectData=objs(assets.get(id+'_object',b'')) if assets.get(id+'_object') else {}
  content={'id':int(id),'objects':resolved,'entities':objectData,'walk':nav(assets.get(id+'_navmesh',b'')),'water':nav(assets.get(id+'_water_navmesh',b''))}
  # Scene object data may be separated into per-area files in the same bundle.
  for name,b in assets.items():
   if name.endswith('_object') and name!=id+'_object':
    extra=objs(b)
    for k,rows in extra.items():
     existing=content['entities'].setdefault(k,[]);known={(r['id'],tuple(r['p']),r.get('type')) for r in existing}
     existing.extend(r for r in rows if (r['id'],tuple(r['p']),r.get('type')) not in known)
  (OUT/(id+'.json.gz')).write_bytes(gzip.compress(json.dumps(content,separators=(',',':')).encode(),6))
  meta[id]={'objects':len(resolved),'areas':[a['Id'] for a in areas if a['Scene']==int(id)],'nav':len(content['walk'])};print(id,len(resolved),len(content['walk']),flush=True)
 except Exception as ex:print('ERROR',row['id'],str(ex),flush=True)
localized={}
for a in areas:a['name']=lang.get(a['Name'],str(a['Id']))
for n in npcs.values():
 n['name']=lang.get(n['Name'],'')
 mo=models.get(n['Model']);n['model']=match(mo['Prefabs'] or mo['Path']) if mo else None
 n['modelScale']=mo['MapSize'] if mo else 1
config={'areas':areas,'mini':json.load(open(ROOT/'MapMiniConfig.json')),'points':json.load(open(ROOT/'MapPointConfig.json')),'worlds':json.load(open(ROOT/'MapWorldConfig.json')),'npcs':list(npcs.values()),'models':list(models.values()),'maps':meta}
(OUT/'config.json.gz').write_bytes(gzip.compress(json.dumps(config,separators=(',',':'),ensure_ascii=False).encode(),6));(ROOT/'world-export-missing.json').write_text(json.dumps(missing,indent=2));print('DONE',len(meta),'missing',len(missing),flush=True)
