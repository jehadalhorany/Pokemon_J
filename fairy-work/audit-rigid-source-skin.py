import importlib.util,json
from pathlib import Path
import UnityPy
from UnityPy.helpers.MeshHelper import MeshHandler
R=Path(__file__).resolve().parent;raw=R.parent/'restored-current/fairy-work/raw';e=UnityPy.Environment()
for bundle in ['e7117792d1b9d392b3cba28a6fb341b0','2ec8756595dd17f21cc7cc0c915448d8','28aa1af281d2a31f9b4066b2c3613ee0','245350332180f026b3e660b99a55b847']:
 b=(raw/(bundle+'.bundle')).read_bytes();e.load_file(b[b.index(b'UnityFS'):],name=bundle)
for o in list(e.objects):
 if o.type.name!='SkinnedMeshRenderer':continue
 r=o.read()
 if len(r.m_Bones)!=1:continue
 mesh=r.m_Mesh.read();h=MeshHandler(mesh);h.process();print('mesh',mesh.m_Name,'bones',len(r.m_Bones),'vertices',mesh.m_VertexData.m_VertexCount,'weights',len(h.m_BoneWeights or []),'bindposes',len(mesh.m_BindPose));print('bindpose',str(mesh.m_BindPose));print('renderer',r.m_GameObject.read().m_Name,'bone',r.m_Bones[0].read().m_GameObject.read().m_Name)
