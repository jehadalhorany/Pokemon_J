// FieldEudemonConfig.BoxId binds scene object group 5 to its original Step range.
// Movement is measured in source map units, independently of screen/frame rate.
export class SourceFieldSteps {
 constructor(records,random=Math.random){this.records=new Map(records.map(r=>[r.BoxId,r]));this.random=random;this.reset();}
 reset(){this.field=null;this.distance=0;this.threshold=null;}
 advance(field,distance){
  const record=this.records.get(field?.id);
  if(!record||!Array.isArray(record.Step)||record.Step.length!==2){this.reset();return null;}
  if(this.field!==field.id){this.field=field.id;this.distance=0;this.threshold=null;}
  if(this.threshold===null){const [min,max]=record.Step;if(!(min>0&&max>=min))return null;this.threshold=min+Math.floor(this.random()*(max-min+1));}
  this.distance+=Math.max(0,distance);
  if(this.distance<this.threshold)return null;
  this.distance=0;this.threshold=null;return record;
 }
}
