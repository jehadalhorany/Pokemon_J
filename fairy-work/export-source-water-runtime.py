import UnityPy,json,re
from pathlib import Path
R=Path(__file__).resolve().parent.parent;raw=R/'restored-current/fairy-work/raw';out=R/'active-project/public/assets/original/water';out.mkdir(exist_ok=True)
e=UnityPy.Environment()
for n in ['ae65c719f3f4998cbc93a9fa20bb54b7','98e8a0990abf60ad28b03abe8e2feee7']:
 b=(raw/(n+'.bundle')).read_bytes();e.load_file(b[b.index(b'UnityFS'):],name=n)
m=next(o.read()for o in e.objects if o.type.name=='Material'and o.read().m_Name=='SampleWater');d={'shader':'Pokemon/SampleWater','sourceBundle':'ae65c719f3f4998cbc93a9fa20bb54b7','floats':dict(m.m_SavedProperties.m_Floats),'textures':{}}
for k,t in m.m_SavedProperties.m_TexEnvs:
 if k not in ['_Normal2','_WaterNormal']:continue
 im=t.m_Texture.read().image;im.save(out/(k+'.png'));d['textures'][k]={'url':'/assets/original/water/'+k+'.png','scale':[t.m_Scale.x,t.m_Scale.y],'offset':[t.m_Offset.x,t.m_Offset.y],'sourceTexture':str(t.m_Texture.m_PathID)}
c=dict(m.m_SavedProperties.m_Colors)['_WaterColor'];d['color']=[c.r,c.g,c.b,c.a]
from UnityPy.helpers import CompressionHelper
b=(raw/'98011065bf2fbc5aede2182269d72494.bundle').read_bytes();shaderEnv=UnityPy.load(b[b.index(b'UnityFS'):]);shader=next(o.read()for o in shaderEnv.objects if o.type.name=='Shader'and o.path_id==2891417073959985199);state=shader.m_ParsedForm.m_SubShaders[0].m_Passes[0].m_State;d['pass']={'zWrite':state.zWrite.val,'zTest':state.zTest.val,'cull':state.culling.val,'srcBlend':state.rtBlend0.srcBlend.val,'dstBlend':state.rtBlend0.destBlend.val};i=shader.platforms.index(9);off=shader.offsets[i][0];ln=shader.compressedLengths[i][0];size=shader.decompressedLengths[i][0];b=CompressionHelper.decompress_lz4(bytes(shader.compressedBlob)[off:off+ln],size);chunks=b.split(b'#version');s=next((b'#version'+c.split(b'\0')[0]).decode()for c in chunks[1:]if b'_CameraDepthTexture'in c.split(b'\0')[0]and b'precision highp float;'in c[:150]);start=s.index('uniform \tvec4 _Time;');s=s[start:];s=s[:s.index('\n}',s.index('void main()'))+2];s=re.sub(r'UNITY_LOCATION\(\d+\) ','',s).replace('layout(location = 0) out','out');(out/'SampleWater.frag').write_text('precision highp float;\nprecision highp int;\n'+s);(out/'material.json').write_text(json.dumps(d,indent=2));print('exported original water fragment and two source normal textures')
