from convert import *
from concurrent.futures import ProcessPoolExecutor
import time

def job(row):
 try:return dict(convert(row),bundle=row['file'],status='converted')
 except Exception as ex:return {'bundle':row['file'],'source':row['paths'][0] if row['paths'] else '', 'status':'unconverted','error':str(ex)}
if __name__=='__main__':
 rows=json.load(open(ROOT/'inventory.json'));selected=[r for r in rows if any(p.endswith('.prefab') for p in r['paths'])];start=time.time();out=[]
 with ProcessPoolExecutor(max_workers=4) as pool:
  for i,result in enumerate(pool.map(job,selected,chunksize=5),1):
   out.append(result)
   if i%200==0:
    json.dump(out,open(ROOT/'conversion-progress.json','w'));print(i,'/',len(selected),'converted',sum(r['status']=='converted' for r in out),'seconds',round(time.time()-start),flush=True)
 json.dump(out,open(ROOT/'conversion-results.json','w'),ensure_ascii=False)
 print('COMPLETE',len(out),'converted',sum(r['status']=='converted' for r in out),flush=True)
