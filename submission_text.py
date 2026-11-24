"""English report prose, kept separate from the reproducible artifact builder."""


def evaluation_report(m, review, table):
    ac_rows=[[r['id'],r['requirement_id'],r['judgment'].replace('_',' '),r['reason']] for r in review['criteria']]
    task_rows=[[r['id'],r['judgment'].replace('_',' '),r['reason']] for r in review['tasks']]
    raci_rows=[[str(r['expected_index']+1),r['expected']['activity'],r['judgment'],', '.join(r['actual_activity_ids']) or 'None'] for r in review['raci_expected_checks']]
    return '''# Business Analysis Assistant — consolidated evaluation report

Version evaluated: v1.2-eval. Date: 21 November 2026. Model: gemini-3.1-flash-lite.

## 1. Executive assessment

The prototype extracts a useful structured analysis and correctly preserves an intentionally unresolved conflict. Its strongest measured properties are exact source quotation, reference integrity and safe refusal to finalize. It does not demonstrate reliable positive end-to-end completion on the final test set. The library trajectory fails during clarification; a separately owner-approved recovery then repeatedly stops on an unnecessary performance question.

Every implemented component is reviewed in this document. Where final-test execution did not reach a component, a preserved development output is assessed separately. These retrospective dev assessments close a component-inspection gap; they do not replace held-out evidence or turn an assisted output into an unassisted success. No new API call was made while compiling this report.

## 2. Evidence, datasets and scope

Three evidence groups are kept separate:

- Original final-test trajectories: two owner-approved synthetic test cases from two families, library and equipment. Four analysis calls are recorded after the library clarification extension. Gold labels and frozen application files were unchanged.
- Owner-assisted library component branch: two documented editorial changes (correct one quotation; restore available-copy borrowing), explicit owner approval, two work-generation calls and one intervening clarification. No final document package was produced.
- Retrospective development review: the saved PURE_002_without_team browser RACI-repair output. The analysis is a reference fixture, reply routing was reconstructed and test approval was simulated. The live RACI result and assembled documents are preserved, but this is not a fresh conversation from a new brief.

The final collection contains 7 live requests: 4 original and 3 assisted. Development examples and software tests are not added to that denominator. Original raw inputs, responses, rejected outputs and failures remain unchanged. Content judgments below use a single assistant-assisted assessment. No independent second-rating or inter-rater agreement study was performed.

## 3. Method and scoring conventions

Python checks JSON structure, nonempty exact quotes in the named source, ID/reference integrity, current approval, per-requirement coverage and RACI cardinality. Humans inspect whether the cited source supports the full claim, whether conditions are preserved and whether a question or assignment is justified.

Precision = correct extracted requirements / all extracted requirements. Recall = matched applicable gold units / all applicable gold units. Partial matches are reported separately. The equipment requirement metric uses six already-approved expected units and five output records. Library initial recall is not calculated because its approved initial labels do not define an exhaustive atomic requirement inventory. The library's after-clarification facts are not silently reused as initial gold.

Citation fidelity counts source occurrences, including repeated occurrences across revisions. It does not measure unique facts or semantic entailment. ID coverage is mechanical coverage, not acceptance-test completeness. Conflict matching checks the actual incompatible source pair. Missing final documents are N/A on the intentionally blocked trajectory; a failed positive trajectory remains a failure.

## 4. Original final-test results

| Indicator | Count | Rate | Qualification |
| --- | --- | --- | --- |
| Exact quote occurrences | 84/85 | 98.8% | Four original analysis snapshots; repeated quotations counted |
| Structurally accepted analysis outputs | 3/4 | 75.0% | Response-level metric, not scenario success |
| Equipment requirement precision | 5/5 | 100% | Assisted semantic annotation on one case |
| Equipment requirement recall | 5/6 | 83.3% | Coordinator-review requirement omitted as a separate record |
| Correct initial conflict-pair precision | 1/1 | 100% | Only one positive labeled conflict |
| Correct initial conflict-pair recall | 1/1 | 100% | No false conflict on the one clean initial case |
| Unchanged equipment requirements after reply | 5/5 | 100% | Existing output preserved; initial omission remains |

![Equipment initial requirement precision and recall — assisted matching](figures/equipment_requirement_metrics.png)

The equipment output has R1 browse, R2 submit one-item request, R3 view own requests, R4 remain pending until coordinator approval and R5 immediate approval without review. The explicit coordinator review action appears in U2 but not as a separate requirement. The contradictory R4/R5 pair is correctly retained rather than reconciled without authority.

![Exact quotation by original stage](figures/quote_fidelity.png)

Initial library: 22/22 exact occurrences. Initial equipment: 15/15. Equipment clarification: 16/16. Library clarification: 31/32. The invalid library quotation is R4, "Members sign in before... viewing their own current loans." The supplied sentence contains no ellipsis. The rejected output remains in the denominator.

## 5. Goals, product users, project roles and questions

The expected business goal appears in each initial result. Both expected product roles appear in each case: 4/4 case-role occurrences. Project-role presence is library 5/5 and equipment 4/4. The library representative is retained as a project adviser rather than automatically made a product user. These are assisted presence checks, not full precision/recall for all duties or evidence support.

![Descriptive initial record counts](figures/initial_record_counts.png)

| Item inspected | Observation | Assessment |
| --- | --- | --- |
| Library R1 | Add and update book-copy records share one requirement | Both actions retained; atomicity failure |
| Library R3/R4 sources | Short fragments omit the Member actor | Full brief supports facts; standalone citation context incomplete |
| Library Q1 | How to identify members and copies | Partly relevant to access/data identity; technical delegation required clarification |
| Library Q2 | Whether a project adviser needs application access | Low-value/uncertain relevance; not a product role by default |
| Expected library clarification | Borrowing eligibility or loan limits | Required loan-limit topic not asked |
| Equipment Q1 | Choose between incompatible approval policies | Relevant, neutral and correctly conflict-linked |
| Equipment Q2 | Preferred interfaces and viewing history | Lower-priority UI topic; history wording requires scope review |

No aggregate question precision, duty recall or semantic source-support percentage is invented from these observations. The owner considers the initial library analysis generally consistent with the brief; that practical acceptance coexists with these specific limitations.

## 6. Applying answers and complete-trajectory attempts

Equipment: the approved reply explicitly defers the approval-policy decision. A1 is recorded as still_open, C1 and both positions remain, and all five requirement records stay unchanged. Approval and generation guards both reject the resulting state, with zero additional API calls. This demonstrates the intended negative trajectory, not universal success on every applicable semantic check.

Library: after actual owner clarifications and the prepared business-rule response, the raw analysis fails exact-source validation. It also loses the standalone positive available-copy borrowing requirement. The original trajectory therefore does not reach approval or final documents.

![Original trajectories toward finalization](figures/scenario_progression.png)

The owner approved a separate recovery with two explicit changes: replace the R4 ellipsis with the original A1 sentence; restore available-copy borrowing as R15. The first work generation then asks about performance and blocks. The already-approved answer says that no quantitative target is agreed and the detail is nonblocking. Reanalysis passes, with requirements, goals, users, team and assumptions unchanged. The next work generation nevertheless asks the same blocking performance question again, attached to the English-language requirement R12. Further requests stop.

This exposes overblocking and a schema limitation: every work-plan open question blocks finalization, so an irrelevant/nonblocking question can prevent progress. The frozen system was not modified to force a passing test.

## 7. Specification component — separate development evidence

The specification is assembled by Python from approved analysis, rather than rewritten by the LLM. On the saved dev package, the complete specification equals the deterministic current-analysis projection. All 16 requirement records are preserved (16/16); all 9 expected sections are present (9/9). Export revalidates approval, source registry and package integrity.

This measures faithful copying of the supplied analysis, not the correctness or completeness of that analysis relative to the original brief. Proposed assumptions are in a separate section; the inspected real package has an empty assumptions array, so positive nonempty-assumption behavior is supported by software tests, not this observation. No final-test library specification was produced.

## 8. Tasks and acceptance criteria

On the second assisted library work output, five tasks and thirteen criteria mechanically cover all thirteen implementable requirement IDs. Both ID coverage rates are 13/13. The work remains intermediate because its performance question blocks finalization; no RACI is requested.

![Assisted library work-stage ID coverage](figures/assisted_link_coverage.png)

A separate retrospective dev package contains three tasks and thirteen criteria. All thirteen implementable IDs are task-covered and criterion-covered (13/13 each). All three tasks refer to existing requirements. Scope fidelity is weaker: 2/3 tasks stay within supplied capabilities; TASK1 says CRUD, which introduces deletion beyond explicit create/update.

''' + table(['Task','Judgment','Evidence-based reason'],task_rows) + '''

The following criterion review separates business wording from full citation support and full requirement-level test coverage. Nine of thirteen records have faithful business wording; two contain unsupported authentication preconditions and two are partial test definitions. This 9/13 (69.2%) is a retrospective assisted wording assessment, not final-test accuracy. AC5 is faithful to the full facts but its citation set is incomplete. AC8 is a valid positive scenario, while the negative quantity scenarios remain absent.

''' + table(['Criterion','Requirement','Judgment','Reason'],ac_rows) + '''

The assisted library output independently shows similar risks: AC13 omits the fewer-than-three-active-loans condition from successful borrowing; AC3/AC4 invent automatic sign-in redirection; AC1/AC9 add librarian sign-in as a precondition. These are content findings, even when every requirement ID is covered.

## 9. RACI — separate development evidence

The saved dev browser repair has six RACI rows. All six have exactly one Accountable and at least one Responsible, valid role IDs and supported task references (6/6 structural rows). Implementation now covers TASK1-TASK3 (3/3). Twelve of thirteen assignments have explicit source support under the conservative assisted review. The remaining QA Consulted assignment at UAT acceptance is not established by its cited testing-duty sentence; it may be reasonable, but must be proposed or confirmed rather than claimed as sourced.

Completeness is a separate issue. The approved dev labels contain eight role/activity semantic checks. Four pass, two partially cover implementation without deployment, and two lack test-execution activity. These are eight label checks, not eight distinct activities; some assess different assignments of the same expected activity.

''' + table(['Gold check','Expected activity','Result','Actual row(s)'],raci_rows) + '''

Thus assignment support is 12/13 (92.3%), while strict completion of these expected checks is only 4/8 (50.0%). The apparent contrast is meaningful: the assignments that exist are mostly supported, but entire duties are omitted. Neither metric is a held-out RACI score. Per-assignment source quotes and actual records are preserved in component_review.json.

## 10. Timing, software verification and uncertainty

The final/assisted collection's 7 requests total 35.698 seconds of measured response time; mean 5.100 seconds per request. Human review and local processing are excluded. This small descriptive sample is not a response-time guarantee or a cost measurement.

![Observed request timings](figures/request_latency.png)

The v1.2 application has 86 Python tests; with collection-tool tests the suite has 89, plus four offline UI orchestration scenarios. These verify mechanics and guards with controlled responses. They do not increase the model-quality sample size. The historical actual-browser dev test used one RACI repair request and reached visible documents. It began with a reconstructed checkpoint and simulated approval; it is not a fresh final-test success.

Main validity limits: two test families, one conflict, one initial response per case, incomplete initial-library gold enumeration, assistant-authored annotations without inter-rater agreement, and a retrospective dev sample that has already influenced tuning. Rates from dev, final tests and assisted branches must not be pooled.

## 11. Conclusion and priorities

The prototype demonstrates useful extraction, traceable evidence and conservative unresolved-conflict handling. It has measurable weaknesses in citation context, atomicity, query relevance, acceptance-condition preservation, RACI duty completeness and positive workflow completion. An accepted initial analysis and high ID coverage do not establish a working complete positive trajectory.

Priority improvements for a later version: distinguish blocking and nonblocking work-stage questions; suppress questions already answered with an explicit scope decision; use source IDs in analysis as well as planning; enforce actor/condition preservation; test complete delivery RACI coverage. Such changes should be tuned on dev and evaluated on new held-out cases, rather than silently changing the current test result.

## 12. Artifact index and reproducibility

- Final raw evidence: tests/evaluation/pass-01/; separate recovery: tests/evaluation/pass-01-assisted-library/.
- Retrospective package: dev/evaluation/ui-raci-pass-01/after.session.json.
- Test metrics: test_metrics.json. Detailed retrospective annotations: component_review.json.
- Six figures: figures/ in PNG and SVG. Architecture: diagrams/ in PNG, SVG, PDF and Mermaid.
- Rebuild the package: python build_submission.py. Recompute final-test figures: python build_evaluation_figures.py.

No raw model response, test label or application file was changed to compile this report. The Word version contains editable headings, text and tables. The assisted annotations are exploratory and are not independently human-verified scores.
'''


def final_report(m, review, table):
    return '''# Business Analysis Assistant — project report

Evaluation date: 21 November 2026. Publication preparation: 24 November 2026.

Application version: v1.2-eval. Model: gemini-3.1-flash-lite. All application briefs and outputs are English.

## 1. Task, users and selected scope

I built an NLP prototype that helps business analysts, Product Owners and small-project managers convert a small web-application brief into a structured requirements analysis and work plan. It extracts goals, product users, requirements, constraints and project roles; identifies gaps and contradictions; asks clarification questions; and uses reviewed requirements to prepare a specification, task breakdown, acceptance criteria and RACI.

The intended value is to reduce the manual effort of structuring a brief while retaining traceability and human control. The prototype does not treat model output as an agreed specification automatically. Facts must have supplied sources; assumptions remain separate; unresolved business decisions prevent finalization.

Selected scope includes English briefs, a Python CLI, a local single-user web interface, saved session revisions, explicit human review, Gemini API calls, structured JSON, source validation and individual browser-based PDF exports. Cloud deployment, integrations with project-management tools, authentication for the assistant itself, multi-user collaboration and automatic implementation of the generated tasks are outside scope. No RAG database or runtime multi-agent system is required for this selected information-extraction and generation task.

## 2. System architecture and component responsibilities

![System architecture — blue: model calls; green: Python; amber: human/UI](diagrams/system_diagram.png)

| Component | Input | Output / responsibility |
| --- | --- | --- |
| Local UI / CLI | Brief, actual replies, review actions | Explicit workflow actions; display evidence and validation errors |
| Session and source store | Original brief and replies | Source documents brief/A1/A2, question history, revision snapshots and approval hash |
| Analysis call | Current sources, previous analysis and actual question/reply history | Structured facts, gaps, conflicting requirement pairs, questions and resolutions |
| Analysis validator | Structured result and named sources | Schema/reference checks and exact nested quotations; rejection on errors |
| Review and approval gate | Current analysis and human actions | Clarifications or revision-bound approval; no finalization with blockers |
| Source registry | Original source text and approved evidence | Deterministic S-IDs, document names, exact fragments and offsets |
| Work-plan call and checks | Approved facts plus registry | Tasks and testable criteria with requirement/source IDs; open planning questions if needed |
| RACI call and checks | Fixed work, confirmed roles and registry | RACI with one A, at least one R, evidence and implementation-task coverage |
| Repair orchestration | First failed RACI and exact errors | At most one automatic RACI-only repair in the UI; first failure remains visible |
| Assembly and export | Validated current package | Deterministic specification, hydrated original quotes, editable session JSON, Markdown and print-ready individual documents |

Gemini is called for analysis/reanalysis, then for work planning and RACI separately. Python handles validation, identity/reference rules, session updates and exports. A typical initial-plus-one-clarification path to documents would use four model calls, or five if the single RACI repair is needed; additional real clarification turns can add calls. This is a description of control flow, not a measured completion guarantee.

The four document outputs are a specification, task breakdown, acceptance criteria and RACI. PDF export uses the browser's Print / Save as PDF destination and needs no model request. Text, headings and tables in this report are editable; the separate diagram SVG/Mermaid sources can be edited independently.

## 3. CRISP-DM applied to the project

### Business understanding

The business task was scoped to small web applications and reviewable analyst drafts. Success means preserving the brief's actors, actions, scope and conditions, asking necessary questions, applying actual replies, retaining source provenance and producing mutually consistent documents. Human agreement and source support are separate concepts. A supported fact can still await approval; an assumption is not implementation scope until confirmed.

### Data understanding

The development dataset contains four scenarios in two source families, adapted from supplied PURE-tagged briefs with synthetic stakeholder replies. All variants of a family stay in dev. Two separate synthetic domains — community library and equipment requests — were approved for final testing. Their expected behavior was fixed before generation. The repository records supplied PURE source-case IDs; the original external publication reference was not independently verified.

The data were examined for explicit requirements, process actors, team authority, conflicting statements and missing decisions. Team adviser participation was kept distinct from product access. Requirements evidence was traced to the brief or an actually supplied reply.

### Data preparation

Briefs are UTF-8 and must be nonempty within prototype limits. Each actual reply becomes a separately identified source. Expected labels and future answers remain outside model context. Approved test files and implementation snapshots are frozen with SHA-256 hashes. Initial input, raw outputs, failures and timing are retained. API keys come from .env/environment and are excluded from reports and experiment snapshots.

### Modeling

Gemini is accessed through a Python standard-library HTTP client with a JSON response schema. English prompts define the extraction categories, require exact evidence, distinguish facts from assumptions and forbid inventing policy. Goals, users, team roles, requirements, gaps, conflicts and questions have typed IDs and links.

Roles have one ID and multiple individually sourced responsibilities. Contradictions retain both requirements and refer to their IDs. Questions target a gap or conflict and indicate blocking status. After clarification, resolutions record whether a supplied answer resolved the question or left it open.

Planning uses a source-ID registry so the model selects evidence IDs and Python inserts original quotations. Tasks/criteria are generated before RACI. The second stage cannot rewrite validated work. One automatic RACI repair receives actual validation errors and the previous RACI; a second failure stops. The specification is copied from reviewed analysis rather than generated again.

### Evaluation

Software checks were combined with final-test observations and explicit content review. All components were inspected, but evidence strength differs. Final tests exercised analysis, clarification and blocking; downstream components were additionally reviewed from existing development outputs. Retrospective dev and owner-assisted results are reported separately rather than pooled with held-out outcomes.

Metrics include requirement precision/recall where approved countable gold units exist, exact quote occurrence rate, conflict-pair precision/recall, unchanged-requirement preservation, task/criterion ID coverage, scope fidelity, RACI structure, source-supported assignments and expected-duty completion. Missing/unexecuted stages are reported as such. Exact quotation, valid references and complete link coverage do not by themselves prove semantic correctness.

### Deployment / delivery

The application runs locally with python web_ui.py or the existing CLI. The UI supports brief analysis, batched replies, reviewer corrections, button-based requirements approval, generation, the single RACI repair and exports. Sessions stay in server memory unless downloaded; CLI sessions are saved explicitly. Page refresh preserves accepted server state but does not preserve unsent text. Cloud deployment is not part of this prototype. A demo video is still a submission deliverable, not an already recorded result.

## 4. Evaluation results

The owner-approved final dataset has two independent families. Seven live calls were recorded: four original-trajectory analysis calls and three calls in a separately owner-approved editorial recovery. No prompt or application tuning was performed from these final observations.

| Evidence group | Result | Important boundary |
| --- | --- | --- |
| Original quote fidelity | 84/85, 98.8% | Occurrences, not unique facts or semantic support |
| Original structural acceptance | 3/4, 75.0% | Responses, not full scenarios |
| Equipment requirement matching | Precision 5/5; recall 5/6 | Assisted per-record mapping on one case |
| Initial conflict matching | Precision 1/1; recall 1/1 | One positive and one clean initial case |
| Deferred-answer preservation | Existing equipment requirements 5/5 unchanged | Conflict correctly remains open |
| Assisted library work links | Tasks 13/13; criteria 13/13 | No final package: repeated performance question blocks |
| Retrospective dev specification | 16/16 requirements copied; 9/9 sections | Preserves supplied analysis; not an extraction-quality guarantee |
| Retrospective dev tasks | 2/3 scope-faithful | CRUD wording adds unrequested deletion |
| Retrospective dev criterion wording | 9/13 faithful; 2 partial; 2 unsupported preconditions | Citation support and missing negative scenarios assessed separately |
| Retrospective dev RACI | Structure 6/6; explicitly supported assignments 12/13; strict gold checks 4/8 | Entire test/deployment duties are missing despite mostly supported existing assignments |

![Quote fidelity across original analysis stages](figures/quote_fidelity.png)

The consolidated evaluation report contains the per-record task/criterion review, RACI expected-check mapping, source evidence and all six figures. These are single-assessor, assistant-assisted annotations without independent verification. The initial library analysis was qualitatively accepted as generally consistent with its brief; this assessment is separate from atomic metric scoring.

## 5. Scenario walkthrough and practical limitations

The equipment case contains two explicit incompatible rules: remain pending until coordinator approval, and immediately become approved without review. The system keeps both, asks a neutral question and receives an undecided reply. The resolution remains still_open. Approval and generation guards correctly reject finalization. The coordinator-review capability is nevertheless omitted as a separate requirement; correct blocking does not erase that extraction error.

The initial library analysis is usable and qualitatively accepted. During clarification, the model inserts an ellipsis into a supposed exact quotation and loses a standalone positive borrowing requirement. The validator rejects the result. In a separate owner-approved component branch, those two records are corrected, but the planner repeatedly raises a performance question that was already explicitly described as nonblocking. The positive final-test journey therefore does not reach final documents.

A historical simple office-hours demo and a saved dev RACI-repair browser test show document assembly and display working under controlled inputs. The latter uses a reconstructed checkpoint and simulated test approval. These must be presented as such in the video; they are not proof of a fresh successful final-test conversation.

Main limitations are small sample size, model nondeterminism, uneven question relevance, merged actions, incomplete citation context, acceptance criteria that omit preconditions or invent implementation behavior, and missing RACI duties. The current work-question schema treats every planning question as blocking, which amplifies irrelevant questions into workflow failure. High local scores do not imply successful full completion.

Future development should prioritize blocking/nonblocking planning decisions, suppression of already-answered questions, source IDs for analysis, semantic preservation of actors and conditions, and complete delivery responsibility. New changes should be tuned on dev and evaluated on new held-out material.

## 6. Managing the AI coding assistant

I used the coding assistant to implement and inspect the prototype, write local regressions, preserve experiment artifacts and prepare reproducible evaluation tooling. Its context included the intended users and scope, current schemas, source rules, approved dev expectations and actual validator failures. Final-test expected labels remained outside application requests and were not used to tune the frozen implementation.

AGENTS.md records the project constraints and CRISP-DM guidance: do not invent decisions, preserve source links, distinguish product and project roles, keep assumptions separate, validate output and report offline checks separately from live calls. The prepare-eval-case skill standardizes source/expectation preparation and owner approval. The run-analysis-eval skill standardizes artifact capture, reference/evidence checks and error diagnosis.

The owner reviewed briefs, labels and requirements and supplied additional business decisions where needed. The assistant proposed and implemented changes; local tests checked mechanics. A concrete lesson is that stronger structural safeguards can reveal additional model failures and can overblock a valid small project. I therefore kept semantic review distinct from Python validation and retained unsuccessful attempts rather than reporting only successful demonstrations.

## 7. Reproducibility and running the application

From the project directory, configure GEMINI_API_KEY privately in .env. The default model is gemini-3.1-flash-lite. The runtime uses the Python standard library; plotting/report tooling additionally uses matplotlib, numpy and Pillow.

```powershell
python web_ui.py
```

Open http://127.0.0.1:8000. Analyze a brief, inspect evidence, submit actual answers, request corrections if needed, then approve and generate. A first RACI failure is shown and automatically repaired once. Inspect the content before using it. PDF buttons open a printable individual document; choose Save as PDF in the browser dialog. Download session JSON before stopping the server.

```powershell
python -m unittest -q test_business_analysis test_workflow test_component_eval test_plan_coverage test_reviewed_baseline test_plan_sources test_web_ui test_staged_plan test_document_export test_evaluation_collection
node test_generation_ui.cjs
python build_evaluation_figures.py
python build_submission.py
```

The recorded software suite has 89 passing Python tests including collection-tool tests, plus four offline UI flow scenarios. These are not 89 model-quality test cases. Frozen code, raw request/response logs, exact source text, execution outcomes and hashes make the reported observations auditable.

## 8. Suggested video outline — maximum 10 minutes

| Time | What to show |
| --- | --- |
| 0:00–1:00 | Problem, intended users and selected scope |
| 1:00–2:30 | Architecture diagram; identify Python versus model calls |
| 2:30–5:30 | Running local UI, evidence and clarification; explicitly label any saved checkpoint or synthetic demonstration |
| 5:30–6:30 | One document package and separate PDF export; explain approval and validation |
| 6:30–8:30 | Evaluation plots, one actual error and the correctly blocked conflict; distinguish dev/test/assisted results |
| 8:30–9:30 | AGENTS.md, custom skills, context management and key lessons |
| 9:30–10:00 | Limitations and next improvements |

Demonstrations distinguish newly generated output from saved checkpoints. The library final-test trajectory did not complete successfully.

## 9. Conclusion

This project meets the intended NLP assistant architecture: structured extraction, follow-up questions, source-aware state and a reviewed document-generation workflow. The evaluation demonstrates useful initial analysis and safe unresolved-conflict handling, while exposing weak positive completion and incomplete downstream semantics. The prototype and evidence are suitable for a critical assignment report, provided those limitations and the scope of successful demonstrations are stated clearly.

## References and project artifacts

- GenAI. Assignment 1. Build an NLP System.pdf, supplied assignment, pages 1–4.
- AGENTS.md; .agents/skills/prepare-eval-case/SKILL.md; .agents/skills/run-analysis-eval/SKILL.md.
- tests/ba_test_cases.json, final version 1.0; dev/cases/ba_dev_cases.json, version 0.4.
- tests/evaluation/pass-01/ and tests/evaluation/pass-01-assisted-library/.
- dev/evaluation/ui-raci-pass-01/; dev/evaluation/final-system/v1.2-eval/.
- Evaluation_Report.docx; component_review.json; test_metrics.json; separate architecture and plotting assets.
'''
