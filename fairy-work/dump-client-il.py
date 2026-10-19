from pathlib import Path
import dnfile,sys,json
from dncil.cil.body import CilMethodBody
from dncil.cil.body.reader import CilMethodBodyReaderBytes
root=Path(__file__).resolve().parent/'recovered-client'
p=dnfile.dnPE(str(root/sys.argv[1]));tables=p.net.mdtables
owners={m.row_index:t['name'] for t,row in zip(json.loads((root/(sys.argv[1]+'.types.json')).read_text()),tables.TypeDef.rows) for m in row.MethodList}
def token(v):
 n=v.value;kind=n>>24;idx=n&0xffffff
 if kind==0x70:
  try:return repr(p.net.user_strings.get(idx).value)
  except:return hex(n)
 table={6:'MethodDef',10:'MemberRef',4:'Field',2:'TypeDef',1:'TypeRef',43:'MethodSpec'}.get(kind)
 if not table:return hex(n)
 row=getattr(tables,table).rows[idx-1]
 if table=='MethodSpec':
  raw=bytes(row.Instantiation.value);pos=2;args=[]
  def compressed():
   nonlocal pos
   n=raw[pos];pos+=1
   if n<128:return n
   if n<192:n=((n&63)<<8)|raw[pos];pos+=1;return n
   n=((n&31)<<24)|int.from_bytes(raw[pos:pos+3],'big');pos+=3;return n
  while pos<len(raw):
   code=compressed()
   if code in [17,18]:
    ref=compressed();target=[tables.TypeDef,tables.TypeRef,tables.TypeSpec][ref&3].rows[(ref>>2)-1];args.append(str(getattr(target,'TypeNamespace',''))+'.'+str(getattr(target,'TypeName','?')))
   else:args.append(hex(code))
  return token(type(v)((row.Method.table.number<<24)|row.Method.row_index))+'<'+','.join(args)+'>'

 return (owners.get(idx,'')+'::' if table=='MethodDef' else '')+str(getattr(row,'Name',getattr(row,'TypeName',hex(n))))
out=root/'il';out.mkdir(exist_ok=True)
for index in map(int,sys.argv[2:]):
 row=tables.MethodDef.rows[index-1];body=CilMethodBody(CilMethodBodyReaderBytes(p.get_data(row.Rva,100000)))
 lines=[owners.get(index,'')+'::'+str(row.Name)]
 for i in body.instructions:
  v=i.operand
  if hasattr(v,'value'):v=token(v)
  lines.append(f'{i.offset:04x} {i.opcode.name} {v if v is not None else ""}')
 dest=out/(str(index)+'-'+str(row.Name)+'.txt');dest.write_text('\n'.join(lines));print(dest,flush=True)
