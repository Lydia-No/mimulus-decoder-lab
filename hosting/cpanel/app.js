const $=id=>document.getElementById(id);
const state={image:'',action:null,runs:[],parentRunId:null,parentLabel:null};
const actionLabels={look:'Look',decode:'Decode',translate:'Translate',branch:'Branch',test:'Test',compare:'Compare'};

function setView(id){
  document.querySelectorAll('.view').forEach(v=>v.classList.toggle('is-active',v.id===id));
  document.querySelectorAll('.tab').forEach(b=>b.classList.toggle('is-active',b.dataset.view===id));
  window.scrollTo({top:0,behavior:'smooth'});
}
document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>setView(b.dataset.view)));
document.querySelectorAll('[data-go]').forEach(b=>b.addEventListener('click',e=>{e.preventDefault();setView(b.dataset.go)}));

$('imageInput').addEventListener('change',()=>{
  const f=$('imageInput').files[0];state.image='';$('preview').hidden=true;
  if(!f)return updateSourceState();
  if(f.size>5_500_000){$('status').textContent='Use a crop under about 5 MB.';return;}
  const r=new FileReader();r.onload=()=>{state.image=r.result;$('preview').src=state.image;$('preview').hidden=false;updateSourceState();};r.readAsDataURL(f);
});
$('sourceText').addEventListener('input',updateSourceState);$('question').addEventListener('input',updateSourceState);

function hasSource(){return Boolean(state.image||$('sourceText').value.trim()||$('question').value.trim())}
function updateSourceState(){
  $('sourceState').textContent=hasSource()?'source ready':'waiting for source';
  $('runButton').disabled=!state.action||(!hasSource()&&state.action!=='compare');
}

function selectAction(action){
  state.action=action;
  document.querySelectorAll('.action').forEach(b=>b.classList.toggle('is-selected',b.dataset.action===action));
  $('translateOptions').hidden=action!=='translate';
  $('testOptions').hidden=action!=='test';
  $('runButton').textContent=action==='compare'?'Compare branches':`${actionLabels[action]} this`;
  if(action==='compare'&&state.runs.length<2){$('status').textContent='Create at least two branches first.';}else{$('status').textContent='';}
  updateSourceState();
}
document.querySelectorAll('.action').forEach(b=>b.addEventListener('click',()=>selectAction(b.dataset.action)));

function modeFor(action){return ({look:'observe',decode:'decode',translate:'translate',branch:'branch',test:'test',compare:'compare'})[action]||'explore'}
function composedNote(){
  const parts=[];
  if($('question').value.trim())parts.push($('question').value.trim());
  if(state.action==='test'&&$('hypothesis').value.trim())parts.push(`HYPOTHESIS TO TEST:\n${$('hypothesis').value.trim()}`);
  if(state.action==='compare'){
    parts.push('COMPARE THESE BRANCHES FROM THE SAME EXPLORATION TRAIL:\n'+state.runs.slice(-6).map((r,i)=>`BRANCH ${i+1} [${r.action}]\n${r.output}`).join('\n\n'));
  }
  if(state.parentRunId)parts.push(`PARENT RUN: ${state.parentRunId}${state.parentLabel?` (${state.parentLabel})`:''}. Treat supplied text as descendant material, not as an independent source.`);
  return parts.join('\n\n');
}

async function run(){
  if(!state.action)return;
  if(state.action==='compare'&&state.runs.length<2){$('status').textContent='Create at least two branches first.';return;}
  if(!hasSource()&&state.action!=='compare')return;
  $('runButton').disabled=true;$('status').textContent=`${actionLabels[state.action]} running…`;
  const payload={
    image_data_url:state.action==='compare'?undefined:(state.image||undefined),
    transcription:state.action==='compare'?'':$('sourceText').value,
    note:composedNote(),mode:modeFor(state.action),profile:$('profile').value,
    action:state.action,target_language:$('targetLanguage').value.trim()||'English',
    parent_run_id:state.parentRunId||undefined,parent_label:state.parentLabel||undefined
  };
  try{
    const headers={'Content-Type':'application/json'};const token=$('token').value.trim();if(token)headers['x-mimulus-explorer-token']=token;
    const res=await fetch('/api/explore',{method:'POST',headers,body:JSON.stringify(payload)});
    const data=await res.json();if(!res.ok)throw new Error(data.detail||data.error||'Request failed');
    const record={...data,action:state.action,parent_run_id:state.parentRunId||data.parent_run_id||null,target_language:payload.target_language,created_at:new Date().toISOString()};
    state.runs.push(record);state.parentRunId=null;state.parentLabel=null;renderRuns();
    $('status').textContent=`${actionLabels[state.action]} complete.`;
  }catch(err){$('status').textContent=err.message||String(err)}finally{$('runButton').disabled=false;updateSourceState()}
}
$('runButton').addEventListener('click',run);

function escapeHtml(s=''){return s.replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[m])}
function lineageText(r){
  if(r.parent_run_id)return `Derived from run ${r.parent_run_id}. This branch inherits that run's assumptions; it is not independent evidence from the original source.`;
  if(r.action==='translate')return `Translation from the supplied representation. Useful as an interpretation layer, not independent confirmation of the source.`;
  return `Direct branch from the supplied source/representation. Independence depends on what assumptions changed, not on the number of runs.`;
}
function renderRuns(){
  $('emptyState').hidden=state.runs.length>0;$('clearRuns').disabled=!state.runs.length;$('exportRuns').disabled=!state.runs.length;
  $('runs').innerHTML=state.runs.map((r,i)=>`<article class="run-card" data-i="${i}"><div class="run-head"><div><span class="run-kicker">${escapeHtml(actionLabels[r.action]||r.action||'Run')}</span><h3>${escapeHtml(titleFor(r))}</h3></div><div class="run-meta">${escapeHtml(r.run_id||'local')}<br>${escapeHtml(r.model||'')}</div></div><div class="run-output">${escapeHtml(r.output||'(No output)')}</div><div class="lineage">${escapeHtml(lineageText(r))}</div><div class="run-actions"><button data-next="branch">Branch this</button><button data-next="translate">Translate this</button><button data-next="test">Test this</button><button data-copy>Copy</button></div></article>`).join('');
  document.querySelectorAll('.run-card').forEach(card=>{
    const r=state.runs[Number(card.dataset.i)];
    card.querySelectorAll('[data-next]').forEach(b=>b.onclick=()=>useRun(r,b.dataset.next));
    card.querySelector('[data-copy]').onclick=()=>navigator.clipboard.writeText(r.output||'');
  });
}
function titleFor(r){
  if(r.action==='translate')return `Translation → ${r.target_language||'target language'}`;
  if(r.action==='decode')return 'Candidate decoding';
  if(r.action==='compare')return 'Cross-branch residue';
  if(r.action==='test')return 'Hypothesis stress test';
  if(r.action==='branch')return 'Competing branch';
  return 'Source observations';
}
function useRun(r,next){
  $('sourceText').value=r.output||'';state.image='';$('preview').hidden=true;$('imageInput').value='';
  state.parentRunId=r.run_id||`local-${state.runs.indexOf(r)+1}`;state.parentLabel=titleFor(r);selectAction(next);updateSourceState();
  document.querySelector('.workspace').scrollIntoView({behavior:'smooth',block:'start'});
  $('status').textContent=`Using ${state.parentLabel} as descendant input. Lineage will be preserved.`;
}
$('clearRuns').onclick=()=>{state.runs=[];state.parentRunId=null;state.parentLabel=null;renderRuns();$('status').textContent='Trail cleared locally.'};
$('exportRuns').onclick=()=>{const blob=new Blob([JSON.stringify({object:'mimulus_greenhouse_trail',exported_at:new Date().toISOString(),runs:state.runs},null,2)],{type:'application/json'});const u=URL.createObjectURL(blob);const a=document.createElement('a');a.href=u;a.download='mimulus-trail.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000)};

let path='abc';
function renderPath(){
  const gateOff=$('gateToggle').checked;const reachable=path==='abc'||gateOff;
  $('futureState').className=`future ${reachable?'open':'closed'}`;
  $('futureState').innerHTML=`<small>future</small><strong>${reachable?'1111 reachable':'1111 blocked'}</strong>`;
  $('pathExplanation').textContent=path==='abc'?'A happened before B. The history-sensitive gate is satisfied, so the final transition remains available.':gateOff?'B happened before A, but the history gate has been removed. The previously lost future is reopened.':'B happened before A. The present state is still 1110, but the baseline history gate blocks the final transition.';
  document.querySelectorAll('.path-choice').forEach(b=>b.classList.toggle('is-active',b.dataset.path===path));
}
document.querySelectorAll('.path-choice').forEach(b=>b.onclick=()=>{path=b.dataset.path;renderPath()});$('gateToggle').onchange=renderPath;renderPath();renderRuns();updateSourceState();
