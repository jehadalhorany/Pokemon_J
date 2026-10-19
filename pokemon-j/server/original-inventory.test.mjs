import test from 'node:test';import assert from 'node:assert/strict';
import fs from 'node:fs';import {gunzipSync} from 'node:zlib';
import {buyOriginalGold,originalInventory} from './original-inventory.mjs';
const rows=JSON.parse(gunzipSync(fs.readFileSync(new URL('../public/data/original/configs/ShopGoinDataConfig.json.gz',import.meta.url))));
const offer=rows.find(r=>r.Type===1&&r.VipLevel===0&&r.MinLevel<=5&&r.MaxLevel>=5&&r.BuyNum!==0);
const account=()=>({level:5,vip:0,coins:100000,gems:100000,inventory:{'poke-ball':10},original:{inventory:{1001:10},shopPurchases:{}}});
test('native bag does not double count the legacy alias and its source reward record',()=>{assert.equal(originalInventory(account()).find(r=>r.id===1001).count,10);});
test('source gold offer charges and grants its exact configured currencies',()=>{const s=account(),before=structuredClone(s);buyOriginalGold(s,offer.Id);const key=id=>id===1?'coins':'gems';assert.equal(s[key(offer.BuyItem[0])],before[key(offer.BuyItem[0])]-offer.BuyItem[1]);assert.equal(s[key(offer.ShopItem[0])],before[key(offer.ShopItem[0])]+offer.ShopItem[1]);});
test('invalid or unaffordable source shop purchases preserve balances and inventory',()=>{const s=account();s.coins=0;s.gems=0;const before=structuredClone(s);assert.throws(()=>buyOriginalGold(s,offer.Id),/currency/);assert.deepEqual(s,before);assert.throws(()=>buyOriginalGold(s,offer.Id,-1),/quantity/);assert.deepEqual(s,before);assert.throws(()=>buyOriginalGold(s,999999),/unavailable/);assert.deepEqual(s,before);});
