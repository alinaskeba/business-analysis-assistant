# Final implementation for assignment evaluation: v1.2-eval

The implementation is frozen after the UI RACI checkpoint test. This means no further tuning
while collecting evaluation results. It does not certify semantic correctness or all-case success.
Current code and prompts are copied into final-system/v1.2-eval with SHA-256 hashes. API keys are
excluded. The earlier v1-eval snapshot remains unchanged. Version 1.1 adds button approval,
reviewer corrections and one visible automatic RACI repair in the UI; it does not tune model prompts.
Version 1.2 adds separate print-ready exports for specification, tasks, criteria and RACI, using
browser Save as PDF. Prompts, schemas and generation policy remain unchanged from version 1.1.

Protocol:

1. Fix case labels and scenarios before execution. Existing dev families are development evaluation,
   not held-out evidence. Keep variants of the same source brief in one split.
2. Evaluate extraction from the initial brief without future answers or expected labels in input.
3. Supply only clarification answers corresponding to questions actually asked. Record supplied
   answers, unresolved questions and explicit approval; never silently manufacture a decision.
4. Generate work once, then RACI once. Permit at most one RACI repair (automatic in UI) with the same work,
   previous RACI and actual validator errors. No further attempts for the scored scenario.
5. Score first-attempt and repaired outcomes separately, including failures and request counts.
6. Score content against fixed expectations: preserved conditions, omissions, unsupported claims,
   evidence entailment, task/criterion coverage and actual RACI authority. Valid IDs are not entailment.
7. Distinguish fresh live journeys, saved-output browser demonstrations, fixtures and offline tests.

Current evidence: 86 Python tests and four offline UI generation-flow scenarios pass. The earlier
actual browser RACI-only repair passed automatic checks. The automatic two-attempt flow is tested
locally with mocked responses; no new live call was made for the UI changes.
Fresh initial analysis, clarification and initial work generation were not exercised in that browser
test. Known semantic failures remain in the tested plan and must be counted during evaluation.
Held-out final evaluation and complete live-journey scoring have not yet been performed.
