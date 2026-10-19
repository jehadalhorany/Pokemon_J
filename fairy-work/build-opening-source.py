from pathlib import Path
import json,struct,UnityPy
from PIL import Image
r=Path(__file__).resolve().parent;out=r.parent/'pokemon-j';ids={};meta={}
for p in r.glob('*_fui.bin'):
 b=p.read_bytes();n=struct.unpack_from('>H',b,9)[0];ids[b[11:11+n].decode()]=p.stem[:-4];meta[p.stem[:-4]]=json.loads((r/f'fui-{p.stem[:-4]}.json').read_text())
layout=json.loads((out/'public/data/original/native-components.json').read_text());components={pkg:{c['id']:c for c in d['components']}for pkg,d in layout['packages'].items()};needed={};seen=set();used={}
def image(pkg,id):
 if id:needed.setdefault(pkg,set()).add(id)
def visit(pkg,id):
 if (pkg,id) in seen:return
 seen.add((pkg,id));c=components.get(pkg,{}).get(id)
 if not c:return
 used.setdefault(pkg,{})[id]=c
 for n in c['children']:
  pp=ids.get(n.get('packageId'),pkg)
  if n['type']==0:image(pp,n['sourceId'])
  elif n['type']==9:visit(pp,n['sourceId'])
  if n.get('url','') and n['url'].startswith('ui://'):
   u=n['url'][5:];image(ids[u[:8]],u[8:])
for c in components['Eudemon'].values():
 if c['name'] in ['EudemonGen_MiniWindow','EudemonGenChooseButton','EudemonSelect_MiniWindow','EudemonSelectItem']:visit('Eudemon',c['id'])
for pkg in ['Item','Eudemon']:
 for it in meta[pkg]['items']:
  name=it.get('name') or ''
  if it['type']==0 and (name.startswith('sdxz') or name.startswith('jlxz_bg_card') or name in ['word_'+str(i) for i in range(1,10)]):image(pkg,it['id'])
rows=json.loads((r/'inventory-fast.json').read_text());paths={p:row['file'] for row in rows for p in row['paths']};cache={};images={};dest=out/'public/assets/original/opening';dest.mkdir(parents=True,exist_ok=True)
def atlas(pkg,item):
 path='Assets/Bundles/UIRes/UIPackage/'+pkg+'_'+item['file'];f=paths[path]
 if f not in cache:
  b=(r/'raw'/f).read_bytes();env=UnityPy.load(b[b.index(b'UnityFS'):]);imgs={}
  for o in env.objects:
   if o.type.name=='Texture2D':
    t=o.read();imgs[t.m_Name]=t.image
  cache[f]=imgs
 name=pkg+'_'+Path(item['file']).stem;im=cache[f].get(name,cache[f].get(Path(item['file']).stem)).convert('RGBA');a=cache[f].get(name+'!a')
 if a is not None:im.putalpha(a.convert('RGB').getchannel('R'))
 return im
for pkg,keys in needed.items():
 its={i['id']:i for i in meta[pkg]['items']};sprites={i['id']:i for i in meta[pkg]['sprites']}
 for id in keys:
  if id not in sprites:continue
  sp=sprites[id];im=atlas(pkg,its[sp['atlas']]);x,y,w,h=sp['rect'];im=im.crop((x,y,x+w,y+h))
  if sp['rotated']:im=im.transpose(Image.Transpose.ROTATE_270)
  file=pkg+'-'+id+'.png';im.save(dest/file);images[pkg+'/'+id]={'name':its[id]['name'],'url':'/assets/original/opening/'+file,'size':list(im.size),'sourceId':id}
(out/'public/data/original/opening-source.json').write_text(json.dumps({'source':'Uploaded FairyGUI binaries and Unity atlases','packageIds':ids,'components':used,'images':images},separators=(',',':')))
print('components',sum(map(len,used.values())),'images',len(images))
