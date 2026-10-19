import fs from 'node:fs';
const file=new URL('../server/rules.mjs',import.meta.url);let text=fs.readFileSync(file,'utf8');
if(!text.includes('Object.assign(c,sourceCreatureStats(c,p,nature))')){
 const start=text.indexOf('const bonus=',text.indexOf('export function recalculate'));
 const end=text.indexOf('const max=',start);
 if(start<0||end<0)throw Error('Unrecognized rules version. No files changed.');
 text=text.slice(0,start)+'Object.assign(c,sourceCreatureStats(c,p,nature));'+text.slice(end);
 if(!text.includes("from './source-stats.mjs'"))text="import {sourceCreatureStats} from './source-stats.mjs';\n"+text;
 if(!fs.existsSync(new URL('../server/rules.mjs.before-stats-v04',import.meta.url)))fs.copyFileSync(file,new URL('../server/rules.mjs.before-stats-v04',import.meta.url));
 fs.writeFileSync(file,text);
}
console.log('Original stat calculation installed. Saves preserved. Restart server.');
