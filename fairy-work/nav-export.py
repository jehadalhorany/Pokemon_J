import struct,json,gzip,pathlib
b=pathlib.Path('fairy-work/walk-nav.bin').read_bytes();o=48;h=struct.unpack_from('<15I',b,o);polys,verts=h[6:8];v=[list(struct.unpack_from('<3f',b,o+100+i*12)) for i in range(verts)];start=o+100+verts*12;out=[]
for i in range(polys):
 p=start+i*32;ids=struct.unpack_from('<6H',b,p+4);n=b[p+30]
 if n<3 or n>6:continue
 out.append([[round(v[j][0],3),round(v[j][2],3),round(v[j][1],3)] for j in ids[:n]])
p=pathlib.Path('pokemon-j/public/data/world/walk.json.gz');p.write_bytes(gzip.compress(json.dumps(out,separators=(',',':')).encode(),6));print(polys,verts,len(out),out[:2])
