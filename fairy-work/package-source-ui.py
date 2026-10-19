from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent.parent;root=R/'active-project'
files=set()
for p in (root/'public').glob('*'):
 if p.is_file()and p.suffix in ['.js','.css','.html']:files.add(p.relative_to(root))
for folder in ['public/vendor','public/assets/original/packages','public/assets/original/opening','public/data/original','server']:
 for p in (root/folder).rglob('*'):
  if p.is_file()and '__pycache__'not in p.parts and 'node_modules'not in p.parts:files.add(p.relative_to(root))
files.update(Path(p)for p in ['public/assets/original/source-world-map.png','INSTALL_SOURCE_UI_AR.md','SOURCE_MAP_VALIDATION.json','OPENING_VALIDATION.json'])
manifest={str(p):hashlib.sha256((root/p).read_bytes()).hexdigest()for p in sorted(files)}
patch=R/'Pokemon_J_v04_source_ui_patch.zip'
with zipfile.ZipFile(patch,'w',zipfile.ZIP_DEFLATED,compresslevel=5)as z:
 for p in sorted(files):z.write(root/p,str(p))
 z.writestr('SOURCE_UI_PATCH_SHA256.json',json.dumps(manifest,indent=2))
assert zipfile.ZipFile(patch).testzip()is None
print('Validated source UI patch',patch.stat().st_size,'bytes',len(files),'files',flush=True)
checkpoint=R/'Pokemon_J_v04_checkpoint.zip'
with zipfile.ZipFile(checkpoint,'w',zipfile.ZIP_DEFLATED,compresslevel=5)as z:
 for p in root.rglob('*'):
  if not p.is_file():continue
  rel=p.relative_to(root)
  if any(x in ['node_modules','__pycache__']for x in rel.parts)or rel.parts[0]=='data'or '/assets/imported/'in str(p)or p.suffix in ['.sqlite','.db']or('assets/original/packages'in str(rel)and p.suffix=='.png'):continue
  z.write(p,str(Path('pokemon-j')/rel))
 for p in (R/'build-tools').glob('*'):
  if p.is_file()and(p.suffix in ['.py','.cjs','.mjs','.md']or p.name.endswith('_fui.bin')or p.name.startswith('fui-')and p.suffix in ['.json','.bin']or p.name in ['cab-index.json','ui-bundle-provenance.json','inventory-fast.json','language-en.json','portrait-bundles.jsonl']):z.write(p,str(Path('fairy-work')/p.name))
assert zipfile.ZipFile(checkpoint).testzip()is None
print('Validated checkpoint',checkpoint.stat().st_size,'bytes',flush=True)
