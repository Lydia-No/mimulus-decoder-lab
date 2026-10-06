const M=require('./engine.js');
function assert(ok,msg){if(!ok)throw new Error(msg);}
function eq(a,b){return JSON.stringify(a)===JSON.stringify(b);}

const originalReset=M.run({condition:'original',historyIntervention:'reset'});
assert(eq(originalReset.blindedFamilyOutputs.map(x=>x.boundaries),[[4,8],[4,8],[4,8]]),'original/reset should produce [4,8] in all three decoder families');
assert(originalReset.metaObservation.features.length===2,'original/reset should expose two candidate features');
assert(originalReset.metaObservation.features.every(x=>x.classification==='SOURCE_SUPPORTED_INVARIANT'),'original/reset boundaries should be source-supported invariants');
assert(originalReset.historyControls.patternPass===true,'original source should pass the declared history control pattern');

const originalTrained=M.run({condition:'original',historyIntervention:'trained'});
assert(eq(originalTrained.blindedFamilyOutputs.map(x=>x.boundaries),[[4,8],[4,8],[]]),'trained history consensus should diverge from the two non-history families');
assert(originalTrained.metaObservation.features.every(x=>x.classification==='DECODER_DEPENDENT_SUPPORTED'),'trained-history loss should be classified as decoder-dependent, not source absence');

const permutedReset=M.run({condition:'permuted',historyIntervention:'reset'});
assert(eq(permutedReset.knownAnswer.boundaryIndices,[]),'permuted condition must have no known A-B-A boundaries');
assert(permutedReset.metaObservation.features.length>0,'permuted condition should provoke unsupported candidate boundaries');
assert(permutedReset.metaObservation.features.every(x=>!x.inKnownAnswer),'permuted candidates must remain outside the answer key');
assert(permutedReset.metaObservation.features.every(x=>x.classification.includes('UNSUPPORTED')),'permuted candidate structure must be labeled unsupported');

const ablatedTrained=M.run({condition:'ablated',historyIntervention:'trained'});
assert(eq(ablatedTrained.decoderDetails.Q7.boundaries,[]),'contrast ablation should remove local-delta boundaries');
assert(eq(ablatedTrained.decoderDetails.L4.boundaries,[4,8]),'motif recurrence should still recover the preserved block positions');
assert(ablatedTrained.historyControls.patternPass===false,'contrast ablation should eliminate the designed history divergence pattern');

const matrix=M.matrix();
assert(matrix.runs.length===12,'matrix must contain 3 source conditions × 4 history interventions = 12 cells');
console.log('Pilot 001 assertions passed:',matrix.runs.length,'cells');
