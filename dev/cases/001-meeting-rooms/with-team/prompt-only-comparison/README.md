# Prompt-only comparison: preparation

[baseline-v5/manifest.json](baseline-v5/manifest.json) freezes the previously obtained response and
configuration with file hashes. Original artifacts were not overwritten. It remains a Ukrainian run.
[expectations.draft.md](expectations.draft.md) is now an English translated adaptation with the same
36 E-IDs and DRAFT status. Original wording is preserved in history/pre-english at the same relative path.
Formal scoring, prompt examples and live comparisons have not run: approval was a user prerequisite.
Translation does not supply that approval.

After translation review and label approval, assess baseline coverage with source fragments and
output paths; add only prompt examples of users plus separate requirements and a neutral conflict
question; keep structural schema, validator, model and inputs fixed for a controlled comparison.
An English baseline needs a separate authorized run; do not relabel the Ukrainian baseline.
Track correctness, omissions and unsupported facts, not just counts.

The repository has one dev family: meeting rooms with and without the team. Its translations remain
in the same split. Other independent dev briefs with draft expectations are needed for broader checks,
including a clean case without a conflict and a different business process. Freeze expectations before
examining new outputs; do not use held-out cases for prompt tuning.
