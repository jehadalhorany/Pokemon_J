import {openSourcePanel,sourceText} from './source-map.js';
import {interfaceData,sourceItems,sourceImage,clearSourceLists,wireSourceClose,hideSource,fillSourceItem} from './source-widgets.js';
let report={open:false};
export function sourceResourceStatus(){return report;}
export async function openSourceResources(state,key,action){
 const resource=state.resources?.[key],offer=state.resourceOffers?.[key];if(!resource||!offer)return;
 const id=key==='power'?3:4,item=sourceItems.get(id);
 return openSourcePanel('Common','BuyPoweOrFatigue_MiniWindow',root=>{
  clearSourceLists(root);wireSourceClose(root);sourceText(root.getChild('win').getChild('title'),item.name);sourceText(root.getChild('win').getChild('title2'),item.name);hideSource(root,'lb_go','Click_levelUp');
  sourceText(root.getChild('lb_power'),sourceItems.get(3).name+' '+state.resources.power.value+'/'+state.resources.power.max);
  sourceText(root.getChild('lb_fatigue'),sourceItems.get(4).name+' '+state.resources.fatigue.value+'/'+state.resources.fatigue.max);
  const remain=Math.max(0,Math.ceil((resource.at+resource.intervalMs-Date.now())/1000));
  sourceText(root.getChild('lb_time'),Math.floor(remain/60)+':'+String(remain%60).padStart(2,'0'));
  sourceText(root.getChild('lb_tip'),item.description);
  const buy=root.getChild('buyItem');buy.getController('State').selectedPage='Buy';
  sourceText(buy.getChild('lb_name'),item.name);sourceText(buy.getChild('lb_desc'),item.description);sourceText(buy.getChild('lb_num'),offer.used+'/'+offer.limit);
  fillSourceItem(buy.getChild('goodItem'),id,offer.amount,state);sourceText(buy.getChild('sure'),interfaceData.text.BuyBtn||'Buy');sourceText(buy.getChild('btn_cost'),offer.record?.PriceNum??'');
  const transact=async()=>{if(await action({action:'refill',resource:key}))openSourceResources(window.sourceCurrentState(),key,action);};
  buy.getChild('sure').grayed=offer.used>=offer.limit||resource.value>=resource.max;buy.getChild('sure').onClick(transact);buy.getChild('btn_cost').onClick(transact);
  const gifts=interfaceData.global[key==='power'?'powerGift':'fatigueGift']||[],list=root.getChild('list_goods');
  for(const giftId of gifts){const owned=state.original?.inventory?.[giftId]||0,cell=list.addItemFromPool(),gift=sourceItems.get(giftId);cell.getController('State').selectedPage='Have';sourceText(cell.getChild('lb_name'),gift.name);sourceText(cell.getChild('lb_desc'),gift.description);sourceText(cell.getChild('lb_num'),owned);fillSourceItem(cell.getChild('goodItem'),giftId,owned,state);hideSource(cell,'btn_cost');sourceText(cell.getChild('sure'),interfaceData.text.ItemUse||'Use');cell.getChild('sure').grayed=!owned;cell.getChild('sure').onClick(async()=>{if(await action({action:'useResourceGift',item:giftId}))openSourceResources(window.sourceCurrentState(),key,action);});}
  report={open:true,key,value:resource.value,max:resource.max,used:offer.used,limit:offer.limit,gifts:gifts.map(id=>({id,count:state.original?.inventory?.[id]||0}))};
 });
}
