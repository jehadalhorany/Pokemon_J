from pathlib import Path
import dnfile,json
root=Path(__file__).resolve().parent/'recovered-client'
for name in ['Hotfix.dll','Model.dll']:
 p=dnfile.dnPE(str(root/name));types=[]
 for row in p.net.mdtables.TypeDef.rows:
  types.append({'name':str(row.TypeName),'namespace':str(row.TypeNamespace),'fields':[str(f.row.Name)for f in row.FieldList],'methods':[{'name':str(m.row.Name),'rva':m.row.Rva,'index':m.row_index}for m in row.MethodList]})
 (root/(name+'.types.json')).write_text(json.dumps(types,separators=(',',':')))
 print(name,len(types),flush=True)
