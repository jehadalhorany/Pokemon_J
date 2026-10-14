"""Import location names/links from the supplied index HTML, not encounter tables."""
from pathlib import Path
from lxml import html
import re,json,sys
root=Path(__file__).resolve().parents[1]
doc=html.fromstring(Path(sys.argv[1]).read_text())
regions=[]
for panel in doc.xpath('//*[@id]'):
 if not panel.get('id').startswith('loc-'):continue
 key=panel.get('id')[4:]
 items=[]
 for col in panel.xpath('.//div[contains(concat(" ",normalize-space(@class)," ")," grid-col ")]'):
  for n in col:
   if n.tag not in ['a','span']:continue
   name=' '.join(n.text_content().split())
   if not name:continue
   url=n.get('href') if n.tag=='a' else None
   items.append({'id':url.rsplit('/',1)[1] if url else key+'-'+re.sub(r'[^a-z0-9]+','-',name.lower()).strip('-'),'name':name,'sourceUrl':url,'hasEncounterPage':bool(url)})
 assert len({i['id'] for i in items})==len(items)
 regions.append({'id':key,'name':key.title(),'locations':items})
assert len(regions)==10
result={'source':'https://pokemondb.net/location','regionCount':len(regions),'locationCount':sum(len(r['locations']) for r in regions),'regions':regions,'notes':['This supplied file is a location index. It contains names and detail-page links, not map geometry, species encounters or encounter levels.','hasEncounterPage indicates a linked reference page; it does not assign game spawn probabilities.']}
(root/'public/data/locations.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print({r['name']:len(r['locations']) for r in regions});print(result['locationCount'])
