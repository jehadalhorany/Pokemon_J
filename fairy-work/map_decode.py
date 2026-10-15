import struct,json,sys,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent));from convert import Env,ROOT
def var(b,p):
 v=0;s=0
 while True:
  n=b[p];p+=1;v|=(n&127)<<s;s+=7
  if n<128:return v,p
  if s>70:raise ValueError()
def decode(b):
 p=0;r={}
 while p<len(b):
  tag,p=var(b,p);f,w=tag>>3,tag&7
  if not f:raise ValueError()
  if w==0:v,p=var(b,p)
  elif w==2:n,p=var(b,p);v=b[p:p+n];p+=n
  elif w==5:v=struct.unpack_from('<f',b,p)[0];p+=4
  elif w==1:v=struct.unpack_from('<d',b,p)[0];p+=8
  else:raise ValueError(w)
  r.setdefault(f,[]).append(v)
 return r
def show(v,depth=0):
 if isinstance(v,bytes):
  try:
   s=v.decode();
   if s and all(ord(c)>=32 for c in s):return s
  except:pass
  if depth>4:return v.hex()[:100]
  try:return {k:[show(z,depth+1) for z in a[:3]]+(['... '+str(len(a))] if len(a)>3 else []) for k,a in decode(v).items()}
  except:return v.hex()[:100]
 return v
if __name__=='__main__':
 e=Env();e.load_file((ROOT/'raw/d7d70f729c562bba141e00add824a7d9.bundle').read_bytes(),name='map')
 for o in e.objects:
  if o.type.name=='TextAsset' and o.read().m_Name=='1000001':
   b=o.read().m_Script.encode('utf8','surrogateescape');print(json.dumps(show(b),indent=1))
def signed(n):return n-(1<<64) if n>(1<<63) else n
def vector(b,default=0):
 d=decode(b);return [signed(d.get(k,[default])[0]) for k in [1,2,3]]
def placements(d):
 rows=[]
 for chunk in d.get(9,[]):
  q=decode(decode(chunk)[2][0])
  for entry in q.get(1,[]):
   e=decode(entry);name=e[1][0].decode()
   for raw in e.get(2,[]):
    t=decode(raw)
    for raw2 in t.get(1,[]):
     tr=decode(raw2);rows.append({'name':name,'p':vector(tr.get(1,[b''])[0]),'r':vector(tr.get(2,[b''])[0]),'s':vector(tr.get(3,[b''])[0],10),'fields':list(tr)})
 return rows
