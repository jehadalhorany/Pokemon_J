const {spawn}=require('node:child_process'),fs=require('node:fs'),path=require('node:path');
const {chromium}=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const assert=require('node:assert/strict');
const cwd=path.resolve(__dirname,'../active-project'),server=spawn(process.execPath,['server/index.mjs'],{cwd,env:{...process.env,PORT:'3110',DATA_DIR:fs.mkdtempSync('/tmp/pokemon-layout-')},stdio:'ignore'});
(async()=>{let browser;try{
 for(let i=0;i<100;i++){try{if((await fetch('http://127.0.0.1:3110/health')).ok)break;}catch{}await new Promise(r=>setTimeout(r,200));}
 browser=await chromium.launch({executablePath:'/tmp/pokemon-chromium',headless:true,env:{...process.env,LD_LIBRARY_PATH:'/tmp',VK_ICD_FILENAMES:'/tmp/vk_swiftshader_icd.json'},args:['--no-sandbox','--no-zygote','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader','--disable-dev-shm-usage']});
 const page=await browser.newPage({viewport:{width:1440,height:810}});
 await page.goto('http://127.0.0.1:3110/data/original/interface.json');
 const result=await page.evaluate(async()=>{
  const {openSourceStory}=await import('/source-dialogue.js');
  const root=await openSourceStory('Dr. Oki',"You've been waiting a long time. I'm Dr. Oki, who works on Pokemon.");
  const content=root.getChild('lb_content');window.storyLayoutRoot=root;
  return {text:content.text,align:content.align,font:content.textFormat,width:content.width,height:content.height,lines:content._textField._lines.map(l=>({width:l.width,chars:l.charCount})),rect:content._textField._contentRect};
 });
 assert.equal(result.text,"You've been waiting a long time. I'm Dr. Oki, who works on Pokemon.");assert(result.lines.every(l=>l.width<=result.rect.width));
 await page.waitForTimeout(300);await page.screenshot({path:'/tmp/pokemon-story-layout.png'});
 await page.setViewportSize({width:1280,height:720});
 const bounds=await page.evaluate(()=>({x:storyLayoutRoot.xMin,y:storyLayoutRoot.yMin}));assert.deepEqual(bounds,{x:0,y:0});
 await page.keyboard.press('Enter');
 assert.equal(await page.evaluate(async()=>{const m=await import('/source-dialogue.js');return m.sourceDialogueStatus().open;}),false);
 fs.writeFileSync(path.join(cwd,'SOURCE_DIALOGUE_LAYOUT_VALIDATION.json'),JSON.stringify({validatedAt:new Date().toISOString(),originalWindow:'Dialogue/Dialogue_MiniWindow',englishLinesFit:true,nativeWidth:result.width,nativeHeight:result.height,resizePivotAligned:true,enterCloses:true},null,2));console.log('PASS native dialogue text bounds, resize pivot, Enter close');
 }finally{await browser?.close();server.kill();}
})().catch(e=>{console.error(e);process.exitCode=1;});
