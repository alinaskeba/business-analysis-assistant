# Historical prompt iterations on the team dev brief

Used run-analysis-eval. Draft expectations were unchanged and unapproved; no held-out evaluation ran.
The brief, model and schema stayed fixed; only instructions changed. Each directory stores instructions,
schema and run metadata with hashes. There was one live request per version, not a stability study.

| Version | Python validation | Observation |
| --- | --- | --- |
| Initial team analysis | pass | 4 team roles, 6 requirements; manager and PO launch authority missing |
| prompt-v3 | fail | T1 quote absent from brief; raw response not captured, so content review skipped |
| prompt-v3.1 | fail | 5 roles, 10 requirements; T1 joins sentences using invented [...] |
| prompt-v3.2 | fail | Quotes/structure/references passed preceding checks; M2 has no question |

Instructions added sentence coverage, users-to-requirements duplication, independent actions,
nontechnical project participants, explicit authority, separate role entries for distant evidence,
neutral questions and relevant unknowns. v3.2 required separate entries and forbade joined quotes.

v3.1 restored viewing (R2), creation (R3), own cancellation (R4), room attributes (R5), overlap prevention
(R6) and manager advice/acceptance (T5). The approval user was missing; Q1 still proposed combining rules.
v3.2 had six duty records for five roles: T1/T2 represented PO and T2 retained launch authority;
T6 retained manager advice and acceptance. But only five requirements remained: viewing, creating,
cancelling, adding rooms and preventing overlap were missing. The approval user was missing again.
M2 invented signing an acceptance certificate; questions addressed C1 and M1 only, leaving M2 uncovered.
T1's description also claimed launch authority beyond its own quote, despite T2 containing that evidence.

None of these three candidates passed all checks. v3.1/v3.2 raw outputs are stored unedited and marked
failed; the CLI rejects them. Three local tests passed then; they validated Python, not model quality.
The experimental v3.2 prompt was later superseded. A proposed separate extraction/coverage pass was
not implemented in this experiment. Original artifacts remain unchanged; this review is English.
