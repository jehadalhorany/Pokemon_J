"""Lossless deduplication of identical buffer views/accessors/meshes; no geometry changes."""
import json,gzip,struct,hashlib
from pathlib import Path
root=Path(__file__).resolve().parent.parent/'pokemon-j/public/assets/imported/models'
report=[]
for p in root.glob('source-battle-*.glb.gz'):
 raw=gzip.decompress(p.read_bytes());size=struct.unpack_from('<I',raw,12)[0];d=json.loads(raw[20:20+size]);offset=20+size;binsize=struct.unpack_from('<I',raw,offset)[0];oldbin=raw[offset+8:offset+8+binsize];newbin=bytearray();views=[];seen={};vm={}
 for i,v in enumerate(d['bufferViews']):
  content=oldbin[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']];meta={k:x for k,x in v.items()if k not in ['byteOffset','buffer']};key=(json.dumps(meta,sort_keys=True),hashlib.sha256(content).digest())
  if key not in seen:
   while len(newbin)%4:newbin.append(0)
   seen[key]=len(views);views.append({**meta,'buffer':0,'byteOffset':len(newbin)});newbin.extend(content)
  vm[i]=seen[key]
 am={};accessors=[];seen={}
 for i,a in enumerate(d['accessors']):
  a={**a,'bufferView':vm[a['bufferView']]};key=json.dumps(a,sort_keys=True)
  if key not in seen:seen[key]=len(accessors);accessors.append(a)
  am[i]=seen[key]
 meshes=[];mm={};seen={}
 for i,m in enumerate(d['meshes']):
  for prim in m['primitives']:
   prim['attributes']={k:am[v]for k,v in prim['attributes'].items()}
   if 'indices'in prim:prim['indices']=am[prim['indices']]
  key=json.dumps(m,sort_keys=True)
  if key not in seen:seen[key]=len(meshes);meshes.append(m)
  mm[i]=seen[key]
 for n in d['nodes']:
  if 'mesh'in n:n['mesh']=mm[n['mesh']]
 for s in d.get('skins',[]):
  if 'inverseBindMatrices'in s:s['inverseBindMatrices']=am[s['inverseBindMatrices']]
 oldviews=len(d['bufferViews']);d['bufferViews']=views;d['accessors']=accessors;d['meshes']=meshes
 while len(newbin)%4:newbin.append(0)
 d['buffers'][0]['byteLength']=len(newbin);body=json.dumps(d,separators=(',',':')).encode();body+=b' '*((-len(body))%4);out=struct.pack('<III',0x46546c67,2,28+len(body)+len(newbin))+struct.pack('<II',len(body),0x4e4f534a)+body+struct.pack('<II',len(newbin),0x004e4942)+newbin
 compressed=gzip.compress(out,6,mtime=0);before=p.stat().st_size;p.write_bytes(compressed);report.append({'file':p.name,'before':before,'after':len(compressed),'viewsBefore':oldviews,'viewsAfter':len(views)})
print(json.dumps(report,indent=2));(root.parent.parent.parent.parent/'SOURCE_BATTLE_OPTIMIZATION.json').write_text(json.dumps(report,indent=2))
