let cubeSelection=null;
function cubeSvg(tag,attributes){const el=document.createElementNS('http://www.w3.org/2000/svg',tag);for(const [key,value] of Object.entries(attributes))el.setAttribute(key,value);return el}
function cubePosition(bits){return {x:55+bits[0]*160+bits[2]*65+bits[3]*420,y:45+bits[1]*160+bits[2]*65}}
function renderHypercube(report){
  const cube=report.hypercube,svg=$('cube-diagram');svg.replaceChildren();report.inspection_trace=[];cubeSelection=null;
  const positions=new Map(cube.nodes.map(n=>[n.id,cubePosition(n.bits)]));
  const colors=['#85c3a0','#e4b57a','#8eabed','#c3a0db'];
  for(const edge of cube.edges){const a=positions.get(edge.from),b=positions.get(edge.to),axis=cube.axes.findIndex(x=>x.id===edge.axis);svg.append(cubeSvg('line',{x1:a.x,y1:a.y,x2:b.x,y2:b.y,stroke:colors[axis],'stroke-opacity':.4,'stroke-width':1.5}))}
  for(const item of cube.nodes){const p=positions.get(item.id),g=cubeSvg('g',{role:'button',tabindex:'0','aria-label':`Context ${item.id}`,'data-vertex':item.id});g.append(cubeSvg('circle',{cx:p.x,cy:p.y,r:19,fill:'#172b21',stroke:'#7d9c85','stroke-width':2}));const text=cubeSvg('text',{x:p.x,y:p.y+4,fill:'#eef5ef','text-anchor':'middle','font-size':12});text.textContent=item.id;g.append(text);const score=cubeSvg('text',{x:p.x,y:p.y+35,fill:'#b8c8bd','text-anchor':'middle','font-size':12});score.textContent=item.recovery?`${Math.round(item.recovery.token_accuracy*100)}%`:'no reference';g.append(score);g.onclick=()=>selectCubeVertex(item.id);g.onkeydown=event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();selectCubeVertex(item.id)}};svg.append(g)}
  $('cube-boundary').textContent=cube.boundary;
  selectCubeVertex('0000');
}
function selectCubeVertex(id){
  if(!lastReport)return;const cube=lastReport.hypercube,item=cube.nodes.find(n=>n.id===id);if(!item||id===cubeSelection)return;
  const before=cubeSelection,changed=before?[...id].map((bit,i)=>bit!==before[i]?i:-1).filter(i=>i>=0):[];
  MimulusTokenCube.inspect(lastReport,before,id);
  lastReport.inspection_trace.push({from:before,to:id,event:!before?'start':changed.length===1?'axis_transition':'jump',axis:changed.length===1?cube.axes[changed[0]].id:null,at:new Date().toISOString()});cubeSelection=id;
  document.querySelectorAll('[data-vertex]').forEach(g=>{const selected=g.getAttribute('data-vertex')===id;g.setAttribute('aria-pressed',String(selected));g.querySelector('circle').setAttribute('fill',selected?'#466b50':'#172b21')});
  $('selected-context').textContent=`Context ${id}`;$('cube-assumptions').replaceChildren();$('cube-axis-controls').replaceChildren();
  for(let axis=0;axis<cube.axes.length;axis++){const config=cube.axes[axis];$('cube-assumptions').append(node('li',`${config.label}: ${config.choices[item.bits[axis]]}`));const button=node('button',`Change ${config.label}`,'secondary');button.type='button';button.onclick=()=>{const bits=[...item.bits];bits[axis]=1-bits[axis];selectCubeVertex(bits.join(''))};$('cube-axis-controls').append(button)}
  $('cube-output').textContent=item.reading.semantic_reading||'No candidate output';$('cube-mapping').textContent=Object.entries(item.mapping).map(([from,to])=>`${from} → ${to}`).join(' · ')||'No active mappings';
  $('cube-score').textContent=item.recovery?`${Math.round(item.recovery.token_accuracy*100)}% recovered · ${item.recovery.unresolved_tokens} unresolved`:'Recovery unavailable: no known original';
  $('cube-uncertainty').replaceChildren();for(const text of item.reading.uncertainties)$('cube-uncertainty').append(node('li',text));
  $('cube-trace').textContent=lastReport.inspection_trace.map(e=>`${e.event==='jump'?'↪ ':''}${e.to}`).join(' → ');
  $('export-panel').hidden=true;$('export-json').value='';
}
