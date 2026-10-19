import test from 'node:test';
import assert from 'node:assert/strict';
import {SourceFieldSteps} from '../public/source-field-steps.js';
test('catching uses the source BoxId and Step range, with no keyboard trigger',()=>{
 const s=new SourceFieldSteps([{BoxId:119101,Step:[15,30]}],()=>0);
 assert.equal(s.advance({id:119101},14),null);
 assert.equal(s.advance({id:119101},0),null);
 assert.equal(s.advance({id:119101},1).BoxId,119101);
 assert.equal(s.advance({id:119101},14),null);
 s.advance(null,100);
 assert.equal(s.advance({id:119101},1),null);
 assert.equal(s.advance({id:42},1000),null);
});
test('source maximum Step is reachable and movement subdivisions do not alter progress',()=>{
 const a=new SourceFieldSteps([{BoxId:1,Step:[15,30]}],()=>.99999);
 for(let i=0;i<119;i++)assert.equal(a.advance({id:1},.25),null);
 assert.equal(a.advance({id:1},.25).BoxId,1);
});
