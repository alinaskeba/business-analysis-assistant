# Offline RACI review

OpenAI support was removed at the user's request. No new live API requests were made.
Gemini remains the only provider. Existing evaluation labels and historical responses are unchanged.

Fixed a false-positive rule: Consulted/Informed evidence was required to name the same governance
decision verb as Accountable/Responsible. Consultation and notification do not establish approval
authority. All assignments still require existing team-role IDs, existing source IDs and role-linked
evidence. A/R governance checks remain. C/I relevance is explicitly retained in semantic review,
not claimed to be proved by a role-source intersection.

This correction does not fix missing implementation RACI or unknown roles in generated responses.
The existing source-ID shopping-store runs still fail task coverage; do not report them as successes.
Prompt v4 explicitly requests that coverage, but no new shopping-store run was authorized/performed
in this offline review. Overall quality on the dev set is not established by these local tests.

Next development option: generate implementation tasks and acceptance criteria separately from RACI,
so a RACI failure can be retried alone with the exact validation errors and unchanged approved facts.
Do not fill responsibilities from role titles, inject expected labels, or mark invalid plans final.
