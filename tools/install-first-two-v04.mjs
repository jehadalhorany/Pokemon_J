import fs from 'node:fs';import path from 'node:path';import {fileURLToPath}from'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),file=path.join(root,'server/index.mjs');let s=fs.readFileSync(file,'utf8'),out=s;
out=out.replace(/import \{([^}]+)\} from '\.\/original-encounters\.mjs';/,(_,names)=>{const list=names.split(',').map(n=>n.trim());for(const n of ['originalBattleContext','repairOriginalBattleContext'])if(!list.includes(n))list.push(n);return `import {${list.join(',')}} from './original-encounters.mjs';`;});
if(!out.includes('battle.originalScene=context.scene;')){
 if(!out.includes('const sourceCost=resourceCost(challenge);')||!out.includes('battle.originalResourceCost=sourceCost;'))throw Error('Unknown server version. No server file was changed.');
 out=out.replace('const sourceCost=resourceCost(challenge);','const context=originalBattleContext(s,b.originalField,challenge);const sourceCost=resourceCost(challenge);').replace('battle.originalResourceCost=sourceCost;','battle.originalResourceCost=sourceCost;battle.originalArea=context.area;battle.originalScene=context.scene;');
}
if(!out.includes('function safe(s){repairOriginalBattleContext(s);'))out=out.replace('function safe(s){','function safe(s){repairOriginalBattleContext(s);');
if(!out.includes('function safe(s){repairOriginalBattleContext(s);')||!out.includes('import {originalWild,originalChallenge,originalBattleContext,repairOriginalBattleContext}'))throw Error('Unsupported server imports. No server file was changed.');
if(out!==s){const backup=file+'.before-first-two-v04';if(!fs.existsSync(backup))fs.writeFileSync(backup,s);fs.writeFileSync(file,out);}
console.log('v04 native battle binding installed. Saves untouched. Start the server normally.');
