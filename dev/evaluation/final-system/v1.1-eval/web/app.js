const $ = id => document.getElementById(id);
let state = {session:null, blocking_reasons:[]}, token, example, demoBrief, demoAvailable=false, busy = false, ready = false, generating = false, tab = 'requirements';
const answerDrafts = new Map();
const categories = ['requirements','goals','users','team_roles','contradictions','missing_information','questions','documents','sources'];
const titles = {team_roles:'Team roles',missing_information:'Gaps',contradictions:'Conflicts',questions:'Questions',documents:'Documents',sources:'Sources',requirements:'Requirements',goals:'Goals',users:'Users'};
function node(tag,text,cls){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;}
function evidence(parent,source){if(!source)return;parent.append(node('blockquote',`${source.document}: ${source.quote}`));}
function controls(){const s=state.session,locked=busy||generating;
 $('demo-brief').disabled=locked||!ready;$('demo-result').disabled=locked||!ready||!demoAvailable;
 $('analyze').disabled=locked||!ready;$('example').disabled=locked||!ready;$('reset').disabled=locked||!ready;
 const attempts=s?.generation_progress?.raci_attempts||0;
 $('generate').disabled=locked||!s||state.blocking_reasons.length>0||attempts>=2;
 $('generate').textContent=attempts>=2?'RACI failed after 2 attempts':attempts?'Retry RACI (attempt 2 of 2)':s?.approval?'Generate documents':'Approve & generate documents';
 $('request-changes').disabled=locked||!s;$('apply-changes').disabled=locked||!s;$('review-feedback').disabled=locked;
 $('download').disabled=locked||!s;document.querySelectorAll('.reply, #content textarea').forEach(b=>b.disabled=locked);
}

function render(){const s=state.session;controls();$('attempts').replaceChildren();if(s){const hash=s.approval?.revision_hash;for(const event of (s.events||[]).filter(e=>e.action==='raci_validation_failed'&&e.revision_hash===hash)){$('attempts').append(node('p',`RACI attempt ${event.attempt||1} failed: ${(event.errors||[]).join('; ')}`,'warn'));}const success=(s.events||[]).findLast(e=>e.action==='generate'&&e.revision_hash===hash);if(success?.raci_attempt>1)$('attempts').append(node('p',`RACI attempt ${success.raci_attempt} passed automatic checks.`,'badge'));}$('stats').replaceChildren();$('tabs').replaceChildren();if(!s){$('content').replaceChildren(node('p','Paste a brief or load the example to begin.'));$('blockers').textContent='Analyze a brief first.';return;}
 for(const key of ['requirements','questions','team_roles'])$('stats').append(node('span',`${s.analysis[key].length} ${titles[key].toLowerCase()}`,'badge'));
 if(s.demo_notice)$('stats').append(node('p',s.demo_notice,'warn'));
 $('stats').append(node('span',`Revision ${s.revision}${s.approval?' · Approved':''}`,'badge'));
 $('blockers').textContent=state.blocking_reasons.length?state.blocking_reasons.join('\n'):s.documents?'Document package passed automated checks; human content review is still required.':s.approval?'Requirements approved. Document generation and validation are still required.':'No blocking questions. Review requirements before approval.';
 $('blockers').className=state.blocking_reasons.length?'warn':'muted';
 for(const key of categories){const b=node('button',titles[key],tab===key?'active':'secondary');b.onclick=()=>{tab=key;render();};$('tabs').append(b);}
 const content=$('content');content.replaceChildren();
 if(tab==='documents'){if(!s.documents){if(s.generation_progress?.status==='raci_failed'){content.append(node('p','Tasks and acceptance criteria passed structural checks. RACI failed; no final document package was accepted. The first failure triggers one automatic repair. After two failures, review the errors and request changes. Content still needs human review.','warn'),node('pre',s.generation_progress.errors.join('\n')));const saved=node('details');saved.append(node('summary','Inspect saved tasks and criteria'),node('pre',JSON.stringify(s.generation_progress.work_plan,null,2)));content.append(saved);return;}content.append(node('p',s.planning_attempt?'Generation raised clarification questions. Answer them before approving again.':'No accepted documents yet. Resolve blockers, approve requirements, then generate.','muted'));return;}
 content.append(node('p','Draft for document review. Valid structure does not prove semantic correctness.','warn'));
 const docs=s.documents;
 content.append(node('h3','Specification - confirmed requirements'));
 for(const req of s.analysis.requirements){const card=node('article',undefined,'card');card.append(node('span',req.id,'id'),node('p',req.description));evidence(card,req.source);content.append(card);}
 content.append(node('h3','Implementation tasks'));
 for(const task of docs.tasks){content.append(node('h3',`${task.id}: ${task.title}`),node('p',task.description),node('p',`Requirements: ${task.requirement_ids.join(', ')}`,'muted'));}
 content.append(node('h3','Acceptance criteria'));
 for(const ac of docs.acceptance_criteria){const card=node('article',undefined,'card');card.append(node('span',`${ac.id} / ${ac.requirement_id}`,'id'),node('p',`Given: ${ac.given}`),node('p',`When: ${ac.when}`),node('p',`Then: ${ac.then}`));for(const source of ac.sources||[])evidence(card,source);content.append(card);}
 content.append(node('h3','RACI'));
 const names=new Map(s.analysis.team_roles.map(r=>[r.id,r.name]));
 for(const row of docs.raci){const card=node('article',undefined,'card');card.append(node('h3',`${row.id}: ${row.activity}`),node('p',`Tasks: ${row.task_ids.join(', ')||'Governance'}`,'muted'));for(const [key,label] of [['accountable','Accountable'],['responsible','Responsible'],['consulted','Consulted'],['informed','Informed']])card.append(node('p',`${label}: ${row[key].map(a=>names.get(a.role_id)||a.role_id).join(', ')||'-'}`));content.append(card);}
 const raw=node('details');raw.append(node('summary','Inspect full document JSON'),node('pre',JSON.stringify(docs,null,2)));content.append(raw);return;}
 if(tab==='sources'){for(const [id,text] of Object.entries(s.sources)){content.append(node('h3',id),node('blockquote',text));}return;}
 if(tab==='questions'){content.append(node('p','Fill in one or more answers, then click Apply answers & reanalyze. Blank answers are not sent. You do not have to answer all questions at once.','muted'));}
 const items=s.analysis[tab]||[];if(!items.length)content.append(node('p','No items in this category.','muted'));
 for(const item of items){const card=node('article',undefined,'card');card.append(node('span',item.id,'id'));if(item.kind)card.append(node('span',item.kind,'badge'));card.append(node('p',item.description||item.name||item.text||item.topic||''));if(item.why_needed)card.append(node('p',item.why_needed));if(item.requirement_ids)card.append(node('p',`Requirements: ${item.requirement_ids.join(', ')}`,'muted'));evidence(card,item.source);
 for(const duty of item.responsibilities||[]){card.append(node('p',duty.description));evidence(card,duty.source);}
 if(tab==='questions'){card.append(node('p',`${item.target_type}: ${item.target_id} · ${item.blocks_final_specification?'Blocks final specification':'Non-blocking'}`,'muted'));const answer=node('textarea');answer.placeholder='Your answer in English';answer.setAttribute('aria-label',`Answer ${item.id}`);answer.value=answerDrafts.get(item.id)||'';answer.disabled=busy;answer.oninput=()=>answerDrafts.set(item.id,answer.value);card.append(answer);}
 const details=node('details');details.append(node('summary','Inspect record'),node('pre',JSON.stringify(item,null,2)));card.append(details);content.append(card);}
 if(tab==='questions'&&items.length){const send=node('button','Apply answers & reanalyze','reply');send.disabled=busy;send.onclick=()=>{const answers=items.filter(q=>(answerDrafts.get(q.id)||'').trim()).map(q=>({question_id:q.id,text:answerDrafts.get(q.id)}));if(!answers.length){showError('Fill in at least one answer first.');return;}act({action:'reply_many',answers},'Applying answers and reanalyzing...');};content.append(send,node('p','One submission = one model request. If validation fails, your draft answers stay here and the previous analysis remains active.','muted'));}
 if(tab==='requirements'&&s.analysis.proposed_assumptions?.length){content.append(node('h3','Proposed assumptions — not confirmed requirements'),node('pre',JSON.stringify(s.analysis.proposed_assumptions,null,2)));}}
function showError(message){$('errors').replaceChildren(node('div',message,'error'));$('errors').hidden=false;$('errors').scrollIntoView({block:'nearest'});}
async function act(data,label){
 if(busy||!ready)return false;
 if(data.action==='start'&&!data.brief.trim()){showError('Enter a brief or click Load meeting-room example first.');$('brief').focus();return false;}
 busy=true;controls();$('errors').hidden=true;$('status').textContent=label;
 const started=Date.now(), timer=setInterval(()=>{$('status').textContent=`${label} ${Math.floor((Date.now()-started)/1000)}s - please wait`;},1000);
 const controller=new AbortController(), timeout=setTimeout(()=>controller.abort(),210000);
 try{
  const response=await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json','X-Demo-Token':token},body:JSON.stringify(data),signal:controller.signal});
  const result=await response.json();
  if(!response.ok){clearInterval(timer);showError([result.message,...(result.errors||['Request failed'])].filter(Boolean).join('\n\n'));$('status').textContent='Action rejected - last accepted session preserved';return false;}
  state=result;if(['reply_many','reset','start','load_demo'].includes(data.action))answerDrafts.clear();render();clearInterval(timer);$('status').textContent=data.action==='reset'?'Ready to analyze':state.session?.generation_progress?.status==='raci_failed'?'Tasks saved; RACI failed - see attempt details':'Done - review the result';return true;
 }catch(e){clearInterval(timer);showError(e.name==='AbortError'?'No response within 210 seconds. The server may still be working. Reload the page to check the session before retrying.':'Could not complete the request. Check that web_ui.py is running and reload this page.');$('status').textContent='Request failed';return false;}
 finally{clearInterval(timer);clearTimeout(timeout);busy=false;controls();}
}
$('demo-brief').onclick=()=>{$('brief').value=demoBrief;};
$('demo-result').onclick=()=>{if(!state.session||confirm('Replace this session with a saved live demonstration? Download the current session first if needed.')){tab='documents';act({action:'load_demo'},'Loading saved live demonstration...');}};
$('example').onclick=()=>{$('brief').value=example;};
$('analyze').onclick=()=>{if(!state.session||confirm('Replace the current session? Download it first if needed.'))act({action:'start',brief:$('brief').value},'Analyzing with Gemini…');};
$('reset').onclick=async()=>{if(!state.session||confirm('Clear this session? Download it first if needed.')){if(await act({action:'reset'},'Clearing session…')){$('brief').value='';$('review-feedback').value='';}}};
$('request-changes').onclick=()=>{$('review-editor').hidden=false;$('review-feedback').focus();};
$('apply-changes').onclick=async()=>{if(await act({action:'request_changes',text:$('review-feedback').value},'Applying reviewer corrections...')){$('review-feedback').value='';$('review-editor').hidden=true;}};
$('generate').onclick=async()=>{if(generating||busy)return;generating=true;tab='documents';controls();try{await generateWithOneRepair((action,label)=>act({action},label),()=>state,message=>{$('status').textContent=message;});}finally{generating=false;controls();}};
$('download').onclick=()=>{const blob=new Blob([JSON.stringify(state.session,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=node('a');a.href=url;a.download='ba-demo.session.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
controls();
fetch('/api/state',{signal:AbortSignal.timeout(10000)}).then(r=>{if(!r.ok)throw Error();return r.json();}).then(data=>{token=data.token;example=data.example;demoBrief=data.demo_brief;demoAvailable=data.demo_available;state=data;ready=true;$('model').textContent=`Model: ${data.model}`;if(state.session)$('brief').value=state.session.sources.brief;render();$('status').textContent='Ready to analyze';}).catch(()=>{showError('Cannot initialize the interface. Open http://127.0.0.1:8000 and reload the page.');$('status').textContent='Connection failed';});
