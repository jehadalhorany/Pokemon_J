import UnityPy,pathlib,json
root=pathlib.Path(__file__).resolve().parent;out=root/'ui-original';out.mkdir(exist_ok=True)
for row in [json.loads(s)for s in (root/'portrait-bundles.jsonl').read_text().splitlines()]:
 b=(root/'raw'/row['file']).read_bytes();e=UnityPy.load(b[b.index(b'UnityFS'):])
 for o in e.objects:
  if o.type.name=='TextAsset':
   a=o.read();(root/(a.m_Name+'.bin')).write_bytes(a.m_Script.encode('utf8','surrogateescape'));print(a.m_Name,flush=True)
  if o.type.name=='Texture2D':
   a=o.read();a.image.save(out/(a.m_Name+'.png'));print(a.m_Name,a.m_Width,a.m_Height,flush=True)
