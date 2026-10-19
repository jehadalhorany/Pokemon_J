from pathlib import Path
import struct,json,lz4.block,lzma
R=Path(__file__).resolve().parent;raw=R.parent/'restored-current/fairy-work/raw';result={}
for path in raw.glob('*'):
 try:
  b=path.read_bytes();b=b[b.index(b'UnityFS'):];p=b.index(b'\0')+1;ver=struct.unpack_from('>I',b,p)[0];p+=4
  for _ in range(2):p=b.index(b'\0',p)+1
  size,cs,us,flags=struct.unpack_from('>QIII',b,p);p+=20
  if ver>=7:p=(p+15)//16*16
  info=b[size-cs:size]if flags&128 else b[p:p+cs];mode=flags&63
  info=lz4.block.decompress(info,uncompressed_size=us)if mode in (2,3)else lzma.decompress(info)if mode==1 else info
  n=struct.unpack_from('>I',info,16)[0];i=20+n*10;cnt=struct.unpack_from('>I',info,i)[0];i+=4
  for _ in range(cnt):
   i+=20;end=info.index(b'\0',i);name=info[i:end].decode();i=end+1;result[name.lower()]=path.name
 except Exception:pass
(R/'cab-index.json').write_text(json.dumps(result));print(len(result))
