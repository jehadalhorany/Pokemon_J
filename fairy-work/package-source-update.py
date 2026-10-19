from pathlib import Path
import zipfile,json,hashlib
root=Path(__file__).resolve().parent.parent;project=root/'active-project';dest=root/'delivery';dest.mkdir(exist_ok=True)
files=[]
for top in ['public','server']:
 for p in sorted((project/top).rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(project)
  if str(rel).startswith('public/assets/imported/') and rel!=Path('public/assets/imported/catalog.json'):continue
  if p.suffix in ['.sqlite','.db']:continue
  files.append((p,rel))
for name in ['package.json','INSTALL_SOURCE_UPDATE_AR.md','SOURCE_STORY_VALIDATION.json','SOURCE_DIALOGUE_LAYOUT_VALIDATION.json','SOURCE_MAP_VALIDATION.json','SOURCE_PACKAGE_VALIDATION.json','RECOVERY_STATUS_2026-10-17.md']:
 files.append((project/name,Path(name)))
chunks=[];current=[];size=0;limit=36*1024*1024
for p,rel in files:
 if current and size+p.stat().st_size>limit:chunks.append(current);current=[];size=0
 current.append((p,rel));size+=p.stat().st_size
if current:chunks.append(current)
manifest=[]
for index,chunk in enumerate(chunks,1):
 out=dest/f'Pokemon_J_v04_source_update_{index:02d}.zip'
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for p,rel in chunk:z.write(p,str(rel))
 with zipfile.ZipFile(out) as z:assert z.testzip() is None
 manifest.append({'name':out.name,'files':len(chunk),'size':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
 print(index,len(chunk),out.stat().st_size,flush=True)
(dest/'SOURCE_UPDATE_PARTS.json').write_text(json.dumps(manifest,indent=2))
print('parts',len(manifest),'files',len(files))
