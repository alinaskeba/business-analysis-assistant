# Draft expectations for manual approval - English translated adaptation

Status: **DRAFT - not approved**. Case: 001-meeting-rooms/with-team/en. Split: dev.
This is a translated adaptation of the existing 36 expectations, preserving E-IDs and draft status.
The source is the translated brief with the team addition, not the observed model response.
No English model run or formal assessment has been performed.

| ID | Expected finding / preserved conditions | Expected location | Verbatim English evidence or context | Question / check |
| --- | --- | --- | --- | --- |
| E01 | Reduce scheduling clashes; do not invent a numeric target. | goals | The goal is to reduce scheduling clashes in bookings. |  |
| E02 | A small web application for this office; internal scope, not public customers. | requirements: scope/constraint | We need a small web application for booking meeting rooms in our office. / A small team is building the internal meeting-room booking application. The first version is planned in one month. |  |
| E03 | The employee views available rooms by BOTH date and time. | users: Employee AND separate functional requirement | An employee views available rooms by date and time, creates and cancels their own booking. |  |
| E04 | The employee creates their OWN booking. | users: Employee AND separate functional requirement | An employee views available rooms by date and time, creates and cancels their own booking. |  |
| E05 | The employee cancels their OWN booking, not arbitrary bookings. | users: Employee AND separate functional requirement distinct from E04 | An employee views available rooms by date and time, creates and cancels their own booking. |  |
| E06 | The administrator adds rooms with capacity AND equipment. Editing/deleting is not stated. | users: Administrator AND functional requirement with attributes | An administrator adds rooms, their capacity and equipment. |  |
| E07 | Prohibit overlapping booking times for the SAME room, not different rooms. | functional requirement | The system does not allow the same room to be booked for a time that overlaps another booking. |  |
| E08 | ALL bookings are confirmed automatically AND immediately; retain despite the conflict. | separate functional requirement | All bookings are confirmed automatically and immediately. |  |
| E09 | EVERY booking must be approved by the office manager BEFORE confirmation. Preserve actor, scope and timing. | users: Office manager AND separate functional requirement | Every booking must be approved by the office manager before confirmation. |  |
| E10 | Sign-in uses corporate email; no provider or protocol is specified. | functional requirement | Sign-in uses corporate email. |  |
| E11 | Email booking confirmations; no invented templates, recipients or extra reminders. | functional requirement | Email booking confirmations are required. |  |
| E12 | One-month deadline for the first version. Repetition is not a second requirement; classify as constraint, not an extra business goal. | one constraint requirement | We want the first version in one month. / The first version is planned in one month. |  |
| E13 | Product Owner FROM THE ADMINISTRATIVE DEPARTMENT sets priorities. | team_roles responsibility; one record per each of the five roles | The Product Owner from the administrative department sets priorities and makes decisions about booking rules. |  |
| E14 | Product Owner decides booking rules; authority is not an already selected rule. | team_roles responsibility; one record per each of the five roles | The Product Owner from the administrative department sets priorities and makes decisions about booking rules. |  |
| E15 | Product Owner decides whether to launch the first version. | team_roles responsibility; one record per each of the five roles | The Product Owner makes the decision to launch the first version. |  |
| E16 | Business Analyst gathers requirements. | team_roles responsibility; one record per each of the five roles | The Business Analyst gathers requirements, prepares the specification and agrees it with the Product Owner. |  |
| E17 | Business Analyst prepares the specification. | team_roles responsibility; one record per each of the five roles | The Business Analyst gathers requirements, prepares the specification and agrees it with the Product Owner. |  |
| E18 | Business Analyst agrees the specification WITH the Product Owner. | team_roles responsibility; one record per each of the five roles | The Business Analyst gathers requirements, prepares the specification and agrees it with the Product Owner. |  |
| E19 | Full-stack Developer is responsible for technical implementation. | team_roles responsibility; one record per each of the five roles | The Full-stack Developer is responsible for technical implementation and deployment. |  |
| E20 | Full-stack Developer is responsible for deployment; do not equate this with launch authority. | team_roles responsibility; one record per each of the five roles | The Full-stack Developer is responsible for technical implementation and deployment. |  |
| E21 | QA Engineer is responsible for testing. | team_roles responsibility; one record per each of the five roles | The QA Engineer is responsible for testing, including checking simultaneous bookings of the same room. |  |
| E22 | QA testing explicitly includes simultaneous bookings of the SAME room. | team_roles responsibility; one record per each of the five roles | The QA Engineer is responsible for testing, including checking simultaneous bookings of the same room. |  |
| E23 | Office manager advises on room-use rules. | team_roles responsibility; one record per each of the five roles | The office manager advises on room-use rules and participates in acceptance testing. |  |
| E24 | Office manager participates in acceptance testing; launch authority is not assigned to them. | team_roles responsibility; one record per each of the five roles | The office manager advises on room-use rules and participates in acceptance testing. |  |
| E25 | Exactly one expected conflict: immediate automatic confirmation of all bookings versus approval of every booking before confirmation; link two distinct requirement IDs. | contradictions | All bookings are confirmed automatically and immediately. / Every booking must be approved by the office manager before confirmation. | Neutral: Which booking-confirmation rule should apply? blocks_final_specification=true. Do not propose cancellation after confirmation. |
| E26 | Do not duplicate E25 as a booking-status gap requiring the same decision. | contradictions only for this decision | All bookings are confirmed automatically and immediately. / Every booking must be approved by the office manager before confirmation. | One conflict and its linked question suffice. |
| E27 | An unknown manager interaction channel does not remove the role from users. A separate conditional gap is relevant if approval is retained. | missing_information + question | Every booking must be approved by the office manager before confirmation. | How should the manager participate in approval if this process is selected? Do not treat a web interface as agreed. |
| E28 | The time zone is unspecified and affects time interpretation and overlaps. | missing_information + question | An employee views available rooms by date and time, creates and cancels their own booking. / The system does not allow the same room to be booked for a time that overlaps another booking. | Which time zone should apply? Do not invent a value. |
| E29 | Booking duration/time-interval rules are not specified and affect booking behavior. | missing_information + question | An employee views available rooms by date and time, creates and cancels their own booking. / The system does not allow the same room to be booked for a time that overlaps another booking. | What start/end or duration rules are allowed? Do not invent increments or limits. |
| E30 | The stated goal has no measurable success criterion. | missing_information + question | The goal is to reduce scheduling clashes in bookings. | How will the customer decide that clashes have decreased sufficiently? Do not invent a percentage. |
| E31 | Corporate email does not specify the business sign-in method. | missing_information + question | Sign-in uses corporate email. | How should users sign in with corporate email? Do not require an OAuth/stack choice as a business decision. |
| E32 | Do not add room editing/deletion, recurring bookings, reminders, new statuses or automatic cancellation as confirmed requirements. | unsupported-fact check |  |  |
| E33 | Do not make PO, BA, Developer or QA product users solely because they are on the team; do not equate Administrator with PO. | role separation check |  |  |
| E34 | Do not declare the conflict resolved by PO authority; do not treat deployment as launch permission. | decision check |  |  |
| E35 | All quotes are verbatim without [...]; references exist; every gap/conflict has a question; missing facts have no invented evidence. | validation and evidence check |  |  |
| E36 | Questions do not introduce new behavior as given or desired. Alternatives only clarify the existing contradictory rules. | neutrality check |  |  |

A slash separates distinct evidence options in this table; it never permits joining them in source.quote.
E04 and E05 require separate requirements. Capacity and equipment in E06 qualify the stated add action;
do not invent separate management operations. One team-role record may contain several responsibilities,
but every duty must be explicitly preserved with sufficient evidence. Office manager is also a user by E09.

E27 depends on the answer to E25. Assess blocking for E28-E31 individually with an explanation;
no single blocking flag is imposed on all gaps. New relevant gaps require human review, not automatic
rejection. Missing topics are not gaps without a specific impact. Gap evidence is context only,
not a quote proving an absent fact; do not attach source to missing_information.

After approval, assess each E-ID as correct / partial / missing / needs-human-review, with the brief
fragment, JSON path and output ID or an explicit missing entry. Record unsupported facts separately.
Match by meaning/evidence, not unstable model IDs. Freeze approved labels; revise them explicitly.
The proposed prompt-only comparison remains pending approval and translation review.
