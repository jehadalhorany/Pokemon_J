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
 const resources=await page.evaluate(()=>qaHud.getChild('currencyList')._children.map(c=>c.getChild('itemNums').text));assert.deepEqual(resources,['68/68','68/68']);results.push({independentResourceLabels:resources});
 const click=async name=>{const b=await page.evaluate(async name=>{const {sourceControlBounds}=await import('/source-widgets.js');return sourceControlBounds(qaHud.getChild(name));},name);await page.mouse.click(b.x+b.width/2,b.y+b.height/2);await page.waitForTimeout(120);};
 await click('btn_menu');assert.equal(await page.evaluate(()=>qaHud.getController('BagState').selectedPage),'Open');
 await click('img_menu');assert.equal(await page.evaluate(()=>qaHud.getController('BagState').selectedPage),'Close');results.push({menuOpenAndClosePhysicalClick:true});
 await page.evaluate(async()=>{await(await import('/source-dex.js')).openSourceDex(qaState);});
 for(const generation of [2,3,5,9]){
  const bounds=await page.evaluate(async generation=>{const F=await import('/vendor/fairygui.module.js');const root=F.GRoot.inst._children.at(-1),list=root.getChild('list_gather');list.scrollToView(generation-1,false);F.Stage.update();const {sourceControlBounds}=await import('/source-widgets.js');return sourceControlBounds(list.getChildAt(generation-1));},generation);
  await page.mouse.click(bounds.x+bounds.width/2,bounds.y+bounds.height/2);await page.waitForTimeout(150);
  const status=await page.evaluate(async()=> (await import('/source-dex.js')).sourceDexStatus());assert.equal(status.generation,generation);assert(status.entries>0);results.push({generation,entries:status.entries});
 }
 assert.deepEqual(errors,[]);fs.writeFileSync(cwd+'/SOURCE_MENU_DEX_VALIDATION.json',JSON.stringify({results,pageErrors:errors},null,2));console.log('PASS',results);
 }finally{await browser?.close();server.kill();}
})().catch(e=>{console.error(e);process.exitCode=1;});
