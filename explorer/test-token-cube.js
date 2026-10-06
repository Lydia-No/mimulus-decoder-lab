const assert=require('node:assert/strict');
globalThis.crypto=require('node:crypto').webcrypto;
const {analyze,inspect}=require('./token-cube.js');
(async()=>{
 const payload={mode:'known',source:'sun water sun stone',encoder:{sun:'q',water:'x',stone:'z'},decoder_a:{q:'sun',x:'water',z:'stone'},decoder_b:{q:'king',x:'war',z:'crown'}};
 const r=await analyze(payload),q=r.hypercube;
 assert.equal(r.beqube.representation.kind,'transcription');assert(r.beqube.artifacts.some(a=>a.id===r.beqube.source.artifactRef));for(const run of r.beqube.runs){assert.equal(run.decoderId,r.beqube.decoder.id);assert(r.beqube.outputs.some(o=>o.id===run.outputRef));}
 assert.equal(q.nodes.length,16);assert.equal(q.edges.length,32);
 assert.equal(q.nodes[0].recovery.token_accuracy,1);assert.equal(q.nodes[1].recovery.token_accuracy,0);
 for(const edge of q.edges)assert.equal([...edge.from].filter((b,i)=>b!==edge.to[i]).length,1);
 assert.equal(new Set(q.nodes.map(n=>n.reading.source_id)).size,1);
 inspect(r,null,'0000');inspect(r,'0000','1000');inspect(r,'1000','0001');
 assert.equal(r.beqube.transitions.length,1);assert.equal(r.beqube.inspectionEvents[2].event,'jump');
 for(const t of r.beqube.transitions){assert(r.beqube.states.some(s=>s.id===t.beforeStateRef));assert(r.beqube.states.some(s=>s.id===t.afterStateRef));assert(r.beqube.interventions.some(i=>i.id===t.interventionId));}
 assert.throws(()=>inspect(r,'bad','0000'),/Unknown state/);
 const opaque=await analyze({mode:'opaque',source:'q q x',decoder_a:{q:'sun'},decoder_b:{}});
 assert(opaque.hypercube.nodes.every(n=>n.recovery===null));assert.equal(opaque.reference,null);
 const repeated=await analyze({...payload,source:'sun\nwater sun\tstone'});assert.equal(repeated.observation.source_id,r.observation.source_id);
 await assert.rejects(analyze({...payload,encoder:{sun:'q',water:'q',stone:'z'}}),/lossy/);
 await assert.rejects(analyze({...payload,allow_lossy:null}),/explicitly selected/);
 const lossy=await analyze({...payload,encoder:{sun:'q',water:'q',stone:'z'},allow_lossy:true});assert.equal(lossy.results[0].recovery.token_accuracy,.75);
 const odd=await analyze({mode:'opaque',source:'__proto__ q',decoder_a:JSON.parse('{"__proto__":"sun","q":"water"}'),decoder_b:{}});assert.equal(odd.results[0].reading.semantic_reading,'sun water');
 // Compare actual Python decoder scores/mappings for every context, not just graph shape.
 const {spawnSync}=require('node:child_process');
 const cases=[payload,
  {mode:'opaque',source:'q\u0085x\u001cq',decoder_a:{q:'sun',x:'water'},decoder_b:{}},
  {...payload,encoder:{sun:'q',water:'q',stone:'z'},allow_lossy:true},
  {mode:'opaque',source:'__proto__ q',decoder_a:JSON.parse('{"__proto__":"sun","q":"water"}'),decoder_b:{}},
  {mode:'opaque',source:'\ue000 😀 a',decoder_a:{'\ue000':'one','😀':'two',a:'three'},decoder_b:{}},
  {...payload,decoder_a:payload.decoder_b}];
 for(const sample of cases){
  const py=spawnSync(process.env.MIMULUS_TEST_PYTHON||'python3',['-c','import json,sys; from mimulus_decoder.interactive import analyze; r=analyze(json.load(sys.stdin)); r["observation"]["transcription"]=" ".join(r["observation"]["transcription"].split()); print(json.dumps(r))'],{input:JSON.stringify(sample),env:{...process.env,PYTHONPATH:'src'},encoding:'utf8',timeout:10000});
  assert.equal(py.status,0,py.stderr);const gold=JSON.parse(py.stdout),browser=await analyze(sample);
  assert.equal(browser.observation.transcription,gold.observation.transcription);
  for(let i=0;i<16;i++){const actual=browser.hypercube.nodes[i],expected=gold.hypercube.nodes[i];assert.deepEqual(actual.mapping,expected.mapping);assert.equal(actual.reading.semantic_reading,expected.reading.semantic_reading);assert.equal(actual.recovery?.token_accuracy,expected.recovery?.token_accuracy);assert.equal(actual.recovery?.unresolved_tokens,expected.recovery?.unresolved_tokens);}
 }
 console.log('Explorer hypercube checks passed: topology, references, interventions, opaque/lossy modes, and 96 Python parity contexts');
})().catch(e=>{console.error(e);process.exitCode=1});
