from convert import Env,ROOT,GLB
E=Env();E.load_file((ROOT/'raw'/'01fd539f979286f109329b1f300b6a38.bundle').read_bytes())
for f in list(E.cabs.values()):
 if not hasattr(f,'objects'):continue
 for o in list(f.objects.values()):
  if o.type.name!='Transform':continue
  t=o.read()
  if not t.m_Father and t.m_GameObject.read().m_Name=='ZhanDou_04':
   g=GLB();g.transform(type('Ref',(),{'deref':lambda self:o})());g.add_renderers()
for f in list(E.cabs.values()):
 if not hasattr(f,'objects'):continue
 for o in list(f.objects.values()):
  if o.type.name!='Material':continue
  m=o.read()
  if m.m_Name=='SM_Battle_005_03_Floor_Msk3':
   print(m.m_Name,[(str(k),v.m_Texture.path_id,v.m_Scale) for k,v in m.m_SavedProperties.m_TexEnvs]);print(m.m_SavedProperties.m_Colors)
