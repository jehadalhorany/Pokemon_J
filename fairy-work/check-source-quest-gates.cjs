const {spawn}=require('node:child_process'),fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const cwd=process.env.POKEMON_PROJECT_ROOT||path.resolve(__dirname,'../active-project'),server=spawn(process.execPath,['server/index.mjs'],{cwd,env:{...process.env,PORT:'3114',DATA_DIR:fs.mkdtempSync('/tmp/pokemon-bindings-')},stdio:'ignore'});
(async()=>{let browser;try{
 for(let i=0;i<100;i++){try{if((await fetch('http://127.0.0.1:3114/health')).ok)break;}catch{}await new Promise(r=>setTimeout(r,200));}
 browser=await chromium.launch({executablePath:'/tmp/pokemon-chromium',headless:true,env:{...process.env,LD_LIBRARY_PATH:'/tmp',VK_ICD_FILENAMES:'/tmp/vk_swiftshader_icd.json'},args:['--no-sandbox','--no-zygote','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader','--disable-dev-shm-usage']});
 const page=await browser.newPage({viewport:{width:1909,height:905}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:3114/data/original/interface.json');
 await page.evaluate(async()=>{
  document.body.innerHTML='<div class="topline"></div>'+['dialog-modal','dex-modal','activity-modal','native-profile','native-toolbar','original-quest','native-joystick','minimap-button','starter'].map(id=>`<div id="${id}" hidden style="display:none"></div>`).join('');
  window.toast=console.log;const {initializeSourceHud}=await import('/source-hud.js');const F=await import('/vendor/fairygui.module.js');
  window.qaState=await fetch('/api/create',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json());window.sourceCurrentState=()=>qaState;
  window.act=async b=>{const r=await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)});const s=await r.json();if(!r.ok)throw Error(s.error);qaState=s;return true;};
  window.qaHud=await initializeSourceHud({state:()=>qaState,area:()=>1201,map:()=>{},quests:()=>{},go:()=>{},action:act});F.Stage.update();
 });
 await page.evaluate(async()=>{window.qaToasts=[];window.toast=m=>qaToasts.push(m);const {openSourceQuests}=await import('/source-quests.js');await openSourceQuests(qaState,()=>{});});const results=[];for(let index=0;index<4;index++){const bounds=await page.evaluate(async i=>{const F=await import('/vendor/fairygui.module.js'),{sourceControlBounds}=await import('/source-widgets.js');return sourceControlBounds(F.GRoot.inst._children.at(-1).getChild('list_tab').getChildAt(i));},index);await page.mouse.click(bounds.x+bounds.width/2,bounds.y+bounds.height/2);await page.waitForTimeout(100);results.push(await page.evaluate(async()=>({report:(await import('/source-quests.js')).sourceQuestStatus(),toasts:qaToasts.slice()})));}for(let i=1;i<4;i++){assert.equal(results[i].report.lastCategory.id,803+i);assert.equal(results[i].report.lastCategory.locked,true);assert(!results[i].toasts.at(-1).includes('Function_OpenDes'));}assert.deepEqual(errors,[]);fs.writeFileSync(cwd+'/SOURCE_QUEST_GATES_VALIDATION.json',JSON.stringify({physicalClicks:4,results,pageErrors:errors,scope:'Locked category responses only; unlocked category instances remain unbound'},null,2));console.log('PASS four source quest tab clicks and unlock text');
 }finally{await browser?.close();server.kill();}
})().catch(e=>{console.error(e);process.exitCode=1;});
