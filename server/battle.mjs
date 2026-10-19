import {damage,multiplier,moves,getMoveSet,creature,captureLevel,recalculate,getSpecies,train} from './rules.mjs';
const fresh=()=>({ailment:'none',turns:0,stages:{},flinched:false});
export function beginBattle(s,enemy,kind){s.battle={schema:2,kind,enemy,enemyHp:enemy.hp,active:0,health:s.team.map(c=>c.hp),pp:s.team.map(c=>getMoveSet(c).map(m=>m.pp)),effects:s.team.map(fresh),enemyEffects:fresh(),enemyPP:getMoveSet(enemy).map(m=>m.pp),log:['The battle begins']};return s.battle;}
const stage=(value,key,effect)=>{const n=effect.stages[key]||0;return value*(n>=0?(2+n)/2:2/(2-n));};
function adjusted(c,effect){const p={...c};for(const k of ['attack','defense','specialAttack','specialDefense','speed'])p[k]=stage(c[k],k,effect);if(effect.ailment==='paralysis')p.speed*=.5;if(c.ability?.slug==='guts'&&effect.ailment!=='none')p.attack*=1.5;else if(effect.ailment==='burn')p.attack*=.5;return p;}
export function predictDamage(c,enemy,move,effect=fresh(),enemyEffect=fresh()){return damage(adjusted(c,effect),adjusted(enemy,enemyEffect),move);}
export function battleAction(s,b){const t=s.battle;if(!t)throw Error('No active battle');t.visualId??=crypto.randomUUID();t.visualSequence=(t.visualSequence||0)+1;s.battleVisual={battleId:t.visualId,sequence:t.visualSequence,events:[]};let end=null;const enemy=t.enemy;
 const log=message=>t.log.push(message);
 const hp=(side)=>side==='player'?t.health[t.active]:t.enemyHp;
 const setHP=(side,value)=>{if(side==='player')t.health[t.active]=Math.max(0,Math.min(s.team[t.active].hp,value));else t.enemyHp=Math.max(0,Math.min(enemy.hp,value));};
 const effects=(side)=>side==='player'?t.effects[t.active]:t.enemyEffects;
 const actor=(side)=>side==='player'?s.team[t.active]:enemy;
 const check=()=>{if(t.enemyHp<=0){end='win';return;}if(t.health[t.active]<=0){const options=s.team.map((c,i)=>({i,n:t.health[i]>0?Math.max(...getMoveSet(c).map(m=>predictDamage(c,enemy,m,t.effects[i],t.enemyEffects)),0):-1})).sort((a,b)=>b.n-a.n);if(options[0].n<0)end='loss';else{t.active=options[0].i;log(`${s.team[t.active].name} enters the battle.`);}}};
 const use=(side,move,slot=null)=>{if(end||hp(side)<=0)return;const c=actor(side),e=effects(side),other=side==='player'?'enemy':'player',target=actor(other),te=effects(other);
 if(e.flinched){e.flinched=false;return log(`${c.name} flinched.`);}if(e.ailment==='sleep'){if(e.turns-->0)return log(`${c.name} is asleep.`);e.ailment='none';}if(e.ailment==='paralysis'&&Math.random()<.25)return log(`${c.name} is paralyzed.`);if(e.ailment==='freeze'){if(Math.random()>=.2)return log(`${c.name} is frozen.`);e.ailment='none';}
 if(slot!==null&&slot>=0){const pp=side==='player'?t.pp[t.active]:t.enemyPP;pp[slot]--;}
 const visual={side,attackerUid:c.uid,targetUid:target.uid,skillId:move.id?10000+move.id:null,hit:false,damage:0};s.battleVisual.events.push(visual);
 const accuracyStage=(c.ability?.slug==='keen-eye'?Math.max(0,e.stages.accuracy||0):e.stages.accuracy||0)-(c.ability?.slug==='keen-eye'?0:te.stages.evasion||0);const accuracyFactor=accuracyStage>=0?(3+accuracyStage)/3:3/(3-accuracyStage);if(move.accuracy!=null&&Math.random()*100>move.accuracy*accuracyFactor)return log(`${c.name}'s ${move.name} missed.`);
 const immune=multiplier(move.type,target.types)===0;if((move.category!=='status'||move.ailment==='paralysis')&&immune)return log(`${move.name} has no effect.`);
 let dealt=0;if(move.power){const count=move.maxHits>1?move.minHits+Math.floor(Math.random()*(move.maxHits-move.minHits+1)):1;for(let i=0;i<count;i++){let n=predictDamage(c,target,move,e,te);if(['overgrow','blaze','torrent'].includes(c.ability?.slug)&&hp(side)<=c.hp/3&&move.type===c.type)n=Math.floor(n*1.5);n=Math.max(1,Math.floor(n*(.85+Math.random()*.15)));dealt+=Math.min(hp(other),n);setHP(other,hp(other)-n);if(!hp(other))break;}const eff=multiplier(move.type,target.types);log(`${c.name} used ${move.name}: ${dealt}${eff>1?' · super effective':eff<1?' · not very effective':''}.`);}else log(`${c.name} used ${move.name}.`);
 visual.hit=true;visual.damage=dealt;
 if(move.healing)setHP(side,hp(side)+Math.floor(c.hp*move.healing/100));if(move.drain)setHP(side,hp(side)+Math.floor(dealt*move.drain/100));
 const self=move.target===7;if(move.statChanges?.length&&(move.category==='status'||target.ability?.slug!=='shield-dust')&&(move.category==='status'||Math.random()*100<(move.statChance||100))){const effect=self?e:te;for(const change of move.statChanges)effect.stages[change.stat]=Math.max(-6,Math.min(6,(effect.stages[change.stat]||0)+change.change));}
 if(['sleep','paralysis','poison','burn','freeze'].includes(move.ailment)&&te.ailment==='none'&&hp(other)>0&&(move.category==='status'||target.ability?.slug!=='shield-dust')&&(move.category==='status'||Math.random()*100<move.ailmentChance)){
  const blocked=move.ailment==='poison'&&target.types.some(v=>['poison','steel'].includes(v))||move.ailment==='burn'&&target.types.includes('fire')||move.ailment==='paralysis'&&target.types.includes('electric')||move.ailment==='freeze'&&target.types.includes('ice');if(!blocked){te.ailment=move.ailment;te.turns=1+Math.floor(Math.random()*3);log(`${target.name}: ${move.ailment}.`);}
 }
 if(move.flinchChance&&Math.random()*100<move.flinchChance)te.flinched=true;check();
 };
 const enemyAttack=()=>{const candidates=getMoveSet(enemy).map((m,i)=>({m,i,score:t.enemyPP[i]>0?predictDamage(enemy,s.team[t.active],m,t.enemyEffects,t.effects[t.active]):-1})).sort((a,b)=>b.score-a.score);const pick=candidates[0];if(pick&&pick.score>=0){use('enemy',pick.m,pick.i);}else use('enemy',{id:165,name:'Struggle',type:'normal',category:'physical',power:50,accuracy:null});};
 if(b.action==='run')end='retreat';
 else if(b.action==='capture'){
  if(t.kind!=='wild'){log('You cannot catch another trainer’s Pokémon.');return null;}
  const ball=b.ball||'poke-ball';if(!['poke-ball','ultra-ball','master-ball'].includes(ball)||(s.inventory[ball]||0)<1)throw Error('You do not have that Poké Ball');
  const rare=getSpecies(enemy.id).rareCapture;
  if(rare&&ball!=='master-ball'&&(ball!=='ultra-ball'||t.enemyHp>enemy.hp*.25||!['sleep','paralysis'].includes(t.enemyEffects.ailment)))throw Error('Use a Master Ball, or weaken it and apply Sleep/Paralysis before an Ultra Ball');
  s.inventory[ball]--;const chance=ball==='master-ball'?1:Math.min(.98,(rare?.08:.72)+(1-t.enemyHp/enemy.hp)*.22+(ball==='ultra-ball'?.2:0)+(['sleep','paralysis'].includes(t.enemyEffects.ailment)?.1:0));
  if(Math.random()<chance){const caught=structuredClone(enemy);caught.uid=crypto.randomUUID();caught.level=captureLevel(s.level,enemy.level);caught.locked=false;recalculate(caught);(s.team.length<6?s.team:s.box).push(caught);end='capture';log(`${enemy.name} was caught.`);}else{log('The Pokémon broke free.');enemyAttack();}
 }else if(b.action==='switch'){const i=Number(b.index);if(!Number.isInteger(i)||!s.team[i]||t.health[i]<=0||i===t.active)throw Error('Selection unavailable');t.active=i;enemyAttack();}
 else{
  const c=s.team[t.active],available=getMoveSet(c);let i=Number(b.move);
  if(b.action==='auto'){s.autoEnabled=true;i=available.map((m,i)=>({i,n:t.pp[t.active][i]>0?predictDamage(c,enemy,m,t.effects[t.active],t.enemyEffects):-1})).sort((a,b)=>b.n-a.n)[0]?.i;}
  const exhausted=t.pp[t.active].every(n=>!n);if(exhausted)i=-1;if(!exhausted&&(!Number.isInteger(i)||!available[i]||!t.pp[t.active][i]))throw Error('Move unavailable or out of PP');const m=exhausted?{id:165,name:'Struggle',type:'normal',category:'physical',power:50,accuracy:null,drain:-25}:available[i];const em=getMoveSet(enemy).filter((m,i)=>t.enemyPP[i]>0).sort((a,b)=>predictDamage(enemy,c,b)-predictDamage(enemy,c,a))[0];const playerFirst=(m.priority||0)>(em?.priority||0)||(m.priority||0)===(em?.priority||0)&&adjusted(c,t.effects[t.active]).speed>=adjusted(enemy,t.enemyEffects).speed;
  if(playerFirst){use('player',m,exhausted?null:i);if(!end)enemyAttack();}else{const active=t.active;enemyAttack();if(!end&&t.active===active&&hp('player')>0)use('player',m,exhausted?null:i);}
 }
 if(!end){for(const side of ['player','enemy']){const e=effects(side),c=actor(side);e.flinched=false;if(c.ability?.slug==='shed-skin'&&e.ailment!=='none'&&Math.random()<1/3)e.ailment='none';if(['poison','burn'].includes(e.ailment)){setHP(side,hp(side)-Math.max(1,Math.floor(c.hp/(e.ailment==='burn'?16:8))));log(`${c.name} took ${e.ailment} damage.`);}}check();}
 if(end==='win'){const c=s.team[t.active];for(const [stat,n] of Object.entries(getSpecies(enemy.id).evYield)){if(n){try{train(c,stat,n);}catch{}}}c.friendship=Math.min(255,c.friendship+2);}
 t.log=t.log.slice(-8);return end;
}

export function advanceOriginalOpponent(t){if(!t.opponents||t.opponentIndex+1>=t.opponents.length)return false;t.opponentIndex++;t.enemy=t.opponents[t.opponentIndex];t.enemyHp=t.enemy.hp;t.enemyEffects=fresh();t.enemyPP=getMoveSet(t.enemy).map(m=>m.pp);t.log.push(t.enemy.name+' enters the battle.');t.log=t.log.slice(-8);return true;}
