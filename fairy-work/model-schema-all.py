import dnfile,json
p=dnfile.dnPE('fairy-work/Model.dll');out={};const={}
for c in p.net.mdtables.Constant:
 if c.Parent.table.name=='Field':const[c.Parent.row_index]=c.Value.value.hex()
for t in p.net.mdtables.TypeDef:
 out[str(t.TypeName)]=[{'name':str(f.row.Name),'signature':f.row.Signature.value.hex(),'constant':const.get(f.row_index)} for f in t.FieldList]
open('fairy-work/model-types-all.json','w').write(json.dumps(out))
print({k:v for k,v in out.items() if k in ['ObjectType','MapInfo','TileInfo','NpcInfo','NpcType','TileType','BlockType'] or any(s in k for s in ['MapCell','GridType','TileType','MapObject','Door'])})
