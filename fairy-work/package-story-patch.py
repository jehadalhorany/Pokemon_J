from pathlib import Path
import json,zipfile
root=Path(__file__).resolve().parent.parent;project=root/'active-project'
files=[Path('public')/n for n in ['scene.js','source-map.js','source-hud.js','native-package-loader.js','source-dialogue.js','source-menu.js']]
base=Path('public/assets/original/packages')
files.extend(base/n for n in ['Dialogue.fui','Dialogue_atlas0.png','images.json','provenance.json'])
images=json.loads((project/base/'images.json').read_text())['Dialogue']
files.extend(Path('public')/v['url'].lstrip('/') for v in images.values())
files.extend(Path(n) for n in ['INSTALL_STORY_PATCH_AR.md','SOURCE_STORY_VALIDATION.json','SOURCE_DIALOGUE_LAYOUT_VALIDATION.json'])
assert json.loads((project/'SOURCE_STORY_VALIDATION.json').read_text())['previewDoesNotGrantPartner']
out=root/'Pokemon_J_v04_story_patch.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for rel in files:z.write(project/rel,str(rel))
with zipfile.ZipFile(out) as z:assert z.testzip() is None
print(out,out.stat().st_size,'files',len(files))
