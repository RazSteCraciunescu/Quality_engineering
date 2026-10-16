# Portfolio map

This page connects the repository to work a quality engineer would perform during a real delivery cycle. It separates executable evidence from examples that need an optional tool.

| Capability | Practical evidence | Execution level |
|---|---|---|
| Requirement analysis | Acceptance criteria, ambiguity review and risk register | Reviewed document |
| Test planning | Scope, entry/exit criteria, environments, test levels and ownership | Reviewed document |
| ISTQB black-box design | Boundary values, partitions, decision tables and state transitions | Automated + manual |
| Static testing | API/schema review checklist, code-quality checks and threat-model review | Automated + manual |
| Unit testing | Booking rules, formatting, risk detection and evidence-gate calculations | Core automated |
| Integration testing | FastAPI + SQLite transactions, cancellation promotion and metrics | Core automated |
| API testing | Positive, negative, error contract, duplicate, idempotency and rate-limit paths | Core automated |
| Contract testing | Checked-in OpenAPI schema plus response validation | Core automated |
| UI system testing | Booking and quality-assistant user journeys | Optional Playwright |
| Acceptance testing | Gherkin examples written in user/business language | Optional Cucumber |
| Regression | Risk-ranked automated suite and release-gate thresholds | Core + CI |
| Exploratory testing | Time-boxed charters with notes, oracles and follow-up questions | Manual evidence |
| Accessibility | Keyboard, focus, labels, live regions, reduced motion and axe | Manual + optional automated |
| Compatibility | Desktop/mobile projects and browser support matrix | Optional Playwright |
| Visual testing | Stable dashboard baseline and screenshot comparison | Optional Playwright |
| Performance | Smoke, load, spike and soak scripts with explicit SLOs | Optional k6/JMeter |
| Reliability | Idempotency, duplicate protection, transaction boundaries and recovery | Core automated |
| Security | Threat model, input validation, headers, DAST/SAST/secrets/container scans | Core + optional tools |
| Privacy | Data minimization, synthetic fixtures and retention/deletion test ideas | Design + tests |
| SEO | Metadata, structured data, robots, sitemap and Lighthouse budgets | Core + optional Lighthouse |
| Data quality | Constraints, zero-row SQL assertions, duplicate/overbooking snapshot | Core automated |
| AI quality | Injection resistance, output schema, deterministic baseline and fallback | Core automated |
| Observability | Correlation IDs, structured logs, health and Prometheus metrics | Core automated |
| CI/CD | GitHub Actions, Jenkins and Azure Pipelines examples | Pipeline configuration |
| Containers/cloud | Docker, Compose, Kubernetes, Helm and Terraform | Optional infrastructure |
| RPA | Evidence aggregation bot with deterministic gate decision | Core automated |
| Lean Six Sigma | DMAIC case study and control plan for flaky automation | Process evidence |
| Enterprise tooling | Jira, Confluence, QMetry, TestRail and Jenkins-shaped fixtures | Public-safe samples |

## Test pyramid used here

- **Large base:** fast unit tests for business rules and pure formatting.
- **Middle:** API/integration/contract/data/security tests through an in-process FastAPI client.
- **Smaller UI layer:** a handful of critical user journeys across representative browser/device projects.
- **Targeted non-functional layers:** accessibility, security, performance, SEO and resilience checks selected by risk rather than run indiscriminately on every commit.

The project does not treat the pyramid as a quota. A test belongs at the lowest level that can detect the risk with sufficient confidence and useful diagnostics.
