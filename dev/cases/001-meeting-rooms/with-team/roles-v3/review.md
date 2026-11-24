# Historical v4 baseline and v5 candidate with role schema v3

Same dev case 001-meeting-rooms/with-team; run-analysis-eval was used. baseline-v4 is a copy of an
existing live response, not a regeneration; script, prompt, schema, metadata and brief were preserved.
candidate-v5 was one new live request on the same input/model, with provenance and hashes in run.json.
**Schema, prompt and validator changed together.** Effects cannot be attributed to one change alone.
Expectations remained draft; scoring against approved labels was skipped.

| Check | v4 baseline | v5 candidate |
| --- | --- | --- |
| Quotes | fail: T1 contains [...] | pass: all nested quotes are verbatim |
| Question coverage | fail: M1 uncovered | pass: Q1 targets C1, Q2 targets M1 |
| One PO role, separate duty evidence | Not supported by old schema | T1 has two responsibilities and separate quotes |
| Approval process role | Missing from users | U3 is Office manager with original approval quote |
| Unknown interaction method | Not separated | M1 channel gap, Q2 approval-method question |
| Duplicate conflict as gap | Status gap duplicates conflict | Separate M1 needs a channel decision |
| Requirement coverage | 10 requirements | 6; omissions remain |

One PO record preserves priorities/rules and launch authority in separate responsibilities. All five
team roles are present; C1 references R4/R5 without being resolved by the model.

## Remaining human-review issues

- U1/U2 contain viewing, creating/cancelling own bookings and adding rooms, but requirements omit these actions.
- Q1 introduces automatic confirmation followed by cancellation if the manager refuses; this behavior is
  absent from the brief. It is a leading question, not a confirmed requirement.
- U3's description drops before-confirmation timing, though its quote and R5 retain it.
- G2 treats the one-month deadline as an outcome as well as constraint R6. Classification needs review.
  Time zone and success metrics are still not clarified.
- The approval-channel gap is relevant only if approval is retained after resolving C1.

The new validator finds both known errors in the original baseline using its archived schema.
The new candidate passed with zero errors. Ten local tests covered nested quotes, joined evidence
plus uncovered gaps, independent errors, duplicate roles, empty duties, archives and CLI rejection.
Passing validation does not prove semantic support or full extraction; one request does not establish
stability or held-out generalization. These raw Ukrainian runs remain historical, not English outputs.
