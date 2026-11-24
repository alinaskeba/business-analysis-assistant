"""Build a unified evaluation report, standalone architecture diagram and editable Word draft."""
import copy
import hashlib
import json
from pathlib import Path
import shutil

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

from ba_assistant import ba_workflow as wf
from scripts import collect_test_evaluation as collect
from .report_docx import Document

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports'


def ratio(n, d):
    return {'numerator': n, 'denominator': d, 'value': n/d if d else None}


def downstream_review():
    source = ROOT / 'dev/evaluation/ui-raci-pass-01/after.session.json'
    session = collect.read(source)
    wf.render_documents(session)
    docs, analysis = session['documents'], session['analysis']
    ac_decisions = {
        'AC1': ('unsupported_precondition', 'Staff sign-in is not a confirmed product policy; S12 supports create permission, not authentication.'),
        'AC2': ('unsupported_precondition', 'Staff sign-in is not established by the account-creation source.'),
        'AC3': ('faithful', 'Available-product browsing and a displayed list are supported.'),
        'AC4': ('faithful', 'Customer, available product, add action and cart result are preserved.'),
        'AC5': ('faithful', 'Signed-in customer, selected items and quantities match the full supplied facts; cited S14 alone omits the sign-in condition.'),
        'AC6': ('faithful', 'Guest browsing without sign-in is supported.'),
        'AC7': ('partial_test_definition', 'Does not explicitly assert that no order exists until successful sign-in; processing is less precise than placement.'),
        'AC8': ('faithful', 'Positive integer update is observable and checks the requested value; negative quantity scenarios are still missing at requirement level.'),
        'AC9': ('faithful', 'Removal produces an observable absence from the cart.'),
        'AC10': ('faithful', 'Both allowed staff roles and product update are retained.'),
        'AC11': ('faithful', 'Both allowed staff roles and account update are retained.'),
        'AC12': ('faithful', 'Reference display follows successful creation; uniqueness is not invented.'),
        'AC13': ('partial_test_definition', 'No-order rejection is correct, but a signed-in precondition is needed to isolate empty-cart failure from access failure.')}
    criteria = []
    reqs = {r['id']: r for r in analysis['requirements']}
    for item in docs['acceptance_criteria']:
        verdict, note = ac_decisions[item['id']]
        criteria.append({'id': item['id'], 'requirement_id': item['requirement_id'],
            'judgment': verdict, 'reason': note, 'actual': item,
            'requirement_source': reqs[item['requirement_id']]['source'],
            'source_support_note': 'Incomplete citation set: add sign-in evidence S10.' if item['id']=='AC5' else 'See judgment and original resolved sources.'})
    tasks = [{'id': t['id'], 'judgment': 'unsupported_scope_expansion' if t['id']=='TASK1' else 'faithful',
              'reason': 'CRUD introduces deletion beyond supplied create/update operations.' if t['id']=='TASK1' else 'The described work stays within the linked supplied scope.',
              'actual': t, 'linked_sources': [reqs[r]['source'] for r in t['requirement_ids']]} for t in docs['tasks']]
    assignments = []
    for row in docs['raci']:
        for code in ('accountable','responsible','consulted','informed'):
            for item in row[code]:
                established = not (row['id']=='RA4' and code=='consulted')
                assignments.append({'activity_id': row['id'], 'activity_type': row['activity_type'],
                    'assignment': code, 'role_id': item['role_id'], 'explicitly_supported': established,
                    'reason': 'A/R duty is supported by the resolved authority evidence.' if established else 'S7 describes QA testing duties, not an explicit consultation assignment for accepting UAT results.',
                    'sources': item['sources']})
    dataset = collect.read(ROOT / 'dev/cases/ba_dev_cases.json')
    case = next(c for c in dataset['cases'] if c['case_id']=='PURE_002_without_team')
    original_checks = case['expected_journey']['raci']['semantic_checks']
    matches = [('pass',['RA1']),('pass',['RA2']),('partial',['RA6']),('missing',[]),
               ('pass',['RA5']),('pass',['RA3']),('missing',[]),('partial',['RA6'])]
    raci_checks = [{'expected_index': i, 'expected': expected, 'judgment': verdict,
                    'actual_activity_ids': refs} for i, (expected,(verdict,refs)) in enumerate(zip(original_checks,matches))]
    spec_reqs = docs['specification']['functional_requirements'] + docs['specification']['quality_requirements_and_constraints']
    same_spec = docs['specification'] == wf.specification(session)
    preserved = sum(r in spec_reqs for r in analysis['requirements'])
    implementable = {r['id'] for r in analysis['requirements'] if r['kind']!='constraint'}
    covered_tasks = {rid for t in docs['tasks'] for rid in t['requirement_ids']}
    covered_ac = {a['requirement_id'] for a in docs['acceptance_criteria']}
    assessment = {
        'status':'single_assistant_content_review',
        'scope':'Retrospective development-output review; not a final-test or fresh end-to-end success.',
        'source_artifact':str(source.relative_to(ROOT)), 'source_sha256':collect.sha(source),
        'approval_origin':'Simulated approval and reconstructed checkpoint in the original UI experiment.',
        'specification':{'exact_current_analysis_copy':same_spec,'requirement_preservation':ratio(preserved,len(analysis['requirements'])),
                         'section_presence':ratio(len(docs['specification']),9),'assumption_note':'Separate assumptions section exists; this saved example contains no proposed assumptions.'},
        'tasks':tasks,'criteria':criteria,'raci_assignments':assignments,'raci_expected_checks':raci_checks,
        'metrics':{'task_link_coverage':ratio(len(implementable & covered_tasks),len(implementable)),
                   'criterion_link_coverage':ratio(len(implementable & covered_ac),len(implementable)),
                   'scope_faithful_tasks':ratio(sum(t['judgment']=='faithful' for t in tasks),len(tasks)),
                   'faithful_criterion_wording':ratio(sum(a['judgment']=='faithful' for a in criteria),len(criteria)),
                   'structural_raci_rows':ratio(sum(len(r['accountable'])==1 and bool(r['responsible']) for r in docs['raci']),len(docs['raci'])),
                   'explicit_raci_assignment_support':ratio(sum(a['explicitly_supported'] for a in assignments),len(assignments)),
                   'strict_raci_expected_checks':ratio(sum(c['judgment']=='pass' for c in raci_checks),len(raci_checks))}}
    assert same_spec and preserved==16 and len(criteria)==13 and len(assignments)==13 and len(raci_checks)==8
    return assessment


def architecture():
    plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none'})
    fig, ax = plt.subplots(figsize=(17,10.6))
    fig.patch.set_facecolor('white');ax.set(xlim=(0,17),ylim=(-.5,10.5));ax.axis('off')
    ax.text(.5,10.05,'Business Analysis Assistant — system data flow',fontsize=23,weight='bold',color='#173456')
    ax.text(.5,9.6,'Frozen v1.2-eval · English input/output · Local Python + Gemini API · Human approval before documents',fontsize=12,color='#526078')
    nodes={
      'input':(2,8.4,'1. User / local web UI','Brief, replies, reviewer changes','human'),
      'session':(6.25,8.4,'2. Source-aware session','brief + A-IDs; revision history','python'),
      'analysis':(10.5,8.4,'3. Gemini: analysis','Facts, gaps, conflicts, questions','model'),
      'av':(14.75,8.4,'4. Analysis checks','Schema, quotes and references','python'),
      'review':(14.75,5.8,'5. Human review','Answer / correct / approve','human'),
      'gate':(10.5,5.8,'6. Approval gate','No blockers; revision-bound approval','python'),
      'registry':(6.25,5.8,'7. Source registry','Original text → deterministic S-IDs','python'),
      'work':(2,5.8,'8. Gemini: work plan','Tasks + criteria + open questions','model'),
      'wv':(2,3.15,'9. Work-stage checks','Links, sources, criterion coverage','python'),
      'raci':(6.25,3.15,'10. Gemini: RACI','Fixed tasks + duties + source IDs','model'),
      'pv':(10.5,3.15,'11. Full plan checks','One A; roles, evidence, task coverage','python'),
      'package':(14.75,3.15,'12. Document package','Python copies specification; hydrates\nplan evidence from source registry','python'),
      'export':(14.75,.25,'13. Review / export','Separate documents → browser PDF\nSession JSON and Markdown','human')}
    colors={'model':('#e4edfc','#3863a7'),'python':('#e4f2eb','#3a8060'),'human':('#fff1db','#a96a1a')}
    w,h=3.65,1.12
    for key,(x,y,title,text,kind) in nodes.items():
        face,edge=colors[kind]
        ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=0.07,rounding_size=.12',facecolor=face,edgecolor=edge,linewidth=1.4))
        ax.text(x,y+.22,title,ha='center',va='center',fontsize=13,weight='bold',color='#173456')
        ax.text(x,y-.21,text,ha='center',va='center',fontsize=10.5,color='#263a50')
    def arrow(start,end,color='#526078',dashed=False,rad=0):
        ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=15,color=color,linewidth=1.5,
                                    linestyle='--' if dashed else '-',connectionstyle=f'arc3,rad={rad}'))
    for a,b in [('input','session'),('session','analysis'),('analysis','av'),('review','gate'),('gate','registry'),('registry','work'),('wv','raci'),('raci','pv'),('pv','package')]:
        xa,ya,*_=nodes[a];xb,yb,*_=nodes[b];direction=1 if xb>xa else -1
        arrow((xa+direction*w/2,ya),(xb-direction*w/2,yb))
    for a,b in [('av','review'),('work','wv'),('package','export')]:
        xa,ya,*_=nodes[a];xb,yb,*_=nodes[b];arrow((xa,ya-h/2),(xb,yb+h/2))
    # The rerun uses the same RACI-only endpoint; it cannot rewrite validated work.
    ax.plot([10.5,10.5,6.25],[2.52,2.1,2.1],color='#b76626',linestyle='--',linewidth=1.5)
    arrow((6.25,2.1),(6.25,2.52),'#b76626',True)
    ax.text(8.3,1.73,'First RACI failure → previous RACI + errors\nONE automatic repair; second failure → stop',ha='center',va='center',fontsize=11,color='#995019')
    # Actual clarification/reviewer feedback re-enters source handling and analysis.
    ax.plot([16.65,16.9,16.9,6.25],[5.8,5.8,9.17,9.17],color='#995019',linestyle='--',linewidth=1.5)
    arrow((6.25,9.17),(6.25,9.0),'#995019',True)
    ax.text(11.7,9.26,'Replies / requested corrections → reanalysis',ha='center',fontsize=10,color='#995019',bbox={'facecolor':'white','edgecolor':'none','pad':2})
    ax.text(.2,1.65,'BLOCKING RULES',fontsize=12,weight='bold',color='#173456')
    ax.text(.2,1.18,'Invalid analysis: keep last valid revision.\nWork-stage questions: return to clarification; no RACI call.\nUnresolved conflict: no approval or final documents.',fontsize=10.8,va='top',color='#526078')
    ax.text(.2,-.13,'Blue = Gemini API call     Green = deterministic Python     Amber = human/UI     Dashed = feedback / repair',fontsize=10.5,color='#526078')
    fig.subplots_adjust(left=.01,right=.99,top=.99,bottom=.03)
    for ext in ('png','svg','pdf'):
        fig.savefig(OUT/'diagrams'/f'system_diagram.{ext}',dpi=260,bbox_inches='tight',facecolor='white')
    plt.close(fig)
    (OUT/'diagrams/system_diagram.mmd').write_text('''flowchart TD
  U[User: brief / replies / review changes] --> S[Source-aware session and revision history]
  S --> A[Gemini: structured analysis]
  A --> V[Python: schema, quotes and references]
  V --> H[Human review and clarification]
  H -->|actual reply / correction| S
  H --> G[Python approval gate]
  G -->|no blockers; current approval| SR[Python source-ID registry]
  SR --> W[Gemini: tasks and acceptance criteria]
  W --> WC[Python work-stage checks]
  WC -->|open questions| H
  WC -->|validated fixed work| R[Gemini: RACI]
  R --> P[Python full-plan checks]
  P -->|first failure: prior RACI and exact errors; once only| R
  P -->|second failure| STOP[Stop; preserve work and both outcomes]
  P -->|pass| D[Python: specification copy and evidence hydration]
  D --> E[Human document review; PDF / JSON / Markdown export]
''',encoding='utf-8')


def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(str(c).replace('|','/') for c in row)+' |' for row in rows])


def main():
    collect.verify(ROOT/'tests/evaluation/pass-01')
    OUT.mkdir(exist_ok=True);(OUT/'diagrams').mkdir(exist_ok=True);(OUT/'figures').mkdir(exist_ok=True)
    metrics=collect.read(ROOT/'tests/evaluation/pass-01/report-assets/metrics.json')
    if 'equipment_requirement_matching' in metrics:
        metrics['equipment_requirement_matching']['status']='single_assistant_manual_matching'
    annotation=downstream_review()
    (OUT/'component_review.json').write_text(json.dumps(annotation,indent=2)+'\n',encoding='utf-8')
    (OUT/'test_metrics.json').write_text(json.dumps(metrics,indent=2)+'\n',encoding='utf-8')
    for file in (ROOT/'tests/evaluation/pass-01/report-assets').glob('*'):
        if file.suffix in ('.png','.svg','.csv'):shutil.copyfile(file,OUT/'figures'/file.name)
    architecture()
    from .submission_text import evaluation_report, final_report
    evaluation=evaluation_report(metrics,annotation,table)
    final=final_report(metrics,annotation,table)
    for stem,text,title in [('Evaluation_Report',evaluation,'Business Analysis Assistant — consolidated evaluation'),('Project_Report',final,'Business Analysis Assistant — project report')]:
        (OUT/f'{stem}.md').write_text(text,encoding='utf-8')
        doc=Document(title);doc.markdown(text,OUT);doc.save(OUT/f'{stem}.docx')
    write_readme()
    manifest={'created_on':'2026-11-24','language':'English','application_version':'v1.2-eval','new_api_calls':0,
              'manual_review_status':'Single assistant-assisted assessment; no independent second-rating study. Raw evidence and gold labels are unchanged.',
              'artifacts':{str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.rglob('*') if p.is_file() and p.name!='manifest.json'}}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'output_directory':str(OUT),'word_documents':2,'diagram_formats':['png','svg','pdf','mmd'],'new_api_calls':0,'downstream_review_metrics':annotation['metrics']}))


def write_readme():
    (OUT/'README.md').write_text('''# Submission materials

- Evaluation_Report.docx: one editable consolidated evaluation report; matching Markdown source.
- Project_Report.docx: editable project report with CRISP-DM, architecture, results and limitations.
- diagrams/system_diagram.png: high-resolution image for Word/slides.
- diagrams/system_diagram.svg: scalable vector diagram with editable text.
- diagrams/system_diagram.pdf: vector diagram for print and PDF composition.
- diagrams/system_diagram.mmd: editable Mermaid source.
- figures/: the six existing evaluation plots in PNG/SVG.
- component_review.json: per-record retrospective dev review with original source evidence.
- test_metrics.json: preserved final-test/assisted-branch metrics with explicit scope.

All prose is English, matching the project language. Word headings, paragraphs and tables are native
editable content; diagrams/plots are embedded images, with separate vector/source files for editing.
Semantic judgments use one assistant-assisted assessment without an independent second-rating study.
Historical outputs are separated from final-test evidence. Building the reports makes no API calls.

Rebuild with `python -m scripts.build_submission` (matplotlib, numpy and Pillow are used for figures).
DOCX generation uses standard-library OOXML and does not require Microsoft Word or python-docx.
Historical outputs, frozen system code and approved test labels remain unchanged.
''',encoding='utf-8')


if __name__=='__main__':main()
