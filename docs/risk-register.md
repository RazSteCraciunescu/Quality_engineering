# Product quality risk register

Scoring uses **probability × impact**, each from 1 to 5. A score of 15–25 is critical, 8–12 high, 4–6 medium and 1–3 low. Scores guide depth and order; they do not replace judgment.

| ID | Risk | P | I | Score | Test response | Residual risk |
|---|---|---:|---:|---:|---|---|
| R-01 | Concurrent requests overbook the final place | 3 | 5 | 15 | Transaction boundary, capacity BVA, near-simultaneous API test, DB assertion | SQLite locking differs from distributed production DB |
| R-02 | Cancellation promotes the wrong wait-listed person | 3 | 5 | 15 | State-transition model, FIFO integration test, timestamp checks | Equal timestamps need deterministic secondary ordering |
| R-03 | Retry or double-click creates duplicate registrations | 4 | 4 | 16 | Idempotency and case-insensitive unique constraints, UI disable, replay tests | Clients that omit keys still depend on business duplicate detection |
| R-04 | Under-age or non-consenting person is accepted | 2 | 5 | 10 | BVA at minimum age, server-side negative tests | Source age is self-declared |
| R-05 | Personal data is exposed or retained unnecessarily | 2 | 5 | 10 | Response review, log review, privacy checklist, synthetic data | Demo has no automated retention job |
| R-06 | Injection/XSS payload executes | 3 | 5 | 15 | Parameterized SQL, escaped templates, security tests, ZAP/Semgrep | New render paths require continued review |
| R-07 | Rate limiting blocks legitimate shared-network users | 3 | 3 | 9 | Boundary test, Retry-After, production design review | In-memory/IP limiter is demo-only |
| R-08 | Mobile or keyboard user cannot complete booking | 3 | 4 | 12 | Responsive Playwright projects, keyboard charter, axe | Automated tools cannot prove full usability |
| R-09 | Error contract differs from OpenAPI/client expectation | 3 | 3 | 9 | Contract tests and negative cases | Generated clients not included |
| R-10 | AI assistant follows injected requirement text | 3 | 4 | 12 | Delimiting, deterministic baseline, injection evals, schema validation | Optional model behavior varies by model/version |
| R-11 | AI suggestions are accepted as evidence without review | 3 | 4 | 12 | UI/repository review note, process gate, provenance field | Human process risk remains |
| R-12 | Slow event list or registration harms conversion | 2 | 4 | 8 | k6 budgets, browser/Lighthouse budgets, metrics | Local load model is not production capacity planning |
| R-13 | Bad metadata prevents discovery | 2 | 3 | 6 | SEO unit checks, Lighthouse, robots/sitemap review | Placeholder domain must be replaced before deployment |
| R-14 | Deployment appears healthy while database is unavailable | 2 | 5 | 10 | Readiness probe, health test, container smoke | Single-node demo has no failover |
| R-15 | Flaky automation hides genuine regression | 3 | 4 | 12 | Stable selectors, isolated data, no product retries, DMAIC control plan | Browser/network variance remains |

## Review cadence

Review when acceptance criteria change, a defect escapes, a new dependency/trust boundary is introduced, or performance/security evidence changes the estimated probability or impact.
