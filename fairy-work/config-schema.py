import dnfile,json
from pathlib import Path
p=dnfile.dnPE('fairy-work/Model.dll');out={}
def compressed(b,i):
 a=b[i]
 if a<128:return a,i+1
 if a<192:return ((a&63)<<8)|b[i+1],i+2
 return ((a&31)<<24)|(b[i+1]<<16)|(b[i+2]<<8)|b[i+3],i+4
def typ(b,i=1):
 k=b[i];i+=1
 if k==0x1d:
  t,i=typ(b,i);return {'array':t},i
 if k in [0x11,0x12]:
  token,i=compressed(b,i);table=[p.net.mdtables.TypeDef,p.net.mdtables.TypeRef,p.net.mdtables.TypeSpec][token&3];row=table[(token>>2)-1];return {'struct' if k==0x11 else 'class':str(getattr(row,'TypeName','?'))},i
 return {2:'bool',4:'sbyte',5:'byte',6:'short',7:'ushort',8:'int',9:'uint',10:'long',11:'ulong',12:'float',13:'double',14:'string'}.get(k,'unknown'+hex(k)),i
for t in p.net.mdtables.TypeDef:
 name=str(t.TypeName)
 if name.endswith('Config') or name in ['MapAreaConfig','MapWorldConfig','MapPointConfig','MapMiniConfig','NpcConfig','ModelConfig','Int2','Int3','Long2','int2','int3','long2','MapObjectType','NpcType','SceneType','MapAreaType','LanguageConfig','FunctionConfig','NpcFunctionConfig'] or name.endswith('ConfigCategory'):
  out[name]=[{'name':str(f.row.Name).replace('<','').replace('>k__BackingField','').lstrip('_'),'type':typ(f.row.Signature.value)[0]} for f in t.FieldList if str(f.row.Name) not in ['Instance','_instance']]
Path('fairy-work/config-schema.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k in ['MapMiniConfig','int2','Int2','Long2','MapAreaType']})
