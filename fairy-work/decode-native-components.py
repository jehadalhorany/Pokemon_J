"""Decode source FairyGUI component dimensions and child placements.
Only block-0 fields are decoded. Controllers, relations, gears, transitions
and extension behavior remain explicitly unresolved, never fabricated.
"""
import json,struct
from pathlib import Path
R=Path(__file__).resolve().parent
class Buffer:
 def __init__(self,data,strings):self.data=data;self.strings=strings;self.p=0
 def n(self,fmt):v=struct.unpack_from('>'+fmt,self.data,self.p)[0];self.p+=struct.calcsize('>'+fmt);return v
 def s(self):
  i=self.n('H')
  if i==65534:return None
  if i==65533:return ''
  return self.strings[i]
 def seek(self,index,block):
  old=self.p;self.p=index;count=self.n('B');short=self.n('B')==1
  if block<count:
   self.p+=(2 if short else 4)*block;off=self.n('H' if short else 'I')
   if off:self.p=index+off;return True
  self.p=old;return False
out={};errors=[]
for package in sorted(R.glob('fui-*.json')):
 meta=json.loads(package.read_text())
 if not all(k in meta for k in ['items','strings']):continue
 pkg=package.stem[4:];components=[]
 for item in meta['items']:
  if item['type']!=3:continue
  path=R/f"fui-{pkg}-component-{item['name']}.bin"
  if not path.exists():continue
  try:
   b=Buffer(path.read_bytes(),meta['strings']);assert b.seek(0,0)
   record={'id':item['id'],'name':item['name'],'extension':item.get('extension'),'size':[b.n('i'),b.n('i')],'children':[],'unresolved':['controllers','gears','relations','transitions','extension behavior']}
   if b.seek(0,2):
    count=b.n('H')
    for _ in range(count):
     length=b.n('H');start=b.p;end=start+length;assert end<=len(b.data)
     assert b.seek(start,0)
     child={'type':b.n('B'),'sourceId':b.s(),'packageId':b.s(),'id':b.s(),'name':b.s(),'position':[b.n('i'),b.n('i')]}
     if b.n('B'):child['size']=[b.n('i'),b.n('i')]
     record['children'].append(child);b.p=end
   components.append(record)
  except Exception as e:errors.append({'package':pkg,'component':item['name'],'error':type(e).__name__+': '+str(e)})
 out[pkg]={'components':components,'images':[i for i in meta['items'] if i['type']==0]}
dest=R.parent/'pokemon-j/public/data/original/native-components.json';dest.write_text(json.dumps({'source':'Uploaded FairyGUI package binaries','scope':'source placements only; not a working UI runtime','packages':out,'errors':errors},ensure_ascii=False,separators=(',',':')))
print('packages',len(out),'components',sum(len(v['components'])for v in out.values()),'errors',len(errors));print(errors[:3])
