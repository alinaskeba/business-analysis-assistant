> OFFLINE MOCK FIXTURE: partial illustration, not live model output.

# Business analysis document package

Status: draft for document review.
Requirements are human-approved; proposed assumptions remain unapproved.

## Business Goals

```json
[
  {
    "id": "G1",
    "description": "Enable new online retailers to run a store",
    "source": {
      "document": "brief",
      "quote": "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business."
    }
  }
]
```

## Product Users

```json
[]
```

## Scope And Exclusions

```json
[
  {
    "id": "R3",
    "kind": "constraint",
    "status": "confirmed",
    "description": "No online payment or shipping integrations in release one",
    "source": {
      "document": "A2",
      "quote": "Orders are submitted for staff processing; online payments and shipping integrations are outside the first release."
    }
  }
]
```

## Functional Requirements

```json
[
  {
    "id": "R1",
    "description": "Store staff manage products",
    "source": {
      "document": "brief",
      "quote": "Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
    },
    "kind": "functional",
    "status": "confirmed"
  },
  {
    "id": "R2",
    "description": "Reject empty-cart submission",
    "source": {
      "document": "A2",
      "quote": "An empty cart cannot be submitted."
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
    "kind": "constraint",
    "status": "confirmed",
    "description": "No online payment or shipping integrations in release one",
    "source": {
      "document": "A2",
      "quote": "Orders are submitted for staff processing; online payments and shipping integrations are outside the first release."
    }
  }
]
```

## Project Team

```json
[
  {
    "id": "T1",
    "name": "Product Owner",
    "responsibilities": [
      {
        "description": "The Product Owner defines priorities, approves business requirements, and makes the final release decision.",
        "source": {
          "document": "A1",
          "quote": "The Product Owner defines priorities, approves business requirements, and makes the final release decision."
        }
      }
    ]
  },
  {
    "id": "T2",
    "name": "Business Analyst",
    "responsibilities": [
      {
        "description": "The Business Analyst gathers and clarifies requirements, prepares the specification, and maintains links between requirements and implementation tasks.",
        "source": {
          "document": "A1",
          "quote": "The Business Analyst gathers and clarifies requirements, prepares the specification, and maintains links between requirements and implementation tasks."
        }
      }
    ]
  },
  {
    "id": "T3",
    "name": "Full-stack Developer",
    "responsibilities": [
      {
        "description": "The Full-stack Developer makes technical implementation decisions, develops the application, and deploys releases.",
        "source": {
          "document": "A1",
          "quote": "The Full-stack Developer makes technical implementation decisions, develops the application, and deploys releases."
        }
      }
    ]
  },
  {
    "id": "T4",
    "name": "QA Engineer",
    "responsibilities": [
      {
        "description": "The QA Engineer prepares and executes tests, records defects, and reports whether the release meets the agreed acceptance criteria.",
        "source": {
          "document": "A1",
          "quote": "The QA Engineer prepares and executes tests, records defects, and reports whether the release meets the agreed acceptance criteria."
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
    "description": "The user supplied this decision",
    "source": {
      "document": "A1",
      "quote": "The project team consists of a Product Owner, a Business Analyst, a Full-stack Developer, and a QA Engineer. The Product Owner defines priorities, approves business requirements, and makes the final release decision. The Business Analyst gathers and clarifies requirements, prepares the specification, and maintains links between requirements and implementation tasks. The Full-stack Developer makes technical implementation decisions, develops the application, and deploys releases. The QA Engineer prepares and executes tests, records defects, and reports whether the release meets the agreed acceptance criteria. The Product Owner approves the user acceptance testing results."
    }
  },
  {
    "question_id": "Q2",
    "answer_id": "A2",
    "outcome": "resolved",
    "description": "The user supplied this decision",
    "source": {
      "document": "A2",
      "quote": "The first release serves one store. Customers may browse without signing in but must sign in before placing an order. Customers can add available products to the cart, change quantities to positive whole numbers, and remove items. Store owners and sales personnel can create and update products and customer accounts. Orders are submitted for staff processing; online payments and shipping integrations are outside the first release. A successful submission creates one order containing the selected items and quantities and displays its reference. An empty cart cannot be submitted. The business goal is to let store staff receive and process orders without manually transcribing customer messages. The Product Owner accepts the first release when the agreed browse-cart-order flow passes user acceptance testing. The first release is due eight weeks after requirements approval. Store owner is the Product Owner for this project."
    }
  },
  {
    "question_id": "Q3",
    "answer_id": "A3",
    "outcome": "resolved",
    "description": "The user supplied this decision",
    "source": {
      "document": "A3",
      "quote": "The Product Owner is accountable for specification acceptance and user acceptance testing. The Business Analyst is responsible for preparing the specification. The Full-stack Developer is accountable for implementation and deployment. The QA Engineer is accountable for test execution. The Product Owner is accountable for the final release decision."
    }
  }
]
```

## Proposed Assumptions

```json
[
  {
    "id": "P1",
    "description": "A shared staging environment may help delivery",
    "rationale": "Proposal only; not supplied by the customer",
    "status": "proposed"
  }
]
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
    "title": "Implement product management",
    "description": "Implement supported staff operations",
    "requirement_ids": [
      "R1"
    ]
  },
  {
    "id": "TASK2",
    "title": "Reject empty checkout",
    "description": "Enforce empty-cart rule",
    "requirement_ids": [
      "R2",
      "R3"
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
    "given": "A store staff member",
    "when": "They manage a product",
    "then": "The supported product operation succeeds",
    "source": {
      "document": "brief",
      "quote": "Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
    }
  },
  {
    "id": "AC2",
    "requirement_id": "R2",
    "given": "An empty cart",
    "when": "The customer attempts order submission",
    "then": "No order is submitted",
    "source": {
      "document": "A2",
      "quote": "An empty cart cannot be submitted."
    }
  }
]
```

## Raci

```json
[
  {
    "id": "RA1",
    "activity": "Implement and deploy",
    "task_ids": [
      "TASK1",
      "TASK2"
    ],
    "accountable": [
      {
        "role_id": "T3",
        "source": {
          "document": "A3",
          "quote": "The Full-stack Developer is accountable for implementation and deployment."
        }
      }
    ],
    "responsible": [
      {
        "role_id": "T3",
        "source": {
          "document": "A1",
          "quote": "The Full-stack Developer makes technical implementation decisions, develops the application, and deploys releases."
        }
      }
    ],
    "consulted": [],
    "informed": []
  }
]
```
