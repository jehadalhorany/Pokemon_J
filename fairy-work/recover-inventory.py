import UnityPy,pathlib,json,concurrent.futures
root=pathlib.Path(__file__).resolve().parent
files=list((root/'raw').glob('*.bundle'))
def scan(p):
 try:
  b=p.read_bytes();offset=b.find(b'UnityFS');e=UnityPy.load(b[offset:]);paths=list(e.container.keys());return {'file':p.name,'paths':paths}
 except Exception as ex:return {'file':p.name,'error':str(ex)}
rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 for i,row in enumerate(pool.map(scan,files)):
  rows.append(row)
  if i%1000==0:print(i,flush=True)
  if any('/UIRes/UIActivity/EudemonIcon/' in p for p in row.get('paths',[])):
   print('PORTRAIT',row,flush=True);(root/'portrait-bundles.jsonl').open('a').write(json.dumps(row)+'\n')
(root/'inventory.json').write_text(json.dumps(rows));print('DONE',len(rows),flush=True)
