from convert import Env,ROOT,GLB,OUT
E=Env();E.load_file((ROOT/'raw'/'01fd539f979286f109329b1f300b6a38.bundle').read_bytes())
for f in list(E.cabs.values()):
 if not hasattr(f,'objects'):continue
 for o in list(f.objects.values()):
  if o.type.name!='Transform':continue
  t=o.read()
  if t.m_Father:continue
  name=t.m_GameObject.read().m_Name
  if name not in ['ZhanDou_04']:continue
  g=GLB();g.doc['scenes'][0]['nodes'].append(g.transform(type('Ref',(),{'deref':lambda self:o})()));g.add_renderers();id='battle-forest' if name=='ZhanDou_04' else 'battle-indoor';g.save(OUT/'models'/(id+'.glb'));print(id,len(g.doc['meshes']),g.warnings,flush=True)
