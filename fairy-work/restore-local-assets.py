import zipfile,pathlib
r=pathlib.Path(__file__).resolve().parent;root=r.parent/'pokemon-j';(r/'raw').mkdir(exist_ok=True)
for p in (r.parent.parent/'packs').glob('*.zip'):
 with zipfile.ZipFile(p) as z:
  for n in z.namelist():
   if n.endswith('/'):continue
   if p.name.startswith('Fairy'):
    name=n.rsplit('/',1)[-1]
    if name.endswith('.bundle') and not (r/'raw'/name).exists():(r/'raw'/name).write_bytes(z.read(n))
   elif 'public/assets/imported/' in n:
    target=root/n[n.index('public/assets/imported/'):];target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists():target.write_bytes(z.read(n))
print('restored',len(list((r/'raw').glob('*.bundle'))),flush=True)
