from pathlib import Path
import json,struct
from PIL import Image
R=Path(__file__).resolve().parent;out=R.parent/'active-project/public/assets/original/packages';dest=out/'images';dest.mkdir(exist_ok=True);manifest={}
for pkg in ['Base','Common','Item','EudemonIcon','Role','Spine','Main','Map','Assignment']:
 meta=json.loads((R/f'fui-{pkg}.json').read_text());items={i['id']:i for i in meta['items']};data=(R/(pkg+'_fui.bin')).read_bytes();p=9
 for _ in range(2):n=struct.unpack_from('>H',data,p)[0];p+=2+n
 index=p+20;short=data[index+1];offset=struct.unpack_from('>H'if short else'>I',data,index+2+2*(2 if short else 4))[0];p=index+offset;cnt=struct.unpack_from('>H',data,p)[0];p+=2;strings=meta['strings'];cached={}
 def n(t):
  global p
  v=struct.unpack_from('>'+t,data,p)[0];p+=struct.calcsize('>'+t);return v
 for _ in range(cnt):
  size=n('H');end=p+size;id=strings[n('H')];atlas=strings[n('H')];x,y,w,h=[n('i')for _ in range(4)];rot=n('B');trim=n('B');off=[0,0];original=[h,w]if rot else[w,h]
  if trim:off=[n('i'),n('i')];original=[n('i'),n('i')]
  p=end
  if not rot:continue
  file=pkg+'_'+items[atlas]['file']
  if file not in cached:cached[file]=Image.open(out/file).convert('RGBA')
  im=cached[file].crop((x,y,x+w,y+h)).transpose(Image.Transpose.ROTATE_270)
  if trim:
   full=Image.new('RGBA',tuple(original));full.paste(im,tuple(off));im=full
  name=pkg+'-'+id+'.png';im.save(dest/name);manifest.setdefault(pkg,{})[id]='/assets/original/packages/images/'+name
 print(pkg,len(manifest.get(pkg,{})),flush=True)
(out/'rotated-images.json').write_text(json.dumps(manifest,separators=(',',':')))
