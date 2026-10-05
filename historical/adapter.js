/* Research direction, conceptual framing and methodology: Linda Thorstensen. */
(function(root){
const SYNTHETIC_GATE={
  artifact:'results/pilot-001/frozen-summary.json',
  engineBlobSha:'aa5a5cce53ee848fba773074505c014c9e4e48b7',
  fixtureId:'synthetic-decoder-persistence-001',
  fixtureVersion:'1.0',
  status:'frozen_pass'
};

function uniq(xs){return [...new Set(xs)];}
function stableSort(xs){return [...xs].sort((a,b)=>String(a).localeCompare(String(b)));}
function assertString(value,name){if(typeof value!=='string'||!value.trim())throw new Error(name+' must be a non-empty string');}
function hasFrozenImage(image){return !!(image&&image.status==='frozen'&&typeof image.sha256==='string'&&image.sha256.length===64&&image.extraction&&image.extraction.status==='frozen');}
function validTranscription(t){
  if(!t) return true;
  return t.status==='frozen'&&typeof t.sha256==='string'&&t.sha256.length===64&&typeof t.convention==='string'&&t.convention.trim()&&typeof t.version==='string'&&t.version.trim();
}

function buildHistoricalInput({fixture,transcription=null,layoutObservations=[],preprocessing=[]}={}){
  if(!fixture||typeof fixture!=='object')throw new Error('fixture is required');
  assertString(fixture.fixture_id,'fixture.fixture_id');
  assertString(fixture.source_id,'fixture.source_id');
  assertString(fixture.folio,'fixture.folio');
  const sourceImage=fixture.source_layers&&fixture.source_layers.image?fixture.source_layers.image:null;
  const blockers=[];
  if(!hasFrozenImage(sourceImage)) blockers.push('SOURCE_IMAGE_NOT_FROZEN');
  if(transcription&&!validTranscription(transcription)) blockers.push('TRANSCRIPTION_PROVENANCE_INCOMPLETE');
  if(fixture.experimental_boundary&&fixture.experimental_boundary.require_synthetic_gate_before_historical_run&&SYNTHETIC_GATE.status!=='frozen_pass') blockers.push('SYNTHETIC_GATE_NOT_PASSED');
  const record={
    version:'historical-input-0.1',
    fixture:{id:fixture.fixture_id,sourceId:fixture.source_id,folio:fixture.folio,authorityPointer:fixture.source_region&&fixture.source_region.authority_pointer||null},
    syntheticGate:{...SYNTHETIC_GATE},
    source:{
      image:sourceImage,
      transcription,
      layoutObservations:[...layoutObservations],
      preprocessing:[...preprocessing]
    },
    gate:{
      historicalRunAllowed:blockers.length===0,
      blockers
    },
    layerPolicy:{
      sourceImage:'SOURCE_IMAGE',
      transcription:'TRANSCRIPTION',
      preprocessing:'PREPROCESSING',
      decoderOutput:'DERIVED_STRUCTURE',
      semanticReading:'CANDIDATE_INTERPRETATION',
      comparison:'META_OBSERVATION'
    },
    interpretationBoundary:'Historical records have no independent answer key. Cross-decoder agreement must not be labeled source-supported, correct, true, translated or deciphered solely because decoders agree.'
  };
  return record;
}

function validateRun(run,input){
  if(!input||!input.gate||input.gate.historicalRunAllowed!==true)throw new Error('Historical input gate is closed');
  if(!run||typeof run!=='object')throw new Error('run is required');
  assertString(run.runId,'run.runId');
  if(run.frozen!==true)throw new Error('run must be frozen before comparison');
  if(!run.decoder||typeof run.decoder!=='object')throw new Error('run.decoder is required');
  assertString(run.decoder.blindCode,'run.decoder.blindCode');
  assertString(run.decoder.version,'run.decoder.version');
  if(!Array.isArray(run.decoder.assumptions))throw new Error('run.decoder.assumptions must be an array');
  if(!Array.isArray(run.claims))throw new Error('run.claims must be an array');
  for(const claim of run.claims){
    assertString(claim.claimKey,'claim.claimKey');
    assertString(claim.target,'claim.target');
    assertString(claim.proposition,'claim.proposition');
    if(!Array.isArray(claim.evidence)||!claim.evidence.length)throw new Error('claim.evidence must contain explicit provenance');
    for(const ev of claim.evidence){
      if(!['SOURCE_IMAGE','TRANSCRIPTION','PREPROCESSING','DERIVED_STRUCTURE'].includes(ev.layer))throw new Error('unsupported evidence layer: '+ev.layer);
      assertString(ev.locator,'evidence.locator');
    }
  }
  return true;
}

function compareFrozenRuns(runs,input){
  if(!Array.isArray(runs)||runs.length<2)throw new Error('at least two frozen runs are required');
  runs.forEach(r=>validateRun(r,input));
  const codes=runs.map(r=>r.decoder.blindCode);
  if(uniq(codes).length!==codes.length)throw new Error('decoder blind codes must be unique across compared runs');
  const byClaim=new Map();
  for(const run of runs){
    for(const claim of run.claims){
      const item=byClaim.get(claim.claimKey)||{claimKey:claim.claimKey,target:claim.target,propositions:new Map(),supportingDecoders:[]};
      const p=item.propositions.get(claim.proposition)||[];p.push(run.decoder.blindCode);item.propositions.set(claim.proposition,p);item.supportingDecoders.push(run.decoder.blindCode);byClaim.set(claim.claimKey,item);
    }
  }
  const observations=[];
  for(const item of byClaim.values()){
    const propositionEntries=[...item.propositions.entries()].map(([proposition,support])=>({proposition,supportingDecoders:stableSort(support)}));
    const supporting=uniq(item.supportingDecoders);
    let classification;
    if(propositionEntries.length>1) classification='INCOMPATIBLE_READINGS';
    else if(supporting.length===runs.length) classification='CROSS_DECODER_RESIDUE';
    else if(supporting.length>1) classification='PARTIAL_CROSS_DECODER_RESIDUE';
    else classification='DECODER_SPECIFIC';
    observations.push({claimKey:item.claimKey,target:item.target,classification,supportCount:supporting.length,totalDecoders:runs.length,propositions:propositionEntries});
  }
  observations.sort((a,b)=>a.claimKey.localeCompare(b.claimKey));
  return {
    version:'historical-meta-observer-0.1',
    fixture:input.fixture,
    comparedDecoders:stableSort(codes),
    observations,
    forbiddenInference:['SOURCE_SUPPORTED_INVARIANT','DECODER_DEPENDENT_SUPPORTED','CORRECT_TRANSLATION','HISTORICAL_TRUTH'],
    scope:'Agreement is a historical meta-observation only. Without an independent answer key, these classifications describe persistence or conflict across frozen decoder outputs, not correctness.'
  };
}

const api={SYNTHETIC_GATE,hasFrozenImage,validTranscription,buildHistoricalInput,validateRun,compareFrozenRuns};
if(typeof module!=='undefined'&&module.exports)module.exports=api;root.MimulusHistorical=api;
})(typeof globalThis!=='undefined'?globalThis:this);
