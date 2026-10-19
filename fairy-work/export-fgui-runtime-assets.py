from pathlib import Path
import json,UnityPy,shutil,sys
R=Path(__file__).resolve().parent;raw=R/'raw';out=R.parent/'pokemon-j/public/assets/original/packages';out.mkdir(parents=True,exist_ok=True)
rows=json.loads((R/'inventory-fast.json').read_text());paths={Path(p).name:(row['file'],p)for row in rows for p in row['paths']};manifest=json.loads((out/'provenance.json').read_text()).get('files',{}) if (out/'provenance.json').exists() else {};errors=[]
for pkg in (sys.argv[1:] or ['Base','Common','Item','EudemonIcon','Role','Spine','Main','Map','Assignment']):
 shutil.copyfile(R/(pkg+'_fui.bin'),out/(pkg+'.fui'));meta=json.loads((R/f'fui-{pkg}.json').read_text());done=set()
 for item in meta['items']:
  if item['type']not in [4,2]:continue
  file=item['file']
  if not file:continue
  source=pkg+'_'+file
  if source not in paths:errors.append(source);continue
  bundle,path=paths[source]
  if bundle in done:continue
  done.add(bundle);b=(raw/bundle).read_bytes();e=UnityPy.load(b[b.index(b'UnityFS'):]);textures={}
  for o in e.objects:
   if o.type.name=='Texture2D':
    t=o.read();textures[t.m_Name]=t.image
   elif o.type.name=='AudioClip':
    try:
     a=o.read()
     for filename,data in a.samples.items():(out/(pkg+'_'+filename)).write_bytes(data)
    except:pass
  for name,im in textures.items():
   if name.endswith('!a'):continue
   im=im.convert('RGBA');alpha=textures.get(name+'!a')
   if alpha is not None:im.putalpha(alpha.convert('RGB').getchannel('R'))
   dest=out/(name+'.png');im.save(dest);manifest[dest.name]={'source':path,'bundle':bundle,'size':list(im.size)}
 print(pkg,len(done),flush=True)
(out/'provenance.json').write_text(json.dumps({'files':manifest,'missing':errors},separators=(',',':')));print('atlas files',len(manifest),'missing',errors,flush=True)
