import pathlib,gzip,json,re,collections
ROOT=pathlib.Path(__file__).resolve().parent;PUBLIC=ROOT.parent/'pokemon-j/public';OUT=PUBLIC/'data/original/derived';OUT.mkdir(exist_ok=True)
language=json.load(open(ROOT/'language-en.json'))
def rows(n):return json.load(gzip.open(PUBLIC/'data/original/configs'/(n+'Config.json.gz')))
def text(k):return language.get(k,k or '')
def slug(s):return re.sub(r'[^a-z0-9]+','-',s.lower().replace('♀','-f').replace('♂','-m')).strip('-')
def save(n,x):(OUT/(n+'.json')).write_text(json.dumps(x,ensure_ascii=False,separators=(',',':')))
source='Uploaded Fairy Tamer original configuration records and English language table'
# Existing identifiers are used only to preserve saved copy identities. No old stats or content are copied.
legacy=json.load(open(PUBLIC/'data/pokedex.json'))['entries'];identities={(p['number'],(p.get('form') or p['name']).casefold()):p['id'] for p in legacy}
typeRows=rows('EudemonType');types={r['Id']:{'flight':'flying','toxic':'poison'}.get(text(r['Name']).lower(),text(r['Name']).lower()) for r in typeRows}
quality={r['Id']:text(r['Name']) for r in rows('EudemonQuality')};stars={r['Id']:r for r in rows('EudemonStar')};models={r['Id']:r for r in rows('Model')}
raw=rows('Eudemon');rawById={r['Id']:r for r in raw};entries=[];bySource={};used=set()
for r in raw:
 if r['IsFlash']:continue
 name=text(r['Name']);number=int(re.search(r'\d+',r['Num']).group()) if re.search(r'\d+',r['Num']) else r['Id'];id=identities.get((number,name.casefold()),slug(name))
 if id in used:id+='-'+str(r['Id'])
 used.add(id);bySource[r['Id']]=id;stats=dict(zip(['hp','attack','defense','specialAttack','specialDefense','speed'],[r['Hp'],r['Atk'],r['Def'],r['Satk'],r['Sdef'],r['Speed']]));stats['total']=r['Species']
 entries.append({'id':id,'originalId':r['Id'],'modelKey':models.get(r['Model'],{}).get('Prefabs'),'shinyModelKey':models.get(rawById.get(r['OtherForm'],{}).get('Model'),{}).get('Prefabs'),'number':number,'name':name,'form':None,'types':[types[t] for t in r['types'] if t in types and t!=20],'baseStats':stats,'imageUrl':'/assets/original/portraits/'+r['Icon']+'.png','generation':r['Gen'],'genderRate':-1 if not r['IfSex'] else r['FemalePro']/1250,'captureRate':r['CatchRate'],'baseFriendship':0,'evYield':{},'rareCapture':r['CatchRate']<=2,'rarity':quality.get(r['Quality'],'Quality '+str(r['Quality'])),'initialStars':stars.get(r['StarId'],{}).get('star',1),'abilities':[{'id':r[f],'hidden':f=='HideAbility','slot':i+1}for i,f in enumerate(['Ability1','Ability2','Ability3','HideAbility'])if r[f]],'description':text(r['Des']),'classify':text(r['Classify']),'height':r['Height'],'weight':r['Weight'],'icon':r['Icon'],'releaseItem':r['FreeItem'],'original':r})
# Shiny species reference the normal species ID and carry shiny state on the saved copy.
for r in raw:
 if r['IsFlash']:
  normal=rawById.get(r['OtherForm']);normal=normal if normal and not normal['IsFlash'] else next((p for p in raw if not p['IsFlash'] and p['Num']==r['Num'] and p['Name']==r['Name']),None)
  if normal and normal['Id'] in bySource:bySource[r['Id']]=bySource[normal['Id']]
for entry in entries:
 entry['portraitAvailable']=(PUBLIC/entry['imageUrl'].lstrip('/')).exists()
 if not entry['portraitAvailable']:entry['imageUrl']=None
save('pokedex',{'source':source,'speciesCount':len(set(p['number']for p in entries)),'entryCount':len(entries),'entries':entries,'sourceIds':bySource})
save('abilities',{'source':source,'entries':{r['Id']:{'id':r['Id'],'name':text(r['Name']),'slug':slug(text(r['Name'])),'description':text(r['Des']),'original':r}for r in rows('EudemonAbility')}})
learnsets={}
for r in rows('EudemonSkill'):
 if r['Id']not in bySource:continue
 learnsets[bySource[r['Id']]]={'versionGroup':'original','levelUp':[{'moveId':sid-10000,'level':level,'originalId':sid}for sid,level in r['skillId']],'machine':[],'historicalTutor':[],'original':r}
save('learnsets',{'source':source,'entries':learnsets})
moves={}
for r in rows('Skill'):
 mid=r['Id']-10000
 moves[mid]={'id':mid,'originalId':r['Id'],'slug':slug(text(r['Name'])),'name':text(r['Name']),'type':types.get(r['Element'],'none'),'category':{1:'physical',2:'special',3:'status'}.get(r['Category'],'status'),'power':r['Power'],'pp':r['PP'],'accuracy':r['Hit'],'priority':r['Priority'],'effect':text(r['Des']),'original':r,'effectsDecoded':False}
save('moves',{'source':source,'moves':moves})
save('type-chart',{'source':source,'types':[types[r['Id']]for r in typeRows if r['Id']<=18],'chart':{types[r['Id']]:{types[i+1]:v/10000 for i,v in enumerate(r['type'])}for r in typeRows if r['Id']<=18}})
save('evolution',{'source':source,'nodes':{p['id']:{'id':p['id'],'name':p['name'],'number':p['number'],'imageUrl':p['imageUrl']}for p in entries},'edges':[{'from':bySource[r['EudemonId']],'to':bySource[r['EvolveEudemonId']],'condition':text('') or ('Level '+str(r['Level']) if r['Level'] else ''),'original':r}for r in rows('EudemonEvolve')if r['EudemonId']in bySource and r['EvolveEudemonId']in bySource]})
fields=rows('FieldEudemon');monsters={r['Id']:r for r in rows('EudemonMonster')};pools={}
for f in fields:
 pool=[]
 for condition,mid,weight in f['trainerMonster']:
  m=monsters.get(mid)
  if m and m['Eudemon']in bySource:pool.append({'id':bySource[m['Eudemon']],'originalSpecies':m['Eudemon'],'monsterId':mid,'level':m['Lv'],'stars':m['Star'],'weight':weight,'condition':condition,'original':m})
 pools[f['BoxId']]={'id':f['Id'],'boxId':f['BoxId'],'mapArea':f['MapArea'],'pool':pool,'original':f}
save('wild-pools',{'source':source,'fields':pools})
print('source catalog',len(entries),'species',len(set(p['number']for p in entries)),'moves',len(moves),'learnsets',len(learnsets),'fields',len(pools),'unresolved monsters',sum(1 for f in fields for _,mid,_ in f['trainerMonster'] if mid not in monsters))
