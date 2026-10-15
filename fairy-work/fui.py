import struct,json,pathlib,sys
PACKAGE=sys.argv[1] if len(sys.argv)>1 else 'Map'
ROOT=pathlib.Path(__file__).resolve().parent
class Buf:
 def __init__(self,b,strings=None):self.b=b;self.p=0;self.strings=strings or []
 def n(self,t):v=struct.unpack_from('>'+t,self.b,self.p)[0];self.p+=struct.calcsize('>'+t);return v
 def utf(self):n=self.n('H');v=self.b[self.p:self.p+n].decode('utf8');self.p+=n;return v
 def s(self):i=self.n('H');return None if i==65534 else '' if i==65533 else self.strings[i]
 def seek(self,index,block):
  old=self.p;self.p=index;cnt=self.n('B');short=self.n('B')==1
  if block<cnt:
   self.p+=(2 if short else 4)*block;off=self.n('H' if short else 'I')
   if off:self.p=index+off;return True
  self.p=old;return False
b=Buf((ROOT/(PACKAGE+'_fui.bin')).read_bytes());print(b.n('I'),b.n('I'));compressed=b.n('B');print('compress',compressed,'id',b.utf(),'name',b.utf());b.p+=20;index=b.p
b.seek(index,4);n=b.n('I');b.strings=[b.utf() for _ in range(n)];print('strings',n)
b.seek(index,1);n=b.n('H');items=[]
for i in range(n):
 length=b.n('I');end=b.p+length;typ=b.n('B');id=b.s();name=b.s();path=b.s();file=b.s();export=b.n('B');w=b.n('I');h=b.n('I');item={'type':typ,'id':id,'name':name,'path':path,'file':file,'size':[w,h]}
 if typ==3:
  item['extension']=b.n('B');length=b.n('I');raw=b.b[b.p:b.p+length];(ROOT/('fui-'+PACKAGE+'-component-'+str(name)+'.bin')).write_bytes(raw)
 items.append(item);b.p=end
b.seek(index,2);n=b.n('H');sprites=[]
for i in range(n):
 end=b.n('H')+b.p;s={'id':b.s(),'atlas':b.s(),'rect':[b.n('I') for j in range(4)],'rotated':b.n('B')};sprites.append(s);b.p=end
(ROOT/('fui-'+PACKAGE+'.json')).write_text(json.dumps({'items':items,'sprites':sprites,'strings':b.strings},ensure_ascii=False,indent=2));print(items)
