import {test} from 'node:test';import assert from 'node:assert/strict';import {charge,regenerate,captureLevel,damage,creature,multiplier,typeChart,hasSwimPartner} from './rules.mjs';
test('wild costs five for every result',()=>{for(const result of ['win','loss','capture','retreat'])assert.equal(charge({energy:300},'wild',result).energy,295);});
test('trainers charge only for wins',()=>{assert.equal(charge({energy:300},'trainer','loss').energy,300);assert.equal(charge({energy:300},'trainer','win').energy,290);});
test('capture never exceeds player level',()=>{assert.equal(captureLevel(20,22),20);assert.equal(captureLevel(20,8),8);});
test('regeneration respects cap',()=>{assert.equal(regenerate({energy:299,energyAt:0},120000).energy,300);});
test('water deals more damage to fire than grass',()=>{const a=creature('squirtle'),fire=creature('charmander'),grass=creature('bulbasaur');assert.ok(damage(a,fire,{type:'water',power:12})>damage(a,grass,{type:'water',power:12}));});

test('modern chart has 18 types and preserves immunity',()=>{assert.equal(typeChart.types.length,18);assert.equal(multiplier('electric','ground'),0);assert.equal(multiplier('normal','ghost'),0);assert.equal(multiplier('dragon','fairy'),0);assert.equal(damage(creature('squirtle'),{...creature('bulbasaur'),types:['ghost']},{type:'normal',power:20}),0);});
test('dual types multiply strengths and resistance',()=>{assert.equal(multiplier('ice',['grass','ground']),4);assert.equal(multiplier('fire',['water','dragon']),.25);assert.equal(multiplier('electric',['water','ground']),0);assert.equal(multiplier('ground',['grass','poison']),1);});
test('swimming needs both a water partner and learned Swim',()=>{const water=creature('squirtle');assert.equal(hasSwimPartner({team:[water]}),false);water.learnedMoves=['Swim'];assert.equal(hasSwimPartner({team:[water]}),true);assert.equal(hasSwimPartner({team:[{...creature('charmander'),learnedMoves:['Swim']}]}),false);});
