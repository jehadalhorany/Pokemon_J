import pathlib,zipfile
root=pathlib.Path('pokemon-j');out=pathlib.Path('Pokemon_J_v04_checkpoint.zip')
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 for p in root.rglob('*'):
  if not p.is_file() or any(s in p.parts for s in ['node_modules','__pycache__','data'] if s not in []):
   # public/data is handled below; exclude runtime save databases.
   if not (p.is_file() and 'public' in p.parts and 'data' in p.parts):continue
  if '/assets/imported/' in str(p) or p.suffix in ['.sqlite','.db']:continue
  z.write(p,str(p))
 for p in pathlib.Path('fairy-work').glob('*'):
  if p.is_file() and (p.suffix in ['.py','.cjs','.mjs'] or p.name in ['maps-index.json','config-schema.json','world-export-missing.json','all-config-results.json','original-navigation-results.json','language-en.json','inventory-fast.json','portrait-bundles.jsonl','ui-rotation-fixes.json','fui-EudemonIcon.json','fui-Main.json','fui-Map.json','fui-Common.json','fui-Base.json']):z.write(p,str(p))
print(out.stat().st_size)
