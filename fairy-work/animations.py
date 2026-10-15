from convert import *
from concurrent.futures import ProcessPoolExecutor

def job(r):
 try:
  e=Env();e.load_file((ROOT/'raw'/r['file']).read_bytes(),name=r['file']);clips=[]
  for o in list(e.objects):
   if o.type.name!='AnimationClip':continue
   d=o.read_typetree();tracks=[]
   for key,prop,dim in [('m_RotationCurves','quaternion',4),('m_PositionCurves','position',3),('m_ScaleCurves','scale',3)]:
    for c in d.get(key,[]):
     points=c['curve']['m_Curve']
     if not points:continue
     tracks.append({'path':c['path'],'property':prop,'times':[round(p['time'],6) for p in points],'values':[round(p['value'][axis],7) for p in points for axis in ['x','y','z','w'][:dim]]})
   if tracks:clips.append({'name':d['m_Name'],'tracks':tracks})
  if not clips:return None
  (OUT/'animations').mkdir(exist_ok=True);file=r['file'].replace('.bundle','.json');json.dump(clips,open(OUT/'animations'/file,'w'),separators=(',',':'))
  return {'bundle':r['file'],'file':file,'paths':r['paths'],'clips':[c['name'] for c in clips]}
 except Exception:return None
if __name__=='__main__':
 rows=[r for r in json.load(open(ROOT/'inventory.json')) if r['types'].get('AnimationClip')]
 out=[]
 with ProcessPoolExecutor(max_workers=4) as pool:
  for i,r in enumerate(pool.map(job,rows,chunksize=15),1):
   if r:out.append(r)
   if i%1000==0:print(i,'/',len(rows),flush=True)
 json.dump(out,open(ROOT/'animation-results.json','w'));print('DONE',len(out),flush=True)
