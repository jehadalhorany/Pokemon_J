export const config={energyMax:300,regenMs:60000,wildCost:5,trainerWinCost:10,refillCost:50,refillDailyMax:10,refillAmount:100,levelMax:100,autoMs:20000};
export function regenerate(s,now=Date.now()){const n=Math.floor((now-s.energyAt)/config.regenMs);if(n>0){s.energy=Math.min(config.energyMax,s.energy+n);s.energyAt=s.energy===config.energyMax?now:s.energyAt+n*config.regenMs;}return s;}
export function captureLevel(player,wild){return Math.min(player,wild);}
export function charge(s,kind,result){const cost=kind==='wild'?5:result==='win'?10:0;if(s.energy<cost)throw Error('Not enough energy');s.energy-=cost;return s;}
export const species=[{id:'bulbasaur',name:'Bulbasaur',type:'grass',color:'#72c899'},{id:'charmander',name:'Charmander',type:'fire',color:'#f7a36b'},{id:'squirtle',name:'Squirtle',type:'water',color:'#6bc7e7'}];
export function creature(id,level=5){const a=species.find(x=>x.id===id)||species[0];return {...a,uid:crypto.randomUUID(),level,stars:2,awakening:0,rarity:'SSR',shiny:false,locked:false,hp:40+level*4,attack:12+level*2,defense:10+level,speed:10+level,pp:20};}
export function multiplier(a,b){return ({water:{fire:2,grass:.5},fire:{grass:2,water:.5},grass:{water:2,fire:.5}})[a]?.[b]||1;}
export function damage(a,b,move){return Math.max(1,Math.floor((a.attack+move.power-b.defense*.4)*multiplier(move.type,b.type)));}
