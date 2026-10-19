const {spawn}=require('node:child_process'),fs=require('node:fs'),path=require('node:path');
const {chromium}=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const cwd=path.resolve(__dirname,'../active-project'),server=spawn(process.execPath,['server/index.mjs'],{cwd,env:{...process.env,PORT:'3110',DATA_DIR:fs.mkdtempSync('/tmp/pokemon-hud-ui-')},stdio:'ignore'});
(async()=>{let browser;try{
 for(let i=0;i<100;i++){try{if((await fetch('http://127.0.0.1:3110/health')).ok)break;}catch{}await new Promise(r=>setTimeout(r,200));}
 browser=await chromium.launch({executablePath:'/tmp/pokemon-chromium',headless:true,env:{...process.env,LD_LIBRARY_PATH:'/tmp',VK_ICD_FILENAMES:'/tmp/vk_swiftshader_icd.json'},args:['--no-sandbox','--no-zygote','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader','--disable-dev-shm-usage']});
 const page=await browser.newPage({viewport:{width:1909,height:905}});page.on('pageerror',e=>console.log('ERROR',e.message));
 await page.goto('http://127.0.0.1:3110/data/original/interface.json');
 console.log(await page.evaluate(async()=>{
  document.body.innerHTML='<div class="topline"></div>'+['dialog-modal','dex-modal','activity-modal','native-profile','native-toolbar','original-quest','native-joystick','minimap-button','starter'].map(id=>`<div id="${id}" hidden style="display:none"></div>`).join('');
  const {initializeSourceHud}=await import('/source-hud.js');const F=await import('/vendor/fairygui.module.js');
  const state=await fetch('/api/create',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json());window.qaState=state;
  const hud=await initializeSourceHud({state:()=>state,area:()=>1201,map:()=>{},quests:()=>{},go:()=>{}});window.qaHud=hud;F.Stage.update();
  const all=[];function scan(o){if(!o.visible)return;const p=o.localToGlobal(0,0);if(o.width*F.UIContentScaler.scaleFactor>500)all.push({name:o.name,type:o.constructor.name,x:p.x,y:p.y,width:o.width,height:o.height,url:o.url,source:o.resourceURL});for(const c of o._children||[])scan(c);}scan(hud);
  return all;
 }));
 await page.waitForTimeout(300);await page.screenshot({path:'/tmp/pokemon-hud-isolated.png'});
 const view=await page.evaluate(async()=>{const F=await import('/vendor/fairygui.module.js');const specs=[['Pve','PveMain_Window'],['Main','Main_Bg']];return specs.map(([pkg,name])=>{try{const o=F.UIPackage.createObject(pkg,name);const desc=n=>({name:n.name,type:n.constructor.name,defaultItem:n.defaultItem,children:n._children?.map(c=>({name:c.name,type:c.constructor.name})),controllers:n._controllers?.map(c=>({name:c.name,pages:c._pageNames}))});const data={pkg,name,controllers:o._controllers?.map(c=>({name:c.name,pages:c._pageNames})),children:o._children.map(desc)};for(const l of o._children.filter(c=>c instanceof F.GList&&c.defaultItem)){try{l.removeChildrenToPool();const cell=l.addItemFromPool();data.children.find(c=>c.name===l.name).template=desc(cell);}catch(e){data.children.find(c=>c.name===l.name).error=String(e);}}o.dispose();return data;}catch(e){return{pkg,name,error:String(e)};}});});
 fs.writeFileSync(path.join(__dirname,'pve-main-inspection.json'),JSON.stringify(view,null,2));console.log('inspection saved');
 }finally{await browser?.close();server.kill();}
})().catch(e=>{console.error(e);process.exitCode=1;});
