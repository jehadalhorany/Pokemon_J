from PIL import Image
import pathlib,json
root=pathlib.Path(__file__).resolve().parent;out=root.parent/'pokemon-j/public/assets/original/portraits';out.mkdir(exist_ok=True,parents=True);data=json.load(open(root/'fui-EudemonIcon.json'));items={i['id']:i for i in data['items']};sprites={s['id']:s for s in data['sprites']};atlases={};count=0
for item in data['items']:
 if item['type']!=0:continue
 s=sprites.get(item['id'])
 if not s:continue
 if s['atlas']not in atlases:
  a=items[s['atlas']];p=root/'ui-original'/('EudemonIcon_'+a['file']);im=Image.open(p).convert('RGBA');alpha=p.with_name(p.stem+'!a.png');im.putalpha(Image.open(alpha).convert('RGB').getchannel('R'));atlases[s['atlas']]=im
 x,y,w,h=s['rect'];im=atlases[s['atlas']].crop((x,y,x+w,y+h))
 if s['rotated']:im=im.transpose(Image.Transpose.ROTATE_270)
 im.save(out/(item['name']+'.png'));count+=1
print('portraits',count)
