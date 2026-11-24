# Business Analysis Assistant

A Python 3.10+ CLI for analyzing English briefs for small web applications through the Gemini API.
It uses only the standard library. Application responses and CLI messages are English.

## Full-system workflow

The application now supports saved clarification sessions and approval-gated document generation.
Target users are business analysts, Product Owners and small-project managers.
[System contract and component checks](SYSTEM.md) describe the new workflow, implemented in
`ba_workflow.py`; `business_analysis.py` remains the CLI entry point and supports the old one-shot mode.
No live full-system run was performed during implementation. The compact four-case dev dataset now
has final, user-approved expectations. The separate meeting-room translation review is still pending;
the commands below are for a later authorized live run.

```powershell
# Live initial analysis: only the selected case's initial brief goes to Gemini.
python .\business_analysis.py --workflow start --dev-case PURE_002_without_team --session .\sessions\PURE_002_without_team.session.json

# Offline: inspect questions and the current evidence-linked requirements.
python .\business_analysis.py --workflow review --session .\sessions\PURE_002_without_team.session.json

# Live clarification: answer only a question the application actually asked.
python .\business_analysis.py --workflow reply --session .\sessions\PURE_002_without_team.session.json --answer-file .\answer.json

# Offline: approve only after reviewing the updated requirements and resolving blockers.
python .\business_analysis.py --workflow approve --session .\sessions\PURE_002_without_team.session.json --approval "I approve this reviewed requirements revision."

# Live work-plan generation, followed by offline Markdown export.
python .\business_analysis.py --workflow generate --session .\sessions\PURE_002_without_team.session.json
python .\business_analysis.py --workflow export --session .\sessions\PURE_002_without_team.session.json --output .\package.md
```

An answer file contains exactly `question_id` and `text`, for example:

```json
{"question_id": "Q1", "text": "The Product Owner approves the business requirements and makes the release decision."}
```

Q1 is illustrative: use the real question ID and supply the actual answer. Dataset prepared replies
must be routed by a human when their topic is asked; they are never automatically sent to Gemini.
Repeat reply/review as needed. Unresolved conflicts or blocking questions prevent finalization.
Every reply invalidates earlier approval and documents. Invalid API responses leave the last accepted
session file intact. Export creates a new file and will not overwrite the session or an existing package.
Sessions may contain private source text; `sessions/` is Git-ignored and is the suggested local location.

Full-workflow requirements explicitly distinguish source-confirmed facts from proposed assumptions.
Every task links confirmed requirements; every functional/quality requirement has tasks and testable
criteria. Each RACI activity has one Accountable and at least one Responsible from actual team roles.
The specification copies the approved analysis, including scope/exclusions, decisions, assumptions
and open nonblocking questions. Plans and RACI remain drafts for semantic review.

Plan schema v2 adds `open_questions` for missing business decisions: each has an OQ-ID, requirement_id,
missing_information and question. These do not count as criteria; they return the session to blocking
clarification and clear approval/documents. Every other implementable requirement needs an observable
criterion linked to its ID. Governance RACI can use empty task_ids. Historical plan outputs retain
their original schema; no prior result is silently rewritten.

## Full-system offline evaluation

```powershell
python -m unittest -v test_business_analysis test_workflow
python .\evaluate_dev.py --sessions .\sessions --report .\dev\evaluation\my-report.json
```

The evaluator never calls an API. It checks saved `<case_id>.session.json` files against the matching
brief and per-component invariants and exports draft semantic checklists for human review.
Missing runs are not_run; no semantic pass rate is claimed. Optional `<case_id>.failure.json` files
record execution errors separately. Reports are created without overwriting previous reports.
The current dataset has four dev scenarios in two project groups, version 0.4, with final expectations.
Final labels mean reviewed expectations, not successful runs or a held-out evaluation set.
[Implementation verification report](dev/evaluation/README.md) distinguishes offline mocks from live results.

## Setup and usage

Fill in `.env` next to the script:

```dotenv
GEMINI_API_KEY=your-api-key
GEMINI_MODEL=gemini-3.1-flash-lite
```

The script loads that file regardless of the current working directory. Existing environment variables
have priority, including empty values. Simple KEY=value lines, whole-line comments and single/double
quoted values are supported; interpolation and inline comments are not. `.env` is ignored by Git.
Use `.env.example` as a template after cloning. API calls consume account quota.

```powershell
python .\business_analysis.py --help
python .\business_analysis.py --example
python .\business_analysis.py --brief "We need an internal room-booking application."
python .\business_analysis.py --file .\dev\cases\001-meeting-rooms\en\with-team\brief.txt
```

`--example` uses the translated base brief without the team addition. The file command uses the
full translated version with the team. **The analysis commands call the API. Do not run them yet:
the English translation is awaiting human review; a live run is a separate next step.**
No English live model output has been generated. `--help` and the tests below are offline.
The model can be selected through `--model` or GEMINI_MODEL.

## Analysis schema v3

The active prompt revision is `brief-analysis-v5-en-translation`. Schema descriptions are now English;
field names, types and constraints are unchanged from schema v3.

- goals: id, description and source.
- users and team_roles: one id/name per role in each category and a nonempty responsibilities array.
  Each responsibility has description and its own source.
- requirements: id, description, source and kind (functional, non_functional or constraint).
- missing_information: id, topic and why_needed.
- contradictions: id, description and at least two distinct requirement_ids.
- questions: id, text, target_type (conflict/gap), target_id and boolean blocks_final_specification.

A source has document="brief" and a contiguous verbatim quote. Explicit business-process participation
is retained in users even if the interaction channel is unknown; ask about that channel without
inventing access. A conflict is not duplicated as a gap unless a different decision is needed.
The whole brief, analysis instructions and schema are sent to Gemini. The key is only in the
x-goog-api-key header; .env contents and chat history are not added to the prompt.

## English dev adaptation and experiment history

[Translation notes and provenance](dev/cases/001-meeting-rooms/en/README.md)
link the English base brief, team addition and 36 draft expectations. Review the translation before
approval or a live run. All meeting-room variants remain in dev, not held-out evaluation.

Original Ukrainian briefs and previous run artifacts remain at their original paths, unchanged.
[Pre-English snapshot](history/pre-english/manifest.json) also records their hashes and preserves
original documentation, instructions and code. Maintained Markdown documentation is now English;
quoted historical results inside it are explained in English without changing the raw result files.
The previous [v5 baseline](dev/cases/001-meeting-rooms/with-team/prompt-only-comparison/baseline-v5/manifest.json)
is a historical Ukrainian run, not an English baseline. No result or metadata has been relabeled.
This translation changes both language and prompt/schema descriptions; it does not establish model quality.
The earlier prompt-only comparison remains pending; translation does not imply approval of draft labels.

## Offline validation

```powershell
python -m unittest -v test_business_analysis
```

Python checks input size (30,000 characters), key availability, HTTP failures, blocked/incomplete
responses and JSON. It checks exact fields and types, nonempty strings, enums, booleans, ID formats,
unique IDs, duplicate role names within a category, every nested evidence quote, valid references,
and at least one question per conflict/gap. Independent errors are collected with field paths.
Malformed parent fields skip dependent checks but do not stop unrelated checks.
AnalysisValidationError contains all errors; the CLI rejects invalid results with exit code 1,
prints errors to stderr and emits no success JSON. It does not silently repair evidence.

Historical responses must be validated against their original briefs and saved schemas.
English fixtures are offline test data, never claimed as model output. Python does not prove complete
extraction, semantic support, neutral questioning or correct blocking judgments; humans review those.
UI remains a future stage. Saved-session approval and document generation are implemented as described above.

API references: [generateContent](https://ai.google.dev/api/generate-content),
[Structured Outputs](https://ai.google.dev/gemini-api/docs/structured-output).

## Plan source IDs (schema v3)

The active plan prompt is plan-v3-source-ids-and-governance. The model returns source_ids only;
Python inserts exact registry quotations as sources in documents and exports. Registry IDs do not
prove semantic entailment: evidence-origin/role checks and a separate semantic-review audit remain.
Explicit RACI governance actions have activity_type and independent coverage checks. Archived v2
plans can still be validated through validate_plan_legacy_v2; raw historical artifacts are unchanged.
[The source-ID experiment](dev/evaluation/plan-pass-05-source-ids/README.md) records one successful
request, fixed quote errors, remaining condition omissions and a regression in delivery RACI.
# Evaluation freeze

The final validator checkpoint is recorded in
[plan pass 06](dev/evaluation/plan-pass-06-final-validator/README.md).
Every task must have implementation RACI coverage. The prompt and schema remain unchanged.
65 local tests pass; the single live dev response was rejected for three uncovered tasks.
This version is frozen for evaluation; semantic correctness still requires human review.

# Local web demo

For a small verified demonstration use **Load simple demo brief** or **Open saved live demo**.
The latter displays an actual saved Gemini result without a new API request, with a visible
notice that approval was simulated. See [the walkthrough and run history](dev/demo/office-hours/README.md).
Prompt v4 is a subsequent development change; the previous v3 evaluation freeze stays archived.

Run `python web_ui.py` and open **http://127.0.0.1:8000**. No extra packages are needed.
The API key stays in `.env` as `GEMINI_API_KEY`; optional `GEMINI_MODEL` selects the model.
Use `python web_ui.py --port 8001` if the default port is occupied.

In **Questions**, fill in one or more answers and click **Apply answers & reanalyze** once.
Blank answers are not sent. Each answer keeps its own source ID; the batch triggers one reanalysis.
If the model response fails validation, the previous accepted revision and on-screen answer drafts
are preserved. Draft answers are held only in the current page; refreshing loses unsent text.
A `no clarification question` error means the model omitted a question for an unresolved issue,
not that the user must answer every question. No automatic repair or retry bypasses validation.
Resume a downloaded session with `python web_ui.py --session path/to/session.json`.

For a video: load the English meeting-room example (or paste your own brief), click **Analyze brief**,
inspect requirements and their citations, then open **Questions**. Submit an answer to reanalyze.
Review the updated requirements; when blockers are resolved, enter an explicit approval statement,
approve and generate documents. A rejected model result displays validation errors rather than an
accepted document package. Outputs still require human semantic review. Each analyze or
reply click makes one live API call. Generation uses two sequential calls: work plan,
then RACI. A work-plan clarification stops before the RACI call. There are no automatic retries.

Generation stage revision `staged-plan-v1` retains the same final schema and validators. Stage 1
validates tasks, acceptance criteria, open questions and their sources, without requiring RACI yet.
Stage 2 receives the fixed validated work and generates only RACI; the complete package must pass
the full validator before export. A RACI/API failure saves `generation_progress` with the work,
invalid RACI and errors, and leaves documents unset. **Retry RACI only** makes one new call with
the fixed work and exact errors. A changed analysis revision, model, prompt or schema prevents reuse.
Checkpoint reuse also revalidates the stored work. This is structural validation, not human approval
of the intermediate content. No dev expectations or prepared answers are injected.

This is a single-user local adapter over the existing workflow, with the frozen prompts, schemas
and validators unchanged. A new analysis replaces the current session after confirmation.
Sessions stay in server memory, survive page refresh, and disappear when the server stops.
Download session JSON before stopping; it can also be used by the existing CLI workflow.
The UI does not automatically store briefs, answers or API keys on disk.

