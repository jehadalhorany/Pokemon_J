"""Import a saved PokemonDB all-Pokedex HTML; no network requests."""
from pathlib import Path
import re, html, json, sys
source=Path(sys.argv[1])
s=source.read_text(encoding='utf-8')
table=re.search(r'<tbody\b[^>]*>(.*?)</tbody>',s,re.S).group(1)
clean=lambda x:html.unescape(re.sub('<[^>]+>','',x)).strip()
entries=[]
for row in re.findall(r'<tr\b[^>]*>(.*?)</tr>',table,re.S):
    cells=re.findall(r'<td\b[^>]*>(.*?)</td>',row,re.S)
    assert len(cells)==10, len(cells)
    number=int(clean(cells[0]))
    name=clean(re.search(r'<a class="ent-name"[^>]*>(.*?)</a>',cells[1],re.S).group(1))
    url=html.unescape(re.search(r'<a class="ent-name" href="([^"]+)"',cells[1]).group(1))
    form=re.search(r'<small[^>]*>(.*?)</small>',cells[1],re.S)
    image=re.search(r'<source srcset="([^"]+)"',cells[0])
    local=re.search(r'<img[^>]*src="([^"]+)"',cells[0]).group(1)
    image_url=html.unescape(image.group(1)) if image else None
    key=url.rsplit('/',1)[1]
    if form: key+='--'+re.sub(r'[^a-z0-9]+','-',clean(form.group(1)).lower()).strip('-')
    stats=dict(zip(['total','hp','attack','defense','specialAttack','specialDefense','speed'],map(lambda c:int(clean(c)),cells[3:])))
    assert stats['total']==sum(v for k,v in stats.items() if k!='total')
    entries.append(dict(id=key,number=number,name=name,form=clean(form.group(1)) if form else None,types=[clean(v).lower() for v in re.findall(r'<a class="type-icon[^>]*>(.*?)</a>',cells[2],re.S)],baseStats=stats,imageUrl=image_url,sourceUrl=url))
numbers={e['number'] for e in entries}
assert numbers==set(range(1,1026)), (len(numbers),sorted(set(range(1,1026))-numbers))
assert len({e['id'] for e in entries})==len(entries)
result=dict(source='https://pokemondb.net/pokedex/all',speciesCount=len(numbers),entryCount=len(entries),extraFormCount=len(entries)-len(numbers),notes=['Image URLs are external icon references; image bytes are not included.','Moves, evolution, game rarity and spawn locations are not present in the supplied table.'],entries=entries)
out=Path(__file__).resolve().parents[1]/'public/data/pokedex.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='entries'},ensure_ascii=False))
