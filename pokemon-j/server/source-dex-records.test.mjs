import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {gunzipSync} from 'node:zlib';
import {sourceDexRows} from '../public/source-dex-records.js';
const data=new URL('../public/data/',import.meta.url);
const entries=JSON.parse(fs.readFileSync(new URL('pokedex.json',data))).entries;
const {gather}=JSON.parse(gunzipSync(fs.readFileSync(new URL('original/interface.json.gz',data))));
test('all nine generations use source species IDs rather than catalogue row IDs',()=>{
 for(let generation=1;generation<=9;generation++){
  const expected=gather.filter(r=>r.Type===generation).sort((a,b)=>a.Rank-b.Rank).filter(r=>entries.some(p=>p.originalId===r.EudemonId));
  const actual=sourceDexRows(entries,gather,generation);
  assert(actual.length>0,`empty generation ${generation}`);
  assert.deepEqual(actual.map(p=>p.originalId),expected.map(r=>r.EudemonId));
 }
});
test('search still finds later generations by name and number',()=>{
 const p=entries.find(p=>p.name.toLowerCase()==='sprigatito');assert(p);
 assert(sourceDexRows(entries,gather,1,p.name).some(r=>r.originalId===p.originalId));
 assert(sourceDexRows(entries,gather,1,String(p.number)).some(r=>r.originalId===p.originalId));
});
