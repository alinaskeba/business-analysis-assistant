# Business analysis document package

Status: draft for document review.
Requirements are human-approved; proposed assumptions remain unapproved.

## Business Goals

```json
[
  {
    "id": "G1",
    "description": "Enable beginners to set up and operate online retail businesses.",
    "source": {
      "document": "brief",
      "quote": "GAMMA-J needs a web store that enables people who are new to online commerce to set up and operate an online retail business."
    }
  },
  {
    "id": "G2",
    "description": "The business goal is to let store staff receive and process orders without manually transcribing customer messages.",
    "source": {
      "document": "A2",
      "quote": "The business goal is to let store staff receive and process orders without manually transcribing customer messages."
    }
  }
]
```

## Product Users

```json
[
  {
    "id": "U1",
    "name": "Store owners",
    "responsibilities": [
      {
        "description": "Manage products.",
        "source": {
          "document": "brief",
          "quote": "Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
        }
      },
      {
        "description": "Manage customer accounts.",
        "source": {
          "document": "brief",
          "quote": "Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
        }
      },
      {
        "description": "Store owners and sales personnel create products.",
        "source": {
          "document": "A2",
          "quote": "Store owners and sales personnel can create and update products and customer accounts."
        }
      },
      {
        "description": "Store owners and sales personnel create customer accounts.",
        "source": {
          "document": "A2",
          "quote": "Store owners and sales personnel can create and update products and customer accounts."
        }
      },
      {
        "description": "Store owners and sales personnel update products.",
        "source": {
          "document": "A2",
          "quote": "Store owners and sales personnel can create and update products and customer accounts."
        }
      },
      {
        "description": "Store owners and sales personnel update customer accounts.",
        "source": {
          "document": "A2",
          "quote": "Store owners and sales personnel can create and update products and customer accounts."
        }
      }
    ]
  },
  {
    "id": "U2",
    "name": "Sales personnel",
    "responsibilities": [
      {
        "description": "Manage products.",
        "source": {
          "document": "brief",
          "quote": "Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
        }
      },
      {
        "description": "Manage customer accounts.",
        "source": {
          "document": "brief",
          "quote": "Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
        }
      },
      {
        "description": "Store owners and sales personnel create products.",
        "source": {
          "document": "A2",
          "quote": "Store owners and sales personnel can create and update products and customer accounts."
        }
      },
      {
        "description": "Store owners and sales personnel create customer accounts.",
        "source": {
          "document": "A2",
          "quote": "Store owners and sales personnel can create and update products and customer accounts."
        }
      },
      {
        "description": "Store owners and sales personnel update products.",
        "source": {
          "document": "A2",
          "quote": "Store owners and sales personnel can create and update products and customer accounts."
        }
      },
      {
        "description": "Store owners and sales personnel update customer accounts.",
        "source": {
          "document": "A2",
          "quote": "Store owners and sales personnel can create and update products and customer accounts."
        }
      }
    ]
  },
  {
    "id": "U3",
    "name": "Customers",
    "responsibilities": [
      {
        "description": "Browse available products.",
        "source": {
          "document": "brief",
          "quote": "Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
        }
      },
      {
        "description": "Maintain a shopping cart.",
        "source": {
          "document": "brief",
          "quote": "Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
        }
      },
      {
        "description": "Place orders.",
        "source": {
          "document": "brief",
          "quote": "Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
        }
      },
      {
        "description": "Customers browse available products.",
        "source": {
          "document": "brief",
          "quote": "Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
        }
      },
      {
        "description": "Customers add available products to the cart.",
        "source": {
          "document": "A2",
          "quote": "Customers can add available products to the cart, change quantities to positive whole numbers, and remove items."
        }
      },
      {
        "description": "Successful submission creates one order with selected items and quantities.",
        "source": {
          "document": "A2",
          "quote": "A successful submission creates one order containing the selected items and quantities and displays its reference."
        }
      },
      {
        "description": "Customers may browse without signing in.",
        "source": {
          "document": "A2",
          "quote": "Customers may browse without signing in but must sign in before placing an order."
        }
      },
      {
        "description": "Customers must sign in before order placement.",
        "source": {
          "document": "A2",
          "quote": "Customers may browse without signing in but must sign in before placing an order."
        }
      },
      {
        "description": "Customers change cart quantities to positive whole numbers.",
        "source": {
          "document": "A2",
          "quote": "Customers can add available products to the cart, change quantities to positive whole numbers, and remove items."
        }
      },
      {
        "description": "Customers remove cart items.",
        "source": {
          "document": "A2",
          "quote": "Customers can add available products to the cart, change quantities to positive whole numbers, and remove items."
        }
      },
      {
        "description": "Successful submission displays its order reference.",
        "source": {
          "document": "A2",
          "quote": "A successful submission creates one order containing the selected items and quantities and displays its reference."
        }
      },
      {
        "description": "Reject empty-cart submission without creating an order.",
        "source": {
          "document": "A2",
          "quote": "An empty cart cannot be submitted."
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
    "id": "R18",
    "description": "First release serves one store.",
    "kind": "constraint",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "The first release serves one store."
    }
  },
  {
    "id": "R19",
    "description": "Orders are for staff processing; online payment and shipping integrations are excluded.",
    "kind": "constraint",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "Orders are submitted for staff processing; online payments and shipping integrations are outside the first release."
    }
  },
  {
    "id": "R20",
    "description": "First release is due eight weeks after requirements approval.",
    "kind": "constraint",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "The first release is due eight weeks after requirements approval."
    }
  }
]
```

## Functional Requirements

```json
[
  {
    "id": "R1",
    "description": "Store owners and sales personnel create products.",
    "kind": "functional",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "Store owners and sales personnel can create and update products and customer accounts."
    }
  },
  {
    "id": "R2",
    "description": "Store owners and sales personnel create customer accounts.",
    "kind": "functional",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "Store owners and sales personnel can create and update products and customer accounts."
    }
  },
  {
    "id": "R3",
    "description": "Customers browse available products.",
    "kind": "functional",
    "status": "confirmed",
    "source": {
      "document": "brief",
      "quote": "Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store."
    }
  },
  {
    "id": "R4",
    "description": "Customers add available products to the cart.",
    "kind": "functional",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "Customers can add available products to the cart, change quantities to positive whole numbers, and remove items."
    }
  },
  {
    "id": "R5",
    "description": "Successful submission creates one order with selected items and quantities.",
    "kind": "functional",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "A successful submission creates one order containing the selected items and quantities and displays its reference."
    }
  },
  {
    "id": "R6",
    "description": "Customers may browse without signing in.",
    "kind": "functional",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "Customers may browse without signing in but must sign in before placing an order."
    }
  },
  {
    "id": "R7",
    "description": "Customers must sign in before order placement.",
    "kind": "functional",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "Customers may browse without signing in but must sign in before placing an order."
    }
  },
  {
    "id": "R9",
    "description": "Customers change cart quantities to positive whole numbers.",
    "kind": "functional",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "Customers can add available products to the cart, change quantities to positive whole numbers, and remove items."
    }
  },
  {
    "id": "R10",
    "description": "Customers remove cart items.",
    "kind": "functional",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "Customers can add available products to the cart, change quantities to positive whole numbers, and remove items."
    }
  },
  {
    "id": "R12",
    "description": "Store owners and sales personnel update products.",
    "kind": "functional",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "Store owners and sales personnel can create and update products and customer accounts."
    }
  },
  {
    "id": "R14",
    "description": "Store owners and sales personnel update customer accounts.",
    "kind": "functional",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "Store owners and sales personnel can create and update products and customer accounts."
    }
  },
  {
    "id": "R16",
    "description": "Successful submission displays its order reference.",
    "kind": "functional",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "A successful submission creates one order containing the selected items and quantities and displays its reference."
    }
  },
  {
    "id": "R17",
    "description": "Reject empty-cart submission without creating an order.",
    "kind": "functional",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "An empty cart cannot be submitted."
    }
  }
]
```

## Quality Requirements And Constraints

```json
[
  {
    "id": "R18",
    "description": "First release serves one store.",
    "kind": "constraint",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "The first release serves one store."
    }
  },
  {
    "id": "R19",
    "description": "Orders are for staff processing; online payment and shipping integrations are excluded.",
    "kind": "constraint",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "Orders are submitted for staff processing; online payments and shipping integrations are outside the first release."
    }
  },
  {
    "id": "R20",
    "description": "First release is due eight weeks after requirements approval.",
    "kind": "constraint",
    "status": "confirmed",
    "source": {
      "document": "A2",
      "quote": "The first release is due eight weeks after requirements approval."
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
      },
      {
        "description": "The Product Owner approves the user acceptance testing results.",
        "source": {
          "document": "A1",
          "quote": "The Product Owner approves the user acceptance testing results."
        }
      },
      {
        "description": "The Product Owner is accountable for specification acceptance and user acceptance testing.",
        "source": {
          "document": "A3",
          "quote": "The Product Owner is accountable for specification acceptance and user acceptance testing."
        }
      },
      {
        "description": "The Product Owner is accountable for the final release decision.",
        "source": {
          "document": "A3",
          "quote": "The Product Owner is accountable for the final release decision."
        }
      },
      {
        "description": "Accountable for specification preparation.",
        "source": {
          "document": "A4",
          "quote": "The Product Owner is Accountable for specification preparation."
        }
      },
      {
        "description": "Review and approve the specification; Responsible and Accountable for specification acceptance.",
        "source": {
          "document": "A4",
          "quote": "The Product Owner reviews and approves the specification and is both Responsible and Accountable for its acceptance."
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
      },
      {
        "description": "The Business Analyst is responsible for preparing the specification.",
        "source": {
          "document": "A3",
          "quote": "The Business Analyst is responsible for preparing the specification."
        }
      },
      {
        "description": "Responsible for preparing the specification.",
        "source": {
          "document": "A4",
          "quote": "The Business Analyst is Responsible for preparing the specification."
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
      },
      {
        "description": "The Full-stack Developer is accountable for implementation and deployment.",
        "source": {
          "document": "A3",
          "quote": "The Full-stack Developer is accountable for implementation and deployment."
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
      },
      {
        "description": "The QA Engineer is accountable for test execution.",
        "source": {
          "document": "A3",
          "quote": "The QA Engineer is accountable for test execution."
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
    "description": "The supplied answer provides the requested facts or decision.",
    "source": {
      "document": "A1",
      "quote": "The project team consists of a Product Owner, a Business Analyst, a Full-stack Developer, and a QA Engineer. The Product Owner defines priorities, approves business requirements, and makes the final release decision. The Business Analyst gathers and clarifies requirements, prepares the specification, and maintains links between requirements and implementation tasks. The Full-stack Developer makes technical implementation decisions, develops the application, and deploys releases. The QA Engineer prepares and executes tests, records defects, and reports whether the release meets the agreed acceptance criteria. The Product Owner approves the user acceptance testing results."
    }
  },
  {
    "question_id": "Q2",
    "answer_id": "A2",
    "outcome": "resolved",
    "description": "The supplied answer provides the requested facts or decision.",
    "source": {
      "document": "A2",
      "quote": "The first release serves one store. Customers may browse without signing in but must sign in before placing an order. Customers can add available products to the cart, change quantities to positive whole numbers, and remove items. Store owners and sales personnel can create and update products and customer accounts. Orders are submitted for staff processing; online payments and shipping integrations are outside the first release. A successful submission creates one order containing the selected items and quantities and displays its reference. An empty cart cannot be submitted. The business goal is to let store staff receive and process orders without manually transcribing customer messages. The Product Owner accepts the first release when the agreed browse-cart-order flow passes user acceptance testing. The first release is due eight weeks after requirements approval. Store owner is the Product Owner for this project."
    }
  },
  {
    "question_id": "Q3",
    "answer_id": "A3",
    "outcome": "resolved",
    "description": "The supplied answer provides the requested facts or decision.",
    "source": {
      "document": "A3",
      "quote": "The Product Owner is accountable for specification acceptance and user acceptance testing. The Business Analyst is responsible for preparing the specification. The Full-stack Developer is accountable for implementation and deployment. The QA Engineer is accountable for test execution. The Product Owner is accountable for the final release decision."
    }
  },
  {
    "question_id": "Q4",
    "answer_id": "A4",
    "outcome": "resolved",
    "description": "The supplied clarification specifies preparation and acceptance authority.",
    "source": {
      "document": "A4",
      "quote": "The Business Analyst is Responsible for preparing the specification. The Product Owner is Accountable for specification preparation. The Product Owner reviews and approves the specification and is both Responsible and Accountable for its acceptance."
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
    "title": "Develop product and customer management features",
    "description": "Implement CRUD functionality for store owners and sales personnel to manage products and customer accounts.",
    "requirement_ids": [
      "R1",
      "R2",
      "R12",
      "R14"
    ]
  },
  {
    "id": "TASK2",
    "title": "Develop storefront browsing and cart operations",
    "description": "Implement product catalog browsing and shopping cart management for customers.",
    "requirement_ids": [
      "R3",
      "R4",
      "R6",
      "R9",
      "R10"
    ]
  },
  {
    "id": "TASK3",
    "title": "Develop order submission processing",
    "description": "Implement order creation logic, requirement for sign-in, and feedback of order reference.",
    "requirement_ids": [
      "R5",
      "R7",
      "R16",
      "R17"
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
    "given": "a store owner or sales personnel is logged in",
    "when": "the user creates a new product with valid details",
    "then": "a new product is recorded in the system",
    "source_ids": [
      "S12"
    ],
    "sources": [
      {
        "source_id": "S12",
        "document": "A2",
        "quote": "Store owners and sales personnel can create and update products and customer accounts.",
        "start": 231,
        "end": 317
      }
    ]
  },
  {
    "id": "AC2",
    "requirement_id": "R2",
    "given": "a store owner or sales personnel is logged in",
    "when": "the user creates a new customer account",
    "then": "a new customer account is created",
    "source_ids": [
      "S12"
    ],
    "sources": [
      {
        "source_id": "S12",
        "document": "A2",
        "quote": "Store owners and sales personnel can create and update products and customer accounts.",
        "start": 231,
        "end": 317
      }
    ]
  },
  {
    "id": "AC3",
    "requirement_id": "R3",
    "given": "a visitor to the store",
    "when": "the visitor browses the available products",
    "then": "the product list is displayed",
    "source_ids": [
      "S2"
    ],
    "sources": [
      {
        "source_id": "S2",
        "document": "brief",
        "quote": "Store owners and sales personnel should be able to manage products and customer accounts, while customers should be able to browse the available products, maintain a shopping cart, and place orders through the store.",
        "start": 126,
        "end": 342
      }
    ]
  },
  {
    "id": "AC4",
    "requirement_id": "R4",
    "given": "a product is available in the store",
    "when": "the customer adds the product to the cart",
    "then": "the product is listed in the user's cart",
    "source_ids": [
      "S11"
    ],
    "sources": [
      {
        "source_id": "S11",
        "document": "A2",
        "quote": "Customers can add available products to the cart, change quantities to positive whole numbers, and remove items.",
        "start": 118,
        "end": 230
      }
    ]
  },
  {
    "id": "AC5",
    "requirement_id": "R5",
    "given": "a customer has products in the cart and is signed in",
    "when": "the customer submits the order",
    "then": "one order is created containing the selected items and their quantities",
    "source_ids": [
      "S14"
    ],
    "sources": [
      {
        "source_id": "S14",
        "document": "A2",
        "quote": "A successful submission creates one order containing the selected items and quantities and displays its reference.",
        "start": 434,
        "end": 548
      }
    ]
  },
  {
    "id": "AC6",
    "requirement_id": "R6",
    "given": "a guest visitor",
    "when": "the user browses products",
    "then": "the system displays the product catalog without requiring a sign-in",
    "source_ids": [
      "S10"
    ],
    "sources": [
      {
        "source_id": "S10",
        "document": "A2",
        "quote": "Customers may browse without signing in but must sign in before placing an order.",
        "start": 36,
        "end": 117
      }
    ]
  },
  {
    "id": "AC7",
    "requirement_id": "R7",
    "given": "a guest visitor with items in the cart",
    "when": "the user attempts to place an order",
    "then": "the system mandates a sign-in before order processing proceeds",
    "source_ids": [
      "S10"
    ],
    "sources": [
      {
        "source_id": "S10",
        "document": "A2",
        "quote": "Customers may browse without signing in but must sign in before placing an order.",
        "start": 36,
        "end": 117
      }
    ]
  },
  {
    "id": "AC8",
    "requirement_id": "R9",
    "given": "an item in the cart",
    "when": "the customer updates the quantity to a positive whole number",
    "then": "the cart quantity is updated to that integer",
    "source_ids": [
      "S11"
    ],
    "sources": [
      {
        "source_id": "S11",
        "document": "A2",
        "quote": "Customers can add available products to the cart, change quantities to positive whole numbers, and remove items.",
        "start": 118,
        "end": 230
      }
    ]
  },
  {
    "id": "AC9",
    "requirement_id": "R10",
    "given": "an item in the cart",
    "when": "the customer removes the item",
    "then": "the item is no longer in the cart",
    "source_ids": [
      "S11"
    ],
    "sources": [
      {
        "source_id": "S11",
        "document": "A2",
        "quote": "Customers can add available products to the cart, change quantities to positive whole numbers, and remove items.",
        "start": 118,
        "end": 230
      }
    ]
  },
  {
    "id": "AC10",
    "requirement_id": "R12",
    "given": "an existing product record",
    "when": "a store owner or sales personnel updates the product details",
    "then": "the product record reflects the updated information",
    "source_ids": [
      "S12"
    ],
    "sources": [
      {
        "source_id": "S12",
        "document": "A2",
        "quote": "Store owners and sales personnel can create and update products and customer accounts.",
        "start": 231,
        "end": 317
      }
    ]
  },
  {
    "id": "AC11",
    "requirement_id": "R14",
    "given": "an existing customer account",
    "when": "a store owner or sales personnel updates the account details",
    "then": "the account record reflects the updated information",
    "source_ids": [
      "S12"
    ],
    "sources": [
      {
        "source_id": "S12",
        "document": "A2",
        "quote": "Store owners and sales personnel can create and update products and customer accounts.",
        "start": 231,
        "end": 317
      }
    ]
  },
  {
    "id": "AC12",
    "requirement_id": "R16",
    "given": "a successful order submission",
    "when": "the order creation completes",
    "then": "an order reference is displayed to the customer",
    "source_ids": [
      "S14"
    ],
    "sources": [
      {
        "source_id": "S14",
        "document": "A2",
        "quote": "A successful submission creates one order containing the selected items and quantities and displays its reference.",
        "start": 434,
        "end": 548
      }
    ]
  },
  {
    "id": "AC13",
    "requirement_id": "R17",
    "given": "an empty cart",
    "when": "the user attempts to submit the order",
    "then": "the submission is rejected and no order is created",
    "source_ids": [
      "S15"
    ],
    "sources": [
      {
        "source_id": "S15",
        "document": "A2",
        "quote": "An empty cart cannot be submitted.",
        "start": 549,
        "end": 583
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
    "activity": "Requirements Approval",
    "task_ids": [],
    "accountable": [
      {
        "role_id": "T1",
        "source_ids": [
          "S4"
        ],
        "sources": [
          {
            "source_id": "S4",
            "document": "A1",
            "quote": "The Product Owner defines priorities, approves business requirements, and makes the final release decision.",
            "start": 109,
            "end": 216
          }
        ]
      }
    ],
    "responsible": [
      {
        "role_id": "T1",
        "source_ids": [
          "S4"
        ],
        "sources": [
          {
            "source_id": "S4",
            "document": "A1",
            "quote": "The Product Owner defines priorities, approves business requirements, and makes the final release decision.",
            "start": 109,
            "end": 216
          }
        ]
      }
    ],
    "consulted": [],
    "informed": [],
    "activity_type": "requirements_approval"
  },
  {
    "id": "RA2",
    "activity": "Specification Preparation",
    "task_ids": [],
    "accountable": [
      {
        "role_id": "T1",
        "source_ids": [
          "S26"
        ],
        "sources": [
          {
            "source_id": "S26",
            "document": "A4",
            "quote": "The Product Owner is Accountable for specification preparation.",
            "start": 69,
            "end": 132
          }
        ]
      }
    ],
    "responsible": [
      {
        "role_id": "T2",
        "source_ids": [
          "S21",
          "S25",
          "S5"
        ],
        "sources": [
          {
            "source_id": "S21",
            "document": "A3",
            "quote": "The Business Analyst is responsible for preparing the specification.",
            "start": 91,
            "end": 159
          },
          {
            "source_id": "S25",
            "document": "A4",
            "quote": "The Business Analyst is Responsible for preparing the specification.",
            "start": 0,
            "end": 68
          },
          {
            "source_id": "S5",
            "document": "A1",
            "quote": "The Business Analyst gathers and clarifies requirements, prepares the specification, and maintains links between requirements and implementation tasks.",
            "start": 217,
            "end": 368
          }
        ]
      }
    ],
    "consulted": [],
    "informed": [],
    "activity_type": "specification_preparation"
  },
  {
    "id": "RA3",
    "activity": "Specification Acceptance",
    "task_ids": [],
    "accountable": [
      {
        "role_id": "T1",
        "source_ids": [
          "S20",
          "S27"
        ],
        "sources": [
          {
            "source_id": "S20",
            "document": "A3",
            "quote": "The Product Owner is accountable for specification acceptance and user acceptance testing.",
            "start": 0,
            "end": 90
          },
          {
            "source_id": "S27",
            "document": "A4",
            "quote": "The Product Owner reviews and approves the specification and is both Responsible and Accountable for its acceptance.",
            "start": 133,
            "end": 249
          }
        ]
      }
    ],
    "responsible": [
      {
        "role_id": "T1",
        "source_ids": [
          "S27"
        ],
        "sources": [
          {
            "source_id": "S27",
            "document": "A4",
            "quote": "The Product Owner reviews and approves the specification and is both Responsible and Accountable for its acceptance.",
            "start": 133,
            "end": 249
          }
        ]
      }
    ],
    "consulted": [],
    "informed": [],
    "activity_type": "specification_acceptance"
  },
  {
    "id": "RA4",
    "activity": "User Acceptance Testing",
    "task_ids": [],
    "accountable": [
      {
        "role_id": "T1",
        "source_ids": [
          "S20"
        ],
        "sources": [
          {
            "source_id": "S20",
            "document": "A3",
            "quote": "The Product Owner is accountable for specification acceptance and user acceptance testing.",
            "start": 0,
            "end": 90
          }
        ]
      }
    ],
    "responsible": [
      {
        "role_id": "T1",
        "source_ids": [
          "S17",
          "S8"
        ],
        "sources": [
          {
            "source_id": "S17",
            "document": "A2",
            "quote": "The Product Owner accepts the first release when the agreed browse-cart-order flow passes user acceptance testing.",
            "start": 700,
            "end": 814
          },
          {
            "source_id": "S8",
            "document": "A1",
            "quote": "The Product Owner approves the user acceptance testing results.",
            "start": 616,
            "end": 679
          }
        ]
      }
    ],
    "consulted": [
      {
        "role_id": "T4",
        "source_ids": [
          "S7"
        ],
        "sources": [
          {
            "source_id": "S7",
            "document": "A1",
            "quote": "The QA Engineer prepares and executes tests, records defects, and reports whether the release meets the agreed acceptance criteria.",
            "start": 484,
            "end": 615
          }
        ]
      }
    ],
    "informed": [],
    "activity_type": "uat_acceptance"
  },
  {
    "id": "RA5",
    "activity": "Final Release Decision",
    "task_ids": [],
    "accountable": [
      {
        "role_id": "T1",
        "source_ids": [
          "S24",
          "S4"
        ],
        "sources": [
          {
            "source_id": "S24",
            "document": "A3",
            "quote": "The Product Owner is accountable for the final release decision.",
            "start": 286,
            "end": 350
          },
          {
            "source_id": "S4",
            "document": "A1",
            "quote": "The Product Owner defines priorities, approves business requirements, and makes the final release decision.",
            "start": 109,
            "end": 216
          }
        ]
      }
    ],
    "responsible": [
      {
        "role_id": "T1",
        "source_ids": [
          "S4"
        ],
        "sources": [
          {
            "source_id": "S4",
            "document": "A1",
            "quote": "The Product Owner defines priorities, approves business requirements, and makes the final release decision.",
            "start": 109,
            "end": 216
          }
        ]
      }
    ],
    "consulted": [],
    "informed": [],
    "activity_type": "release_decision"
  },
  {
    "id": "RA6",
    "activity": "Implementation of core store features",
    "task_ids": [
      "TASK1",
      "TASK2",
      "TASK3"
    ],
    "accountable": [
      {
        "role_id": "T3",
        "source_ids": [
          "S22",
          "S6"
        ],
        "sources": [
          {
            "source_id": "S22",
            "document": "A3",
            "quote": "The Full-stack Developer is accountable for implementation and deployment.",
            "start": 160,
            "end": 234
          },
          {
            "source_id": "S6",
            "document": "A1",
            "quote": "The Full-stack Developer makes technical implementation decisions, develops the application, and deploys releases.",
            "start": 369,
            "end": 483
          }
        ]
      }
    ],
    "responsible": [
      {
        "role_id": "T3",
        "source_ids": [
          "S22",
          "S6"
        ],
        "sources": [
          {
            "source_id": "S22",
            "document": "A3",
            "quote": "The Full-stack Developer is accountable for implementation and deployment.",
            "start": 160,
            "end": 234
          },
          {
            "source_id": "S6",
            "document": "A1",
            "quote": "The Full-stack Developer makes technical implementation decisions, develops the application, and deploys releases.",
            "start": 369,
            "end": 483
          }
        ]
      }
    ],
    "consulted": [],
    "informed": [],
    "activity_type": "implementation"
  }
]
```
