import gzip,json,struct,pathlib
from PIL import Image
root=pathlib.Path('pokemon-j/public/assets/imported');w=json.load(gzip.open('pokemon-j/public/data/world/kanto.json.gz'));ids={r['model'] for r in w['objects']+w['floors']};changed=[]
for id in ids:
 p=root/'models'/(id+'.glb.gz');b=gzip.open(p).read();n=struct.unpack_from('<I',b,12)[0];d=json.loads(b[20:20+n]);update=False
 for m in d.get('materials',[]):
  t=m.get('pbrMetallicRoughness',{}).get('baseColorTexture')
  if not t:continue
  uri=d['images'][d['textures'][t['index']]['source']]['uri'];im=Image.open(root/'models'/uri)
  if im.mode=='RGBA' and im.getextrema()[3][0]<128:
   m['alphaMode']='MASK';m['alphaCutoff']=.4;update=True
 if update:
  binary=b[20+n:];j=json.dumps(d,separators=(',',':')).encode();j+=b' '*((-len(j))%4);payload=struct.pack('<III',0x46546c67,2,20+len(j)+len(binary))+struct.pack('<II',len(j),0x4e4f534a)+j+binary;p.write_bytes(gzip.compress(payload,6,mtime=0));changed.append(id)
pathlib.Path('fairy-work/alpha-models.json').write_text(json.dumps(changed));print('Alpha fixed',len(changed))
