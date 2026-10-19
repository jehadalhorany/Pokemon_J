"""Recover source parameters for PokemonDate/Eye texture-coordinate shaders.
No parameters are guessed for unsupported shaders. Shader math was inspected
in the uploaded PokemonBase Vulkan subprogram (fallback of PokemonDate/Eye).
"""
import json,pathlib,UnityPy,concurrent.futures
R=pathlib.Path(__file__).resolve().parent;O=R.parent/'pokemon-j/public/data/original/native-materials.json'
b=(R/'raw/98011065bf2fbc5aede2182269d72494.bundle').read_bytes();e=UnityPy.load(b[b.index(b'UnityFS'):]);shaders={}
for o in e.objects:
 if o.type.name=='Shader':
  s=o.read();shaders[o.path_id]=s.m_ParsedForm.m_Name
rows=[r for r in json.loads((R/'inventory-fast.json').read_text())if any('/Prefabs/Eudmon/' in p and p.endswith('.prefab')for p in r['paths'])]
def scan(row):
 result={}
 try:
  b=(R/'raw'/row['file']).read_bytes();e=UnityPy.load(b[b.index(b'UnityFS'):])
  for o in e.objects:
   if o.type.name!='Material':continue
   m=o.read();shader=shaders.get(m.m_Shader.m_PathID)
   if shader not in ['Pokemon/PokemonDate','Pokemon/PokemonEye']:continue
   floats=dict(m.m_SavedProperties.m_Floats);tex=dict(m.m_SavedProperties.m_TexEnvs).get('_MainTex')
   if tex:result[m.m_Name]={'shader':shader,'scale':[tex.m_Scale.x,tex.m_Scale.y],'offset':[tex.m_Offset.x,tex.m_Offset.y],'doubleTex':floats.get('_DoubleTex',0),'flipMask':floats.get('_FlipMask1',0),'needMoveUV':floats.get('_NeedMoveUV',0),'sourceMaterial':str(o.path_id)}
 except Exception as ex:return row['file'][:-7],{'error':str(ex)}
 return row['file'][:-7],result
if __name__=='__main__':
 result={}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
  for k,v in pool.map(scan,rows):
   if v:result[k]=v
 O.write_text(json.dumps({'source':'Uploaded Unity prefab material records','models':result},separators=(',',':')))
 print('native materials',len(result),'errors',sum('error'in v for v in result.values()),flush=True)
