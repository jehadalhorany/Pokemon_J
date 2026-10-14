import pathlib,json,zipfile,sys,os
import UnityPy
from UnityPy.files.BundleFile import BundleFile
project=pathlib.Path(__file__).resolve().parents[2];root=pathlib.Path(os.environ.get('IMPORT_WORK_DIR',pathlib.Path(__file__).resolve().parent/'work'));(root/'raw').mkdir(parents=True,exist_ok=True)
folder=pathlib.Path(sys.argv[1]);inventory=json.load(open(project/'asset-source-index.json'));names={}
def directory(self,reader,files):self.directory_names=[f.path for f in files]
BundleFile.read_files=directory
for n in range(1,19):
 with zipfile.ZipFile(folder/f'FairyAssets_{n:02}.zip') as z:
  for info in z.infolist():
   if info.is_dir():continue
   name=pathlib.Path(info.filename).name;b=z.read(info);start=b.find(b'UnityFS\0');b=b[start:] if start>=0 else b;(root/'raw'/name).write_bytes(b);e=UnityPy.load(b);bundle=next(iter(e.files.values()))
   for cab in bundle.directory_names:names[cab.lower()]=name
 print('Prepared archive',n,flush=True)
if len(sys.argv)>2:
 with zipfile.ZipFile(sys.argv[2]) as apk:resource=apk.read('assets/bin/Data/unity default resources')
 (root/'raw/unity-default-resources').write_bytes(resource);names['unity default resources']='unity-default-resources'
json.dump(names,open(root/'cab-index.json','w'));json.dump([dict(file=r['bundle'],paths=r['paths'],types=r['types'],archive=r['archive']) for r in inventory],open(root/'inventory.json','w'))
print('Prepared',len(inventory),'bundles')
