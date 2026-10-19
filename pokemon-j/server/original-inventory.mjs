import fs from 'node:fs';import {gunzipSync} from 'node:zlib';
import {ensureResources} from './original-resources.mjs';
const rows=JSON.parse(gunzipSync(fs.readFileSync(new URL('../public/data/original/configs/ShopGoinDataConfig.json.gz',import.meta.url))));
const aliases={1001:'poke-ball',1002:'great-ball',1003:'ultra-ball',1004:'master-ball'};
export function originalItemCount(s,id){if(id===1)return s.coins;if(id===2)return s.gems;if(id===3||id===4){const r=ensureResources(s);return r[id===3?'power':'fatigue'].value;}if(aliases[id])return s.inventory?.[aliases[id]]||0;return s.original?.inventory?.[id]||0;}
export function originalInventory(s){const ids=new Set([...Object.keys(s.original?.inventory||{}).map(Number),...Object.keys(aliases).map(Number)]);return [...ids].map(id=>({id,count:originalItemCount(s,id)})).filter(r=>r.count>0);}
export function buyOriginalGold(s,id,quantity=1){
 const row=rows.find(r=>r.Id===Number(id));if(!row||row.Type!==1)throw Error('Original shop offer unavailable');
 if(!Number.isInteger(quantity)||quantity<1||quantity>1000)throw Error('Invalid purchase quantity');
 if(s.level<row.MinLevel||s.level>row.MaxLevel||(s.vip||0)<row.VipLevel)throw Error('Shop offer is locked');
 s.original.shopPurchases??={};const used=s.original.shopPurchases[row.Id]||0;
 if(row.BuyNum>=0&&used+quantity>row.BuyNum)throw Error('Purchase limit reached');
 const [currency,price]=row.BuyItem,[item,count]=row.ShopItem;
 if(![1,2].includes(currency)||![1,2].includes(item))throw Error('Unsupported original gold exchange');
 if(originalItemCount(s,currency)<price*quantity)throw Error('Not enough currency');
 s[currency===1?'coins':'gems']-=price*quantity;s[item===1?'coins':'gems']+=count*quantity;s.original.shopPurchases[row.Id]=used+quantity;
}

export function changeOriginalItem(s,id,delta){const next=originalItemCount(s,id)+delta;if(!Number.isSafeInteger(delta)||!Number.isSafeInteger(next)||next<0)throw Error('Invalid item balance');if(id===1)s.coins=next;else if(id===2)s.gems=next;else if(id===3||id===4)ensureResources(s)[id===3?'power':'fatigue'].value=next;else if(aliases[id]){s.inventory??={};s.inventory[aliases[id]]=next;}else{s.original??={};s.original.inventory??={};s.original.inventory[id]=next;}return next;}
