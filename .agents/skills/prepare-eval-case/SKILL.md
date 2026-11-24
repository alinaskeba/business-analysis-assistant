---
name: prepare-eval-case
description: Prepare or review a manually labeled evaluation case for the Business Analysis Assistant before running Gemini.
---

1. Read AGENTS.md and any existing evaluation case format. Reuse that format.
2. Record the case ID, split, brief and source. For an adapted public brief,
   record the original link and describe the changes.
3. Draft expected findings from the brief. Record the requirements and
   supporting quotes, expected gaps, conflicting pairs of statements,
   and what a useful clarification question should resolve.
4. Record what the assistant must avoid inferring. For a clean case,
   explicitly record that no contradictions are expected.
5. If the case includes a user reply, record which requirement should
   change after that reply and which facts should remain intact.
6. Show the draft expectations for human review. Keep them as draft until
   approved. If an earlier Gemini output exists, keep it as observed output.
## Language and experiment history

Use English for active briefs, expected findings, application outputs and maintained reports.
Keep the user conversation in the language requested by the user. Translated adaptations
retain the source case family, dev split and existing draft/approved status. Cite evidence
from the matching translated brief, not a different-language source. Preserve historical
inputs, prompts, model outputs and run metadata unchanged. A translation is not a live run.
Do not call Gemini during translation review; wait for the separately authorized live-run step.
