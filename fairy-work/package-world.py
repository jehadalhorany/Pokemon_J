import pathlib,json,gzip,struct,zipfile
root=pathlib.Path('pokemon-j');assets=root/'public/assets/imported';dest=pathlib.Path('Pokemon_J_v04_patch.zip')
with zipfile.ZipFile(dest) as old:files={root/n for n in old.namelist() if (root/n).is_file()}
w=json.load(gzip.open(root/'public/data/world/kanto.json.gz'));ids={r['model'] for r in w['objects']+w['floors']+w.get('extras',[])}|{'battle-forest','battle-indoor'}
for id in ids:
 p=assets/'models'/(id+'.glb.gz');files.add(p);b=gzip.open(p).read();n=struct.unpack_from('<I',b,12)[0];d=json.loads(b[20:20+n])
 for image in d.get('images',[]):files.add((assets/'models'/image['uri']).resolve())
files.update((root/'public/data/world').glob('*'));files.update({root/'public/world-runtime.js',root/'WORLD_REBUILD_v04.md'});files={p.resolve() for p in files};missing=[str(p) for p in files if not p.is_file()];assert not missing,missing
root=root.resolve();temp=dest.with_suffix('.new.zip')
with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(files):z.write(p,str(p.relative_to(root)))
 z.write('Pokemon_J_v04_INSTALL.md','Pokemon_J_v04_INSTALL.md')
temp.replace(dest)
print(json.dumps({'files':len(files)+1,'bytes':dest.stat().st_size,'worldInstances':len(w['objects']),'terrain':len(w['floors']),'modelFiles':len(ids)},indent=2))
