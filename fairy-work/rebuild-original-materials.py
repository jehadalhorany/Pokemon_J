import gzip,json,pathlib
from convert import ROOT,convert
maps=ROOT.parent/'pokemon-j/public/data/original';ids=set()
for p in maps.glob('*.json.gz'):
 if p.name=='config.json.gz':continue
 w=json.load(gzip.open(p));ids.update(r['model'] for r in w['objects'] if r.get('floor'))
rows={r['file']:r for r in json.load(open(ROOT/'inventory.json'))};results=[]
for id in sorted(ids):
 try:results.append(convert(rows[id+'.bundle']));print('OK',id,flush=True)
 except Exception as ex:results.append({'id':id,'error':str(ex)});print('ERROR',id,str(ex),flush=True)
(ROOT/'original-material-results.json').write_text(json.dumps(results));print('DONE',len(ids),flush=True)
