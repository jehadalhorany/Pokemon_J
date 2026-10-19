import fs from 'node:fs';
const tables=JSON.parse(fs.readFileSync(new URL('./source-stat-records.json',import.meta.url),'utf8'));
const keys=['hp','attack','defense','specialAttack','specialDefense','speed'];
const fields=['Hp','Atk','Def','Satk','Sdef','Speed'];
function follow(table,start,predicate){let row=table[start],seen=new Set();while(row&&!predicate(row)&&row.NextId&&!seen.has(row.Id)){seen.add(row.Id);row=table[row.NextId];}return row&&predicate(row)?row:null;}
const attr=(r,id)=>(r?.attr||[]).find(x=>x[0]===id)?.[1]||0;
// Hotfix.dll EudemonHelper methods 138,139,146. Config IDs remain source IDs.
export function sourceCreatureStats(c,p,nature){
 const level=follow(tables.EudemonLevelConfig,p.original.LevelId,r=>r.Level===c.level);
 const star=follow(tables.EudemonStarConfig,p.original.StarId,r=>r.star===Math.max(c.stars,tables.EudemonStarConfig[p.original.StarId]?.star||0));
 const ship=tables.EudemonShipConfig[c.sourceShipId||p.original.ShipId];
 const awakening=follow(tables.EudemonAwakeningConfig,p.original.EudemonAwakeningId,r=>r.Level===(c.awakening||0));
 if(!level||!star||!ship||!awakening)throw Error('Original creature stat configuration missing for '+c.id);
 const result={};for(let i=0;i<keys.length;i++){
  const key=keys[i],id=100+i,base=p.original[fields[i]];
  const f=Math.fround;
  let value=f(f(f(f(base*2)+f(c.ivs[key]*f(8.8)))+f(c.evs[key]*f(2.2)))*level.Level);value=f(value/100);
  value=f(value+(i===0?f(30+f(level.Level*f(2.2))):15));
  if(i!==0&&nature.increases!==nature.decreases)value=f(value*f(1+(key===nature.increases?.1:key===nature.decreases?-.1:0)));
  const extra=attr(level,id)+attr(star,id)+attr(ship,id)+attr(awakening,id)+Math.trunc((ship.species?.[i]||0)*base/10000)+Math.trunc((star.species?.[i]||0)*base*2/10000)+Math.trunc((awakening.species?.[i]||0)*base/10000);
  result[key]=Math.max(1,Math.trunc(f(value+extra)));
 }return result;
}
