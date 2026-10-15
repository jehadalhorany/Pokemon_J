import UnityPy,pathlib,json
from memorypack import Reader
root=pathlib.Path(__file__).resolve().parent
p=root/'raw/25be22d807e5a43a61d653d9dc203b9d.bundle'
b=p.read_bytes();e=UnityPy.load(b[b.index(b'UnityFS'):])
for o in e.objects:
 if o.type.name!='TextAsset':continue
 a=o.read();print(a.m_Name,flush=True)
 if 'LanguageConfig_en' not in a.m_Name:continue
 b=a.m_Script.encode('utf8','surrogateescape');(root/(a.m_Name+'.bin')).write_bytes(b)
 r=Reader(b);print('header',r.value('byte'));n=r.value('int');print('entries',n);rows={}
 for i in range(n):
  count=r.value('byte');assert count==2,(i,count,r.p)
  key=r.value('string');value=r.value('string');rows[key]=value
 assert r.p==len(b),(r.p,len(b))
 (root/'language-en.json').write_text(json.dumps(rows,ensure_ascii=False));print('saved',len(rows),list(rows.items())[:3])
