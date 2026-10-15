import pathlib,gzip,concurrent.futures
paths=list(pathlib.Path('pokemon-j/public/assets/imported').glob('models/*.glb'))+list(pathlib.Path('pokemon-j/public/assets/imported').glob('animations/*.json'))
def compress(p):
 b=p.read_bytes();dst=p.with_name(p.name+'.gz');dst.write_bytes(gzip.compress(b,compresslevel=6,mtime=0));p.unlink();return len(b),dst.stat().st_size
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 r=list(pool.map(compress,paths))
print('Files',len(r),'before',sum(a for a,b in r),'after',sum(b for a,b in r))
