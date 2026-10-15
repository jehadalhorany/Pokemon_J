import fs from 'node:fs';import {gunzipSync} from 'node:zlib';import * as THREE from '../pokemon-j/public/vendor/three.module.js';
const root=new URL('../pokemon-j/public/',import.meta.url),read=p=>JSON.parse(gunzipSync(fs.readFileSync(new URL(p+'.gz',root))));globalThis.fetch=async p=>({json:async()=>read(p.replace(/^\//,''))});globalThis.THREE=THREE;
const code=fs.readFileSync(new URL('original-world.js',root),'utf8').replace(/^import .*\n/gm,'');const {OriginalWorld,original,point}=await import('data:text/javascript;base64,'+Buffer.from(code).toString('base64'));
let worlds=0,portals=0,unresolved=0,near=0,sourceSceneConflicts=[],missingModels=new Set(),failures=[];
for(const id of Object.keys(original.maps)){
 const data=read('data/original/'+id+'.json'),w=new OriginalWorld(data);worlds++;
 for(const obj of data.objects)if(!fs.existsSync(new URL('assets/imported/models/'+obj.model+'.glb.gz',root)))missingModels.add(obj.model);
 for(const p of w.portals){portals++;const dest=original.areas.find(a=>a.Id===p.target.area);if(dest&&dest.Scene!==p.target.scene)sourceSceneConflicts.push({scene:id,portal:p.info.id,areaScene:dest.Scene,spawnScene:p.target.scene});if(!dest||!original.maps[String(p.target.scene)]){unresolved++;failures.push({scene:id,portal:p.info.id});}const v=point(p.info.p);if(w.nearestWalkable(v.x,v.z,32))near++;}
}
const result={worlds,portals,unresolved,portalsNearWalk:near,missingModels:[...missingModels],sourceSceneConflicts,failures};fs.writeFileSync(new URL('original-navigation-results.json',import.meta.url),JSON.stringify(result,null,2));console.log(result);
