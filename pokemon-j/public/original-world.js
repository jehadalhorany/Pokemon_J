import * as THREE from './vendor/three.module.js';
import {loadModel} from './asset-runtime.js';
export const SCALE=16;
export const point=p=>({x:p[0]*1.6,y:(p[1]||0)*1.6,z:-p[2]*1.6});
export const source=(x,z)=>[x/16,-z/16];
export const original=await fetch('/data/original/config.json').then(r=>r.json());
export const areaById=new Map(original.areas.map(a=>[a.Id,a]));
export const npcById=new Map(original.npcs.map(a=>[a.Id,a]));
const cache=new Map(),geometryCache=new Map();
export async function mapData(id){if(!cache.has(id))cache.set(id,fetch('/data/original/'+id+'.json').then(r=>{if(!r.ok)throw Error('Original scene '+id+' is unavailable');return r.json();}));return cache.get(id);}
function contains(poly,x,z){let yes=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j];if((a[1]>z)!==(b[1]>z)&&x<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0])yes=!yes;}return yes;}
function indexPolygons(polys){const cells=new Map();for(const poly of polys){const xs=poly.map(p=>p[0]),zs=poly.map(p=>p[1]);for(let x=Math.floor(Math.min(...xs)/8);x<=Math.floor(Math.max(...xs)/8);x++)for(let z=Math.floor(Math.min(...zs)/8);z<=Math.floor(Math.max(...zs)/8);z++){const k=x+','+z;if(!cells.has(k))cells.set(k,[]);cells.get(k).push(poly);}}return cells;}
function height(poly,x,z){for(let i=1;i<poly.length-1;i++){const a=poly[0],b=poly[i],c=poly[i+1],den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1]);if(!den)continue;const u=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(z-c[1]))/den,v=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(z-c[1]))/den;if(u>=-.001&&v>=-.001&&u+v<=1.001)return ((a[2]||0)*u+(b[2]||0)*v+(c[2]||0)*(1-u-v))*SCALE;}return 0;}
export class OriginalWorld{
 constructor(data){this.data=data;this.root=new THREE.Group();this.root.name='Original scene '+data.id;this.loaded=new Map();this.errors=[];this.walkPolygons=data.walk.map(poly=>poly.map(([x,z,y])=>[-x,z,y]));this.waterPolygons=data.water.map(poly=>poly.map(([x,z,y])=>[-x,z,y]));this.walk=indexPolygons(this.walkPolygons);this.water=indexPolygons(this.waterPolygons);this.cells=new Map();this.navPoints=new Map((data.entities['11']||[]).map(n=>[n.id,n]));this.regions=data.entities['8']||[];
  for(const row of data.objects){if(/yun|cloud/i.test(row.name))continue;const key=Math.floor(row.p[0]/400)+','+Math.floor(row.p[2]/400);if(!this.cells.has(key))this.cells.set(key,[]);this.cells.get(key).push(row);}
  this.npcs=(data.entities['2']||[]).map(info=>({info,config:npcById.get(info.id)})).filter(n=>n.config);
  this.portals=this.npcs.filter(n=>n.config.BirthId&&original.spawns[String(n.config.BirthId)]).map(n=>({...n,target:original.spawns[String(n.config.BirthId)]}));
  this.tiles=new Map();for(const group of ['3','4','5'])for(const tile of data.entities[group]||[]){const k=Math.floor(tile.p[0]/10)+','+Math.floor(tile.p[2]/10);if(!this.tiles.has(k))this.tiles.set(k,[]);this.tiles.get(k).push({...tile,group});}
  // Water navigation is for movement checks; only source scene models render water.
  // Rendering a second flat navmesh surface produced a blue stripe over the world.
 }
 polygonsAt(x,z,water=false){const [sx,sz]=source(x,z);return ((water?this.water:this.walk).get(Math.floor(sx/8)+','+Math.floor(sz/8))||[]).filter(p=>contains(p,sx,sz));}
 canWalk(x,z){return !!this.polygonsAt(x,z).length;}
 isWater(x,z){return !this.canWalk(x,z)&&!!this.polygonsAt(x,z,true).length;}
 heightAt(x,z,water=false){const [sx,sz]=source(x,z);const poly=this.polygonsAt(x,z,water)[0];return poly?height(poly,sx,sz):0;}
 tilesAt(x,z){const [sx,sz]=source(x,z);return this.tiles.get(Math.floor(sx)+','+Math.floor(sz))||[];}
 monsterAt(x,z){return this.tilesAt(x,z).find(t=>t.group==='5');}
 areaAt(x,z,preferred=0){const [sx,sz]=source(x,z);const choices=this.regions.filter(a=>Math.abs(sx-a.p[0]/10)<=a.size[0]/2+.15&&Math.abs(sz-a.p[2]/10)<=a.size[2]/2+.15);return choices.find(a=>a.id===preferred)||choices.find(a=>areaById.get(a.id)?.Gen===areaById.get(preferred)?.Gen)||choices[0];}
 nearestWalkable(x,z,max=80){if(this.canWalk(x,z))return {x,z};let best=null,distance=Infinity;for(let dz=-max;dz<=max;dz+=3)for(let dx=-max;dx<=max;dx+=3){const d=dx*dx+dz*dz;if(d<distance&&this.canWalk(x+dx,z+dz)){best={x:x+dx,z:z+dz};distance=d;}}return best;}
 jumpNear(x,z,dx,dz){
  // Source TileType71..74 and MoveHelper.JumpToAsync/IsNeedJump.
  const length=Math.hypot(dx,dz);if(!length)return null;
  const dirs={71:[0,1],72:[0,-1],73:[1,0],74:[-1,0]};
  for(const t of [...this.tilesAt(x,z),...this.tilesAt(x+dx,z+dz)]){
   const d=t.group==='3'&&dirs[t.type];if(!d||(dx*d[0]+dz*d[1])/length<.5)continue;
   const p=point(t.p);if(Math.hypot(x-p.x,z-p.z)>SCALE*1.1)continue;
   for(let i=1;i<=6;i++){const to={x:x+d[0]*1.2*SCALE*i,z:z+d[1]*1.2*SCALE*i};if(this.canWalk(to.x,to.z))return {from:{x,z},to,node:t,source:'TileWatcher_Transfer'};}
  }
  const [sx,sz]=source(x,z);let best=null,near=Infinity;for(const node of this.navPoints.values()){if(node.type!==82)continue;const p=point(node.p),d=Math.hypot(p.x-x,p.z-z);if(d>23||d>=near)continue;for(const id of node.links){const end=this.navPoints.get(id);if(!end)continue;const q=point(end.p),dot=dx*(q.x-p.x)+dz*(q.z-p.z);if(dot<=0)continue;near=d;best={from:p,to:q,node};}}return best;}
 async update(x,z,radius=1){const [sx,sz]=source(x,z),cx=Math.floor(sx/40),cz=Math.floor(sz/40),jobs=[];for(let dx=-radius;dx<=radius;dx++)for(let dz=-radius;dz<=radius;dz++){const key=(cx+dx)+','+(cz+dz),rows=this.cells.get(key);if(rows&&!this.loaded.has(key)){const job=this.loadCell(key,rows);this.loaded.set(key,job);jobs.push(job);}}await Promise.all(jobs);}
 async loadAll(){await Promise.all([...this.cells].map(([key,rows])=>{if(!this.loaded.has(key))this.loaded.set(key,this.loadCell(key,rows));return this.loaded.get(key);}));}
 async loadCell(key,rows){const cell=new THREE.Group();cell.name='Original cell '+key;this.root.add(cell);const groups=new Map();for(const r of rows){if(!groups.has(r.model))groups.set(r.model,[]);groups.get(r.model).push(r);}await Promise.all([...groups].map(async([id,list])=>{try{
   if(!geometryCache.has(id))geometryCache.set(id,loadModel(id).then(template=>{const prefab=template.children[0].clone(true);prefab.position.set(0,0,0);prefab.updateMatrixWorld(true);const meshes=[];prefab.traverse(node=>{if(!node.isMesh)return;const geo=node.geometry.clone();geo.applyMatrix4(new THREE.Matrix4().makeScale(1,1,-1).multiply(node.matrixWorld));if(geo.index){const a=geo.index.array;for(let i=0;i<a.length;i+=3){const v=a[i+1];a[i+1]=a[i+2];a[i+2]=v;}}meshes.push({geometry:geo,material:node.material,name:node.name});});return meshes;}));
   const meshes=await geometryCache.get(id);for(const m of meshes){const batch=new THREE.InstancedMesh(m.geometry,m.material,list.length),matrix=new THREE.Matrix4(),p=new THREE.Vector3(),q=new THREE.Quaternion(),s=new THREE.Vector3();list.forEach((r,i)=>{const v=point(r.p);p.set(v.x,v.y,v.z);q.setFromEuler(new THREE.Euler((r.r?.[0]||0)*Math.PI/1800,-(r.r?.[1]||0)*Math.PI/1800,-(r.r?.[2]||0)*Math.PI/1800));s.set(SCALE,SCALE,SCALE);matrix.compose(p,q,s);batch.setMatrixAt(i,matrix);});batch.instanceMatrix.needsUpdate=true;batch.computeBoundingSphere();batch.name=m.name;cell.add(batch);}
  }catch(e){this.errors.push({id,error:e.message});console.error('Original asset',id,e);}}));}
 dispose(){this.root.traverse(o=>{if(o.isInstancedMesh)o.dispose();});this.root.parent?.remove(this.root);}
 status(){return {source:'Original configurations',scene:this.data.id,objects:this.data.objects.length,cells:this.loaded.size,navigation:this.data.walk.length,portals:this.portals.length,errors:this.errors};}
}
