# Business Analysis Assistant

## Project context

The assistant serves business analysts, Product Owners and small-project managers. It turns a
small web-application brief into analysis, clarified requirements, specification, linked tasks,
testable acceptance criteria and RACI. The current surface is a Python CLI with saved sessions.
Legacy one-shot analysis stays available. The full workflow uses separate reply source documents,
human approval of the current revision and structured/Markdown document packages.

## Language and evidence

- Active briefs, application responses, prompts, CLI messages and maintained documentation are English.
- The brief is the source of confirmed facts during analysis. A later user clarification may also
  become a source; retain a reference to the specific source.
- Distinguish business-process roles from project-team roles. Label assumptions and obtain user
  confirmation before treating them as agreed requirements.
- Each role has one ID per category and a responsibilities array; each responsibility has its own
  description and source. Preserve explicit participation even when the interaction channel is unknown.
- Every task references a confirmed requirement; every RACI activity has exactly one Accountable
  and at least one Responsible, both referencing actual team roles and source evidence.
- Explicit evidence support is not the same as human approval. Proposed assumptions stay separate
  and never become implementation scope without a supplied confirmation. Do not infer accountability
  from a role title. Block generation on unresolved conflicts, blocking questions or stale approval.
- Tune prompts on dev. Reserve held-out cases for final evaluation. Keep all variants and translations
  of one brief in the same split. Draft expectations stay draft until explicitly approved.
- Preserve historical runs, responses, prompts, schemas and metadata byte-for-byte. English adaptations
  are separate inputs, not translated model runs. Do not call the API until translation review is complete
  and the user authorizes the separate live-run step.

## CRISP-DM working rules

- Business Understanding: clarify goals, users, scope and success criteria; do not invent customer decisions.
- Data Understanding: separate supported facts, gaps and contradictions.
- Data Preparation: check nonempty UTF-8 input; never commit API keys or private briefs to the repository or logs.
- Modeling: use the LLM API with a strict JSON schema and verbatim evidence for extracted facts.
- Evaluation: Python checks structure, quotes and references; humans check meaning and approve requirements.
  Do not describe offline tests as live API tests.
- Deployment: retain the CLI entry point; UI is a later stage. Document generation requires reviewed
  requirements, no blocking decisions and explicit approval bound to the current revision.
- Iterate after clarifications and record changes; do not turn assumptions into approved requirements.
