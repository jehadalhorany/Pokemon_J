export function sourceDexRows(entries,gather,generation,query=''){
 const q=query.trim().toLowerCase();if(q)return entries.filter(p=>(p.form||p.name).toLowerCase().includes(q)||String(p.number)===q);
 const rows=new Map(gather.filter(r=>r.Type===generation).map(r=>[r.Id,r.Rank]));
 return entries.filter(p=>rows.has(p.originalId)).sort((a,b)=>rows.get(a.originalId)-rows.get(b.originalId));
}
