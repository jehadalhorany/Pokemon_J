"""Rasterize uploaded Common/BigMapCom geometry; no generated map artwork."""
from pathlib import Path
from PIL import Image
import json
root=Path(__file__).resolve().parent.parent/'active-project/public'
packages=json.loads((root/'data/original/native-components.json').read_text())['packages']
images=json.loads((root/'assets/original/packages/images.json').read_text())
c=next(c for c in packages['Common']['components']if c['name']=='BigMapCom')
out=Image.new('RGBA',tuple(c['size']));records=[]
for child in c['children']:
 if child['type']!=0 or not child.get('visible',True):continue
 entry=images['Common'][child['sourceId']];im=Image.open(root/entry['url'].lstrip('/')).convert('RGBA')
 size=child.get('size',list(im.size));scale=child.get('scale',[1,1]);size=tuple(round(size[i]*scale[i])for i in range(2))
 im=im.resize(size,Image.Resampling.LANCZOS);out.alpha_composite(im,tuple(child['position']));records.append(child['sourceId'])
out.save(root/'assets/original/source-world-map.png')
(root/'data/original/source-world-map.json').write_text(json.dumps({'source':'Common/BigMapCom','size':c['size'],'images':records,'pointScale':3.7},indent=2))
print('Source map rasterized',out.size,len(records))
