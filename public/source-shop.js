import {openSourcePanel,sourceText} from './source-map.js';
import {interfaceData,sourceItems,clearSourceLists,wireSourceClose,hideSource,fillSourceItem,setSourceCurrency} from './source-widgets.js';
let report={};export function sourceShopStatus(){return report;}
function count(state,id){return id===1?state.coins:id===2?state.gems:state.sourceInventory?.find(i=>i.id===id)?.count||0;}
export async function openSourceShop(state,action){
 return openSourcePanel('Shop','Shop_Window',root=>{
  clearSourceLists(root);wireSourceClose(root);setSourceCurrency(root.getChild('currencyList'),state);
  root.getController('RefreshState').selectedPage='Normal';root.getController('ListState').selectedPage='Normal';
  hideSource(root,'btn_refresh','group_preview','lb_ttime','lb_go','lb_tvip','bg_levelVip','lb_tlimit','lb_tthavenum');
  const tab=root.getChild('list_tab').addItemFromPool();sourceText(tab,sourceItems.get(1)?.name);root.getChild('list_tab').selectedIndex=0;
  const rows=interfaceData.shopGold.filter(r=>state.level>=r.MinLevel&&state.level<=r.MaxLevel&&(state.vip||0)>=r.VipLevel).sort((a,b)=>a.Rank-b.Rank);
  for(const row of rows){const cell=root.getChild('list_shop').addItemFromPool(),item=sourceItems.get(row.ShopItem[0]);fillSourceItem(cell.getChild('itemBtn'),row.ShopItem[0],row.ShopItem[1],state);sourceText(cell.getChild('lb_name'),item.name);sourceText(cell.getChild('lb_des'),item.description);sourceText(cell.getChild('lb_shellNum'),row.BuyItem[1]+' '+sourceItems.get(row.BuyItem[0]).name);for(const name of ['lb_tlimit','lb_limit','lb_tvip','lb_vip','lb_time','lb_discount','lb_discount1','lb_soleOut','lb_lock'])hideSource(cell,name);hideSource(cell,'img_click');cell.onClick(()=>openSourceShopPurchase(state,row,action));}
  report={shopType:1,offers:rows.map(r=>({id:r.Id,item:r.ShopItem,cost:r.BuyItem}))};
 });
}
async function openSourceShopPurchase(state,row,action){return openSourcePanel('Shop','ShopBuy_MiniWindow',root=>{clearSourceLists(root);wireSourceClose(root,()=>openSourceShop(window.sourceCurrentState(),action));const item=sourceItems.get(row.ShopItem[0]);fillSourceItem(root.getChild('item'),row.ShopItem[0],row.ShopItem[1],state);sourceText(root.getChild('lb_name'),item.name);sourceText(root.getChild('lb_havenum'),count(state,item.Id));sourceText(root.getChild('lb_limit'),row.BuyItem[1]+' '+sourceItems.get(row.BuyItem[0]).name);sourceText(root.getChild('paneltext'),item.description);const bar=root.getChild('buyBar');bar.visible=false;sourceText(root.getChild('sure'),interfaceData.text.BuyBtn||'Buy');root.getChild('sure').onClick(async()=>{if(await action({action:'sourceShopBuy',offer:row.Id,quantity:1}))openSourceShop(window.sourceCurrentState(),action);});report.purchase=row.Id;});}
