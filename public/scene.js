let facing=0,walkPhase=0,lastFrame=0,room='home',walkingUntil=0,swimming=false;
const keys=new Set();
const characterAtlas=new Image();characterAtlas.src='/assets/characters.png';
const buildingAtlas=new Image();buildingAtlas.src='/assets/buildings.png';
const npcAtlas=new Image();npcAtlas.src='/assets/npcs.png';
const starterArt={};for(const id of ['bulbasaur','charmander','squirtle']){const img=new Image();img.src=`/assets/pokemon/${id}.png`;starterArt[id]=img;}
const starterIds=['bulbasaur','charmander','squirtle'];
const buildings=[
 {x:135,y:220,w:190,h:190,name:'Home',kind:'home',art:0},
 {x:510,y:220,w:240,h:220,name:'Professor’s Lab',kind:'lab',art:1},
 {x:390,y:425,w:195,h:185,name:'Market',kind:'market',art:2},
 {x:790,y:220,w:160,h:185,name:'Gym · Lv.8',kind:'gym',art:3}
];
const townNpcs=[{x:635,y:342,index:0,name:'Lab Assistant',text:'The professor keeps three partners inside the lab. Open a Poké Ball to meet one.'},{x:725,y:480,index:2,name:'Route Trainer',text:'Tall grass is home to wild Pokémon. A wild encounter costs 5 energy, even if you retreat.'},{x:375,y:420,index:3,name:'Shopkeeper',text:'Welcome! The market will offer Poké Balls and supplies as the town grows.'}];
const rounded=(x,y,w,h,r,fill)=>{ctx.fillStyle=fill;ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fill();};
function shade(x,y,w,h){ctx.fillStyle='#17392735';ctx.beginPath();ctx.ellipse(x,y,w,h,0,0,Math.PI*2);ctx.fill();}
function label(text,x,y){ctx.font='bold 12px Arial';ctx.textAlign='center';ctx.lineWidth=3;ctx.strokeStyle='#24443b';ctx.strokeText(text,x,y);ctx.fillStyle='#fff';ctx.fillText(text,x,y);}
function house(b){shade(b.x+b.w/2,b.y-2,b.w*.36,12);if(buildingAtlas.complete&&buildingAtlas.naturalWidth){const cw=buildingAtlas.naturalWidth/4;const bounds=[[20,91,543,645],[0,51,537,635],[15,116,535,638],[8,50,531,661]][b.art];ctx.drawImage(buildingAtlas,b.art*cw+bounds[0],bounds[1],bounds[2]-bounds[0],bounds[3]-bounds[1],b.x,b.y-b.h,b.w,b.h);}label(b.name,b.x+b.w/2,b.y+18);}
function npc(x,y,index,name){shade(x,y+5,15,6);if(npcAtlas.complete&&npcAtlas.naturalWidth){const w=npcAtlas.naturalWidth/2,h=npcAtlas.naturalHeight/2;ctx.drawImage(npcAtlas,index%2*w,Math.floor(index/2)*h,w,h,x-35,y-82,70,88);}label(name,x,y+20);}
function person(x,y,color='#3a77bd',name='jehad'){
 const player=name==='jehad',riding=player&&swimming;
 if(riding){ctx.strokeStyle='#d1f9fbbb';ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(x,y+7,40+Math.sin(Date.now()/170)*3,12,0,0,Math.PI*2);ctx.stroke();const mount=starterArt.squirtle;if(mount.complete&&mount.naturalWidth)ctx.drawImage(mount,x-42,y-28,84,75);}else shade(x,y+6,16,6);
 if(characterAtlas.complete&&characterAtlas.naturalWidth){const row=name==='Mom'?4:name==='Professor'?5:facing;const walking=player&&Date.now()<walkingUntil;const col=walking?Math.floor(walkPhase)%4:1;const cw=characterAtlas.naturalWidth/4,ch=characterAtlas.naturalHeight/6;ctx.save();if(riding){ctx.beginPath();ctx.rect(x-38,y-93,76,65);ctx.clip();}ctx.drawImage(characterAtlas,col*cw,row*ch,cw,ch,x-38,y-81-(riding?12:0),76,88);ctx.restore();}
 label(name,x,player?y-86:y+20);
}
function tree(x,y,s=1){shade(x+10,y+12,28*s,11*s);rounded(x-5*s,y-37*s,10*s,42*s,3,'#8c6748');for(let j=0;j<3;j++){const yy=y-38*s-j*20*s,ww=(34-j*6)*s;ctx.fillStyle=['#306746','#39804e','#4a925b'][j];ctx.beginPath();ctx.moveTo(x,yy-40*s);ctx.lineTo(x-ww,yy+15*s);ctx.quadraticCurveTo(x,yy+25*s,x+ww,yy+15*s);ctx.closePath();ctx.fill();ctx.strokeStyle='#7ca96b50';ctx.stroke();}}
function grass(x,y,w,h){rounded(x,y,w,h,10,'#478646');for(let j=0;j<h;j+=17)for(let i=0;i<w;i+=14){let xx=x+i+((j*7+i*3)%7),yy=y+j;ctx.fillStyle=(i+j)%3?'#64a849':'#3b733c';ctx.beginPath();ctx.moveTo(xx,yy+17);ctx.quadraticCurveTo(xx-9,yy+4,xx-7,yy);ctx.lineTo(xx+3,yy+9);ctx.lineTo(xx+8,yy-4);ctx.quadraticCurveTo(xx+14,yy+9,xx+7,yy+17);ctx.fill();}}
function floor(){ctx.fillStyle='#88b975';ctx.fillRect(0,0,960,620);for(let i=0;i<700;i++){let x=i*73%960,y=i*137%620;ctx.fillStyle=i%3?'#c6d79660':'#59895140';ctx.fillRect(x,y,2+(i%3),2);}ctx.fillStyle='#b8b6a3';ctx.fillRect(60,235,840,80);ctx.fillRect(305,100,70,470);ctx.fillRect(680,200,70,390);ctx.strokeStyle='#8a97883a';for(let y=235;y<315;y+=20)for(let x=60;x<900;x+=35){ctx.strokeRect(x+(y%40?17:0),y,35,20);}for(let y=100;y<570;y+=25){ctx.strokeRect(305,y,35,25);ctx.strokeRect(340,y,35,25);}for(let y=200;y<590;y+=25){ctx.strokeRect(680,y,35,25);ctx.strokeRect(715,y,35,25);}rounded(35,385,180,170,25,'#648f9b');rounded(45,395,160,150,20,'#73b9c2');ctx.strokeStyle='#d3f3ed70';for(let i=0;i<14;i++){const x=65+i*29%130,y=408+i*37%125;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+17,y);ctx.stroke();}grass(400,475,230,120);grass(770,370,165,190);for(let i=0;i<12;i++){let x=400+i*19,y=355;ctx.fillStyle=i%2?'#f5dc73':'#e8808c';ctx.beginPath();ctx.arc(x,y,4,0,7);ctx.fill();}for(let i=0;i<12;i++){rounded(393+i*20,445,4,22,1,'#d1b48a');}rounded(393,450,230,4,1,'#ddc69e');}
function plant(x,y){rounded(x-12,y-4,24,25,4,'#ba7652');for(let i=0;i<5;i++){ctx.fillStyle=i%2?'#4c9966':'#79b56b';ctx.beginPath();ctx.ellipse(x+(i-2)*5,y-15-i%2*6,7,17,(i-2)*.3,0,Math.PI*2);ctx.fill();}}
function windowPanel(x,y){rounded(x-5,y-5,90,68,5,'#e6efe5');rounded(x,y,80,58,3,'#93cbd8');ctx.fillStyle='#ffffff66';ctx.fillRect(x+8,y+5,8,48);ctx.fillStyle='#eff6e9';ctx.fillRect(x+38,y,4,58);ctx.fillRect(x,y+27,80,4);rounded(x-10,y+59,100,9,3,'#c6d8ca');}
function shelf(x,y,w=115){rounded(x,y,w,85,4,'#8d684a');for(let r=0;r<2;r++){rounded(x+6,y+8+r*35,w-12,29,1,'#614e3b');for(let i=0;i<7;i++){ctx.fillStyle=['#78aaa5','#f0cd7c','#d78676','#c3c8b0'][i%4];ctx.fillRect(x+12+i*(w-20)/7,y+10+r*35,8,24);}ctx.fillStyle='#b98e69';ctx.fillRect(x+5,y+37+r*35,w-10,6);}}
function ball(x,y,hover=false){shade(x,y+18,15,5);ctx.lineWidth=2;ctx.strokeStyle='#274d50';ctx.fillStyle=hover?'#f28073':'#e95c50';ctx.beginPath();ctx.arc(x,y,14,Math.PI,0);ctx.fill();ctx.stroke();ctx.fillStyle='#fff8ec';ctx.beginPath();ctx.arc(x,y,14,0,Math.PI);ctx.fill();ctx.stroke();ctx.fillStyle='#354c52';ctx.fillRect(x-14,y-2,28,4);ctx.beginPath();ctx.arc(x,y,5,0,Math.PI*2);ctx.fill();ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(x,y,2,0,Math.PI*2);ctx.fill();}
function inside(){
 ctx.fillStyle='#132e30';ctx.fillRect(0,0,960,620);
 const colors={home:['#e9cbaa','#a9d0c7'],lab:['#dce8e3','#5c9f9e'],gym:['#e6e0ed','#7d719f'],market:['#ead7b3','#739f94']};const [floorColor,wallColor]=colors[room];
 rounded(175,85,610,475,12,'#849a8f');rounded(185,145,590,405,5,floorColor);
 ctx.save();ctx.beginPath();ctx.rect(185,145,590,405);ctx.clip();ctx.strokeStyle=room==='home'?'#b89b7850':'#829c9350';ctx.lineWidth=1;for(let y=150;y<550;y+=34)for(let x=185;x<775;x+=room==='home'?85:42)ctx.strokeRect(x,y,room==='home'?85:42,34);
 ctx.restore();rounded(175,60,610,90,6,wallColor);rounded(180,145,600,10,2,'#f0eee0');windowPanel(220,80);windowPanel(660,80);
 ctx.fillStyle='#294f50';ctx.font='bold 19px Arial';ctx.textAlign='center';ctx.fillText({home:'Home',lab:'Professor’s Lab',gym:'Pallet Gym',market:'Village Market'}[room],480,99);
 if(room==='home'){
  rounded(222,195,120,135,7,'#8e6b4e');rounded(228,200,108,125,7,'#f3e9d8');rounded(228,242,108,84,4,'#659c9b');rounded(238,210,88,28,6,'#fff7e4');rounded(420,335,160,90,12,'#da8e73');rounded(430,345,140,70,8,'#edb2a0');rounded(450,235,110,65,8,'#976d4d');rounded(455,235,100,8,3,'#c89970');shelf(615,175);plant(245,465);plant(700,455);person(630,355,'#b47ca0','Mom');
 }else if(room==='lab'){
  shelf(210,175,100);shelf(650,175,100);rounded(335,255,290,85,8,'#8c9f96');rounded(328,244,304,74,8,'#f1ecd9');rounded(340,257,280,8,3,'#d3c6a0');for(let i=0;i<3;i++)ball(395+i*85,280);person(480,216,'#f0f0e4','Professor');npc(685,390,0,'Lab Assistant');plant(230,415);plant(720,490);
 }else if(room==='gym'){
  rounded(335,280,290,185,10,'#aa9cbb');ctx.strokeStyle='#eee6fc';ctx.lineWidth=3;ctx.strokeRect(345,290,270,165);ctx.beginPath();ctx.arc(480,373,45,0,Math.PI*2);ctx.stroke();ctx.beginPath();ctx.moveTo(345,373);ctx.lineTo(615,373);ctx.stroke();npc(480,242,1,'Gym Leader');npc(685,415,2,'Gym Guide');plant(245,265);plant(715,265);label('Talk to the Gym Leader to challenge',480,490);
 }else{
  shelf(210,180,120);shelf(630,180,120);rounded(350,280,260,70,8,'#b48559');rounded(340,275,280,18,5,'#edd0a2');npc(480,255,3,'Shopkeeper');plant(250,460);plant(710,460);
 }
 rounded(445,516,70,34,4,'#607e76');label('EXIT',480,539);person(pos.x,pos.y);
}
function drawTown(){floor();for(let i=0;i<13;i++){tree(30+i*75,75,.85);tree(22+i*78,610,.9);}const objects=buildings.map(b=>({y:b.y,draw:()=>house(b)}));for(let i=0;i<7;i++)objects.push({y:340+i*35,draw:()=>tree(245,340+i*35,.85)});for(const n of townNpcs)objects.push({y:n.y,draw:()=>npc(n.x,n.y,n.index,n.name)});objects.push({y:pos.y,draw:()=>person(pos.x,pos.y)});objects.sort((a,b)=>a.y-b.y).forEach(o=>o.draw());}
draw=function(){if(room==='town')drawTown();else inside();$('location').textContent=room==='town'?(swimming?'Pallet Town · Swimming':'Pallet Town · Route 1'):{home:'Home',lab:'Professor’s Lab · Click a Poké Ball',gym:'Pallet Gym · Talk to the leader',market:'Village Market'}[room];};
function isWater(x,y){return x>45&&x<205&&y>395&&y<545;}
function hasSwimPartner(){return state?.team?.some(p=>(p.types||[p.type]).includes('water')&&(p.learnedMoves||[]).includes('Swim'))||false;}
function canEnterWater(){return hasSwimPartner()||$('water-test').checked;}
let waterNoticeAt=0;
step=function(dx,dy){if(state?.battle||uiBlocked())return;const nx=Math.max(room==='town'?25:205,Math.min(room==='town'?935:755,pos.x+dx)),ny=Math.max(room==='town'?100:170,Math.min(room==='town'?585:535,pos.y+dy));if(room==='town'){
 if(buildings.some(b=>nx>b.x+20&&nx<b.x+b.w-20&&ny>b.y-b.h*.47&&ny<b.y-18))return;
 if(isWater(nx,ny)&&!canEnterWater()){if(Date.now()-waterNoticeAt>2500){waterNoticeAt=Date.now();toast('You need a Water-type Pokémon that knows Swim.');}return;}
 swimming=isWater(nx,ny);
 }else swimming=false;pos={x:nx,y:ny};walkingUntil=Date.now()+170;};
function returnToRecovery(){room='home';swimming=false;pos={x:480,y:440};}
function enterBuilding(kind){room=kind;swimming=false;pos={x:480,y:460};keys.clear();draw();}
function leaveBuilding(){const b=buildings.find(b=>b.kind===room);room='town';pos={x:b.x+b.w/2,y:b.y+45};swimming=false;draw();}
function talkToProfessor(){const actions=[];if(state?.team?.some(p=>(p.types||[p.type]).includes('water'))&&state.badges)actions.push({label:'Teach Swim',run:()=>act({action:'learnSwim'})});conversation('Professor',state?'Take good care of your partner. After earning the first badge, I can teach a Water-type partner Swim.':'There are three Poké Balls on the table. Inspect one and choose the partner you want.',actions);}
function talkToLeader(){if(!state)return conversation('Gym Leader','Choose a partner at the laboratory before challenging me.');conversation('Gym Leader',state.badges?'You already earned my badge. Keep training for your next journey.':'Welcome to Pallet Gym. My Pokémon is level 8. Are you ready to challenge me?',state.badges?[]:[{label:'Challenge',run:()=>act({action:'encounter',kind:'boss'})},{label:'Not yet',run:()=>{}}]);}
encounter=function(){if(state?.battle||uiBlocked())return;if(room!=='town'){
 if(pos.y>480)return leaveBuilding();
 if(room==='lab'){if(Math.hypot(pos.x-480,pos.y-216)<95)return talkToProfessor();if(pos.y<435&&Math.abs(pos.x-480)<210&&!state?.team?.length){const i=Math.max(0,Math.min(2,Math.round((pos.x-395)/85)));return previewStarter(starterIds[i]);}if(Math.hypot(pos.x-685,pos.y-390)<95)return conversation('Lab Assistant','I can help your partner learn compatible moves.',state?[{label:'Move Tutor',run:()=>openTutor()}]:[]);return toast('Walk toward the table or the professor.');}
 if(room==='gym'){if(Math.hypot(pos.x-480,pos.y-242)<105)return talkToLeader();if(Math.hypot(pos.x-685,pos.y-415)<95)return conversation('Gym Guide','Speak to the leader at the far end of the room. Trainers take 10 energy only when you win.');return toast('Walk toward the Gym Leader.');}
 if(room==='market')return conversation('Shopkeeper','Training supplies, EV-reducing berries, and Poké Balls are available here.',[{label:'Shop',run:openShop},{label:'Move Tutor',run:()=>openTutor()}]);if(room==='home')return conversation('Mom','Have fun exploring. Walk to the door at the bottom of the room to leave.');
 }
 const near=buildings.find(b=>Math.abs(pos.x-(b.x+b.w/2))<58&&pos.y>b.y-18&&pos.y<b.y+65);if(near)return enterBuilding(near.kind);
 const n=townNpcs.find(n=>Math.hypot(pos.x-n.x,pos.y-n.y)<90);if(n)return conversation(n.name,n.text);
 if(!state)return toast('Choose a partner at the lab first.');if((pos.x>400&&pos.x<630&&pos.y>475)||(pos.x>770&&pos.y>370))return act({action:'encounter',kind:'wild',zone:pos.x>770?'forest':'route1'});toast('Approach a door or a person, or enter tall grass.');
};
cv.addEventListener('click',event=>{if(state?.battle||uiBlocked())return;const rect=cv.getBoundingClientRect();const x=(event.clientX-rect.left)*960/rect.width,y=(event.clientY-rect.top)*620/rect.height;if(room==='lab'&&y>253&&y<312){const i=starterIds.findIndex((id,i)=>Math.abs(x-(395+i*85))<28);if(i>=0){if(Math.hypot(pos.x-x,pos.y-300)>165)return toast('Walk closer to the Poké Balls.');return previewStarter(starterIds[i]);}}const npcs=room==='town'?townNpcs:room==='gym'?[{x:480,y:242,name:'Gym Leader'}]:room==='lab'?[{x:480,y:216,name:'Professor'}]:[];const target=npcs.find(n=>Math.abs(x-n.x)<35&&y<n.y+10&&y>n.y-80);if(target){if(Math.hypot(pos.x-target.x,pos.y-target.y)>110)return toast('Walk closer to talk.');if(target.name==='Gym Leader')return talkToLeader();if(target.name==='Professor')return talkToProfessor();conversation(target.name,target.text);}});
const directions={ArrowDown:[0,1,0],ArrowLeft:[-1,0,1],ArrowRight:[1,0,2],ArrowUp:[0,-1,3]};
document.addEventListener('keydown',e=>{if(e.target.matches('input,textarea')||uiBlocked())return;if(directions[e.key]){e.preventDefault();keys.add(e.key);}if((e.key==='Enter'||e.key.toLowerCase()==='e')&&!e.repeat)encounter();});document.addEventListener('keyup',e=>keys.delete(e.key));window.addEventListener('blur',()=>keys.clear());
for(const button of document.querySelectorAll('[data-direction]')){const key={up:'ArrowUp',down:'ArrowDown',left:'ArrowLeft',right:'ArrowRight'}[button.dataset.direction];button.addEventListener('pointerdown',e=>{e.preventDefault();button.setPointerCapture(e.pointerId);keys.add(key);});for(const event of ['pointerup','pointercancel','lostpointercapture'])button.addEventListener(event,()=>keys.delete(key));}
function frame(now){const dt=Math.min((now-lastFrame)/1000,.04);lastFrame=now;if(!state?.battle&&!uiBlocked()){let dx=0,dy=0;for(const key of keys){const d=directions[key];if(d){dx+=d[0];dy+=d[1];facing=d[2];}}if(dx||dy){const length=Math.hypot(dx,dy);step(dx/length*145*dt,dy/length*145*dt);walkPhase+=dt*8;}}if(!state?.battle)draw();requestAnimationFrame(frame);}
$('starter').style.display='none';pos={x:480,y:440};draw();requestAnimationFrame(frame);
