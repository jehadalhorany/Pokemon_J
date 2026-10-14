"""Import PokemonDB's saved evolution HTML; requires lxml for this offline tool."""
from pathlib import Path
from lxml import html
import json,re,sys
root=Path(__file__).resolve().parents[1]
catalog=json.loads((root/'public/data/pokedex.json').read_text())['entries']
sprite_map={Path(p['imageUrl']).stem:p for p in catalog if p['imageUrl']}
doc=html.fromstring(Path(sys.argv[1]).read_text())
def classes(n):return (n.get('class') or '').split()
def has(n,c):return c in classes(n)
def text(n):return re.sub(r'\s+',' ',' '.join(n.itertext())).strip()
def pokemon(n):
 img=n.xpath('.//img')[0];sources=n.xpath('.//source/@srcset')
 slug=Path(sources[0]).stem if sources else Path(img.get('src')).stem
 found=sprite_map.get(slug)
 return {'id':found['id'] if found else slug,'name':img.get('alt'),'number':found['number'] if found else int(re.search(r'#(\d+)',text(n)).group(1)),'matched':bool(found),'imageUrl':sources[0] if sources else None}
edges=[];nodes={}
def walk(container,current=None,pending=None):
 for child in container:
  if has(child,'infocard-arrow'):pending=text(child).strip('() ')
  elif has(child,'infocard'):
   target=pokemon(child);nodes[target['id']]=target
   if current and pending:edges.append({'from':current['id'],'to':target['id'],'condition':pending})
   current=target;pending=None
  elif has(child,'infocard-evo-split'):
   for branch in child:walk(branch,current,pending)
  elif has(child,'infocard-list-evo'):walk(child,current,pending)
chains=[n for n in doc.iter() if has(n,'infocard-list-evo') and not any(has(p,'infocard-list-evo') for p in n.iterancestors())]
for chain in chains:walk(chain)
edges=list({(e['from'],e['to'],e['condition']):e for e in edges}.values())
assert any(e=={'from':'bulbasaur','to':'ivysaur','condition':'Level 16'} for e in edges)
assert sum(e['from']=='eevee' for e in edges)>=8
assert any(e['from']=='pikachu' and 'alolan' in e['to'] for e in edges)
result={'source':'https://pokemondb.net/evolution','chainCount':len(chains),'nodeCount':len(nodes),'edgeCount':len(edges),'nodes':nodes,'edges':edges,'notes':['Conditions are retained from the source, not converted into invented level gates.','Mega forms and species without evolution may not appear on this page.']}
(root/'public/data/evolution.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'chains':len(chains),'nodes':len(nodes),'edges':len(edges),'unmatched':[p for p in nodes.values() if not p['matched']]},ensure_ascii=False))
