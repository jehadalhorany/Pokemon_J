from pathlib import Path
import json,UnityPy
r=Path(__file__).resolve().parent;raw=r.parent/'restored-current/fairy-work/raw';out={}
for row in json.loads((r/'inventory-fast.json').read_text()):
 paths=[p for p in row['paths']if '/Conmon/MainCamera' in p and p.endswith('.prefab')and 'PostEffect'not in p]
 if not paths:continue
 b=(raw/row['file']).read_bytes();e=UnityPy.load(b[b.index(b'UnityFS'):]);cam=None;follow=None
 for o in e.objects:
  if o.type.name=='Camera':cam=o.read_typetree()
  if o.type.name=='MonoBehaviour':
   try:
    v=o.read_typetree()
    if 'Pos'in v and 'Rot'in v:follow=v
   except:pass
 if cam and follow:
  v=cam['m_BackGroundColor'];out[Path(paths[0]).stem.lower()]={'source':paths[0],'bundle':row['file'],'fov':cam['field of view'],'near':cam['near clip plane'],'far':cam['far clip plane'],'orthographic':cam['orthographic'],'orthographicSize':cam['orthographic size'],'background':[v[k]for k in ['r','g','b']],'position':[follow['Pos'][k]for k in ['x','y','z']],'rotation':[follow['Rot'][k]for k in ['x','y','z','w']]}
p=r.parent/'active-project/public/data/original/cameras.json';p.write_text(json.dumps(out,separators=(',',':')));print('cameras',len(out))
