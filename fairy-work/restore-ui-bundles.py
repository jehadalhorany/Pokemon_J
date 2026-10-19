"""Restore only uploaded native UI bundles; preserve their source hashes."""
from pathlib import Path
import json,zipfile
root=Path(__file__).resolve().parent
inventory=json.loads((root/'inventory-fast.json').read_text())
wanted={r['file']:r for r in inventory if any('/UIRes/UIPackage/' in p for p in r.get('paths',[]))}
out=root/'raw';out.mkdir(exist_ok=True)
found={}
for archive in sorted((root.parent/'raw-packs').glob('*.zip')):
 try:
  with zipfile.ZipFile(archive) as z:
   for name in z.namelist():
    base=Path(name).name
    if base in wanted:
     (out/base).write_bytes(z.read(name));found[base]={'archive':archive.name,'member':name,'paths':wanted[base]['paths']}
 except zipfile.BadZipFile:continue
(root/'ui-bundle-provenance.json').write_text(json.dumps(found,indent=2))
print('native UI bundles',len(found),'of',len(wanted))
