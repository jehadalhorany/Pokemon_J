import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {gunzipSync} from 'node:zlib';
import * as THREE from '../public/vendor/three.module.js';

const root=new URL('../public/',import.meta.url);
const read=name=>JSON.parse(gunzipSync(fs.readFileSync(new URL('data/original/'+name+'.json.gz',root))));
const original=read('config');
const worldCode=fs.readFileSync(new URL('original-world.js',root),'utf8').replace(/^import .*\n/gm,'');
// Evaluate the real scene navigation against uploaded polygons without a renderer.
const moduleCode=worldCode.replace('await fetch(\'/data/original/config.json\').then(r=>r.json())','globalThis.__navigationConfig');
globalThis.__navigationConfig=original;globalThis.THREE=THREE;
const {OriginalWorld,point}=await import('data:text/javascript;base64,'+Buffer.from(moduleCode).toString('base64'));
delete globalThis.__navigationConfig;
const sceneCode=fs.readFileSync(new URL('scene.js',root),'utf8');
const navigationCode=sceneCode.slice(sceneCode.indexOf('function pathTo'),sceneCode.indexOf('function areaRoute'));
function simulate(scene,spawn,target,range=25){
 const world=new OriginalWorld(read(scene));const a=point(spawn),b=point(target),safe=world.nearestWalkable(a.x,a.z,100)||a;
 const context={world,pos:{x:safe.x,y:safe.z},navigation:null,keys:new Set(),loading:false,jump:null,facing:0,toast:()=>{}};
 context.distance=t=>Math.hypot(context.pos.x-t.x,context.pos.y-t.z);
 context.blocked=(x,z)=>!world.canWalk(x,z);
 context.step=(dx,dz)=>{if(!context.blocked(context.pos.x+dx,context.pos.y+dz))context.pos={x:context.pos.x+dx,y:context.pos.y+dz};};
 vm.createContext(context);vm.runInContext(navigationCode,context);
 let arrived=false;context.walkTo(b,()=>{arrived=true;},range);
 for(let i=0;i<3000&&context.navigation;i++)context.updateNavigation(.016);
 return {arrived,distance:context.distance(b)};
}
test('source home navigation reaches stairs, Mom and exit',()=>{
 for(const [spawn,target]of [[7180599,6180501],[7180402,1180401],[7180402,6180401]]){
  const a=original.spawns[spawn],b=original.spawns[target];const result=simulate(a.scene,a.p,b.p);
  assert(result.arrived,'target '+target);assert(result.distance<25);
 }
});
test('source professor walk reaches a starter ball using original CRange',()=>{
 const professor=original.spawns[1180101],config=original.npcs.find(n=>n.Id===1180102);
 const ball=read(professor.scene).objects.filter(o=>o.name.toLowerCase()==='pokeball').sort((a,b)=>a.p[0]-b.p[0])[0];
 const range=config.CRange*16/1000;assert.equal(range,38.4);
 const result=simulate(professor.scene,professor.p,ball.p,range);
 assert(result.arrived);assert(result.distance<range);
});
test('quest target without a character model opens the actual lab ball after walking',()=>{
 const source=sceneCode.slice(sceneCode.indexOf('function navigateToEntity'),sceneCode.indexOf('function updateQuestHud'));
 let called;const ball={kind:'starter',x:32,z:-120,range:38.4,run:()=>{}};
 const context={world:{data:{id:4110002}},areaId:1801,state:{team:[]},interactables:[ball],walkTo:(...args)=>{called=args;}};
 vm.createContext(context);vm.runInContext(source,context);
 context.navigateToEntity({scene:4110002,area:1801},1180102);
 assert.deepEqual(called,[ball,ball.run,38.4]);
});
