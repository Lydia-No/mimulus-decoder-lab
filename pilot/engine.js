/* Research direction and methodology: Linda Thorstensen. Synthetic mechanism demonstrator. */
(function(root){
const source=[2,2,3,3,8,8,7,7,2,2,3,3];
const histories={quiet:[1,2,1,2,1,2],volatile:[1,9,2,8,1,9]};
function learn(values){const changes=values.slice(1).map((v,i)=>Math.abs(v-values[i]));return {meanChange:changes.reduce((a,b)=>a+b,0)/changes.length,observations:values.length};}
function decode(values,frame,memory){const threshold=frame==='fixed'?3:Math.max(0.5,memory.meanChange);const boundaries=values.slice(1).flatMap((v,i)=>Math.abs(v-values[i])>threshold?[i+1]:[]);const cuts=[0,...boundaries,values.length];return {threshold,boundaries,segments:cuts.slice(1).map((end,i)=>({start:cuts[i],end,values:values.slice(cuts[i],end)}))};}
function jaccard(a,b){const aa=new Set(a),bb=new Set(b),u=new Set([...aa,...bb]);return u.size?{value:[...aa].filter(x=>bb.has(x)).length/u.size,empty:false}:{value:null,empty:true};}
function run({frame='adaptive',intervention='trained',condition='original'}={}){let values=[...source];if(condition==='permuted')values=[...source.filter((_,i)=>i%2===0),...source.filter((_,i)=>i%2===1)];if(condition==='ablated')values=values.map((v,i)=>i>=4&&i<8?3:v);
let memories=[learn(histories.quiet),learn(histories.volatile)];if(intervention==='reset')memories=[{meanChange:3,observations:0},{meanChange:3,observations:0}];if(intervention==='swap')memories.reverse();if(intervention==='identical')memories=[learn(histories.quiet),learn(histories.quiet)];
const outputs=memories.map(m=>decode(values,frame,m));const key=decode(values,'fixed',{}).boundaries;return {version:'synthetic-0.1',source:values,frame,intervention,condition,trainingHistories:histories,updateRule:'mean absolute adjacent change; adaptive threshold=max(0.5,meanChange); boundary if delta>threshold',memories,outputs,reference:{rule:'absolute adjacent change > 3',boundaries:key},comparison:jaccard(outputs[0].boundaries,outputs[1].boundaries),scores:outputs.map(o=>jaccard(o.boundaries,key)),scope:'Deterministic synthetic demonstrator. Divergence is designed into the rule, not empirical evidence for a theory, cognition or decipherment.'};}
const api={source,histories,learn,decode,jaccard,run};if(typeof module!=='undefined')module.exports=api;root.Mimulus=api;
})(globalThis);
