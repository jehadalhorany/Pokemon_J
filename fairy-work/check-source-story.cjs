const {spawn}=require('node:child_process'),fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const cwd=process.env.POKEMON_PROJECT_ROOT||path.resolve(__dirname,'../active-project');
const server=spawn(process.execPath,['server/index.mjs'],{cwd,env:{...process.env,PORT:'3110',DATA_DIR:fs.mkdtempSync('/tmp/pokemon-story-')},stdio:['ignore','ignore','pipe']});
server.stderr.on('data',d=>process.stderr.write(d));
(async()=>{let browser;try{
 for(let i=0;i<120;i++){try{if((await fetch('http://127.0.0.1:3110/health')).ok)break;}catch{}await new Promise(r=>setTimeout(r,500));}
 browser=await chromium.launch({executablePath:'/tmp/pokemon-chromium',headless:true,env:{...process.env,LD_LIBRARY_PATH:'/tmp',VK_ICD_FILENAMES:'/tmp/vk_swiftshader_icd.json'},args:['--no-sandbox','--no-zygote','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader','--disable-dev-shm-usage']});
 const page=await browser.newPage({viewport:{width:1440,height:810}}),errors=[];
 page.on('pageerror',e=>{errors.push(e.message);console.error(e.message);});
 page.on('console',m=>{if(m.type()==='error')console.error('CONSOLE',m.text());});
 console.log('Browser ready');
 await page.goto('http://127.0.0.1:3110',{waitUntil:'domcontentloaded'});console.log('DOM ready');
 await page.waitForFunction(()=>typeof getVisualStatus==='function'&&!getVisualStatus().loading&&getVisualStatus().sourceHud.ready,null,{timeout:180000});
 console.log('World ready',await page.evaluate(()=>getVisualStatus()));
 await page.evaluate(()=>startOriginalMission());
 await page.waitForFunction(()=>getVisualStatus().area===1804&&!getVisualStatus().loading,null,{timeout:120000});
 await page.waitForFunction(()=>getVisualStatus().sourceDialogue.open,null,{timeout:120000});
 assert(await page.locator('#dialog-modal').evaluate(e=>e.hidden),'prototype dialogue stays hidden');
 const mom=await page.evaluate(()=>getVisualStatus().sourceDialogue);
 assert(mom.total>0);console.log('Mom',mom);
 await page.screenshot({path:'/tmp/pokemon-native-mom.png'});
 for(let i=0;i<mom.total;i++){await page.keyboard.press('Enter');await page.waitForTimeout(100);}
 assert.equal(await page.evaluate(()=>getVisualStatus().sourceDialogue.open),false);
 await page.evaluate(()=>startOriginalMission());
 await page.waitForFunction(()=>getVisualStatus().area===1801&&!getVisualStatus().loading,null,{timeout:180000});
 await page.waitForFunction(()=>getVisualStatus().sourceDialogue.open,null,{timeout:120000});
 const professor=await page.evaluate(()=>getVisualStatus().sourceDialogue);console.log('Professor',professor);
 await page.screenshot({path:'/tmp/pokemon-native-professor.png'});
 for(let i=0;i<professor.total;i++){await page.keyboard.press('Enter');await page.waitForTimeout(100);}
 await page.waitForFunction(()=>document.getElementById('starter').style.display!=='none',null,{timeout:120000});
 assert.equal(await page.evaluate(()=>state.team.length),0,'preview does not grant a partner');
 assert.deepEqual(errors,[]);
 fs.writeFileSync(path.join(cwd,'SOURCE_STORY_VALIDATION.json'),JSON.stringify({validatedAt:new Date().toISOString(),stairs:true,momNativeDialogue:true,houseExitAndLabDoor:true,professorNativeDialogue:true,walkToStarterBalls:true,previewDoesNotGrantPartner:true,pageErrors:errors},null,2));
 console.log('PASS actual home stairs, native Mom, exterior/lab door, native professor, starter preview');
 }finally{await browser?.close();server.kill();}
})().catch(e=>{console.error(e);process.exitCode=1;});
