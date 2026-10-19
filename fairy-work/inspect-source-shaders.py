import UnityPy,pathlib
from UnityPy.helpers import CompressionHelper
r=pathlib.Path(__file__).resolve().parent;b=(r/'raw/98011065bf2fbc5aede2182269d72494.bundle').read_bytes();e=UnityPy.load(b[b.index(b'UnityFS'):])
for o in e.objects:
 if o.type.name!='Shader':continue
 s=o.read();name=s.m_ParsedForm.m_Name
 if name not in ['Pokemon/PokemonDate','Pokemon/PokemonBase']:continue
 print(name,s.platforms,s.offsets,s.compressedLengths,s.decompressedLengths)
 for i,p in enumerate(s.platforms):
  offsets=s.offsets[i] if isinstance(s.offsets[i],list) else [s.offsets[i]];cs=s.compressedLengths[i] if isinstance(s.compressedLengths[i],list)else[s.compressedLengths[i]];ds=s.decompressedLengths[i]if isinstance(s.decompressedLengths[i],list)else[s.decompressedLengths[i]]
  for j,(off,c,d) in enumerate(zip(offsets,cs,ds)):
   data=CompressionHelper.decompress_lz4(bytes(s.compressedBlob)[off:off+c],d);pathlib.Path('/tmp/'+name.split('/')[-1]+f'-{i}-{j}.bin').write_bytes(data)
