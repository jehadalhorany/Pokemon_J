import sys,pathlib,json,gzip
from memorypack import config,SCHEMA,ROOT
out=ROOT.parent/'pokemon-j/public/data/original/configs';out.mkdir(exist_ok=True,parents=True);success={};errors=[]
for p in ROOT.glob('*ConfigCategory.bin'):
 name=p.name.removesuffix('Category.bin')
 if name not in SCHEMA:continue
 try:
  rows=config(name);(out/(name+'.json.gz')).write_bytes(gzip.compress(json.dumps(rows,separators=(',',':'),ensure_ascii=False).encode(),6));success[name]=len(rows)
 except Exception as ex:errors.append({'name':name,'error':str(ex)})
(ROOT/'all-config-results.json').write_text(json.dumps({'success':success,'errors':errors},indent=2));print('DECODED',len(success),'errors',errors[:20])
