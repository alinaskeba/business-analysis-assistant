# Business analysis document package

Status: draft for document review.
Requirements are human-approved; proposed assumptions remain unapproved.

## Business Goals

```json
[
  {
    "id": "G1",
    "description": "Provide office visitors with a way to check office opening hours.",
    "source": {
      "document": "brief",
      "quote": "Build a small public web page so office visitors can check the office opening hours."
    }
  }
]
```

## Product Users

```json
[
  {
    "id": "U1",
    "name": "Office visitor",
    "responsibilities": [
      {
        "description": "Read office opening hours on the public web page.",
        "source": {
          "document": "brief",
          "quote": "office visitors can check the office opening hours."
        }
      }
    ]
  }
]
```

## Scope And Exclusions

```json
[
  {
    "id": "R3",
    "description": "The application shall not contain editing, booking, accounts or other features.",
    "source": {
      "document": "brief",
      "quote": "This version contains only this static information page; it has no editing, booking, accounts or other product features."
    },
    "kind": "constraint",
    "status": "confirmed"
  },
  {
    "id": "R4",
    "description": "The page must use the existing company hosting environment and the existing company domain.",
    "source": {
      "document": "A1",
      "quote": "The page will use the existing company hosting environment and the existing company domain"
    },
    "kind": "constraint",
    "status": "confirmed"
  }
]
```

## Functional Requirements

```json
[
  {
    "id": "R1",
    "description": "The page must display the fixed text \"Monday to Friday, 09:00-17:00\" to every visitor.",
    "source": {
      "document": "brief",
      "quote": "The page must display the fixed text \"Monday to Friday, 09:00-17:00\" to every visitor."
    },
    "kind": "functional",
    "status": "confirmed"
  },
  {
    "id": "R2",
    "description": "Visitors must be able to read the opening hours without signing in.",
    "source": {
      "document": "brief",
      "quote": "Visitors must be able to read the opening hours without signing in."
    },
    "kind": "functional",
    "status": "confirmed"
  }
]
```

## Quality Requirements And Constraints

```json
[
  {
    "id": "R3",
    "description": "The application shall not contain editing, booking, accounts or other features.",
    "source": {
      "document": "brief",
      "quote": "This version contains only this static information page; it has no editing, booking, accounts or other product features."
    },
    "kind": "constraint",
    "status": "confirmed"
  },
  {
    "id": "R4",
    "description": "The page must use the existing company hosting environment and the existing company domain.",
    "source": {
      "document": "A1",
      "quote": "The page will use the existing company hosting environment and the existing company domain"
    },
    "kind": "constraint",
    "status": "confirmed"
  }
]
```

## Project Team

```json
[
  {
    "id": "T1",
    "name": "Full-stack Developer",
    "responsibilities": [
      {
        "description": "Implement every product requirement and implementation task.",
        "source": {
          "document": "brief",
          "quote": "The Full-stack Developer is both Responsible and Accountable for implementing every product requirement and every implementation task."
        }
      },
      {
        "description": "Test every product requirement.",
        "source": {
          "document": "brief",
          "quote": "The Full-stack Developer is both Responsible and Accountable for testing every product requirement."
        }
      },
      {
        "description": "Deploy the page.",
        "source": {
          "document": "brief",
          "quote": "The Full-stack Developer is both Responsible and Accountable for deploying the page."
        }
      },
      {
        "description": "Provide the hosting environment and the domain name.",
        "source": {
          "document": "A1",
          "quote": "The Full-stack Developer is both Responsible and Accountable for providing the hosting environment and the domain name."
        }
      }
    ]
  }
]
```

## Confirmed Decisions

```json
[
  {
    "question_id": "Q1",
    "answer_id": "A1",
    "outcome": "resolved",
    "description": "The Full-stack Developer is responsible and accountable for the hosting and domain, utilizing existing company assets.",
    "source": {
      "document": "A1",
      "quote": "The Full-stack Developer is both Responsible and Accountable for providing the hosting environment and the domain name. The page will use the existing company hosting environment and the existing company domain; no purchase or new infrastructure is in scope."
    }
  }
]
```

## Proposed Assumptions

```json
[]
```

## Open Questions

```json
[]
```

## Tasks

```json
[
  {
    "id": "TASK1",
    "title": "Develop public static office hours page",
    "description": "Implement the public web page to display the required opening hours text string without any additional features.",
    "requirement_ids": [
      "R1",
      "R2",
      "R3"
    ]
  },
  {
    "id": "TASK2",
    "title": "Configure hosting and domain",
    "description": "Deploy the page using the existing company hosting environment and company domain.",
    "requirement_ids": [
      "R4"
    ]
  }
]
```

## Acceptance Criteria

```json
[
  {
    "id": "AC1",
    "requirement_id": "R1",
    "given": "An office visitor navigates to the public web page",
    "when": "the page loads",
    "then": "the text 'Monday to Friday, 09:00-17:00' is displayed on the screen",
    "source_ids": [
      "S2"
    ],
    "sources": [
      {
        "source_id": "S2",
        "document": "brief",
        "quote": "The page must display the fixed text \"Monday to Friday, 09:00-17:00\" to every visitor.",
        "start": 86,
        "end": 172
      }
    ]
  },
  {
    "id": "AC2",
    "requirement_id": "R2",
    "given": "A visitor is not signed in",
    "when": "the visitor navigates to the public web page",
    "then": "the visitor can view the opening hours text without a sign-in prompt",
    "source_ids": [
      "S3"
    ],
    "sources": [
      {
        "source_id": "S3",
        "document": "brief",
        "quote": "Visitors must be able to read the opening hours without signing in.",
        "start": 173,
        "end": 240
      }
    ]
  },
  {
    "id": "AC3",
    "requirement_id": "R3",
    "given": "A visitor is browsing the page",
    "when": "the visitor interacts with the page",
    "then": "no options for editing, booking, or creating accounts are accessible or visible",
    "source_ids": [
      "S4"
    ],
    "sources": [
      {
        "source_id": "S4",
        "document": "brief",
        "quote": "This version contains only this static information page; it has no editing, booking, accounts or other product features.",
        "start": 241,
        "end": 361
      }
    ]
  },
  {
    "id": "AC4",
    "requirement_id": "R4",
    "given": "The application is ready for release",
    "when": "deployment is initiated",
    "then": "the application is hosted on the existing company hosting environment and accessible via the existing company domain",
    "source_ids": [
      "S11"
    ],
    "sources": [
      {
        "source_id": "S11",
        "document": "A1",
        "quote": "The page will use the existing company hosting environment and the existing company domain; no purchase or new infrastructure is in scope.",
        "start": 120,
        "end": 258
      }
    ]
  }
]
```

## Raci

```json
[
  {
    "id": "RA1",
    "activity": "Implement static page and configure infrastructure",
    "task_ids": [
      "TASK1",
      "TASK2"
    ],
    "accountable": [
      {
        "role_id": "T1",
        "source_ids": [
          "S6",
          "S10"
        ],
        "sources": [
          {
            "source_id": "S6",
            "document": "brief",
            "quote": "The Full-stack Developer is both Responsible and Accountable for implementing every product requirement and every implementation task.",
            "start": 420,
            "end": 554
          },
          {
            "source_id": "S10",
            "document": "A1",
            "quote": "The Full-stack Developer is both Responsible and Accountable for providing the hosting environment and the domain name.",
            "start": 0,
            "end": 119
          }
        ]
      }
    ],
    "responsible": [
      {
        "role_id": "T1",
        "source_ids": [
          "S6",
          "S10"
        ],
        "sources": [
          {
            "source_id": "S6",
            "document": "brief",
            "quote": "The Full-stack Developer is both Responsible and Accountable for implementing every product requirement and every implementation task.",
            "start": 420,
            "end": 554
          },
          {
            "source_id": "S10",
            "document": "A1",
            "quote": "The Full-stack Developer is both Responsible and Accountable for providing the hosting environment and the domain name.",
            "start": 0,
            "end": 119
          }
        ]
      }
    ],
    "consulted": [],
    "informed": [],
    "activity_type": "implementation"
  },
  {
    "id": "RA2",
    "activity": "Test functional requirements",
    "task_ids": [
      "TASK1"
    ],
    "accountable": [
      {
        "role_id": "T1",
        "source_ids": [
          "S7"
        ],
        "sources": [
          {
            "source_id": "S7",
            "document": "brief",
            "quote": "The Full-stack Developer is both Responsible and Accountable for testing every product requirement.",
            "start": 555,
            "end": 654
          }
        ]
      }
    ],
    "responsible": [
      {
        "role_id": "T1",
        "source_ids": [
          "S7"
        ],
        "sources": [
          {
            "source_id": "S7",
            "document": "brief",
            "quote": "The Full-stack Developer is both Responsible and Accountable for testing every product requirement.",
            "start": 555,
            "end": 654
          }
        ]
      }
    ],
    "consulted": [],
    "informed": [],
    "activity_type": "testing"
  },
  {
    "id": "RA3",
    "activity": "Deploy public page",
    "task_ids": [
      "TASK2"
    ],
    "accountable": [
      {
        "role_id": "T1",
        "source_ids": [
          "S8"
        ],
        "sources": [
          {
            "source_id": "S8",
            "document": "brief",
            "quote": "The Full-stack Developer is both Responsible and Accountable for deploying the page.",
            "start": 655,
            "end": 739
          }
        ]
      }
    ],
    "responsible": [
      {
        "role_id": "T1",
        "source_ids": [
          "S8"
        ],
        "sources": [
          {
            "source_id": "S8",
            "document": "brief",
            "quote": "The Full-stack Developer is both Responsible and Accountable for deploying the page.",
            "start": 655,
            "end": 739
          }
        ]
      }
    ],
    "consulted": [],
    "informed": [],
    "activity_type": "deployment"
  }
]
```
