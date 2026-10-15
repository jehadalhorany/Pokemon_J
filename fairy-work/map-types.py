import dnfile,json
p=dnfile.dnPE('fairy-work/Model.dll');out={}
for t in p.net.mdtables.TypeDef:
 name=str(t.TypeName)
 if any(x in name.lower() for x in ['mapobject','mapobj','scenenpc','doortype','mapnpc','mapsprite','maplink','mapdata','areatype','mapmin','modeltype']):
  out[name]=[{'name':str(f.row.Name),'type':f.row.Signature.value.hex()} for f in t.FieldList];print(name,out[name],flush=True)
open('fairy-work/map-types.json','w').write(json.dumps(out))
