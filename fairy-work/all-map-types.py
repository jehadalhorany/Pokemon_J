import dnfile,json
p=dnfile.dnPE('fairy-work/Model.dll');out=[]
for t in p.net.mdtables.TypeDef:
 name=str(t.TypeName)
 if any(s in name.lower() for s in ['map','collider','grid','door','sceneconfig','objecttype','configtype']):
  out.append({'name':name,'fields':[str(f.row.Name) for f in t.FieldList]})
open('fairy-work/all-map-types.json','w').write(json.dumps(out));print('\n'.join(str(x) for x in out if not any(s in x['name'] for s in ['ConfigCategory','Formatter','_DisplayClass'])))
