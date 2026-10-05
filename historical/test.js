const H=require('./adapter.js');
const fixture=require('../fixtures/voynich/f113r/source.json');
function assert(ok,msg){if(!ok)throw new Error(msg);}

const current=H.buildHistoricalInput({fixture});
assert(current.gate.historicalRunAllowed===true,'current f113r source-image gate should be open after authority byte freeze');
assert(current.gate.blockers.length===0,'image-only f113r input should have no provenance blockers');
assert(current.source.image.sha256==='ad748f9012b174be520b7ac837fdadf913e49a696323920ca655ecf5474afb5c','live fixture must retain the authority JPEG hash');

const malformedTranscription={
  status:'frozen',
  sha256:'not-a-real-sha',
  convention:'declared-test-convention',
  version:'test'
};
const blocked=H.buildHistoricalInput({fixture,transcription:malformedTranscription});
assert(blocked.gate.historicalRunAllowed===false,'malformed transcription provenance must close the historical gate');
assert(blocked.gate.blockers.includes('TRANSCRIPTION_PROVENANCE_INCOMPLETE'),'malformed transcription must report its provenance blocker');

const validTranscription={
  status:'frozen',
  sha256:'b'.repeat(64),
  convention:'declared-test-convention',
  version:'test-1.0'
};
const input=H.buildHistoricalInput({fixture,transcription:validTranscription});
assert(input.gate.historicalRunAllowed===true,'properly frozen transcription provenance should preserve the open historical gate');

const runs=[
  {
    runId:'r1',frozen:true,
    decoder:{blindCode:'A2',version:'1.0',assumptions:['structural recurrence only']},
    claims:[
      {claimKey:'boundary-x',target:'region-x',proposition:'boundary present',evidence:[{layer:'SOURCE_IMAGE',locator:'region-x'}]},
      {claimKey:'reading-z',target:'region-z',proposition:'reading alpha',evidence:[{layer:'DERIVED_STRUCTURE',locator:'node-7'}]}
    ]
  },
  {
    runId:'r2',frozen:true,
    decoder:{blindCode:'B5',version:'1.0',assumptions:['layout relation only']},
    claims:[
      {claimKey:'boundary-x',target:'region-x',proposition:'boundary present',evidence:[{layer:'SOURCE_IMAGE',locator:'region-x'}]},
      {claimKey:'reading-z',target:'region-z',proposition:'reading beta',evidence:[{layer:'DERIVED_STRUCTURE',locator:'node-3'}]}
    ]
  },
  {
    runId:'r3',frozen:true,
    decoder:{blindCode:'C8',version:'1.0',assumptions:['declared transcription relation']},
    claims:[
      {claimKey:'boundary-x',target:'region-x',proposition:'boundary present',evidence:[{layer:'SOURCE_IMAGE',locator:'region-x'}]},
      {claimKey:'solo-q',target:'region-q',proposition:'candidate q',evidence:[{layer:'DERIVED_STRUCTURE',locator:'node-9'}]}
    ]
  }
];

const meta=H.compareFrozenRuns(runs,input);
const boundary=meta.observations.find(x=>x.claimKey==='boundary-x');
const conflict=meta.observations.find(x=>x.claimKey==='reading-z');
const solo=meta.observations.find(x=>x.claimKey==='solo-q');
assert(boundary.classification==='CROSS_DECODER_RESIDUE','all-decoder agreement must be residue, not source truth');
assert(conflict.classification==='INCOMPATIBLE_READINGS','incompatible propositions must remain explicit');
assert(solo.classification==='DECODER_SPECIFIC','single-decoder claim must remain decoder-specific');
assert(!meta.observations.some(x=>x.classification.includes('SOURCE_SUPPORTED')),'historical comparison must never emit known-answer source-support labels');
assert(meta.forbiddenInference.includes('SOURCE_SUPPORTED_INVARIANT'),'historical meta-record must explicitly forbid synthetic known-answer inference');
console.log('Historical adapter assertions passed:',meta.observations.length,'meta-observations; live f113r image gate is open');
