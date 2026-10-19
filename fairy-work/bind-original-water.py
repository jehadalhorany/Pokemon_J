from pathlib import Path
import json,gzip,struct,UnityPy
root=Path(__file__).resolve().parent.parent
bundle='ae65c719f3f4998cbc93a9fa20bb54b7.bundle'
b=(root/'restored-current/fairy-work/raw'/bundle).read_bytes()
env=UnityPy.load(b[b.index(b'UnityFS'):])
source=next(o for o in env.objects if o.type.name=='Material' and o.read().m_Name=='SampleWater')
material=source.read();col=dict(material.m_SavedProperties.m_Colors)['_WaterColor']
colour=[col.r,col.g,col.b,1]
p=root/'active-project/public/assets/imported/models/e1476ae351dec682f4304a23e87ad1a7.glb.gz'
b=gzip.decompress(p.read_bytes());length,typ=struct.unpack_from('<II',b,12);doc=json.loads(b[20:20+length]);changed=0
for m in doc['materials']:
 if m['name']=='SampleWater':
  m['pbrMetallicRoughness']['baseColorFactor']=colour
  m['extras']={'sourceBundle':bundle,'sourceMaterial':str(source.path_id),'sourceProperty':'_WaterColor','scope':'original colour binding; original animated water shader not ported'};changed+=1
assert changed==1
j=json.dumps(doc,separators=(',',':')).encode();j+=b' '*(-len(j)%4);rest=b[20+length:]
p.write_bytes(gzip.compress(struct.pack('<III',0x46546c67,2,20+len(j)+len(rest))+struct.pack('<II',len(j),typ)+j+rest,mtime=0))
evidence={'model':p.name,'source':bundle,'material':'SampleWater','property':'_WaterColor','rgba':colour}
(root/'active-project/SOURCE_WATER_BINDING.json').write_text(json.dumps(evidence,indent=2));print(evidence)
