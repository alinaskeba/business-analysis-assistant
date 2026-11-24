# Historical user-proposed prompt v4

One live Gemini request used the unchanged team dev brief. run.json records hashes/model and failure.
Schema/validator stayed fixed; draft expectations remained unapproved. Formal scoring was skipped.
Previous instructions and the script were archived. Copying removed formatting artifacts only:
trailing backslashes, escaped list markers and the HTML space entity.

| Check | Status | Evidence |
| --- | --- | --- |
| JSON structure/types | pass | validate_schema accepts the sections |
| Verbatim evidence | fail | T1 joins two sentences with invented [...] |
| A question for every gap | fail | M1 exists, but the only question Q1 targets C1 |
| Both conflict positions linked | pass | C1 references R6/R7, both with original quotes |
| Business-content coverage | needs human review | Observations below are not automatic proof |

CLI stopped at T1; the missing M1 question was found by separate inspection. The raw response is stored
without repairs. All three local tests passed then; this did not validate prompt quality.
The initial team result had six requirements/four roles; v4 had ten requirements/five roles:
viewing, creation, own cancellation, room attributes, overlap prohibition, both confirmation rules,
sign-in, email and deadline were preserved. PO launch authority returned in the description, but
its joined source was invalid. Office manager remained absent from users despite the approval rule.
M1 about approval status duplicated C1. Time rules, concrete sign-in and success metric remained absent.

One role with one quote makes distant PO duties awkward to represent. A sources array was suggested;
the later responsibilities schema implemented per-duty evidence instead. Raw artifacts remain original.
