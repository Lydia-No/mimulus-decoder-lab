const fs=require('fs');
const path=require('path');
const H=require('./adapter.js');
const fixture=require('../fixtures/voynich/f113r/source.json');

function readJson(p){return JSON.parse(fs.readFileSync(p,'utf8'));}

function main(){
  const outdir=process.argv[2];
  if(!outdir) throw new Error('usage: node historical/compare_image_only.js OUTPUT_DIR');
  const input=H.buildHistoricalInput({fixture});
  if(!input.gate.historicalRunAllowed) throw new Error('historical gate closed: '+input.gate.blockers.join(','));
  const codes=['A2','B5','C8'];
  const runs=codes.map(code=>readJson(path.join(outdir,code+'.json')));
  for(const run of runs){
    if(run.source?.sha256!==fixture.source_layers.image.sha256) throw new Error(run.runId+' source hash mismatch against fixture');
  }
  const meta=H.compareFrozenRuns(runs,input);
  meta.runSet='f113r-image-only-001';
  meta.sourceSha256=fixture.source_layers.image.sha256;
  meta.boundary='Image-only historical comparison. Residue is persistence across these three declared visual decoders, not proof of language, translation, source truth, or decipherment.';
  fs.writeFileSync(path.join(outdir,'meta-observer.json'),JSON.stringify(meta,null,2)+'\n');
  console.log(JSON.stringify(meta,null,2));
}

main();
