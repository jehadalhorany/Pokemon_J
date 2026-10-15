from convert import Env,ROOT
import json
for id in ['3c74f1c12a52c9cb3f237cefd7da525d','25be22d807e5a43a61d653d9dc203b9d','c051f52621051aaeabad21b946821d53','f0accdc9031bc17a26054740d6316e7b','9e6594de12b23627cabd5273225a5e40']:
 E=Env();E.load_file((ROOT/'raw'/(id+'.bundle')).read_bytes())
 for o in E.objects:
  if o.type.name=='TextAsset':
   a=o.read()
   if 'LanguageConfig_'in a.m_Name and 'LanguageConfig_en'not in a.m_Name:continue
   b=a.m_Script.encode('utf8','surrogateescape');(ROOT/(a.m_Name+'.bin')).write_bytes(b);print(a.m_Name,len(b),flush=True)
  if o.type.name=='Texture2D':
   a=o.read();a.image.save(ROOT/(a.m_Name+'.png'));print(a.m_Name,a.m_Width,a.m_Height,flush=True)
