import fs from 'node:fs';import path from 'node:path';import {fileURLToPath}from'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),file=path.join(root,'server/index.mjs');const old=fs.readFileSync(file,'utf8');let s=old;
if(!s.includes("from './source-quests.mjs'"))s="import {sourceQuestCategories,sourceQuestEvent,claimSourceQuest} from './source-quests.mjs';\n"+s;
if(!s.includes('sourceQuestCategories:')){
 const begin=s.indexOf('function safe(s){'),end=s.indexOf('\nhttp.createServer',begin);if(begin<0||end<0)throw Error('Unknown safe-state function. Nothing changed.');let block=s.slice(begin,end);
 if(!block.includes('ensureOriginal(s);')||!block.includes('return {...s,'))throw Error('Unknown state fields. Nothing changed.');
 block=block.replace('ensureOriginal(s);','ensureOriginal(s);const sourceCategories=sourceQuestCategories(s);').replace('return {...s,','return {...s,sourceQuestCategories:sourceCategories,');s=s.slice(0,begin)+block+s.slice(end);
}
if(!s.includes("b.action==='sourceQuestClaim'")){
 const anchor="else if(b.action==='setAuto')";if(!s.includes(anchor))throw Error('Unknown action route. Nothing changed.');s=s.replace(anchor,"else if(b.action==='sourceQuestClaim'){if(s.battle)throw Error('Finish the battle first');claimSourceQuest(s,b.category,b.quest);}\n "+anchor);
}
if(!s.includes('sourceQuestEvent(s,1,')){
 const oldTalk="else if(b.action==='worldTalk')originalTalk(s,Number(b.npc));";if(!s.includes(oldTalk))throw Error('Unknown NPC event. Nothing changed.');s=s.replace(oldTalk,"else if(b.action==='worldTalk'){originalTalk(s,Number(b.npc));sourceQuestEvent(s,1,Number(b.npc));}");
}
if(!s.includes('sourceQuestEvent(s,9,')){
 const shop="else if(b.action==='sourceShopBuy')buyOriginalGold(s,b.offer,b.quantity??1);";if(!s.includes(shop))throw Error('Unknown shop event. Nothing changed.');s=s.replace(shop,"else if(b.action==='sourceShopBuy'){buyOriginalGold(s,b.offer,b.quantity??1);sourceQuestEvent(s,9,1);}");
}
if(!s.includes('sourceQuestEvent(s,13,')){
 const battle='if(end){if(end===\'win\'||end===\'capture\')rewardBattle(s,t,end);';if(!s.includes(battle))throw Error('Unknown battle event. Nothing changed.');s=s.replace(battle,battle+"if(end==='capture')sourceQuestEvent(s,13,t.enemy.originalSpecies);if(end==='win'&&t.originalChallenge)sourceQuestEvent(s,3,t.originalChallenge.npc);");
}
if(s!==old){const backup=file+'.before-quests-v04';if(!fs.existsSync(backup))fs.writeFileSync(backup,old);fs.writeFileSync(file,s);}console.log('v04 quest routes installed. Saves untouched. Start the server normally.');
