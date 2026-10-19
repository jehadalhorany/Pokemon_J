from pathlib import Path
import UnityPy,json,subprocess,sys
r=Path(__file__).resolve().parent;raw=r.parent/'restored-current/fairy-work/raw';rows=json.loads((r/'inventory-fast.json').read_text());count=0
for row in rows:
 if not any(p.endswith('_fui.bytes')for p in row['paths']):continue
 b=(raw/row['file']).read_bytes();env=UnityPy.load(b[b.index(b'UnityFS'):])
 for o in env.objects:
  if o.type.name=='TextAsset':
   a=o.read();p=r/(a.m_Name+'.bin');p.write_bytes(a.m_Script.encode('utf8','surrogateescape'));pkg=a.m_Name[:-4]if a.m_Name.endswith('_fui')else a.m_Name
   q=subprocess.run([sys.executable,str(r/'fui.py'),pkg],capture_output=True,text=True)
   print(pkg,q.returncode,flush=True);count+=1
print('packages',count)
