"""Decode uploaded protobuf activity categories, retaining source field names."""
from pathlib import Path
import gzip,json,struct
ROOT=Path(__file__).resolve().parent
def var(b,p):
 n=s=0
 while True:
  c=b[p];p+=1;n|=(c&127)<<s;s+=7
  if c<128:return n,p
def decode(b):
 r={};p=0
 while p<len(b):
  tag,p=var(b,p);f,w=tag>>3,tag&7
  if w==0:v,p=var(b,p)
  elif w==2:n,p=var(b,p);v=b[p:p+n];p+=n
  elif w==5:v=struct.unpack_from('<f',b,p)[0];p+=4
  elif w==1:v=struct.unpack_from('<d',b,p)[0];p+=8
  else:raise ValueError(w)
  r.setdefault(f,[]).append(v)
 return r
schemas={
 'ActivityDefaultBase':'Id Token FunctionId ActivityName RemarkName OpenLevel OpenQuest Entrance Icon Location Sort OpenInterface IsOpen IsFunction IsHide',
 'ActivityDelegation':'Id SerialId FunctionId IsGlobal ZoneId Token FiliterServerTime TimeType ShowBeginTime ShowEndTime BeginTime EndTime ActivityName ActivityDes OpenLevel OpenQuest Template Icon FilterServer',
 'ActivityTemplate':'Id Token Template ActivityType Sort Name BackPic TextPic Describe Release'}
strings=set('Token ActivityName RemarkName Icon ActivityDes Name BackPic TextPic Describe'.split())
out=ROOT.parent/'active-project/public/data/original/activities';out.mkdir(parents=True,exist_ok=True)
for name,fields in schemas.items():
 source=ROOT/'recovered-client'/(name+'ConfigCategory');category=decode(source.read_bytes());rows=[]
 for entry in category.get(1,[]):
  record=decode(entry);row={}
  for i,key in enumerate(fields.split(),1):
   values=record.get(i,[])
   if key in strings:row[key]=values[0].decode() if values else ''
   elif key in ['ZoneId','FilterServer']:
    a=[]
    for v in values:
     if isinstance(v,bytes):
      p=0
      while p<len(v):n,p=var(v,p);a.append(n)
     else:a.append(v)
    row[key]=a
   else:row[key]=values[0] if values else 0
   if key=='SerialId':row[key]=str(row[key])
  rows.append(row)
 payload={'source':str(source.name),'schema':fields.split(),'records':rows}
 (out/(name+'.json.gz')).write_bytes(gzip.compress(json.dumps(payload,separators=(',',':')).encode(),mtime=0))
 print(name,len(rows),rows[:1])
