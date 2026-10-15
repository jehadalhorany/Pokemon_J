import struct,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
SCHEMA=json.load(open(ROOT/'config-schema.json'))
class Reader:
 def __init__(self,b):self.b=b;self.p=0
 def value(self,t):
  if isinstance(t,dict):
   if 'array'in t:
    n=self.value('int')
    if n==-1:return None
    assert 0<=n<500000,(self.p,n,t)
    return [self.value(t['array']) for _ in range(n)]
   name=t.get('struct') or t.get('class')
   if name in ['int2','int3','int4','long2','long3','float2','float3']:
    return [self.value('long' if name.startswith('long') else 'float' if name.startswith('float') else 'int') for _ in range(int(name[-1]))]
   raise ValueError((self.p,name))
  if t=='string':
   n=self.value('int')
   if n==-1:return None
   if n< -1:
    length=-n-1;self.value('int');v=self.b[self.p:self.p+length].decode('utf8');self.p+=length;return v
   v=self.b[self.p:self.p+n*2].decode('utf-16-le');self.p+=n*2;return v
  fmt={'int':'i','uint':'I','long':'q','ulong':'Q','float':'f','double':'d','bool':'?','byte':'B','sbyte':'b','short':'h','ushort':'H'}[t];v=struct.unpack_from('<'+fmt,self.b,self.p)[0];self.p+=struct.calcsize(fmt);return v
 def object(self,name):
  count=self.value('byte')
  if count==255:return None
  schema=SCHEMA[name];assert count==len(schema),(name,count,len(schema),self.p)
  return {f['name']:self.value(f['type']) for f in schema}
def config(name):
 r=Reader((ROOT/(name+'Category.bin')).read_bytes());assert r.value('byte')==1;n=r.value('int');rows=[r.object(name) for _ in range(n)];assert r.p==len(r.b),(name,r.p,len(r.b));return rows
if __name__=='__main__':
 for name in ['MapWorldConfig','MapAreaConfig','MapMiniConfig','MapPointConfig','ModelConfig','NpcConfig']:
  try:
   rows=config(name);(ROOT/(name+'.json')).write_text(json.dumps(rows,ensure_ascii=False));print(name,len(rows),rows[:1],flush=True)
  except Exception as e:print('ERROR',name,e,flush=True)
