import test from 'node:test';import assert from 'node:assert/strict';
import {sourceResourceLabels} from '../public/source-resource-hud.js';
test('HUD displays independent server balances including over-cap rewards',()=>{
 const r=sourceResourceLabels({level:100,resources:{power:{value:260,max:260},fatigue:{value:267,max:260}}},[]);
 assert(r.ready);assert.deepEqual(r.rows.map(r=>r.text),['260/260','267/260']);
});
test('outdated backend is shown as unknown, never a made-up full balance',()=>{
 const r=sourceResourceLabels({level:8},[{Id:8,PowerMax:76,FatigueMax:76}]);
 assert.equal(r.ready,false);assert.deepEqual(r.rows.map(r=>r.text),['—/76','—/76']);
});
