import * as F from './vendor/fairygui.module.js';
import {openSourcePanel,closeSourcePanel,sourceText,onSourcePanelClose} from './source-map.js';
let status={open:false};
export function sourceDialogueStatus(){return {...status};}
export async function openSourceStory(speaker,text,completion){
 const lines=String(text||'').split(/\n\s*\n/).map(s=>s.trim()).filter(Boolean);
 if(!lines.length)return completion?.();
 return openSourcePanel('Dialogue','Dialogue_MiniWindow',root=>{
  let index=0,closed=false;
  status={open:true,speaker,line:1,total:lines.length};
  root.getController('State').selectedPage='NoTimer';
  root.getChild('playerIcon').visible=false;root.getChild('lb_timer').visible=false;
  sourceText(root.getChild('lb_name'),speaker);
  const content=root.getChild('lb_content');content.singleLine=false;content.autoSize=F.AutoSizeType.Shrink;content.setSize(975,124);
  function show(){sourceText(content,lines[index]);status.line=index+1;}
  function advance(){if(closed)return;if(++index<lines.length)return show();closeSourcePanel();completion?.();}
  function key(e){if(e.key==='Enter'&&!e.repeat){e.preventDefault();e.stopImmediatePropagation();advance();}}
  root.getChild('nextBtn').onClick(advance);
  document.addEventListener('keydown',key,true);
  onSourcePanelClose(()=>{closed=true;status={open:false};document.removeEventListener('keydown',key,true);});
  show();
 });
}
