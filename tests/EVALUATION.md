# Final test evaluation, dataset 1.0-final

The owner approved the original two test scenarios and expectations on 2026-11-21. The exact
pre-approval file is retained in history. Only statuses, version and review metadata were changed;
expected behavior and briefs were not changed. Both domains remain test, not prompt-tuning data.
Exact-brief and group-ID overlap with dev are checked; this does not establish absence of all
semantic overlap or prove that a domain has never previously been seen by a model.

Implementation: final-system/v1.2-eval. Collection verifies source hashes and dataset hashes before
every live stage. Evaluation tooling is outside the frozen implementation; fixes to collection code
must be recorded separately and must not alter the application or test expectations.

## Collection commands

```powershell
python -m scripts.collect_test_evaluation prepare --directory tests/evaluation/pass-01
python -m scripts.collect_test_evaluation initial --directory tests/evaluation/pass-01
```

Each initial case gets one API request, no retry. Raw inputs, instructions, schemas, raw responses,
execution/validation failures, counts and evidence checks are preserved. Invalid outputs remain
observations; do not omit them or rerun until a favorable answer is obtained.

For clarification, inspect the questions actually asked. Choose only related questions, for example:

```powershell
python -m scripts.collect_test_evaluation clarify --directory tests/evaluation/pass-01 --case TEST_001_library_complete --prepared-reply A1 --question Q1
```

`Q1` is an example, not a predefined runtime ID. Multiple `--question` arguments route the prepared
reply to multiple related questions; runtime source IDs and routing are recorded. Never answer an
unasked topic merely to inject the final target state. Additional relevant questions without a
prepared answer await owner review; do not invent replies. The equipment conflict must stay open.

After the owner reviews an actual generated library analysis, explicit approval can be recorded
with the existing CLI using the collection case's current.session.json. Approval is not implied
by approval of the test labels. Then the `generate` action collects both stages and at most one
RACI repair, preserving the first failure. Do not generate final documents for the unresolved case.

## Measurement rubric

Every semantic judgment needs an output ID/path, actual source text, expected path where applicable,
and a reason. Use `supported`, `incorrect`, `partial`, `unsupported`, `duplicate`, or `pending`.
Keep assisted judgments distinct from owner-approved annotations. Partial items are not fully
correct under strict scoring; report them separately rather than silently rounding up.

| Component | Automatic evidence | Manual annotation / metric |
| --- | --- | --- |
| Requirements | IDs, kinds, references, counts | Precision = fully correct output requirements / all output requirements; recall = matched gold units / all applicable gold units. Retain actors and conditions. |
| Sources | Exact nonempty quote occurrences / all quote occurrences, separately by stage | Fully source-supported factual records / reviewed factual records; exact quote alone is insufficient. |
| Goals | Record IDs and quotes | Separate precision/recall for goals. |
| Users | Role and responsibility records | Separate entity coverage and responsibility coverage; distinguish product/process users from team. |
| Team | Role and duty records | Separate entity and duty coverage, including advisers and authority. |
| Conflicts | Requirement links exist, both positions retained | Match the actual incompatible pair. Report TP/FP/FN and precision/recall. Clean cases contribute false-positive checks; zero gold conflicts makes recall N/A, not 100%. |
| Gaps/questions | Target links and blocking flags | Covered necessary clarification topics / expected applicable topics; relevant neutral nonduplicate questions / all questions. Record unnecessary blockers separately. |
| Answers | Actual reply sources and resolution records | Correctly applied answer decisions / supplied assessable decisions; unchanged facts preserved / applicable unchanged facts. A deferred decision must remain open. |
| Specification | Current approval, deterministic copy, quotes | Coverage of agreed facts, assumption labels, unsupported assertions and cross-section inconsistency. |
| Tasks/criteria | Per-ID coverage, links, source IDs | Per-requirement complete meaning and testability; count omissions and invented behavior. Count constraints separately from implementable requirements. |
| RACI | One A, at least one R, valid roles/tasks, implementation coverage | Supported assignments / reviewed assignments; required-activity coverage. Report first-attempt and repaired results separately. |
| End to end | Revisions, approval, finalization/blocking events | Cases satisfying every applicable mandatory check / all attempted cases; unresolved conflict blocking is success for the blocked trajectory. |

Gold units must come from the fixed approved expectations, with an explicit counting convention.
The library's initial expectations do not include an exhaustive initial requirements list: prepare
and approve an atomic mapping before claiming an initial-requirement recall percentage. Do not
silently use after-clarification facts as the initial gold set. Initial collection can proceed while
that mapping is pending. Preserve the original approved labels; store any supplemental annotation
as a separate reviewed artifact.

## Reporting

Write numerator and denominator beside every rate. Report pending semantic annotations as null /
not measured, not zero and not a structural pass. Keep execution failures distinct from semantic
failures, but retain failed attempts in scenario totals. Documents on the intentionally blocked
equipment case are N/A, not zero; correct refusal to finalize is an end-to-end check.
Report per-case and micro totals, sample size (two independent families) and limitations. Do not
claim broad generalization or an unseen evaluation if test results are later used for prompt tuning.

The collector creates per-output manual-review.json files, source-level automatic-checks.json,
raw evidence and an empty metrics template. Human semantic annotations are still required before
precision/recall or final scenario success can be reported.
