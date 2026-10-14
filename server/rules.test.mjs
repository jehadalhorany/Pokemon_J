import {test} from 'node:test';import assert from 'node:assert/strict';import {charge,regenerate,captureLevel,damage,creature} from './rules.mjs';
test('wild costs five for every result',()=>{for(const result of ['win','loss','capture','retreat'])assert.equal(charge({energy:300},'wild',result).energy,295);});
test('trainers charge only for wins',()=>{assert.equal(charge({energy:300},'trainer','loss').energy,300);assert.equal(charge({energy:300},'trainer','win').energy,290);});
test('capture never exceeds player level',()=>{assert.equal(captureLevel(20,22),20);assert.equal(captureLevel(20,8),8);});
test('regeneration respects cap',()=>{assert.equal(regenerate({energy:299,energyAt:0},120000).energy,300);});
test('water deals more damage to fire than grass',()=>{const a=creature('squirtle'),fire=creature('charmander'),grass=creature('bulbasaur');assert.ok(damage(a,fire,{type:'water',power:12})>damage(a,grass,{type:'water',power:12}));});
