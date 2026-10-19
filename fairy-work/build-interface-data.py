from pathlib import Path
import json,gzip,collections
R=Path(__file__).resolve().parent;P=R.parent/'active-project/public/data/original';lan=json.loads((R/'language-en.json').read_text())
def read(n):return json.loads(gzip.decompress((P/'configs'/(n+'Config.json.gz')).read_bytes()))
client=read('LanguageClient');chinese=collections.defaultdict(set);keys={}
for r in client:
 keys[r['Id']]=r['en']
 if r['cn']:chinese[r['cn']].add(r['en'])
cn={k:next(iter(v))for k,v in chinese.items()if len(v)==1};data={'source':'Uploaded configuration tables and English language records','text':keys,'cn':cn,'items':read('Item'),'quality':read('ItemQuality'),'levels':read('LevelUp'),'global':read('GlobalValue')[0],'main':read('QuestMain'),'branches':read('QuestBranch'),'daily':read('QuestDaily'),'bounty':read('QuestBounty'),'mini':read('MapMini'),'bagCategories':read('ItemBag'),'generations':read('SelectEudemon'),'types':read('EudemonType'),'abilities':read('EudemonAbility'),'gather':read('Gather'),'resourceBuys':read('PowAndFatBuy'),'vip':read('Vip'),'activityWindows':read('ActivityWindow'),'pushWindows':read('PushOpenWindows'),'shopTypes':read('ShopType'),'shopGold':read('ShopGoinData')}
data['catchingFields']=read('FieldEudemon')
for group in ['items','main','branches','daily','bounty','mini','bagCategories','generations','types','abilities','activityWindows','pushWindows']:
 for r in data[group]:
  if 'Name'in r:r['name']=lan.get(r['Name'],r['Name'])
  if 'Des'in r:r['description']=lan.get(r['Des'],r['Des'])
  if 'Desc'in r:r['description']=lan.get(r['Desc'],r['Desc'])
(P/'interface.json.gz').write_bytes(gzip.compress(json.dumps(data,separators=(',',':')).encode(),mtime=0));print('interface records',len(data['items']),len(data['mini']),len(keys))
