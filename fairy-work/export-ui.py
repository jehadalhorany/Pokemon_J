from convert import Env,ROOT
import json,pathlib
rows=json.load(open(ROOT/'inventory.json'));prefixes=['Base','Res','FunctionOpen'];names=[]
for row in rows:
 if not any('/UIRes/UIActivity/Main/' in p for p in row['paths']):continue
 E=Env();E.load_file((ROOT/'raw'/row['file']).read_bytes())
 for o in E.objects:
  if o.type.name=='TextAsset':
   a=o.read();(ROOT/(a.m_Name+'.bin')).write_bytes(a.m_Script.encode('utf8','surrogateescape'))
  if o.type.name=='Texture2D':
   a=o.read();p=ROOT/'ui-original'/ (a.m_Name+'.png');p.parent.mkdir(exist_ok=True);a.image.save(p);names.append(a.m_Name)
print('UI textures',names,flush=True)
for row in rows:
 if not any('/Sound/' in p and any(s in p.lower() for s in ['click','button','sound_map1101','sound_map1201','sound_opendoor','sound_exitdoor']) for p in row['paths']):continue
 try:
  E=Env();E.load_file((ROOT/'raw'/row['file']).read_bytes())
  for o in E.objects:
   if o.type.name=='AudioClip':
    a=o.read();samples=a.samples
    for name,data in samples.items():
     path=ROOT.parent/'pokemon-j/public/assets/original/audio'/name;path.parent.mkdir(exist_ok=True,parents=True);path.write_bytes(data);print('AUDIO',name,len(data),flush=True)
 except Exception as e:print('AUDIO ERROR',row['paths'],str(e),flush=True)
