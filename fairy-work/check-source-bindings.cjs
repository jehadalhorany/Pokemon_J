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
 const results=[];
 const clickNative=async name=>{const b=await page.evaluate(async name=>{const {sourceControlBounds}=await import('/source-widgets.js');return sourceControlBounds(qaHud.getChild(name));},name);await page.mouse.click(b.x+b.width/2,b.y+b.height/2);};
 await clickNative('btn_menu');await page.waitForTimeout(100);const bag=await page.evaluate(async()=>{const {sourceControlBounds}=await import('/source-widgets.js');return sourceControlBounds(qaHud.getChild('list_menu')._children.find(b=>b.data.Id===201));});await page.mouse.click(bag.x+bag.width/2,bag.y+bag.height/2);await page.waitForFunction(()=>window.sourcePanelOpen,null,{timeout:20000});await page.keyboard.press('Escape');results.push({mainMenuBagPhysicalClick:true});
 for(const [module,fn,args]of [['source-bag','openSourceBag',[]],['source-shop','openSourceShop',[]],['source-dex','openSourceDex',[1]],['source-resources','openSourceResources',['power']]]){
  console.log('OPEN',module);
  await page.evaluate(async({module,fn,args})=>{const m=await import('/'+module+'.js');await m[fn](qaState,...(module==='source-dex'?args:module==='source-resources'?[...args,act]:[act]));},{module,fn,args});
  await page.waitForTimeout(300);assert.equal(await page.evaluate(()=>!!window.sourcePanelOpen),true);
  await page.screenshot({path:'/tmp/'+module+'-bound.png'});
  await page.keyboard.press('Escape');assert.equal(await page.evaluate(()=>window.sourcePanelOpen),false);results.push({module,opened:true,escape:true});
 }
 assert.deepEqual(errors,[]);fs.writeFileSync(cwd+'/SOURCE_BINDINGS_VALIDATION.json',JSON.stringify({results,pageErrors:errors},null,2));console.log('PASS',results);
 }finally{await browser?.close();server.kill();}
})().catch(e=>{console.error(e);process.exitCode=1;});
