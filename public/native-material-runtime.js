import {ShaderChunk} from './vendor/three.module.js';
// Texture-coordinate math from uploaded PokemonBase shader bytecode.
// Only the explicitly recovered PokemonDate/PokemonEye material records apply.
export function bindNativeMaterials(scene,records){if(!records)return;scene.traverse(node=>{if(!node.isMesh)return;for(const material of [].concat(node.material)){const r=records[material.name];if(!r||!material.map)continue;const num=x=>Number.isFinite(x)?Number(x).toFixed(9):'0.0';const signature=JSON.stringify(r);material.onBeforeCompile=shader=>{const sample='vec4 sampledDiffuseColor = texture2D( map, vMapUv );';if(!ShaderChunk.map_fragment.includes(sample))throw Error('Native material sample binding unavailable');const code=`
vec2 nativeUv = vec2(vMapUv.x, 1.0-vMapUv.y);
nativeUv = nativeUv*vec2(${r.scale.map(num)})+vec2(${r.offset.map(num)});
${r.doubleTex!==0?'':`float nativeFlip = sin(nativeUv.x*6.28318548)<=0.0?1.0:0.0;
${r.needMoveUV!==0?'nativeFlip=1.0-nativeFlip;':''}
nativeUv.x=2.0-2.0*nativeUv.x+${r.flipMask!==0?'0.0':'0.5'}+nativeFlip*(4.0*nativeUv.x-2.0);`}
nativeUv.y=1.0-nativeUv.y;
vec4 sampledDiffuseColor=texture2D(map,nativeUv);`;
shader.fragmentShader=shader.fragmentShader.replace('#include <map_fragment>',ShaderChunk.map_fragment.replace(sample,code));};material.customProgramCacheKey=()=>signature;material.userData.nativeSource=r;material.needsUpdate=true;}});}
