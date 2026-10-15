from convert import Env,ROOT
import json
E=Env();E.load_file((ROOT/'raw/3c74f1c12a52c9cb3f237cefd7da525d.bundle').read_bytes())
for o in E.objects:
 if o.type.name=='TextAsset':
  a=o.read()
  if any(s in a.m_Name for s in ['MapWorld','MapMini','MapPoint','NpcConfig','AreaConfig','MapArea']):
   b=a.m_Script.encode('utf8','surrogateescape');(ROOT/(a.m_Name+'.bin')).write_bytes(b);print(a.m_Name,len(b),repr(b[:260]))
