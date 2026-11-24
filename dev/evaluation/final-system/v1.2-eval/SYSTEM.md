# Business Analysis Assistant: full-system contract

Target users: business analysts, Product Owners and managers of small web-application projects.
The CLI produces an evidence-linked analysis, asks clarification questions and turns reviewed answers
into a specification and work plan. The application and its documents are English.

## Workflow and evidence

1. Start with the brief only. Extract goals, business-process users, requirements/constraints,
   team responsibilities, gaps, contradictions and linked questions.
2. A human routes an actual reply to an actually asked question. Each reply becomes A1, A2, etc.
   Prepared answers or expected findings from an evaluation dataset are never automatically injected.
3. Reanalyze brief plus supplied replies, preserving sources for unchanged facts and citing the reply
   for new decisions. Resolutions mark whether each reply actually resolved its question.
   The session retains previous analysis revisions and reports added/removed/modified requirement IDs.
4. Review the updated analysis. Any edit/reply invalidates approval and document packages.
   Historical blocking questions cannot silently disappear: an explicit reply resolution is needed.
5. Explicitly approve the current requirements revision. Approval is bound to a hash of sources,
   replies, analysis and revision. Contradictions, blocking questions, missing team or no requirements
   prevent approval and generation. An undecided answer leaves the issue open.
6. Generate tasks, criteria and RACI through Gemini. Assemble the specification directly from the
   approved analysis rather than asking a model to rewrite confirmed facts. Validate before saving.
   Export a Markdown package. Documents remain draft for document review; approval of requirements
   does not claim that every generated task or RACI assignment is semantically correct.

Original brief text is document `brief`; each answer is a distinct document named by its A-ID.
Every quote must exist in the specifically named document. A quote from A2 cannot be attributed to
the brief simply because it exists elsewhere in the session. Source/reply records must agree.
Failed calls or invalid responses do not overwrite the last accepted session revision.

## Confirmed facts versus proposed assumptions

Workflow requirements have status=confirmed: supported by an actual source, not necessarily approved
for finalization yet. Assumptions are separate P-ID records with description, rationale and
status=proposed. They have no fabricated evidence and cannot be task/criterion requirement references.
A human reply confirming a proposal can support a new confirmed requirement; it must cite that reply.
Blanket approval of requirements does not approve proposed assumptions. The legacy analysis schema
is unchanged for compatibility; status and resolution fields are part of the new workflow schema.

## Component checks

| Component | Implementation | Local checks | Semantic review still required |
| --- | --- | --- | --- |
| Initial analysis | Gemini + structured schema | Structure, nested evidence, ID/reference integrity | Complete extraction, conditions, correct conflicts |
| Clarification | Questions + explicitly routed replies | Asked-question references, actual answer sources, outcome records | Relevant questions; truthful resolution of ambiguous replies |
| Updated requirements | Reanalysis + immutable revision snapshots | Source integrity, requirement change list, approval invalidation | Preserve unchanged meaning; correctly apply changed decisions |
| Specification | Copy approved analysis into explicit sections | Exact agreement with current approved facts at export | Wording, scope/exclusions, completeness of approved analysis |
| Tasks | Gemini plan | Every task has confirmed requirement links; functional/quality coverage | Work breakdown quality; no hidden new features |
| Acceptance criteria | Given/When/Then + evidence | Valid requirement links, evidence, coverage | Testability, edge cases, correct expected outcomes |
| RACI | Activities + evidence-backed A/R/C/I arrays | Exactly one A, at least one R, valid team-role/task links | Actual authority supports assignment; no inferred accountability |
| End-to-end | Approval-gated session and export | No generation while blocked; stale approval/package rejected | Documents faithfully reflect all supplied decisions |

Constraints are requirements with kind=constraint and appear in scope/exclusions and quality/constraint
sections. Functional and non-functional requirements require task and criterion coverage. Coverage
checks do not justify implementing excluded scope: human review must verify task meaning.
Responsible and Accountable may be the same role. Unknown authority must be clarified before planning.

### Plan schema v2: criteria or explicit unanswered decisions

The plan prompt revision is `plan-v2-complete-criteria`. Every implementable requirement needs at
least one meaningful Given/When/Then criterion linking its ID. Preserve actors, access and scope.
If a necessary business decision is missing, return `open_questions` with id, requirement_id,
missing_information and question. Questions do not count as criterion coverage. Generation stores
the blocked attempt, adds blocking session questions and clears approval/documents. A fresh review
is required after clarification. Empty task/criterion/RACI arrays can represent blocked attempts;
complete unblocked plans still need tasks and RACI. Trivial success placeholders are rejected;
semantic testability and preservation of conditions still require review.
Governance `task_ids=[]` was already legal and remains so. Requirement approval, specification
acceptance and release decisions must not be attached to artificial implementation tasks.

## Evaluation boundaries

`dev/cases/ba_dev_cases.json` version 0.4 contains four final, user-reviewed scenarios in two project
groups: a store with/without a team and university inventory with resolved/unresolved conflict.
All remain dev. Final expectations do not imply measured model quality. Do not tune on held-out inputs.
`evaluate_dev.py` reads saved artifacts offline, reports per-component execution/structural status and
exports semantic checklists plus empty correct/omissions/unsupported-facts fields for human judgment.
It never calls a model or assigns a semantic quality score from string matching.

Unit tests use explicitly hand-authored mock responses with actual scenario input/reply text. They
verify mechanics and invariants, not model extraction quality across the scenarios. Unexecuted
cases are not_run; execution failures are not semantic model failures. The separate historical
meeting-room expectation drafts retain their original status; only the reviewed compact dataset is final.
No live full-system run has been performed in this implementation step.

## Active plan schema v3: source-ID registry

Plan generation uses source_ids arrays and a Python-built registry of original sentence fragments
with source-document IDs and character offsets. The model does not write evidence quotes. Python
hydrates display/export evidence and rejects unknown IDs, unrelated origin/role references and
modified hydrated text. Multiple IDs support conditions from separate statements. The analysis
schema still uses its existing source objects; only generator-plan evidence changes representation.

The source-alignment audit remains needs_semantic_review: registry membership is not semantic
entailment. Human/assistant-assisted review must check actors, quantities, access, prohibition and
actual authority. RACI activity_type coverage requires explicit approval/acceptance/release actions
found in the supplied role evidence. The first source-ID run covers governance but omits delivery
RACI; this semantic regression is recorded separately from structural success. No later validator
change is claimed as part of that run. See dev/evaluation/plan-pass-05-source-ids/README.md.
