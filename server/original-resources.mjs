import fs from 'node:fs';
import {gunzipSync} from 'node:zlib';
const read=n=>JSON.parse(gunzipSync(fs.readFileSync(new URL('../public/data/original/configs/'+n+'Config.json.gz',import.meta.url))));
const levels=new Map(read('LevelUp').map(r=>[r.Id,r])),global=read('GlobalValue')[0],vip=read('Vip'),buys=read('PowAndFatBuy'),gifts=new Map(read('ItemGift').map(r=>[r.Id,r]));
const fields={power:{item:3,max:'PowerMax',reply:'PowerReply',buy:1,value:'PowerValue',vip:'BuyPowerNum'},fatigue:{item:4,max:'FatigueMax',reply:'FatigueReply',buy:2,value:'FatigueValue',vip:'BuyFatigueNum'}};
export function ensureResources(s,now=Date.now()){
 const level=levels.get(s.level);if(!level)throw Error('Original level resource limits unavailable');
 s.resources??={schema:1,power:{value:Math.min(Number.isFinite(s.energy)?s.energy:level.PowerMax,level.PowerMax),at:now},fatigue:{value:level.FatigueMax,at:now},purchases:{day:new Date(now).toISOString().slice(0,10),power:0,fatigue:0},level:s.level};
 const r=s.resources;
 // Existing account and partner data remain intact. Legacy energy becomes Power once.
 if(r.level<s.level){for(let l=r.level+1;l<=s.level;l++){const row=levels.get(l);r.power.value+=row?.RewPower||0;r.fatigue.value+=row?.RewFatigue||0;}r.level=s.level;}
 for(const [key,f]of Object.entries(fields)){
  const item=r[key],max=level[f.max],interval=global[f.reply]*1000;
  if(!(interval>0))throw Error('Original resource recovery interval unavailable');
  const ticks=Math.max(0,Math.floor((now-item.at)/interval));
  if(ticks){item.value=Math.min(max,item.value+ticks);item.at=item.value===max?now:item.at+ticks*interval;}
  item.max=max;item.intervalMs=interval;item.itemId=f.item;
 }
 s.energy=r.power.value;return r;
}
export function resourceCost(challenge){return challenge?Number(challenge.config.NeedPower??0):Number(global.NeedFatigue);}
export function requireResource(s,key,amount,now=Date.now()){const r=ensureResources(s,now);if(!fields[key]||!Number.isFinite(amount)||amount<0)throw Error('Invalid original resource cost');if(r[key].value<amount)throw Error('Not enough '+(key==='power'?'Energy':'Zip'));return r[key];}
export function spendResource(s,key,amount){const item=requireResource(s,key,amount);item.value-=amount;if(key==='power')s.energy=item.value;}
export function addResource(s,id,amount){const key=Object.keys(fields).find(k=>fields[k].item===id);if(!key||!(amount>=0))throw Error('Invalid original resource reward');const r=ensureResources(s);r[key].value=Math.min(r[key].max,r[key].value+amount);if(key==='power')s.energy=r[key].value;}
export function refillOffer(s,key,now=Date.now()){
 const r=ensureResources(s,now),f=fields[key];if(!f)throw Error('Unknown resource');
 const day=new Date(now).toISOString().slice(0,10);if(r.purchases.day!==day)r.purchases={day,power:0,fatigue:0};
 const tier=vip.find(v=>v.Level===(s.vip||0))||vip[0],used=r.purchases[key],record=buys.find(b=>b.Type===f.buy&&b.Num===used+1);
 return {key,used,limit:tier[f.vip],record:record||null,amount:record?.[f.value]||0};
}
export function refillResource(s,key){
 const offer=refillOffer(s,key),r=s.resources,rec=offer.record;
 if(!rec||offer.used>=offer.limit)throw Error('Daily refill limit reached');
 if(r[key].value>=r[key].max)throw Error('Resource is already full');
 const wallet=rec.PriceItem===2?'gems':rec.PriceItem===1?'coins':null;
 if(!wallet||s[wallet]<rec.PriceNum)throw Error('Not enough currency');
 s[wallet]-=rec.PriceNum;r.purchases[key]++;addResource(s,fields[key].item,offer.amount);
}
export function useResourceGift(s,id){
 const gift=gifts.get(Number(id)),inventory=s.original?.inventory;
 if(!gift||!gift.fixReward.length||!gift.fixReward.every(([item])=>[3,4].includes(item)))throw Error('Not an original Energy or Zip gift');
 if(!(inventory?.[id]>0))throw Error('Gift is not owned');
 ensureResources(s);if(gift.fixReward.every(([item])=>{const key=item===3?'power':'fatigue';return s.resources[key].value>=s.resources[key].max;}))throw Error('Resource is already full');
 inventory[id]--;for(const [item,count]of gift.fixReward)addResource(s,item,count);
}
