/* Research direction, conceptual framing and methodology: Linda Thorstensen. */
(function(root){
const FIXTURE={
  id:'synthetic-decoder-persistence-001',
  version:'1.0',
  conditions:{
    original:{values:[2,2,3,3,8,8,7,7,2,2,3,3],answerKey:[4,8],role:'unaltered known-answer source'},
    permuted:{values:[2,8,3,7,2,8,3,7,2,3,2,3],answerKey:[],role:'count-preserving order destruction'},
    ablated:{values:[2,2,3,3,3,3,3,3,2,2,3,3],answerKey:[4,8],role:'middle-block contrast ablation'}
  },
  histories:{quiet:[1,2,1,2,1,2],volatile:[1,9,2,8,1,9]}
};

function same(a,b){return a.length===b.length&&a.every((v,i)=>v===b[i]);}
function intersection(a,b){const s=new Set(b);return a.filter(x=>s.has(x));}
function learn(values){const changes=values.slice(1).map((v,i)=>Math.abs(v-values[i]));return {meanChange:changes.reduce((a,b)=>a+b,0)/changes.length,observations:values.length};}
function boundarySegments(values,boundaries){const cuts=[0,...boundaries,values.length];return cuts.slice(1).map((end,i)=>({start:cuts[i],end,values:values.slice(cuts[i],end)}));}
function thresholdBoundaries(values,threshold){return values.slice(1).flatMap((v,i)=>Math.abs(v-values[i])>threshold?[i+1]:[]);}
function jaccard(a,b){const aa=new Set(a),bb=new Set(b),u=new Set([...aa,...bb]);return u.size?{value:[...aa].filter(x=>bb.has(x)).length/u.size,empty:false}:{value:null,empty:true};}

function localDelta(values){const threshold=3;const boundaries=thresholdBoundaries(values,threshold);return {family:'local_delta',assumption:'A boundary is indicated by an adjacent numeric change greater than 3.',threshold,boundaries,segments:boundarySegments(values,boundaries)};}

function motifRecurrence(values){
  const maxLen=Math.floor(values.length/3);let repeatLength=null;
  for(let len=maxLen;len>=2;len--){if(same(values.slice(0,len),values.slice(values.length-len))){repeatLength=len;break;}}
  const boundaries=repeatLength?[repeatLength,values.length-repeatLength].filter((v,i,a)=>v>0&&v<values.length&&a.indexOf(v)===i):[];
  return {family:'motif_recurrence',assumption:'Repeated prefix/suffix motifs imply a recurrent outer unit; inferred boundaries bracket the intervening unit.',repeatLength,boundaries,segments:boundarySegments(values,boundaries)};
}

function historyMemories(intervention){
  let memories=[learn(FIXTURE.histories.quiet),learn(FIXTURE.histories.volatile)];
  if(intervention==='reset') memories=[{meanChange:3,observations:0},{meanChange:3,observations:0}];
  if(intervention==='swap') memories.reverse();
  if(intervention==='identical') memories=[learn(FIXTURE.histories.quiet),learn(FIXTURE.histories.quiet)];
  return memories;
}
function historyAdaptive(values,intervention){
  const memories=historyMemories(intervention);
  const outputs=memories.map(memory=>{const threshold=Math.max(0.5,memory.meanChange);const boundaries=thresholdBoundaries(values,threshold);return {memory,threshold,boundaries,segments:boundarySegments(values,boundaries)};});
  const consensus=intersection(outputs[0].boundaries,outputs[1].boundaries);
  return {family:'history_adaptive',assumption:'A boundary is a change larger than the retained mean adjacent change from prior exposure.',intervention,outputs,boundaries:consensus,internalAgreement:jaccard(outputs[0].boundaries,outputs[1].boundaries)};
}

function historyControlSummary(values){
  const runs={};for(const name of ['trained','reset','swap','identical']) runs[name]=historyAdaptive(values,name);
  const t=runs.trained.outputs.map(o=>o.boundaries),r=runs.reset.outputs.map(o=>o.boundaries),s=runs.swap.outputs.map(o=>o.boundaries),i=runs.identical.outputs.map(o=>o.boundaries);
  const checks={trained_diverges:!same(t[0],t[1]),reset_converges:same(r[0],r[1]),identical_converges:same(i[0],i[1]),swap_exchanges:same(s[0],t[1])&&same(s[1],t[0])};
  return {checks,patternPass:Object.values(checks).every(Boolean),runs:Object.fromEntries(Object.entries(runs).map(([k,v])=>[k,{observerBoundaries:v.outputs.map(o=>o.boundaries),consensusBoundaries:v.boundaries}]))};
}

function classifyBoundary(index,families,key){
  const supporting=families.filter(f=>f.boundaries.includes(index)).map(f=>f.blindCode);const inKey=key.includes(index);
  let classification;
  if(!supporting.length&&inKey) classification='MISSED_SOURCE_FEATURE';
  else if(supporting.length===families.length) classification=inKey?'SOURCE_SUPPORTED_INVARIANT':'SHARED_UNSUPPORTED';
  else classification=inKey?'DECODER_DEPENDENT_SUPPORTED':'DECODER_DEPENDENT_UNSUPPORTED';
  return {index,inKnownAnswer:inKey,supportingDecoders:supporting,supportCount:supporting.length,totalDecoderFamilies:families.length,classification};
}
function metaObserve(families,key){
  const positions=[...new Set([...key,...families.flatMap(f=>f.boundaries)])].sort((a,b)=>a-b);
  const features=positions.map(i=>classifyBoundary(i,families,key));
  const pairwise=[];for(let a=0;a<families.length;a++)for(let b=a+1;b<families.length;b++)pairwise.push({a:families[a].blindCode,b:families[b].blindCode,overlap:jaccard(families[a].boundaries,families[b].boundaries)});
  return {features,pairwise,allFamilyAgreement:families.every((f,i)=>i===0||same(f.boundaries,families[0].boundaries))};
}

function run({condition='original',historyIntervention='reset'}={}){
  if(!FIXTURE.conditions[condition]) throw new Error('Unknown condition: '+condition);
  const c=FIXTURE.conditions[condition],values=[...c.values],key=[...c.answerKey];
  const d1=localDelta(values),d2=motifRecurrence(values),d3=historyAdaptive(values,historyIntervention);
  const families=[
    {blindCode:'Q7',family:d1.family,boundaries:d1.boundaries,details:d1},
    {blindCode:'L4',family:d2.family,boundaries:d2.boundaries,details:d2},
    {blindCode:'N9',family:d3.family,boundaries:d3.boundaries,details:d3}
  ];
  return {
    version:'pilot-001.0',
    fixture:{id:FIXTURE.id,version:FIXTURE.version},
    condition,conditionRole:c.role,source:values,knownAnswer:{boundaryIndices:key,indexing:'zero-based; boundary index is the start of the next segment'},
    historyIntervention,
    blindedFamilyOutputs:families.map(f=>({blindCode:f.blindCode,boundaries:f.boundaries})),
    decoderRegistry:Object.fromEntries(families.map(f=>[f.blindCode,{family:f.family,assumption:f.details.assumption}])),
    decoderDetails:Object.fromEntries(families.map(f=>[f.blindCode,f.details])),
    metaObservation:metaObserve(families,key),
    historyControls:historyControlSummary(values),
    scope:'Deterministic known-answer measurement test. It tests whether the scaffold can separate cross-decoder persistence, decoder dependence, unsupported structure and a controlled history effect. It is not empirical evidence for cognition, a general theory or Voynich decipherment.'
  };
}
function matrix(){const runs=[];for(const condition of Object.keys(FIXTURE.conditions))for(const historyIntervention of ['trained','reset','swap','identical'])runs.push(run({condition,historyIntervention}));return {version:'pilot-001.0',fixture:{id:FIXTURE.id,version:FIXTURE.version},runs,scope:'Twelve deterministic cells; repeated execution is reproducibility, not independent replication.'};}

const api={FIXTURE,same,learn,jaccard,localDelta,motifRecurrence,historyAdaptive,historyControlSummary,metaObserve,run,matrix};if(typeof module!=='undefined'&&module.exports)module.exports=api;root.Mimulus=api;
})(typeof globalThis!=='undefined'?globalThis:this);
