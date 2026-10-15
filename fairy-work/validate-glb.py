import pathlib,gzip,struct,json,concurrent.futures
root=pathlib.Path('pokemon-j/public/assets/imported/models')
def job(p):
 b=gzip.decompress(p.read_bytes());n=struct.unpack_from('<I',b,12)[0];d=json.loads(b[20:20+n]);offset=20+n;blen=struct.unpack_from('<I',b,offset)[0];binary=bytearray(b[offset+8:offset+8+blen]);changed=0;errors=[]
 for a in d['accessors']:
  view=d['bufferViews'][a['bufferView']];width={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']];fmt={5126:'f',5125:'I',5123:'H'}[a['componentType']];bs=struct.calcsize(fmt);expected=a['count']*width*bs
  if expected==view['byteLength']:continue
  actualWidth=view['byteLength']//(a['count']*bs)
  if width!=4 or actualWidth>4 or actualWidth<1:errors.append('Invalid accessor');continue
  start=view.get('byteOffset',0);vals=struct.unpack_from('<'+str(a['count']*actualWidth)+fmt,binary,start);expanded=[]
  for i in range(a['count']):expanded.extend(vals[i*actualWidth:(i+1)*actualWidth]);expanded.extend([0]*(4-actualWidth))
  while len(binary)%4:binary.append(0)
  view['byteOffset']=len(binary);view['byteLength']=expected;binary.extend(struct.pack('<'+str(len(expanded))+fmt,*expanded));changed+=1
 if changed:
  d['buffers'][0]['byteLength']=len(binary);js=json.dumps(d,separators=(',',':'),ensure_ascii=False).encode();js+=b' '*((-len(js))%4);binary.extend(b'\0'*((-len(binary))%4));payload=struct.pack('<III',0x46546c67,2,12+8+len(js)+8+len(binary))+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(binary),0x004e4942)+binary;p.write_bytes(gzip.compress(payload,6,mtime=0))
 return changed,errors
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:r=list(pool.map(job,root.glob('*.glb.gz')))
print('Validated',len(r),'fixed accessors',sum(n for n,e in r),'errors',sum(len(e) for n,e in r))
