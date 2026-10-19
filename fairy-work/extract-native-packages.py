from pathlib import Path
import json,UnityPy
r=Path(__file__).resolve().parent
rows=json.loads((r/'ui-bundle-provenance.json').read_text())
count=0
for name,row in rows.items():
 if not any(p.endswith('_fui.bytes') for p in row['paths']):continue
 b=(r/'raw'/name).read_bytes();env=UnityPy.load(b[b.index(b'UnityFS'):])
 for o in env.objects:
  if o.type.name=='TextAsset':
   a=o.read();(r/(a.m_Name+'.bin')).write_bytes(a.m_Script.encode('utf8','surrogateescape'));count+=1;print(a.m_Name,flush=True)
print('package binaries',count)
