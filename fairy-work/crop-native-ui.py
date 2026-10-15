from PIL import Image
import pathlib,json
ROOT=pathlib.Path('fairy-work');OUT=pathlib.Path('pokemon-j/public/assets/original/ui');OUT.mkdir(exist_ok=True,parents=True);manifest={}
for package in ['Main','Map','Common','Base']:
 data=json.load(open(ROOT/('fui-'+package+'.json')));items={r['id']:r for r in data['items']};atlases={};sprites={r['id']:r for r in data['sprites']}
 for item in data['items']:
  name=item['name']or''
  if item['type']!=0 or not (package=='Main' and (name.startswith('fun_') or any(s in name.lower() for s in ['joy','zjm_txd','yd_renwu','zjm_rank'])) or package=='Map' or package=='Common' and name in ['ty_btn_back','ty_bth_close','zjm_exp_jd','zjm_jd','ty_bth_1','ty_bth_2','ty_bg_tz_1','ty_bth_jia'] or package=='Base'):continue
  sprite=sprites.get(item['id'])
  if not sprite:continue
  aid=sprite['atlas']
  if aid not in atlases:
   a=items[aid];file=ROOT/'ui-original'/(package+'_'+a['file']);image=Image.open(file).convert('RGBA');alpha=file.with_name(file.stem+'!a.png')
   if alpha.exists():image.putalpha(Image.open(alpha).convert('RGB').getchannel('R'))
   atlases[aid]=image
  x,y,w,h=sprite['rect'];im=atlases[aid].crop((x,y,x+w,y+h))
  if sprite['rotated']:im=im.transpose(Image.Transpose.ROTATE_270)
  dest=OUT/(package+'-'+name.replace('/','_')+'.png');im.save(dest);manifest[package+'/'+name]={'url':'/assets/original/ui/'+dest.name,'size':list(im.size),'sourceId':item['id']}
pathlib.Path('pokemon-j/public/data/original/ui.json').write_text(json.dumps(manifest,separators=(',',':'),ensure_ascii=False));print('ICONS',len(manifest))
