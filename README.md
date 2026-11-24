# Business Analysis Assistant

**[Final project report (PDF)](FINAL_REPORT.pdf)** · **[Evaluation report (PDF)](EVALUATION_REPORT.pdf)**

A local NLP prototype that converts English briefs for small web applications into source-linked
requirements, clarification questions and a reviewed work plan. Python + Gemini API.

## Quick start

Python 3.10+ is required. The application runtime uses the standard library.

1. Copy `.env.example` to `.env` and set `GEMINI_API_KEY`.
2. Run `python app.py`.
3. Open **http://127.0.0.1:8000**. Use `--port 8001` if needed.

The default model is `gemini-3.1-flash-lite`. Access and quota depend on the configured account.
Secrets come from the environment or ignored local `.env`; never commit credentials.

## Workflow

- Analyze a brief and inspect requirements, roles, gaps, contradictions and source evidence.
- Answer one or more questions in one reanalysis request.
- **Needs changes** records reviewer corrections as additional source evidence.
- **Approve & generate documents** records approval of the current requirements revision.
- Generation produces tasks/criteria, then RACI. A first RACI failure triggers one automatic
  RACI-only repair. Both outcomes are recorded; a second failure stops the workflow.
- Individual specification, task, criterion and RACI exports use browser **Print / Save as PDF**.

Unresolved conflicts and blocking questions prevent finalization. New replies invalidate approval
and documents. Python resolves source IDs to original quotations. Exact quotes and valid links do
not prove semantic correctness; the generated package remains a draft for content review.

The app is local and single-user. Accepted sessions stay in server memory until downloaded.
Page refresh keeps the accepted session but loses unsent input. Resume a downloaded session with
`python app.py --session path/to/session.json`. Private sessions belong in ignored `sessions/`.

## Reports and architecture

- [Project report](reports/Project_Report.md): scope, CRISP-DM, components and limitations.
- [Consolidated evaluation](reports/Evaluation_Report.md): metrics and component-level findings.
- Editable Word: [project report](reports/Project_Report.docx), [evaluation](reports/Evaluation_Report.docx).
- Architecture: [PNG](reports/diagrams/system_diagram.png), [SVG](reports/diagrams/system_diagram.svg),
  [PDF](reports/diagrams/system_diagram.pdf), [Mermaid](reports/diagrams/system_diagram.mmd).
- [System contract](SYSTEM.md) and [evaluation protocol](tests/EVALUATION.md).

## Evaluation summary

Two final synthetic test families were evaluated: library and equipment. Original trajectories and
assisted recovery are separate: 7 live calls, 84/85 exact quote occurrences in original trajectories,
and 3/4 structurally accepted analysis responses. The equipment conflict correctly remains open.
The positive library trajectory does not complete: invalid evidence and repeated overblocking
prevent final documents. Retrospective dev packages provide separate downstream-component evidence.
They are not held-out or unassisted end-to-end success. Semantic scores use a single assistant-assisted
assessment without an independent second-rating study.

## Tests and reproducibility

```powershell
python -m unittest discover -s tests -t . -q
node tests/test_generation_ui.cjs
```

The recorded suite has 89 Python tests and four offline UI scenarios. These are software checks,
not 89 independent model observations. Historical fixtures are retained for regression/provenance.

Reporting-only dependencies: `python -m pip install -r requirements-reporting.txt`.

```powershell
python -m scripts.build_evaluation_figures
python -m scripts.build_submission
```

These commands do not call an LLM. `python -m scripts.collect_test_evaluation` is an explicit live collection tool,
documented in `tests/EVALUATION.md`. Historical snapshot hashes remain unchanged. Publication edits
to prose and configuration examples are distinct from executable-runtime changes.

## AI-assisted development

The project used an AI coding assistant, with human scope decisions and review. `AGENTS.md` records
quality and CRISP-DM rules; `.agents/skills/` contains evaluation preparation/execution workflows.
The project report describes the process and its limitations, as required by the assignment.
Local credentials, personal sessions, browser profiles, superseded report bundles and temporary
files are excluded by `.gitignore`. Cloud deployment is not required.

## Repository layout

```text
app.py                 Local web UI entry point
ba_assistant/          Analysis, workflow, validation and export modules
web/                   Browser interface and print assets
scripts/               Evaluation, plotting, reporting and GitHub packaging tools
tests/                 Unit tests, final cases and observed test evidence
dev/                   Development cases and recorded development experiments
history/               Immutable regression/provenance fixtures
reports/               Current project/evaluation reports and diagrams
FINAL_REPORT.pdf       Final project report
EVALUATION_REPORT.pdf  Final evaluation report
```

CLI example: `python -m ba_assistant --example` (live API request).
Build a secret-checked public archive with `python -m scripts.prepare_github`.
The import/path reorganization is documented in `layout_migration.json`; original experiment
snapshots and test labels are unchanged. Model prompts and response schemas retain their evaluated
values. Historical report commands describe the earlier layout; this README lists current commands.
