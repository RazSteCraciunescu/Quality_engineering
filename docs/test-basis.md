# Test basis

## Product summary

CivicShift allows a visitor to browse published volunteer events and register for one. A registration is either **confirmed** or **wait-listed**. A confirmed registration can be cancelled, at which point the oldest eligible wait-listed registration is promoted.

All data is fictional. The service is a portfolio system, not a real volunteer platform.

## Actors

- **Visitor:** browses events and submits a registration.
- **Registered volunteer:** can retrieve or cancel a registration by its reference in the demo API.
- **Coordinator:** represented by quality reports and fixtures; no production-grade admin identity is implemented.
- **Quality engineer:** reviews requirements, risks, evidence and release gates.

## Functional requirements

### FR-01 Browse published events

The event list shows title, description, start time, location, minimum age, remaining places and wait-list state. Only events with status `published` are returned by the public API.

### FR-02 Validate registration data

Name, email, age and consent are required. Name length is 2–80 visible characters; email length is at most 254 characters; age is 0–120. Product-specific minimum age remains a separate business rule.

### FR-03 Enforce eligibility

A volunteer younger than an event's minimum age cannot register. The exact minimum age is accepted.

### FR-04 Protect capacity

Confirmed registrations must never exceed event capacity. When a place is available, a valid registration is confirmed. When no place remains, it is wait-listed.

### FR-05 Prevent active duplicates

The same normalized email cannot have two active registrations for the same event. A cancelled registration does not prevent a later new registration.

### FR-06 Support safe retries

A valid `Idempotency-Key` is 8–80 characters. Replaying the same successful request with the same key returns the original registration and does not create another row. Reusing the key with a different payload is rejected as a conflict.

### FR-07 Cancel and promote fairly

Cancelling a confirmed registration changes its state to `cancelled` and promotes the oldest wait-listed registration for that event. Cancelling an already-cancelled registration is safe and has no second side effect.

### FR-08 Generate test-design suggestions

The Quality Lab accepts a requirement and risk level, then returns structured test suggestions. The default rules provider works offline. An optional local Ollama provider must fall back safely when unavailable or invalid.

## Non-functional requirements

| ID | Requirement |
|---|---|
| NFR-01 | Main visitor flows are keyboard operable, labelled and understandable at 200% zoom. |
| NFR-02 | Public browse API p95 is under 400 ms in the local reference load model. |
| NFR-03 | Critical API responses include a request identifier and avoid stack traces or secrets. |
| NFR-04 | The public page includes unique title, description, canonical URL, robots and sitemap data. |
| NFR-05 | Stored records preserve capacity, uniqueness and foreign-key constraints. |
| NFR-06 | Service health, structured request logs and basic operational metrics are available. |
| NFR-07 | AI suggestions are treated as proposals; schema validation and human review are mandatory. |

## Out of scope

Real identity, real personal data, payment, email/SMS delivery, background workers and production cloud accounts are intentionally excluded. Their interfaces can be simulated, but the repository does not claim they exist.
