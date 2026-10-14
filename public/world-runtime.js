import * as THREE from './vendor/three.module.js';
import {loadModel} from './asset-runtime.js';
// MapConfig coordinates are decimetres. Prefab root positions are replaced by map placement.
export const WORLD_SCALE=16;
export const toWorld=p=>({x:480+p[0]*1.6,y:(p[1]||0)*1.6,z:1120-p[2]*1.6});
export const toSource=(x,z)=>[(x-480)/16,(1120-z)/16];
export const regionCenters={pallet:[0,57],route1:[0,10],viridian:[0,-35],route2:[0,-80],forest:[110,-100]};
export const spawnFor=id=>{const p=regionCenters[id]||regionCenters.pallet;return {x:480+p[0]*16,y:1120-p[1]*16};};
export async function createWorld(){
 const response=await fetch('/data/world/kanto.json');if(!response.ok)throw Error('World map data unavailable');
 const data=await response.json(),waterPolygons=await fetch('/data/world/water.json').then(r=>r.json()),polygons=await fetch('/data/world/walk.json').then(r=>{if(!r.ok)throw Error('Walk map unavailable');return r.json();}),navCells=new Map(),root=new THREE.Group();for(const poly of polygons){const xs=poly.map(p=>p[0]),zs=poly.map(p=>p[1]);for(let x=Math.floor(Math.min(...xs)/10);x<=Math.floor(Math.max(...xs)/10);x++)for(let z=Math.floor(Math.min(...zs)/10);z<=Math.floor(Math.max(...zs)/10);z++){const k=x+','+z;if(!navCells.has(k))navCells.set(k,[]);navCells.get(k).push(poly);}}
 function canWalk(x,z){const [sx,sz]=toSource(x,z),polys=navCells.get(Math.floor(sx/10)+','+Math.floor(sz/10))||[];return polys.some(poly=>{let inside=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j];if((a[1]>sz)!==(b[1]>sz)&&sx<(b[0]-a[0])*(sz-a[1])/(b[1]-a[1])+a[0])inside=!inside;}return inside;});}root.name='MapConfig_1000001';
 const cells=new Map(),loaded=new Map(),errors=[],colliders=[],ground=data.floors.filter(f=>f.bounds).map(f=>{const p=toWorld(f.p),a=f.bounds.min,b=f.bounds.max;return {x:p.x+(a[0]+b[0])*8,z:p.z-(a[2]+b[2])*8,w:(b[0]-a[0])*16,d:(b[2]-a[2])*16,name:f.name};});let revision=0;
 for(const row of [...data.floors.map(f=>({...f,floor:true})),...data.objects,...(data.extras||[])]){const key=Math.floor(row.p[0]/500)+','+Math.floor(row.p[2]/500);if(!cells.has(key))cells.set(key,[]);cells.get(key).push(row);}
 async function cell(key,rows){
  const group=new THREE.Group();group.name='World cell '+key;root.add(group);
  const byModel=new Map();for(const r of rows){if(!byModel.has(r.model))byModel.set(r.model,[]);byModel.get(r.model).push(r);}
  await Promise.all([...byModel].map(async([id,instances])=>{try{
   const source=await loadModel(id);const prefab=source.children[0].clone(true);prefab.position.set(0,0,0);prefab.updateMatrixWorld(true);
   const bound=new THREE.Box3().setFromObject(prefab);const items=[];prefab.traverse(m=>{if(m.isMesh&&!m.isSkinnedMesh)items.push(m);});
   for(const m of items){const geometry=m.geometry.clone();geometry.applyMatrix4(new THREE.Matrix4().makeScale(1,1,-1).multiply(m.matrixWorld));if(geometry.index){const a=geometry.index.array;for(let j=0;j<a.length;j+=3){const t=a[j+1];a[j+1]=a[j+2];a[j+2]=t;}}const batch=new THREE.InstancedMesh(geometry,instances[0].water?new THREE.MeshStandardMaterial({color:0x65b4c5,roughness:.3,metalness:.12}):m.material,instances.length);batch.castShadow=false;batch.receiveShadow=true;const transform=new THREE.Matrix4(),scale=new THREE.Matrix4().makeScale(16,16,16),translation=new THREE.Matrix4();
    instances.forEach((r,i)=>{const p=toWorld(r.p);translation.makeTranslation(p.x,p.y,p.z);transform.copy(translation).multiply(scale);batch.setMatrixAt(i,transform);});batch.instanceMatrix.needsUpdate=true;batch.computeBoundingSphere();group.add(batch);}
   for(const r of instances){const p=toWorld(r.p),box={x:p.x+(bound.min.x+bound.max.x)*8,z:p.z-(bound.min.z+bound.max.z)*8,w:(bound.max.x-bound.min.x)*16,d:(bound.max.z-bound.min.z)*16};
    if(r.floor&&!r.bounds)ground.push({...box,name:r.name});
    else if(/house|wall|fence|stone|rock|tree/i.test(r.name)&&!(/grass|flower|floor|shadow/i.test(r.name))){if(/tree/i.test(r.name)){box.w=Math.min(12,box.w*.2);box.d=Math.min(12,box.d*.2);}colliders.push({...box,name:r.name});}
   }
  }catch(e){errors.push({id,message:e.message});console.error('World model failed',id,e);}}));revision++;
 }
 return {root,data,canWalk,heightAt(x,z){const [sx,sz]=toSource(x,z),list=navCells.get(Math.floor(sx/10)+','+Math.floor(sz/10))||[];for(const poly of list){for(let i=1;i<poly.length-1;i++){const a=poly[0],b=poly[i],c=poly[i+1],den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1]);if(!den)continue;const u=((b[1]-c[1])*(sx-c[0])+(c[0]-b[0])*(sz-c[1]))/den,v=((c[1]-a[1])*(sx-c[0])+(a[0]-c[0])*(sz-c[1]))/den;if(u>=-.001&&v>=-.001&&u+v<=1.001)return ((a[2]||0)*u+(b[2]||0)*v+(c[2]||0)*(1-u-v))*16;}}return 0;},isWater(x,z){const [sx,sz]=toSource(x,z);return waterPolygons.some(poly=>{let inside=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j];if((a[1]>sz)!==(b[1]>sz)&&sx<(b[0]-a[0])*(sz-a[1])/(b[1]-a[1])+a[0])inside=!inside;}return inside;});},colliders,ground,errors,async update(x,z){const [sx,sz]=toSource(x,z),cx=Math.floor(sx/50),cz=Math.floor(sz/50),jobs=[];for(let dx=-1;dx<=1;dx++)for(let dz=-1;dz<=1;dz++){const key=(cx+dx)+','+(cz+dz),rows=cells.get(key);if(rows&&!loaded.has(key)){const job=cell(key,rows);loaded.set(key,job);jobs.push(job);}}await Promise.all(jobs);},status(){return {source:data.source,instances:data.objects.length,floors:data.floors.length,walkPolygons:polygons.length,cells:loaded.size,revision,errors:[...errors]};}};
}
