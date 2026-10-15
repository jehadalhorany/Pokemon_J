import pathlib,json,UnityPy,subprocess,sys
from PIL import Image
root=pathlib.Path(__file__).resolve().parent
if (root/'ui-rotation-fixes.json').exists():
 print('Existing UI rotation migration already applied');sys.exit(0)
inv=json.load(open(root/'inventory-fast.json'));out=root.parent/'pokemon-j/public/assets/original/ui';fixed=[]
for package in ['Main','Map','Common','Base']:
 row=next(r for r in inv if any(p.endswith('/'+package+'_fui.bytes')for p in r.get('paths',[])));b=(root/'raw'/row['file']).read_bytes();e=UnityPy.load(b[b.index(b'UnityFS'):])
 for o in e.objects:
  if o.type.name=='TextAsset':
   a=o.read()
   if a.m_Name==package+'_fui':(root/(a.m_Name+'.bin')).write_bytes(a.m_Script.encode('utf8','surrogateescape'))
 subprocess.run([sys.executable,str(root/'fui.py'),package],stdout=subprocess.DEVNULL,check=True)
 data=json.load(open(root/('fui-'+package+'.json')));rotated={s['id']for s in data['sprites']if s['rotated']}
 for item in data['items']:
  p=out/(package+'-'+(item['name']or'').replace('/','_')+'.png')
  if item['id']in rotated and p.exists():
   Image.open(p).transpose(Image.Transpose.ROTATE_180).save(p);fixed.append(p.name)
(root/'ui-rotation-fixes.json').write_text(json.dumps(fixed));print('Corrected existing rotated UI sprites',len(fixed))
