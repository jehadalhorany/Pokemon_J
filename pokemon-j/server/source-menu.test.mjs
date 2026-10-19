import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import {gunzipSync} from 'node:zlib';
import {sourceMenuRecords,sourceFunctionOpen} from '../public/source-menu.js';
const config=JSON.parse(gunzipSync(fs.readFileSync(new URL('../public/data/original/config.json.gz',import.meta.url))));
test('original menu includes Backpack and Pokedex even though IsShow is zero',()=>{
 const rows=sourceMenuRecords(config.functions);assert(rows.some(r=>r.Id===201));assert(rows.some(r=>r.Id===202));
 assert(rows.every(r=>r.Pos===5&&!r.IsClose));
 assert.deepEqual(rows.map(r=>r.Id),[...config.functions].filter(r=>r.Pos===5&&!r.IsClose).sort((a,b)=>a.PosRank-b.PosRank||a.Id-b.Id).map(r=>r.Id));
});
test('Pokedex unlock follows its source quest instead of opening on preview',()=>{
 const dex=config.functions.find(r=>r.Id===202);assert.equal(dex.Quest,1000104);
 const state={level:5,original:{completed:[]}};assert.equal(sourceFunctionOpen(dex,state),false);
 state.original.completed.push(1000104);assert.equal(sourceFunctionOpen(dex,state),true);
});
test('function gates retain level VIP guild and disabled conditions',()=>{
 const r={Level:10,Vip:2,GuildLevel:3};const state={level:9,vip:2,guild:{level:3}};
 assert.equal(sourceFunctionOpen(r,state),false);state.level=10;assert.equal(sourceFunctionOpen(r,state),true);
 assert.equal(sourceFunctionOpen({...r,IsClose:1},state),false);
 assert.equal(sourceFunctionOpen(r,{...state,vip:1}),false);assert.equal(sourceFunctionOpen(r,{...state,guild:{level:2}}),false);
});
test('reachable source menu excludes future duplicate capsule beyond level cap',()=>{
 const rows=sourceMenuRecords(config.functions,100);
 assert(rows.some(r=>r.Id===115));assert(!rows.some(r=>r.Id===138));
 assert(rows.every(r=>(r.Level||0)<=100));
});
