import json,pathlib,struct,hashlib,math,sys,collections
import UnityPy
from UnityPy.helpers.MeshHelper import MeshHandler
from UnityPy.export.MeshRendererExporter import get_mesh
import os
ROOT=pathlib.Path(os.environ.get('IMPORT_WORK_DIR',pathlib.Path(__file__).resolve().parent/'work'))
CAB=json.load(open(ROOT/'cab-index.json'))
OUT=pathlib.Path(os.environ.get('GAME_PUBLIC_DIR',pathlib.Path(__file__).resolve().parents[2]/'public'))/'assets/imported'; OUT.mkdir(parents=True,exist_ok=True); (OUT/'textures').mkdir(exist_ok=True);(OUT/'models').mkdir(exist_ok=True)
class Env(UnityPy.Environment):
 def find_file(self,name,is_dependency=True):
  key=name.rsplit('/',1)[-1].lower();cab=self.get_cab(key)
  if cab:return cab
  if key in CAB:
   f=CAB[key];self.load_file((ROOT/'raw'/f).read_bytes(),name=key)
   return self.get_cab(key)
  raise FileNotFoundError('Missing dependency '+name)
def key(o):return (o.assets_file.name,str(o.path_id))
def vec(v,n=3):return [float(getattr(v,c)) for c in ['x','y','z','w'][:n]]
class GLB:
 def __init__(self):
  self.doc={'asset':{'version':'2.0','generator':'Pokemon J Unity asset import'},'scene':0,'scenes':[{'nodes':[]}],'nodes':[],'meshes':[],'materials':[],'textures':[],'images':[],'samplers':[{'magFilter':9729,'minFilter':9987,'wrapS':10497,'wrapT':10497}],'bufferViews':[],'accessors':[]};self.bin=bytearray();self.matcache={};self.meshcache={};self.nodes={};self.transforms={};self.warnings=[]
 def acc(self,rows,typ,component=5126,bounds=False):
  width={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[typ]; flat=rows if width==1 else [v for r in rows for v in r];fmt={5126:'f',5125:'I',5123:'H'}[component]
  if component==5126:flat=[float(v) if math.isfinite(float(v)) else 0 for v in flat]
  while len(self.bin)%4:self.bin.append(0)
  offset=len(self.bin);self.bin.extend(struct.pack('<'+str(len(flat))+fmt,*flat));bv=len(self.doc['bufferViews']);self.doc['bufferViews'].append({'buffer':0,'byteOffset':offset,'byteLength':len(flat)*struct.calcsize(fmt)})
  a={'bufferView':bv,'componentType':component,'count':len(rows),'type':typ}
  if bounds and rows:a.update(min=[min(r[i] for r in rows) for i in range(width)],max=[max(r[i] for r in rows) for i in range(width)])
  idx=len(self.doc['accessors']);self.doc['accessors'].append(a);return idx
 def material(self,p):
  if not p:return None
  o=p.deref();k=key(o)
  if k in self.matcache:return self.matcache[k]
  m=o.read();props=m.m_SavedProperties;colors={str(k):v for k,v in props.m_Colors};c=colors.get('_Color');color=[getattr(c,k) for k in ['r','g','b','a']] if c else [1,1,1,1]
  d={'name':m.m_Name,'doubleSided':True,'pbrMetallicRoughness':{'baseColorFactor':color,'metallicFactor':0,'roughnessFactor':.85}}
  texs={str(k):v for k,v in props.m_TexEnvs};main=texs.get('_MainTex') or texs.get('_BaseMap');mask=texs.get('_RGBMask');image=None
  if mask and mask.m_Texture:
   import numpy as np
   from PIL import Image
   mk=mask.m_Texture.read().image.convert('RGB');diff=main.m_Texture.read().image.convert('RGBA').resize(mk.size) if main and main.m_Texture else Image.new('RGBA',mk.size,(255,255,255,255))
   weights=np.asarray(mk,dtype=np.float32)/255;arr=np.array(diff,dtype=np.float32);tint=np.zeros((*weights.shape[:2],3),dtype=np.float32)
   for channel,prop in enumerate(['_ColorR','_ColorG','_ColorB']):
    c=colors.get(prop);rgb=[getattr(c,k) for k in ['r','g','b']] if c else [1,1,1];tint+=weights[:,:,channel,None]*np.array(rgb)
   black=colors.get('_ColorBlack');rgb=[getattr(black,k) for k in ['r','g','b']] if black else [1,1,1];tint+=np.clip(1-weights.sum(axis=2),0,1)[:,:,None]*np.array(rgb)
   arr[:,:,:3]*=np.clip(tint,0,1);image=Image.fromarray(np.clip(arr,0,255).astype('uint8'),'RGBA')
  elif main and main.m_Texture:image=main.m_Texture.read().image
  if image is not None:
   ident=hashlib.sha1(str(k).encode()).hexdigest()[:24]+'.png';target=OUT/'textures'/ident
   if not target.exists():image.save(target)
   idx=len(self.doc['images']);self.doc['images'].append({'uri':'../textures/'+ident});self.doc['textures'].append({'source':idx,'sampler':0});d['pbrMetallicRoughness']['baseColorTexture']={'index':idx}
  idx=len(self.doc['materials']);self.doc['materials'].append(d);self.matcache[k]=idx;return idx
 def mesh(self,renderer):
  mesh=get_mesh(renderer)
  if mesh is None:return None
  h=MeshHandler(mesh);h.process()
  if not h.m_Vertices:return None
  attrs={'POSITION':self.acc(h.m_Vertices,'VEC3',bounds=True)}
  if h.m_Normals and len(h.m_Normals)==len(h.m_Vertices):attrs['NORMAL']=self.acc([v[:3] for v in h.m_Normals],'VEC3')
  if h.m_UV0 and len(h.m_UV0)==len(h.m_Vertices):attrs['TEXCOORD_0']=self.acc([[u,1-v] for u,v in h.m_UV0],'VEC2')
  bones=getattr(renderer,'m_Bones',None)
  if bones and h.m_BoneIndices and h.m_BoneWeights:
   attrs['JOINTS_0']=self.acc([list(v[:4])+[0]*max(0,4-len(v)) for v in h.m_BoneIndices],'VEC4',5123);attrs['WEIGHTS_0']=self.acc([list(v[:4])+[0]*max(0,4-len(v)) for v in h.m_BoneWeights],'VEC4')
  prim=[]
  for i,tris in enumerate(h.get_triangles()):
   if not tris:continue
   d={'attributes':attrs,'indices':self.acc([j for t in tris for j in t],'SCALAR',5125)}
   if renderer.m_Materials:
    try:
     material=self.material(renderer.m_Materials[min(i,len(renderer.m_Materials)-1)])
     if material is not None:d['material']=material
    except Exception as ex:self.warnings.append(str(ex))
   prim.append(d)
  if not prim:return None
  idx=len(self.doc['meshes']);self.doc['meshes'].append({'name':mesh.m_Name,'primitives':prim});return idx,mesh,h
 def transform(self,p):
  o=p.deref();k=key(o)
  if k in self.nodes:return self.nodes[k]
  t=o.read();name=t.m_GameObject.read().m_Name;idx=len(self.doc['nodes']);self.nodes[k]=idx;self.transforms[k]=t
  node={'name':name,'translation':vec(t.m_LocalPosition),'rotation':vec(t.m_LocalRotation,4),'scale':vec(t.m_LocalScale)};self.doc['nodes'].append(node)
  children=[self.transform(c) for c in t.m_Children if c]
  if children:node['children']=children
  return idx
 def add_renderers(self):
  for k,t in list(self.transforms.items()):
   go=t.m_GameObject.read()
   for comp in go.m_Component:
    p=comp[1] if isinstance(comp,tuple) else comp.component
    if not p:continue
    o=p.deref()
    if o.type.name not in ['MeshRenderer','SkinnedMeshRenderer']:continue
    try:
     r=o.read();result=self.mesh(r)
     if not result:continue
     mi,m,h=result;node={'name':go.m_Name+'_mesh','mesh':mi};ni=len(self.doc['nodes']);self.doc['nodes'].append(node);self.doc['nodes'][self.nodes[k]].setdefault('children',[]).append(ni)
     bones=getattr(r,'m_Bones',None)
     if bones and h.m_BoneWeights:
      joints=[self.transform(b) for b in bones];matrices=[]
      for mat in m.m_BindPose:matrices.append([getattr(mat,f'e{row}{col}') for col in range(4) for row in range(4)])
      skin={'joints':joints}
      if len(matrices)==len(joints):skin['inverseBindMatrices']=self.acc(matrices,'MAT4')
      si=len(self.doc.setdefault('skins',[]));self.doc['skins'].append(skin);node['skin']=si
    except Exception as ex:self.warnings.append(str(ex))
 def save(self,path):
  if not self.doc['meshes']:raise ValueError('No renderable mesh')
  self.doc['buffers']=[{'byteLength':len(self.bin)}]
  for k in ['textures','images','materials']:
   if not self.doc[k]:del self.doc[k]
  js=json.dumps(self.doc,separators=(',',':'),ensure_ascii=False).encode();js+=b' '*((-len(js))%4);binary=bytes(self.bin)+b'\0'*((-len(self.bin))%4)
  import gzip
  total=12+8+len(js)+8+len(binary);payload=(struct.pack('<III',0x46546c67,2,total)+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(binary),0x004e4942)+binary)
  path.with_name(path.name+'.gz').write_bytes(gzip.compress(payload,compresslevel=6,mtime=0))
def convert(row):
 e=Env();e.load_file((ROOT/'raw'/row['file']).read_bytes(),name=row['file']);g=GLB()
 for name,p in [(name,p) for cab in list(e.cabs.values()) if hasattr(cab,'container') for name,p in cab.container.items()]:
  if not name.endswith('.prefab'):continue
  o=p.deref()
  if o.type.name!='GameObject':continue
  go=o.read()
  for comp in go.m_Component:
   ref=comp[1] if isinstance(comp,tuple) else comp.component
   if ref and ref.deref().type.name=='Transform':g.doc['scenes'][0]['nodes'].append(g.transform(ref));break
 g.add_renderers();name=row['file'].replace('.bundle','.glb');g.save(OUT/'models'/name)
 return {'file':name,'source':row['paths'][0],'meshes':len(g.doc['meshes']),'skins':len(g.doc.get('skins',[])),'warnings':list(set(g.warnings))}
if __name__=='__main__':
 rows=json.load(open(ROOT/'inventory.json'));chosen=set(sys.argv[1:]);results=[]
 for r in rows:
  if r['file'] not in chosen:continue
  try:results.append(convert(r))
  except Exception as ex:results.append({'source':r['paths'][0],'error':str(ex)})
 print(json.dumps(results,ensure_ascii=False,indent=2))
