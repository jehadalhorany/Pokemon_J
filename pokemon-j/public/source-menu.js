// FunctionConfig.IsShow is not a menu-membership flag: core entries use zero.
export function sourceMenuRecords(records,maxLevel=Infinity){return records.filter(r=>r.Pos===5&&!r.IsClose&&(r.Level||0)<=maxLevel).sort((a,b)=>a.PosRank-b.PosRank||a.Id-b.Id);}
export function sourceFunctionOpen(record,state){
 if(!record||!state||record.IsClose)return false;
 if((state.level||0)<(record.Level||0))return false;
 if(record.Quest&&!state.original?.completed?.includes(record.Quest))return false;
 if((state.vip||0)<(record.Vip||0))return false;
 if((state.guild?.level||0)<(record.GuildLevel||0))return false;
 return true;
}
