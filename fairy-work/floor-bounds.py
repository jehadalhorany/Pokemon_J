import gzip,json,struct,pathlib
import numpy as np
p=pathlib.Path('pokemon-j/public/data/world/kanto.json.gz');w=json.load(gzip.open(p))
for f in w['floors']:
 b=gzip.open('pokemon-j/public/assets/imported/models/'+f['model']+'.glb.gz').read();n=struct.unpack_from('<I',b,12)[0];d=json.loads(b[20:20+n]);points=[]
 def walk(i,parent,root=False):
  node=d['nodes'][i];x,y,z,q=node.get('rotation',[0,0,0,1]);R=np.array([[1-2*y*y-2*z*z,2*x*y-2*z*q,2*x*z+2*y*q],[2*x*y+2*z*q,1-2*x*x-2*z*z,2*y*z-2*x*q],[2*x*z-2*y*q,2*y*z+2*x*q,1-2*x*x-2*y*y]])
  mat=np.eye(4);mat[:3,:3]=R@np.diag(node.get('scale',[1,1,1]));mat[:3,3]=[0,0,0] if root else node.get('translation',[0,0,0]);mat=parent@mat
  if 'mesh'in node:
   for prim in d['meshes'][node['mesh']]['primitives']:
    a=d['accessors'][prim['attributes']['POSITION']]
    for x in [a['min'][0],a['max'][0]]:
     for y in [a['min'][1],a['max'][1]]:
      for z in [a['min'][2],a['max'][2]]:points.append((mat@np.array([x,y,z,1]))[:3])
  for child in node.get('children',[]):walk(child,mat)
 for i in d['scenes'][0]['nodes']:walk(i,np.eye(4),True)
 points=np.array(points);f['bounds']={'min':points.min(axis=0).round(4).tolist(),'max':points.max(axis=0).round(4).tolist()}
p.write_bytes(gzip.compress(json.dumps(w,separators=(',',':')).encode(),6))
