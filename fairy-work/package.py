import pathlib,json,gzip,struct,zipfile,hashlib
root=pathlib.Path('pokemon-j');assets=root/'public/assets/imported';manifest=json.load(open(assets/'catalog.json'))
# Include all assets needed by the tested starter journey in the small patch.
ids={'96b6f38d651d92c3c4a3c20646fa6852','b6d96f615b09060654aaa8bb15ddd4b8','78c89fcd70f473a4dbd1776afe6ddbfc','37a25367d4d807b079c223290a09264c','2b55d96529d5aca595313f785dd1efc1','e7117792d1b9d392b3cba28a6fb341b0','7946d87f3897ecc1d448ecba8f3676ea','d9bfb0ecbb348c8c241ddce634373842','7a35e884363b6231894a00b11033b44b','c26ed6d3ba0805c4bc08982d7f33e6d4','4ad6fa0a71751d81f708d70a7ee7cc46','5c99f083d4246a1c02a1d26316b25d2c','fb835a6869d68b8e9b486bdc1d4751e1'}
for n in [1,4,7,10,11,13,14,16,19,25]:
 k=str(n).zfill(5)
 if k in manifest['pokemon']:ids.add(manifest['pokemon'][k])
core=set([assets/'catalog.json'])
for id in ids:
 p=assets/'models'/f'{id}.glb.gz';core.add(p);b=gzip.decompress(p.read_bytes());n=struct.unpack_from('<I',b,12)[0];d=json.loads(b[20:20+n])
 for image in d.get('images',[]):core.add(assets/'textures'/pathlib.Path(image['uri']).name)
clipids={'3e8c7a1fc56a7f0fc8769217b441605b','da37809fd36e47cd3b3974f4e4ccf67f'}
for a in manifest['animations']:
 if a['bundle'].replace('.bundle','') in ids or any(any('/pm'+str(n).zfill(4)+'/' in p for n in [1,4,7,10,11,13,14,16,19,25]) and p.endswith('/Idle.anim') for p in a['paths']):clipids.add(a['file'].replace('.json',''))
for id in clipids:
 p=assets/'animations'/f'{id}.json.gz'
 if p.exists():core.add(p)
# Keep patch cumulative over the prior v04 patch.
files=set(core)
for folder in ['server','public/vendor','tools/asset-import']:
 files.update(p for p in (root/folder).rglob('*') if p.is_file() and '__pycache__' not in str(p))
for name in ['public/scene.js','public/asset-runtime.js','public/pokemon-3d.js','public/app.js','public/ui.js','public/index.html','public/style.css','public/import-preview.html','public/asset-browser.html','asset-source-index.json','ASSET_IMPORT_v04.md','PAUSED_CHECKPOINT.md']:files.add(root/name)
patch=pathlib.Path('Pokemon_J_v04_patch.zip')
with zipfile.ZipFile(patch,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(files):z.write(p,str(p.relative_to(root)))
others=[p for p in sorted(assets.rglob('*')) if p.is_file() and p not in core];limit=95*1024*1024;part=0;size=0;packs=[];z=None
for p in others:
 n=p.stat().st_size
 if z is None or size+n>limit:
  if z:z.close()
  part+=1;dest=pathlib.Path(f'Pokemon_J_v04_assets_{part:02}.zip');packs.append(dest);z=zipfile.ZipFile(dest,'w',zipfile.ZIP_STORED);size=0
 z.write(p,str(p.relative_to(root)));size+=n
if z:z.close()
result={'patch':{'file':str(patch),'bytes':patch.stat().st_size,'files':len(files)},'packs':[{'file':str(p),'bytes':p.stat().st_size} for p in packs],'assetFileCount':sum(1 for p in assets.rglob('*') if p.is_file())}
json.dump(result,open('fairy-work/packages.json','w'),indent=2);print(json.dumps(result,indent=2))
