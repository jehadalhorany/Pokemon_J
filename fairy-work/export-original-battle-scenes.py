from pathlib import Path
import json,sys
import convert as c
R=Path(__file__).resolve().parent;c.ROOT=R;c.OUT=R.parent/'pokemon-j/public/assets/imported';out=R.parent/'pokemon-j/public/data/original'
e=c.Env();p=c.ROOT/'raw/01fd539f979286f109329b1f300b6a38.bundle';b=p.read_bytes();e.load_file(b[b.index(b'UnityFS'):]);scenes={}
for f in list(e.cabs.values()):
 if not hasattr(f,'objects'):continue
 for o in list(f.objects.values()):
  if o.type.name=='AssetBundle':
   for path,cab in o.read_typetree().get('m_SceneHashes',[]):scenes[cab.lower()]={'name':Path(path).stem,'source':path,'cab':cab}
for f in list(e.cabs.values()):
 if not hasattr(f,'objects') or f.name.lower() not in scenes:continue
 row=scenes[f.name.lower()];g=c.GLB()
 for o in list(f.objects.values()):
  if o.type.name=='Transform' and not o.read().m_Father:g.doc['scenes'][0]['nodes'].append(g.transform(type('Ref',(),{'deref':lambda self,o=o:o})()))
  if o.type.name=='RenderSettings':row['renderSettings']=o.read_typetree()
 g.add_renderers();row['model']='source-battle-'+row['name'];
 if not g.doc['meshes']:
  row['unavailable']='No renderable source mesh';continue
 g.save(c.OUT/'models'/(row['model']+'.glb'));row['warnings']=g.warnings;print(row['name'],len(g.doc['meshes']),len(g.warnings),flush=True)
result={'scenes':{r['name']:r for r in scenes.values()},'camera':{'source':'c483baf3e646f1d59aa603b179dbcb37','position':[1.8899999857,.6700000167,-6.1100001335],'quaternion':[-.0019949139,-.1705101877,-.0003452091,.9853538275],'fov':25,'near':.5,'far':500},'positions':{'ally':[0,0,-3],'enemy':[0,0,3]},'evidence':'BattleCameraHelper 6113/6115; BattlePosCompoent ctor55583; BattleUnitHelper.GetPos4458'}
(out/'battle-scenes.json').write_text(json.dumps(result,separators=(',',':')))
