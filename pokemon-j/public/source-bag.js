import {openSourcePanel,sourceText} from './source-map.js';
import {interfaceData,sourceItems,sourceImage,clearSourceLists,wireSourceClose,hideSource,fillSourceItem,setSourceCurrency,sourceControlBounds} from './source-widgets.js';
let report={};
export function sourceBagStatus(){return report;}
export async function openSourceBag(state,action,category=1){
 return openSourcePanel('Bag','BagCenter_Window',root=>{
  clearSourceLists(root);wireSourceClose(root);root.getController('ShowState').selectedPage='Show';
  hideSource(root,'btn_sort');root.getController('SortState').selectedPage='Hide';
  const tabs=root.getChild('list_tab'),goods=root.getChild('list_goods'),info=root.getChild('commonItemInfo');
  info.visible=false;root.getChild('list_btn').visible=false;const selected=[];
  function selectItem(id,count){const item=sourceItems.get(id);info.visible=true;info.getChild('icon_goods').url=sourceImage(item.Icon);sourceText(info.getChild('lb_name'),item.name);sourceText(info.getChild('lb_typename'),item.description);sourceText(info.getChild('lb_limit'),count);sourceText(info.getChild('lb_level'),'');hideSource(info,'btn_share','shareItem','bagPanel','btn_complex','list_price','lb_gift');const buttons=root.getChild('list_btn');buttons.removeChildrenToPool();buttons.visible=[40001,40002,40004,40005].includes(id);if(buttons.visible){const b=buttons.addItemFromPool();sourceText(b,interfaceData.text.ItemUse||'Use');b.onClick(async()=>{if(await action({action:'useResourceGift',item:id}))openSourceBag(window.sourceCurrentState(),action,category);});}report.selected=id;}
  function show(id){category=id;info.visible=false;goods.removeChildrenToPool();const rows=(state.sourceInventory||[]).filter(r=>sourceItems.get(r.id)?.StoreType===id);for(const r of rows){const cell=goods.addItemFromPool();fillSourceItem(cell,r.id,r.count,state);cell.onClick(()=>selectItem(r.id,r.count));selected.push(r.id);}sourceText(root.getChild('lb_none'),rows.length?'':interfaceData.text.BagNoItems||'');report={category:id,items:rows.map(r=>({id:r.id,count:r.count})),selected:null};}
  for(const row of interfaceData.bagCategories.filter(r=>r.Type===1).sort((a,b)=>a.Rank-b.Rank)){const tab=tabs.addItemFromPool();sourceText(tab.getChild('lb_title'),row.name);hideSource(tab,'RedDot');tab.onClick(()=>{tabs.selectedIndex=tab.parent.getChildIndex(tab);show(row.Id);});}
  tabs.selectedIndex=Math.max(0,interfaceData.bagCategories.filter(r=>r.Type===1).findIndex(r=>r.Id===category));show(category);
 });
}
