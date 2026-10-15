"""Build local gameplay/reference data from supplied HTML and cached PokeAPI CSVs."""
from pathlib import Path
from lxml import html
import csv,json,re,sys
root=Path(__file__).resolve().parents[1];out=root/'public/data';cache=Path(sys.argv[1]);uploads=Path(sys.argv[2])
def rows(name):return list(csv.DictReader((cache/(name+'.csv')).open()))
def index(name):return {int(r['id']):r for r in rows(name)}
def num(value,default=None):return int(value) if value not in ('',None) else default
def names(name,key):return {int(r[key]):r['name'] for r in rows(name) if r['local_language_id']=='9'}
def write(name,data):(out/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
cat=json.loads((out/'pokedex.json').read_text());entries=cat['entries'];byid={p['id']:p for p in entries}
# Keep the exact Generation 1-9 membership provided in the sprite-gallery attachment.
gallery=html.fromstring(next(uploads.glob('List of*html')).read_text());generation={}
for h in gallery.xpath('//main//h2'):
 match=re.search(r'Generation (\d+)',h.text_content())
 if not match:continue
 for sibling in h.itersiblings():
  if sibling.tag=='h2':break
  for a in sibling.xpath('.//a[contains(concat(" ",normalize-space(@class)," ")," ent-name ")]'):
   generation[a.get('href').rsplit('/',1)[1]]=int(match.group(1))
assert len(generation)==1025
pkm=index('pokemon');spec=index('pokemon_species');types=index('types');vg=index('version_groups');versions=index('versions')
api_by_slug={r['identifier']:r for r in pkm.values()};byapi={}
for p in entries:
 p['generation']=generation.get(p['sourceUrl'].rsplit('/',1)[1],num(spec[p['number']]['generation_id']))
 slug=Path(p['imageUrl']).stem if p['imageUrl'] else p['id']
 candidates=[slug,slug.replace('-alolan','-alola').replace('-galarian','-galar').replace('-hisuian','-hisui').replace('-paldean','-paldea')]
 record=next((api_by_slug[s] for s in candidates if s in api_by_slug),None)
 if not record and not p['form']:record=next((r for r in pkm.values() if num(r['species_id'])==p['number'] and r['is_default']=='1'),None)
 if record:p['apiId']=int(record['id']);byapi[p['apiId']]=p['id']
 base=spec[p['number']];p.update(genderRate=num(base['gender_rate']),captureRate=num(base['capture_rate']),baseFriendship=num(base['base_happiness']),legendary=base['is_legendary']=='1',mythical=base['is_mythical']=='1')
 p['rarity']='SP' if p['mythical'] else 'UR' if p['legendary'] or p['baseStats']['total']>=600 else 'SSR' if p['baseStats']['total']>=500 else 'SR' if p['baseStats']['total']>=400 else 'R' if p['baseStats']['total']>=300 else 'N'
 p['initialStars']=2 if p['rarity'] in ['SSR','UR','SP'] else 1
 p['evYield']={}
statkeys={1:'hp',2:'attack',3:'defense',4:'specialAttack',5:'specialDefense',6:'speed',7:'accuracy',8:'evasion'}
for r in rows('pokemon_stats'):
 key=byapi.get(num(r['pokemon_id']));stat=statkeys.get(num(r['stat_id']))
 if key and stat:byid[key]['evYield'][stat]=num(r['effort'],0)
abnames=names('ability_names','ability_id');abspec=index('abilities');abilities={str(i):{'id':i,'name':abnames.get(i,r['identifier']),'slug':r['identifier']} for i,r in abspec.items()}
for p in entries:p['abilities']=[]
for r in rows('pokemon_abilities'):
 key=byapi.get(num(r['pokemon_id']))
 if key:byid[key]['abilities'].append({'id':num(r['ability_id']),'hidden':r['is_hidden']=='1','slot':num(r['slot'])})
# Move definitions preserve the effects/descriptions in the user's move-list file.
move_doc=html.fromstring(next(uploads.glob('*moves_*html')).read_text());uploaded_moves={}
for tr in move_doc.xpath('//tbody/tr'):
 cells=tr.xpath('./td');a=cells[0].xpath('.//a')[0]
 uploaded_moves[a.get('href').rsplit('/',1)[1]]={'name':' '.join(a.text_content().split()),'effect':' '.join(cells[6].text_content().split())}
movenames=names('move_names','move_id');meta={num(r['move_id']):r for r in rows('move_meta')};ailments={i:r['identifier'] for i,r in index('move_meta_ailments').items()};changes={}
for r in rows('move_meta_stat_changes'):changes.setdefault(num(r['move_id']),[]).append({'stat':statkeys.get(num(r['stat_id'])),'change':num(r['change'])})
prose={num(r['move_effect_id']):r['short_effect'] for r in rows('move_effect_prose') if r['local_language_id']=='9'}
moves={}
for mid,r in index('moves').items():
 m=meta.get(mid,{});ref=uploaded_moves.get(r['identifier'],{});effect=ref.get('effect',prose.get(num(r['effect_id']),''));chance=num(r['effect_chance'],0);effect=effect.replace('$effect_chance',str(chance))
 moves[str(mid)]={'id':mid,'slug':r['identifier'],'name':ref.get('name',movenames.get(mid,r['identifier'])),'type':types[num(r['type_id'])]['identifier'],'category':{1:'status',2:'physical',3:'special'}[num(r['damage_class_id'])],'power':num(r['power']),'pp':num(r['pp'],1),'accuracy':num(r['accuracy']),'priority':num(r['priority'],0),'target':num(r['target_id']),'effect':effect,'effectChance':chance,'ailment':ailments.get(num(m.get('meta_ailment_id')), 'none'),'ailmentChance':num(m.get('ailment_chance'),0),'statChance':num(m.get('stat_chance'),0),'statChanges':changes.get(mid,[]),'healing':num(m.get('healing'),0),'drain':num(m.get('drain'),0),'minHits':num(m.get('min_hits'),1),'maxHits':num(m.get('max_hits'),1),'flinchChance':num(m.get('flinch_chance'),0)}
# Pick one consistent most recent traditional turn-based learnset per available form.
excluded={'legends-arceus','legends-za','mega-dimension','champions'}
learnrows=[r for r in rows('pokemon_moves') if num(r['pokemon_id']) in byapi and vg[num(r['version_group_id'])]['identifier'] not in excluded]
best={}
for r in learnrows:
 pid=num(r['pokemon_id']);gid=num(r['version_group_id']);rank=num(vg[gid]['order']);
 if pid not in best or rank>best[pid][0]:best[pid]=(rank,gid)
learnsets={}
for pid,(_,gid) in best.items():learnsets[byapi[pid]]={'versionGroup':vg[gid]['identifier'],'levelUp':[],'machine':[],'tutor':[],'egg':[]}
methods={1:'levelUp',2:'egg',3:'tutor',4:'machine'}
for r in learnrows:
 pid=num(r['pokemon_id']);gid=num(r['version_group_id']);method=methods.get(num(r['pokemon_move_method_id']))
 if gid!=best[pid][1] or not method:continue
 bucket=learnsets[byapi[pid]][method];entry={'moveId':num(r['move_id']),'level':num(r['level'],0)}
 if entry not in bucket:bucket.append(entry)
for v in learnsets.values():v['levelUp'].sort(key=lambda r:(r['level'],r['moveId']))
for v in learnsets.values():v['historicalTutor']=[]
for r in learnrows:
 if num(r['pokemon_move_method_id'])==3:
  bucket=learnsets[byapi[num(r['pokemon_id'])]]['historicalTutor'];mid=num(r['move_id'])
  if mid not in bucket:bucket.append(mid)
# Nature names and modifiers come from the supplemental CSV, not invented personality labels.
naturenames=names('nature_names','nature_id');natures=[]
for nid,r in index('natures').items():natures.append({'id':nid,'name':naturenames.get(nid,r['identifier'].title()),'increases':statkeys[num(r['increased_stat_id'])],'decreases':statkeys[num(r['decreased_stat_id'])],'personalityIndex':num(r['game_index'])})
# Tutor offerings from the saved reference: include game/section/price/conditions.
tdoc=html.fromstring(next(uploads.glob('*move tutors*html')).read_text());offers=[];game='';section=''
for node in tdoc.xpath('//main')[0].iter():
 if node.tag=='h2':game=' '.join(node.text_content().split());section=''
 elif node.tag=='h3':section=' '.join(node.text_content().split())
 elif node.tag=='table':
  headers=[' '.join(th.text_content().split()).lower() for th in node.xpath('.//thead//th')]
  for tr in node.xpath('.//tbody/tr'):
   cells=tr.xpath('./td');link=cells[0].xpath('.//a[contains(@href,"/move/")]')
   if not link:continue
   slug=link[0].get('href').rsplit('/',1)[1];mid=next((int(i) for i,m in moves.items() if m['slug']==slug),None)
   info={k:' '.join(c.text_content().split()) for k,c in zip(headers,cells)}
   offers.append({'moveId':mid,'moveName':link[0].text_content().strip(),'game':game,'section':section,'sourceCost':info.get('cost'),'location':info.get('location',section),'condition':info.get('condition')})
# Cache original per-version wild encounter slots and levels, preserving game-version differences.
areas=index('location_areas');locations=index('locations');locnames=names('location_names','location_id');regions=index('regions');slots=index('encounter_slots');methods=index('encounter_methods');encounterdata={}
for r in rows('encounters'):
 pid=num(r['pokemon_id']);key=byapi.get(pid)
 if not key:continue
 area=areas[num(r['location_area_id'])];loc=locations[num(area['location_id'])];slot=slots[num(r['encounter_slot_id'])];lid=str(loc['id'])
 record=encounterdata.setdefault(lid,{'id':num(loc['id']),'slug':loc['identifier'],'name':locnames.get(num(loc['id']),loc['identifier']),'region':regions.get(num(loc['region_id']),{}).get('identifier'),'versions':{}})
 version=versions[num(r['version_id'])]['identifier'];bucket=record['versions'].setdefault(version,[])
 bucket.append({'pokemonId':key,'area':area['identifier'],'method':methods[num(slot['encounter_method_id'])]['identifier'],'weight':num(slot['rarity'],1),'minLevel':num(r['min_level']),'maxLevel':num(r['max_level'])})
write('pokedex',cat);write('moves',{'source':'Uploaded Pokémon Database move-list plus PokeAPI CSV metadata','uploadedMoveCount':len(uploaded_moves),'moves':moves});write('learnsets',{'source':'PokeAPI CSV, latest available traditional turn-based version group per form','entries':learnsets});write('natures',{'source':'PokeAPI natures.csv and Pokémon Database nature chart','entries':natures});write('abilities',{'source':'PokeAPI CSV','entries':abilities});write('tutors',{'source':'Uploaded Pokémon Database tutor reference','offers':offers});write('encounters',{'source':'PokeAPI CSV. Original per-version encounters; custom zone levels are configured separately.','locations':list(encounterdata.values())})
print(json.dumps({'catalog':len(entries),'mappedForms':len(byapi),'learnsets':len(learnsets),'moves':len(moves),'uploadedMoves':len(uploaded_moves),'tutorOffers':len(offers),'encounterLocations':len(encounterdata),'natureCount':len(natures)}))
