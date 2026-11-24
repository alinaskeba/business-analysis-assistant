---
name: run-analysis-eval
description: Evaluate the Business Analysis Assistant CLI on a labeled case and diagnose schema, evidence, extraction, conflict or question failures.
---

1. Read AGENTS.md, the CLI run instructions, and the approved expectations
   for the selected case. Default to dev during prompt iteration.
2. Use the existing CLI command for a live run, or validate a saved
   response offline. Record which mode actually ran, the case ID,
   and the model and prompt revision when available.
3. Run available Python checks for JSON structure and evidence quotes.
   Where the schema has ID references, check that the targets exist.
4. Compare the content against the approved expectations. Flag missing
   or unsupported requirements, missed or invented conflicts, and
   questions that do not resolve the identified issue. Show the relevant
   source text and output for each proposed judgment.
5. Report pass, fail, or needs human review for each check. Label skipped
   checks and failed API calls explicitly. Keep expected labels fixed
   during the run.
## Language and experiment history

Use English for active briefs, expected findings, application outputs and maintained reports.
Keep the user conversation in the language requested by the user. Translated adaptations
retain the source case family, dev split and existing draft/approved status. Cite evidence
from the matching translated brief, not a different-language source. Preserve historical
inputs, prompts, model outputs and run metadata unchanged. A translation is not a live run.
Do not call Gemini during translation review; wait for the separately authorized live-run step.
