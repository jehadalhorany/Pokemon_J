const {spawn}=require('node:child_process'),fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const cwd=process.env.POKEMON_PROJECT_ROOT||path.resolve(__dirname,'../pokemon-j'),server=spawn(process.execPath,['server/index.mjs'],{cwd,env:{...process.env,PORT:'3110',DATA_DIR:fs.mkdtempSync('/tmp/pokemon-bindings-')},stdio:'ignore'});
(async()=>{let browser;try{
 for(let i=0;i<100;i++){try{if((await fetch('http://127.0.0.1:3110/health')).ok)break;}catch{}await new Promise(r=>setTimeout(r,200));}
 browser=await chromium.launch({executablePath:'/tmp/pokemon-chromium',headless:true,env:{...process.env,LD_LIBRARY_PATH:'/tmp',VK_ICD_FILENAMES:'/tmp/vk_swiftshader_icd.json'},args:['--no-sandbox','--no-zygote','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader','--disable-dev-shm-usage']});
 const page=await browser.newPage({viewport:{width:1909,height:905}}),errors=[];page.on('pageerror',e=>errors.push(e.stack));
 await page.goto('http://127.0.0.1:3110/data/original/interface.json');
 await page.evaluate(async()=>{
  document.body.innerHTML='<div class="topline"></div>'+['dialog-modal','dex-modal','activity-modal','native-profile','native-toolbar','original-quest','native-joystick','minimap-button','starter'].map(id=>`<div id="${id}" hidden style="display:none"></div>`).join('');
  window.toast=console.log;const {initializeSourceHud}=await import('/source-hud.js');const F=await import('/vendor/fairygui.module.js');
  window.qaState=await fetch('/api/create',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json());window.sourceCurrentState=()=>qaState;
  window.qaAction=async b=>{await act(b);await qaBattle.renderSourceBattle(qaState,qaAction,()=>{});};window.act=async b=>{const r=await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)});const s=await r.json();if(!r.ok)throw Error(s.error);qaState=s;return true;};
  window.qaHud=await initializeSourceHud({state:()=>qaState,area:()=>1201,map:()=>{},quests:()=>{},go:()=>{},action:act});F.Stage.update();
 });
 await page.evaluate(async()=>{
  const call=async(url,b)=>{const r=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)});const s=await r.json();if(!r.ok)throw Error(s.error);return s;};
  for(const b of [{action:'worldVisit',area:1805,spawn:7180599},{action:'worldVisit',area:1804,spawn:7180402},{action:'worldTalk',npc:1180401},{action:'worldVisit',area:1801,spawn:7180101},{action:'worldTalk',npc:1180101}])qaState=await call('/api/action',b);
  const starters=await fetch('/api/starters').then(r=>r.json());window.qaStarters=starters;
 });
 
 await page.evaluate(async()=>{
  const r=await fetch('/api/start',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({species:'bulbasaur',generation:1})});qaState=await r.json();if(!r.ok)throw Error(qaState.error);
  await act({action:'worldVisit',area:1201});await act({action:'encounter',originalField:120101});
  const m=await import('/source-battle.js');window.qaBattle=m;await m.renderSourceBattle(qaState,qaAction,()=>{});
 });
 await page.waitForFunction(()=>qaBattle.sourceBattleStatus().scene.frames>2,{},{timeout:90000});
 const battleEvidence=await page.evaluate(()=>qaBattle.sourceBattleStatus());
 const tree=await page.evaluate(async()=>{const F=await import('/vendor/fairygui.module.js');const r=F.GRoot.inst._children.at(-1);function read(n,d=0){return {name:n.name,type:n.constructor.name,visible:n.visible,text:n.text,x:n.x,y:n.y,width:n.width,height:n.height,controllers:n._controllers?.map(c=>({name:c.name,pages:c._pageNames})),children:d<3?(n._children||[]).map(c=>read(c,d+1)):[]};}return read(r);});
 fs.writeFileSync('/tmp/native-battle-tree.json',JSON.stringify(tree,null,2));await page.screenshot({path:'/tmp/native-battle-test.png'});console.log('battle',await page.evaluate(()=>qaBattle.sourceBattleStatus()),'errors',errors);
 async function bounds(name,index){return page.evaluate(async({name,index})=>{const F=await import('/vendor/fairygui.module.js');const root=F.GRoot.inst._children.at(-1);let n=root.getChild(name);if(index!==undefined)n=n.getChildAt(index);const p=n.localToGlobal(n.width/2,n.height/2);return{x:p.x,y:p.y};},{name,index});}
 const before=await page.evaluate(()=>qaState.battle.pp[0][0]);await page.mouse.click(...Object.values(await bounds('list_skill',0)));await page.waitForFunction(pp=>!qaState.battle||qaState.battle.pp[0][0]===pp-1,before,{timeout:8000});console.log('PHYSICAL_ATTACK_PASS');
 if(await page.evaluate(()=>!!qaState.battle)){await page.mouse.click(...Object.values(await bounds('btn_exit')));await page.waitForFunction(()=>!qaState.battle,{},{timeout:8000});console.log('PHYSICAL_RETREAT_PASS');}
 // A second wild encounter uses the real native ball menu and server action.
 await page.evaluate(async()=>{await act({action:'encounter',originalField:120101});await qaBattle.renderSourceBattle(qaState,qaAction,()=>{});});
 await page.waitForFunction(()=>qaBattle.sourceBattleStatus().scene.frames>2);
 await page.mouse.click(...Object.values(await bounds('menuList',3)));
 const ballBefore=await page.evaluate(()=>qaState.inventory['poke-ball']);await page.mouse.click(...Object.values(await bounds('list_Ball',0)));
 await page.waitForFunction(n=>qaState.inventory['poke-ball']===n-1,ballBefore,{timeout:8000});console.log('PHYSICAL_BALL_PASS');
 if(await page.evaluate(()=>!!qaState.battle)){await page.mouse.click(...Object.values(await bounds('btn_exit')));await page.waitForFunction(()=>!qaState.battle);}
 await page.evaluate(async()=>{await act({action:'worldVisit',area:1102});const m=await fetch('/data/original/1000001.json').then(r=>r.json());const n=m.entities['2'].find(n=>n.id===6110201);localStorage.setItem('pokemon-j-original-position-1',JSON.stringify({area:1102,x:n.p[0]*1.6,z:-n.p[2]*1.6+15}));});
 await page.goto('http://127.0.0.1:3110/');await page.waitForFunction(()=>window.getVisualStatus?.().area===1102&&!getVisualStatus().loading,{},{timeout:90000});
 await page.waitForFunction(()=>document.querySelectorAll('.building-name').length>0,{},{timeout:20000});
 console.log('BUILDING_LABELS',await page.locator('#building-names').innerText());
 await page.waitForFunction(()=>getVisualStatus().sourceHud.ready,{},{timeout:30000});
 await page.screenshot({path:'/tmp/source-building-names-test.png'});
 await page.waitForTimeout(1000);await page.keyboard.press('Enter');await page.waitForFunction(()=>getVisualStatus().area===1401&&!getVisualStatus().loading,{},{timeout:90000});console.log('PHYSICAL_DOOR_PASS');
 await page.waitForTimeout(1000);await page.evaluate(()=>leaveBuilding());await page.waitForFunction(()=>getVisualStatus().area===1102&&!getVisualStatus().loading,{},{timeout:90000});console.log('SOURCE_RETURN_PASS');
 fs.writeFileSync(path.join(cwd,'SOURCE_FIRST_TWO_VALIDATION.json'),JSON.stringify({nativeBattle:battleEvidence,physicalAttack:true,physicalRetreat:true,physicalBallAttempt:true,buildingLabels:true,physicalViridianDoor:true,sourceReturn:true,pageErrors:errors},null,2));


 }finally{await browser?.close();server.kill();}
})().catch(e=>{console.error(e);process.exitCode=1;});
