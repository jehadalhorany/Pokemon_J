import json,gzip
from convert import convert,ROOT
world=json.load(gzip.open(ROOT.parent/'pokemon-j/public/data/world/kanto.json.gz'))
rows={r['file']:r for r in json.load(open(ROOT/'inventory.json'))}
for f in world['floors']:
 try:print(f['name'],convert(rows[f['model']+'.bundle']),flush=True)
 except Exception as e:print('ERROR',f['name'],str(e),flush=True)
