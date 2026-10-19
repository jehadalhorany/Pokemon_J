const {spawn}=require('node:child_process'),fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const cwd=process.env.POKEMON_PROJECT_ROOT||path.resolve(__dirname,'../active-project'),server=spawn(process.execPath,['server/index.mjs'],{cwd,env:{...process.env,PORT:'3110',DATA_DIR:fs.mkdtempSync('/tmp/pokemon-bindings-')},stdio:'ignore'});
(async()=>{let browser;try{
 for(let i=0;i<100;i++){try{if((await fetch('http://127.0.0.1:3110/health')).ok)break;}catch{}await new Promise(r=>setTimeout(r,200));}
 browser=await chromium.launch({executablePath:'/tmp/pokemon-chromium',headless:true,env:{...process.env,LD_LIBRARY_PATH:'/tmp',VK_ICD_FILENAMES:'/tmp/vk_swiftshader_icd.json'},args:['--no-sandbox','--no-zygote','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader','--disable-dev-shm-usage']});
 const page=await browser.newPage({viewport:{width:1909,height:905}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:3110/data/original/interface.json');
 await page.evaluate(async()=>{
  document.body.innerHTML='<div class="topline"></div>'+['dialog-modal','dex-modal','activity-modal','native-profile','native-toolbar','original-quest','native-joystick','minimap-button','starter'].map(id=>`<div id="${id}" hidden style="display:none"></div>`).join('');
  window.toast=console.log;const {initializeSourceHud}=await import('/source-hud.js');const F=await import('/vendor/fairygui.module.js');
  window.qaState=await fetch('/api/create',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json());window.sourceCurrentState=()=>qaState;
  window.act=async b=>{const r=await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)});const s=await r.json();if(!r.ok)throw Error(s.error);qaState=s;return true;};
  window.qaHud=await initializeSourceHud({state:()=>qaState,area:()=>1201,map:()=>{},quests:()=>{},go:()=>{},action:act});F.Stage.update();
 });
 await page.evaluate(async()=>{const {openSourcePanel}=await import('/source-map.js');await openSourcePanel('Battle','NormalBattle_Bg',root=>{for(const c of root._children)if(c.constructor.name==='GList')c.addItemFromPool();});});await page.waitForTimeout(500);const tree=await page.evaluate(async()=>{const F=await import('/vendor/fairygui.module.js');const r=F.GRoot.inst._children.at(-1);function read(n,d=0){return {name:n.name,type:n.constructor.name,text:n.text,controllers:n._controllers?.map(c=>({name:c.name,pages:c._pageNames})),children:d<5?(n._children||[]).map(c=>read(c,d+1)):[]};}return read(r);});fs.writeFileSync('/tmp/native-battle-tree.json',JSON.stringify(tree,null,2));await page.screenshot({path:'/tmp/native-battle-template.png'});console.log('battle template',errors);
 }finally{await browser?.close();server.kill();}
})().catch(e=>{console.error(e);process.exitCode=1;});
