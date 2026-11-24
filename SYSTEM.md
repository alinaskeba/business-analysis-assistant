# System contract

The assistant serves business analysts, Product Owners and small-project managers. Input/output
are English. The surface is a Python CLI and local single-user web UI.

## Components

| Component | Purpose |
| --- | --- |
| business_analysis.py | Gemini transport, analysis prompt/schema, evidence/reference checks, CLI |
| ba_workflow.py | Source-aware sessions, clarification, revisions, approval and specification assembly |
| plan_sources.py | Source registry, quote hydration, plan checks and semantic audit |
| staged_plan.py | Separate work/RACI requests and validated-work reuse |
| web_ui.py and web/ | Review, corrections, approval, one visible RACI repair and document display |
| document_export.py | Individually printable documents for browser PDF export |
| Evaluation/report scripts | Explicit collection, metrics, annotations and reproducible reports |

See the architecture in reports/diagrams/. The original brief is source brief; each actual reply
becomes A1, A2, etc. Each quote must exist in its named source. Roles have one ID and individually
sourced responsibilities. Product users and team roles are distinct. Conflicts retain both rules
and link requirement IDs; questions target gaps/conflicts and specify blocking status.

Confirmed means source-supported, not automatically approved. Assumptions remain separate. Replies
and reviewer changes trigger reanalysis and invalidate approval/documents. Approval binds sources,
replies, analysis and revision. An undecided reply cannot silently close a conflict.

## Planning and safeguards

Plan schema v3 uses source IDs; Python inserts original fragments and rejects unknown IDs or
modified hydrated evidence. Every implementable requirement needs task/criterion coverage. RACI
receives fixed work and confirmed roles. Activities need exactly one A and at least one R; both
may be the same role. Governance may have empty task references. Implementation tasks need
implementation responsibility. Structural validity does not prove semantic support.

The UI permits one automatic RACI-only repair with the previous RACI and actual errors, retaining
both outcomes. A second failure stops. CLI generation is explicit and does not automatically retry.
Work-stage questions return to clarification; all currently block finalization, a known overblocking
risk. Invalid responses preserve the last accepted analysis. Specification assembly copies approved
facts; export revalidates package, evidence and approval. Documents still require content review.
Saved demonstrations identify their recorded origin and any simulated test approval.

## Evaluation boundary

Dev and final test families are separate; expected labels never enter application requests.
Original, assisted and retrospective development observations are reported separately. Missing
stages remain not measured or intentionally N/A. The frozen executable version is v1.2-eval.
Historical raw artifacts and snapshot hashes remain unchanged. Publication prose/config examples
are excluded from executable-code checks, without changing historical metadata or model scores.
See reports/Evaluation_Report.md for observations, scope and limitations.
