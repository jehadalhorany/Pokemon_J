import pathlib,UnityPy,json
root=pathlib.Path(__file__).resolve().parent;b=(root/'raw/3c74f1c12a52c9cb3f237cefd7da525d.bundle').read_bytes();e=UnityPy.load(b[b.index(b'UnityFS'):]);n=0
for o in e.objects:
 if o.type.name=='TextAsset':
  a=o.read();(root/(a.m_Name+'.bin')).write_bytes(a.m_Script.encode('utf8','surrogateescape'));n+=1
print('raw configs',n)
p=root/'config-schema.json';s=json.load(open(p))
for name in ['PveBossCopyConfig','TeraRaidBattleCopyConfig']:
 print(name,s[name][-1]);assert s[name][-1]['type']=='unknown0x15';s[name]=s[name][:-1]
p.write_text(json.dumps(s));print('Removed nonserialized dictionary caches from two schemas')
