export function sourceResourceLabels(state,levels){
 const level=levels.find(r=>r.Id===state.level);
 const rows=['power','fatigue'].map((key,i)=>{
  const resource=state.resources?.[key];
  const ready=Number.isFinite(resource?.value)&&Number.isFinite(resource?.max);
  const maximum=resource?.max??level?.[i?'FatigueMax':'PowerMax'];
  return {key,ready,text:(ready?resource.value:'—')+'/'+(maximum??'—')};
 });
 return {rows,ready:rows.every(r=>r.ready)};
}
