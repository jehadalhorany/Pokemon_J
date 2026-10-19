from pathlib import Path
import json,zipfile,hashlib
root=Path(__file__).resolve().parent.parent
project=root/'active-project'
manifest_path=root/'build-tools/resource-update-manifest.json'
paths=[project/p for p in json.loads(manifest_path.read_text())]
out=root/'delivery/Pokemon_J_v04_resource_walking_update.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in paths:z.write(p,p.relative_to(project))
manifest={str(p.relative_to(project)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in paths}
manifest_path.write_text(json.dumps(manifest,indent=2))
with zipfile.ZipFile(out)as z:
 assert z.testzip() is None
 assert not any(n.startswith('data/')or n.startswith('public/assets/imported/')for n in z.namelist())
print(out,len(paths),'files',out.stat().st_size,'bytes')
