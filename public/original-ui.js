import {original} from './original-world.js';
const icons=await fetch('/data/original/ui.json').then(r=>r.json());
const functions=new Map(original.functions.map(f=>[f.Id,f]));
function icon(key){return icons[key]?.url||'';}
const handlers={201:()=>openOriginalTeam(),103:()=>openOriginalBag(),202:()=>openDex(),802:()=>openMissions()};
const toolbar=document.getElementById('native-toolbar');toolbar.innerHTML=[201,103,202,802].map(id=>{const f=functions.get(id);return `<button class="native-function" data-original-function="${id}" title="${escapeHtml(f.name)}"><img src="${icon('Main/'+f.Icon)}" alt=""><span>${escapeHtml(f.name)}</span></button>`;}).join('');toolbar.addEventListener('click',e=>{const button=e.target.closest('[data-original-function]');if(button)handlers[button.dataset.originalFunction]?.();});
function openOriginalTeam(){if(!state)return;openActivity(functions.get(201).name);document.getElementById('activity-body').innerHTML='<div class="native-team-grid">'+document.getElementById('team').innerHTML+'</div>';}
function openOriginalBag(){if(!state)return;openActivity(functions.get(103).name);document.getElementById('activity-body').innerHTML='<div class="native-team-grid">'+Object.entries(state.inventory||{}).filter(([,n])=>n>0).map(([id,n])=>`<div class="card"><h3>${escapeHtml(id.replaceAll('-',' '))}</h3><p>${n}</p></div>`).join('')+'</div>';}
Object.assign(window,{openOriginalTeam,openOriginalBag});
function refresh(){if(!state)return;document.getElementById('native-trainer').textContent=state.name+' · Lv.'+state.level;document.getElementById('native-currency').textContent='Energy '+state.energy+'/300 · '+state.coins+' Gold · '+state.gems+' Gems';}
const previous=window.originalHudRefresh;window.originalHudRefresh=()=>{previous?.();refresh();};setInterval(refresh,1000);refresh();
const joystick=document.getElementById('native-joystick');let pointer=null;
function move(e){if(pointer!==e.pointerId)return;const rect=joystick.getBoundingClientRect(),x=e.clientX-rect.left-rect.width/2,y=e.clientY-rect.top-rect.height/2;window.keys?.clear();if(Math.abs(x)>12)window.keys?.add(x>0?'ArrowRight':'ArrowLeft');if(Math.abs(y)>12)window.keys?.add(y>0?'ArrowDown':'ArrowUp');}
joystick.addEventListener('pointerdown',e=>{pointer=e.pointerId;joystick.setPointerCapture(pointer);move(e);});joystick.addEventListener('pointermove',move);for(const event of ['pointerup','pointercancel','lostpointercapture'])joystick.addEventListener(event,()=>{pointer=null;window.keys?.clear();});
