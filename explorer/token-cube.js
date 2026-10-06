/* Deterministic token adapter; no model calls or historical adjudication. */
(function(root){
'use strict';
const AXES=[
 {id:'mapping',label:'Base mapping',choices:['A','B']},
 {id:'coverage',label:'Mapping coverage',choices:['Keep all','Withhold first symbol']},
 {id:'assignment',label:'Target assignment',choices:['Declared','Rotate targets']},
 {id:'frequency',label:'Symbol filter',choices:['All observed','Repeated only']}
];
// Match Python str.split()/isspace(), including C0 separators and NEL.
const space=/[\u0009-\u000d\u001c-\u0020\u0085\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000]/u;
const spaces=/[\u0009-\u000d\u001c-\u0020\u0085\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000]+/u;
function codepointOrder(a,b){const aa=Array.from(a,c=>c.codePointAt(0)),bb=Array.from(b,c=>c.codePointAt(0));for(let i=0;i<Math.min(aa.length,bb.length);i++)if(aa[i]!==bb[i])return aa[i]-bb[i];return aa.length-bb.length;}
const owns=(o,k)=>Object.prototype.hasOwnProperty.call(o,k);
function rules(value,name){
 if(!value||typeof value!=='object'||Array.isArray(value)||Object.entries(value).some(([k,v])=>!k||typeof v!=='string'||!v||space.test(k+v)))throw Error(`${name} must contain single nonempty token pairs`);
 return Object.fromEntries(Object.entries(value));
}
function compare(readings){
 const keys=new Set(readings.flatMap(r=>Object.keys(r.mapping_claims))),shared={},conflicts={};
 for(const k of keys){const values=readings.filter(r=>owns(r.mapping_claims,k)).map(r=>r.mapping_claims[k]),unique=[...new Set(values)].sort(codepointOrder);
 if(values.length===readings.length&&unique.length===1)Object.defineProperty(shared,k,{value:unique[0],enumerable:true});
 else if(unique.length>1)Object.defineProperty(conflicts,k,{value:unique,enumerable:true});}
 return {outcome:Object.keys(conflicts).length?'divergence':Object.keys(shared).length?'convergence':'undetermined',shared_mappings:shared,conflicting_mappings:conflicts,shared_structure:[]};
}
function reading(tokens,mapping,sourceId,decoderId){
 const used=Object.fromEntries(tokens.filter(t=>owns(mapping,t)).map(t=>[t,mapping[t]]));
 return {source_id:sourceId,decoder_id:decoderId,mapping_claims:used,semantic_reading:tokens.map(t=>owns(mapping,t)?mapping[t]:`[${t}]`).join(' '),uncertainties:[...new Set(tokens.filter(t=>!owns(mapping,t)))].sort(codepointOrder).map(t=>`No mapping for ${JSON.stringify(t)}`)};
}
async function analyze(payload){
 if(!payload||!['known','opaque'].includes(payload.mode)||typeof payload.source!=='string'||!payload.source.split(spaces).filter(Boolean).length)throw Error('Choose a mode and enter source tokens');
 if(Array.from(payload.source).length>16000)throw Error('Source exceeds the workspace limit');
 const original=payload.source.split(spaces).filter(Boolean),a=rules(payload.decoder_a,'Decoder A'),b=rules(payload.decoder_b,'Decoder B');
 let tokens=original,reference=null;
 if(payload.mode==='known'){
  const encoder=rules(payload.encoder,'Encoder');
  if(typeof (payload.allow_lossy===undefined?false:payload.allow_lossy)!=='boolean')throw Error('Lossy encoding must be explicitly selected');
  if(original.some(t=>!owns(encoder,t)))throw Error('Encoder has no mapping for one or more original tokens');
  if(!payload.allow_lossy&&new Set(Object.values(encoder)).size!==Object.keys(encoder).length)throw Error('Many-to-one codebook requires explicit lossy selection');
  tokens=original.map(t=>encoder[t]);reference={original_tokens:original,encoded_tokens:tokens,codebook:Object.entries(encoder)};
 }
 const transcription=tokens.join(' '),digest=await root.crypto.subtle.digest('SHA-256',new TextEncoder().encode(transcription));
 const hash=[...new Uint8Array(digest)].map(x=>x.toString(16).padStart(2,'0')).join(''),sourceId=`src_token_${hash}`,runId=`run_${root.crypto.randomUUID()}`,representationId=`rep_${hash}`;
 const counts=new Map();tokens.forEach(t=>counts.set(t,(counts.get(t)||0)+1));
 function score(r){if(!reference)return null;const recovered=tokens.map(t=>owns(r.mapping_claims,t)?r.mapping_claims[t]:null),matched=recovered.filter((t,i)=>t===original[i]).length,groups=new Map();for(const [from,to] of reference.codebook){if(!groups.has(to))groups.set(to,[]);groups.get(to).push(from);}return {matched_tokens:matched,total_tokens:original.length,token_accuracy:matched/original.length,exact_recovery:matched===original.length,unresolved_tokens:recovered.filter(t=>t===null).length,recovered_tokens:recovered,collision_groups:[...groups].filter(([,v])=>v.length>1)};}
 const nodes=[];
 for(let v=0;v<16;v++){
  const bits=AXES.map((_,i)=>(v>>i)&1),id=bits.join('');let map={...(bits[0]?b:a)};
  if(bits[2]){const keys=Object.keys(map).sort(codepointOrder),values=keys.map(k=>map[k]);map=Object.fromEntries(keys.map((k,i)=>[k,values[(i+1)%keys.length]]));}
  if(bits[1])delete map[tokens[0]];
  if(bits[3])map=Object.fromEntries(Object.entries(map).filter(([k])=>counts.get(k)>1));
  const r=reading(tokens,map,sourceId,`cube-${id}`);
  nodes.push({id,vertex:v,bits,assumptions:Object.fromEntries(AXES.map((axis,i)=>[axis.id,axis.choices[bits[i]]])),mapping:map,reading:r,recovery:score(r)});
 }
 const edges=[];for(let v=0;v<16;v++)for(let axis=0;axis<4;axis++){const n=v^(1<<axis);if(v<n)edges.push({from:nodes[v].id,to:nodes[n].id,axis:AXES[axis].id,comparison:compare([nodes[v].reading,nodes[n].reading])});}
 const pair=[reading(tokens,a,sourceId,'Decoder A'),reading(tokens,b,sourceId,'Decoder B')];
 const states=nodes.map(n=>({id:`${runId}_state_${n.id}`,sourceId,representationId,contextId:`${runId}_ctx_${n.id}`,bits:n.bits,effectiveMapping:n.mapping,outputRef:`${runId}_output_${n.id}`,historyCondition:'none'}));
 return {version:'explorer-token-cube-v1',created_at:new Date().toISOString(),mode:payload.mode,observation:{source_id:sourceId,transcription},reference,results:pair.map(r=>({reading:r,recovery:score(r)})),comparison:compare(pair),structure:{claims:[...counts].filter(([,n])=>n>1).map(([t,n])=>({text:`Token ${JSON.stringify(t)} occurs ${n} times.`}))},hypercube:{dimensions:4,source_id:sourceId,axes:AXES.map(x=>({...x,choices:[...x.choices]})),nodes,edges,boundary:'Declared interventions can yield identical mappings. Vertices are not independent empirical runs; geometry does not establish meaning.'},beqube:{version:'mimulus-token-state-adapter-v1',source:{id:sourceId,mediaType:'sequence',artifactRef:`artifact_${hash}`,sha256:hash,createdAt:new Date().toISOString(),notes:'Encoded token sequence normalized to single-space separators; not an image or raw source formatting hash.'},representation:{id:representationId,sourceId,kind:'transcription',artifactRef:`artifact_${hash}`,sha256:hash,createdAt:new Date().toISOString(),method:'whitespace tokenization; single-space joining'},artifacts:[{id:`artifact_${hash}`,content:transcription}],decoder:{id:'dec_explicit_token_mapping',family:'user_defined',version:'1',implementation:'explorer/token-cube.js',declaredAssumptions:['One explicit output token per encoded token; unresolved symbols remain unresolved.']},outputs:nodes.map(n=>({id:`${runId}_output_${n.id}`,reading:n.reading,recovery:n.recovery})),states,contexts:nodes.map(n=>({id:`${runId}_ctx_${n.id}`,framing:JSON.stringify(n.assumptions)})),runs:nodes.map(n=>({id:`${runId}_${n.id}`,sourceId,representationId,decoderId:'dec_explicit_token_mapping',contextId:`${runId}_ctx_${n.id}`,inputRef:representationId,outputRef:`${runId}_output_${n.id}`,evidenceClass:'EXPLORATORY_DECODER_OUTPUT',startedAt:new Date().toISOString(),deterministic:true,notes:'Explicit mapping contexts; no observer history or independent model replication.'})),interventions:[],transitions:[],inspectionEvents:[]}};
}
function inspect(report,from,to,at=new Date().toISOString()){
 const q=report.beqube;if(!q||!report.hypercube.nodes.some(n=>n.id===to)||(from!==null&&!report.hypercube.nodes.some(n=>n.id===from)))throw Error('Unknown state');
 if(from===to)return;
 const changed=from?[...to].map((b,i)=>b!==from[i]?i:-1).filter(i=>i>=0):[];
 const event={from,to,event:from===null?'start':changed.length===1?'axis_transition':'jump',axis:changed.length===1?AXES[changed[0]].id:null,at};
 q.inspectionEvents.push(event);
 // A jump is an inspection event, never a one-axis beQube transition.
 if(event.event==='axis_transition'){
  const id=`int_${q.runs[0].id}_${q.interventions.length}`;
  q.interventions.push({id,type:'context_swap',parameters:{axis:event.axis,from,to},rationale:'Inspect an explicit one-axis context intervention on a fixed source.',claimTested:'Does the declared mapping output change when only this context choice changes?'});
  q.transitions.push({beforeStateRef:q.states.find(s=>s.bits.join('')===from).id,interventionId:id,afterStateRef:q.states.find(s=>s.bits.join('')===to).id});
 }
 return event;
}
const api={analyze,inspect};root.MimulusTokenCube=api;if(typeof module!=='undefined')module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
