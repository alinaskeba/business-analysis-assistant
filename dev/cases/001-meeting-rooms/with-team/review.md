# Historical exploratory run: the same brief with a team

Split: dev. The first live request failed with HTTP 503; the second succeeded. Run metadata contains
the model, time and prompt/brief hashes. The prompt and schema were unchanged for this comparison.
Draft expectations were not approved; formal scoring against approved labels was skipped.

| Check | Status | Observation |
| --- | --- | --- |
| Structure, quotes, IDs and references | pass | validate_analysis accepted the response |
| Missing-team gap | needs human review | The earlier M1 asked about the team; that gap disappeared |
| Four core team roles | needs human review | T1-T4: PO, BA, Full-stack Developer, QA; quotes contain their duties |
| Office manager as project participant | needs human review | Missing from team_roles; present only as approval user U3 |
| Launch authority | needs human review | The PO launch-decision sentence is absent from the response evidence/descriptions |
| Contradictory positions | needs human review | Separate R1/R2, C1 references both, Q1 targets C1 and blocks specification |
| Original requirement coverage | needs human review | Available-room viewing, own booking creation/cancellation and adding rooms/attributes are missing |

The source explicitly assigns room-rule advice and acceptance testing to the office manager, but
team_roles has only four entries. Employee actions remain in U1 evidence but not requirements;
room addition/capacity/equipment remain in U2 evidence but not requirements.
Counts changed: team_roles 0 to 4, requirements 9 to 6, gaps 1 to 2. Counts alone do not measure quality.
IDs are not stable across runs: compare meaning and evidence. New gaps concern stack and mail provider;
time zone, duration and success metrics remain unaddressed. U2's infrastructure-management description
is broader than adding rooms. The result is not a ready specification despite Python validation.

The raw output is unedited. Later experiments: [v3-v3.2](prompt-comparison.md),
[user v4](prompt-v4-user/review.md), [schema v3 / prompt v5](roles-v3/review.md).
Use the [English adaptation](../en/README.md) for future reviewed runs.
