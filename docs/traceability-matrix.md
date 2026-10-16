# Requirements traceability matrix

| Requirement | Risk | Automated evidence | Manual/non-functional evidence | Status |
|---|---|---|---|---|
| REQ-01 Published events are browsable with availability and eligibility | R-08, R-12, R-13 | `test_api.py`, Node formatting tests, Playwright event-list test | Responsive/SEO/accessibility review | Covered |
| REQ-02 Eligible registration is confirmed below capacity | R-01, R-04 | `test_valid_registration_is_confirmed`, BDD primary flow | Exploratory booking charter | Covered |
| REQ-03 Registration at/above capacity is wait-listed | R-01 | `test_capacity_boundary_waitlist_and_fifo_promotion`, BDD capacity scenario | Concurrency charter | Covered |
| REQ-04 Cancellation promotes oldest wait-listed record | R-02 | Business-rule integration test, BDD transition scenario | State model review | Covered |
| REQ-05 Under-age and missing consent are rejected | R-04 | BVA/negative API tests | Message clarity review | Covered |
| REQ-06 Active duplicate registration is prevented | R-03 | Duplicate constraint/API tests | Double-click exploration | Covered |
| REQ-07 Retried keyed request returns original result | R-03 | Idempotency replay test | Network interruption charter | Covered |
| REQ-08 Errors use stable problem detail and request ID | R-09 | 404/422/header tests | Observability review | Covered |
| REQ-09 Untrusted input is stored/rendered safely | R-05, R-06 | SQL parameterization, HTML escaping and security tests | Threat-model review, ZAP | Covered |
| REQ-10 Critical flow supports keyboard and mobile viewport | R-08 | Playwright mobile + axe checks | Keyboard and screen-reader spot check | Covered with manual review |
| REQ-11 Public page exposes valid discovery metadata | R-13 | SEO source checks | Lighthouse/structured-data review | Covered |
| REQ-12 Quality assistant returns bounded reviewable suggestions | R-10, R-11 | AI evals, schema and fallback tests | Human review checklist | Covered |
| REQ-13 Service exposes health, timing, IDs and metrics | R-14 | Health/metrics/header tests | Dashboard/runbook review | Covered |
| REQ-14 Release decision consolidates independent evidence | R-15 | Evidence-bot unit/integration tests | Completion review | Covered |

Traceability is many-to-many by design. A single test may support several requirements, and a high-risk requirement should have more than one independent oracle.
