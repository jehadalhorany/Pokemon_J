"""Restore the original single-bone face skin omitted when Unity weights are implicit."""
import json,gzip,struct,UnityPy
from pathlib import Path
R=Path(__file__).resolve().parent.parent;raw=R/'restored-current/fairy-work/raw';env=UnityPy.Environment();avatar='e7117792d1b9d392b3cba28a6fb341b0'
for name in [avatar,'28aa1af281d2a31f9b4066b2c3613ee0','245350332180f026b3e660b99a55b847']:
 b=(raw/(name+'.bundle')).read_bytes();env.load_file(b[b.index(b'UnityFS'):],name=name)
renderer=next(o.read()for o in env.objects if o.type.name=='SkinnedMeshRenderer' and o.path_id==4134019437585199084)
mesh=renderer.m_Mesh.read();bone=renderer.m_Bones[0].read().m_GameObject.read().m_Name
p=R/('active-project/public/assets/imported/models/'+avatar+'.glb.gz');b=gzip.decompress(p.read_bytes());ln=struct.unpack_from('<I',b,12)[0];doc=json.loads(b[20:20+ln]);binary=bytearray(b[28+ln:]);face=next(n for n in doc['nodes']if n['name']=='face_mesh');prims=doc['meshes'][face['mesh']]['primitives'];count=doc['accessors'][prims[0]['attributes']['POSITION']]['count'];assert count==mesh.m_VertexData.m_VertexCount
assert len(renderer.m_Bones)==len(mesh.m_BindPose)==1
joint=next(i for i,n in enumerate(doc['nodes'])if n['name']==bone)
def acc(rows,typ,ct,fmt):
 while len(binary)%4:binary.append(0)
 off=len(binary);binary.extend(struct.pack('<'+str(sum(len(x)for x in rows))+fmt,*[v for row in rows for v in row]));view=len(doc['bufferViews']);doc['bufferViews'].append({'buffer':0,'byteOffset':off,'byteLength':len(binary)-off});i=len(doc['accessors']);doc['accessors'].append({'bufferView':view,'componentType':ct,'count':len(rows),'type':typ});return i
j=acc([[0,0,0,0]]*count,'VEC4',5123,'H');w=acc([[1,0,0,0]]*count,'VEC4',5126,'f');mat=mesh.m_BindPose[0];matrix=[getattr(mat,f'e{row}{col}')for col in range(4)for row in range(4)];ibm=acc([matrix],'MAT4',5126,'f')
for prim in prims:prim['attributes'].update(JOINTS_0=j,WEIGHTS_0=w)
if 'skin'in face:doc['skins'][face['skin']]={'joints':[joint],'inverseBindMatrices':ibm}
else:face['skin']=len(doc['skins']);doc['skins'].append({'joints':[joint],'inverseBindMatrices':ibm})
face['extras']={'sourceRenderer':'4134019437585199084','sourceBone':bone,'implicitSingleBoneWeight':1};doc['buffers'][0]['byteLength']=len(binary);js=json.dumps(doc,separators=(',',':')).encode();js+=b' '*(-len(js)%4);binary+=b'\0'*(-len(binary)%4);payload=struct.pack('<III',0x46546c67,2,28+len(js)+len(binary))+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(binary),0x004e4942)+binary;p.write_bytes(gzip.compress(payload,mtime=0));(R/'active-project/SOURCE_FACE_SKIN_BINDING.json').write_text(json.dumps({'sourceAvatar':avatar,'mesh':mesh.m_Name,'bone':bone,'vertices':count,'inverseBindMatrix':matrix,'implicitWeight':1},indent=2));print('bound source face skin',count,bone)
