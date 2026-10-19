from pathlib import Path
import zipfile

root=Path(__file__).resolve().parent.parent
out=root/'Pokemon_J_v04_checkpoint.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 for p in sorted((root/'active-project').rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(root/'active-project')
  if rel.parts[0] in ['data','node_modules'] or p.suffix in ['.db','.sqlite']:continue
  if str(rel).startswith('public/assets/imported/'):continue
  if str(rel).startswith('public/assets/original/packages/') and p.suffix=='.png':continue
  z.write(p,str(Path('pokemon-j')/rel))
 for p in sorted((root/'build-tools').glob('*')):
  if not p.is_file():continue
  if p.suffix in ['.py','.cjs','.mjs'] or p.name.endswith('_fui.bin') or p.name.startswith('fui-') or p.name in ['resource-update-manifest.json','pve-main-inspection.json','menu-runtime-inspection.json','maps-index.json','config-schema.json','world-export-missing.json','all-config-results.json','original-navigation-results.json','language-en.json','inventory-fast.json','portrait-bundles.jsonl','ui-rotation-fixes.json','ui-bundle-provenance.json']:
   z.write(p,str(Path('fairy-work')/p.name))
 for p in sorted((root/'build-tools/recovered-client').rglob('*')):
  if p.is_file() and not any(part.startswith('.') for part in p.relative_to(root/'build-tools/recovered-client').parts):z.write(p,str(Path('fairy-work/recovered-client')/p.relative_to(root/'build-tools/recovered-client')))
print(out,out.stat().st_size)
