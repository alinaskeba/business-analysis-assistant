# Office hours demonstration

Synthetic development/demo scenario, not a held-out evaluation case. Expectations and the assisted
semantic review below are draft, not user-approved labels. Original evaluation cases are unchanged.

Use **Load simple demo brief** for a fresh live analysis, or **Open saved live demo** for a
reliable video walkthrough of the actual saved response. Loading the saved result makes no API call.
The UI explicitly labels saved origin and simulated approval. The API remains stochastic; a fresh
run is not guaranteed to reproduce the same questions or pass validation.

## Script for a live walkthrough

1. Load the brief and analyze. Inspect visitor role, source quotes, requirements and exclusions.
2. If asked who provides hosting/domain, use this fictional scenario answer:

   The Full-stack Developer is both Responsible and Accountable for providing the hosting environment
   and the domain name. The page will use the existing company hosting environment and the existing
   company domain; no purchase or new infrastructure is in scope.

3. Apply the answer and review the updated requirements. Approve only after your own review.
4. Generate and inspect the specification, tasks, criteria and RACI. Download the session.

The saved test journey used the same synthetic answer and a clearly marked simulated approval,
not an approval from the project user. `verified.session.json` is copied unchanged from the successful
live run; it is not an edited model answer. `documents.md` is a deterministic Python export.

## Recorded attempts

- run-20261121-114636: analysis network timeout, no usable model result.
- run-20261121-115343: analysis passed; one hosting/domain question blocked finalization.
- run-20261121-115437: clarification passed; plan failed coverage for standalone test/deployment tasks.
- run-20261121-115524: new plan on the same validated analysis passed all automated checks.

The successful plan uses prompt `plan-v4-explicit-implementation-task-coverage`. Its change clarifies
implementation-task ownership and distinguishes the additional governance list from the entire RACI.
Schema and validators were not weakened. The previous v3 evaluation freeze and raw outputs remain intact;
v4 is a subsequent development change and must not be reported as that frozen version's result.

## Assisted content review, pending user review

| Expected behavior | Actual result |
| --- | --- |
| Exact fixed opening hours | R1 / AC1 retains Monday to Friday, 09:00-17:00 |
| Reading without signing in | R2 / AC2 tests an unsigned visitor |
| No editing, booking or account features | R3 / AC3 preserves exclusions |
| Existing company hosting/domain after clarification | R4 / AC4 cites reply evidence |
| Evidence-supported implementation ownership | RA1: T1 is both A and R; covers TASK1 and TASK2 |
| Separate testing and deployment | RA2 and RA3, each with exactly one A and an R |

Two tasks, four criteria, three RACI rows, no open questions. Source IDs resolve to original text.
No unsupported product feature was identified in this assisted review. This simple success does not
establish overall extraction recall, robustness or correctness on the larger shopping-store cases.
