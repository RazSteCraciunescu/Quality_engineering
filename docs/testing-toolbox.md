# Testing toolbox

The repository uses tools where they add a distinct signal. It does not claim that every team should run every tool on every commit.

| Concern | Primary implementation | Why it is here |
|---|---|---|
| Python service tests | pytest + FastAPI TestClient | Fast business, middleware and API feedback |
| Browser journeys | Playwright + TypeScript | Cross-browser, mobile, API context, traces and visual evidence |
| Accessibility | axe with Playwright + manual checklist | Automated triage plus human interaction review |
| Frontend units | Node test runner over compiled TypeScript modules | Fast utility, escaping and formatting checks without browser cost |
| BDD | Cucumber/Gherkin | Business-readable capacity and queue rules |
| API collaboration | OpenAPI + Postman | Contract, exploration and collection execution |
| Legacy browser stack | Selenium example | Demonstrates migration/maintenance awareness without duplicating the suite |
| Data | SQLite constraints + SQL assertions | Verify invariants directly |
| Performance | k6; JMeter equivalent | Code-based load model and enterprise-compatible plan |
| SEO | Lighthouse CI + static tests | Technical discoverability and performance budgets |
| Security | Threat model, pytest, ZAP, Semgrep, gitleaks, Trivy | Layered prevention and detection |
| AI quality | deterministic provider, Ollama adapter, JSON schema, eval dataset | Practical AI assistance with controlled failure modes |
| RPA/QualityOps | Python evidence aggregator | Remove repetitive report assembly, not tester judgement |
| CI/CD | GitHub Actions, Jenkinsfile, Azure Pipelines | Portable examples of quality gates |
| Deployability | Docker, Kubernetes, Helm, Terraform | Enough platform context to test releases and probes |
| Observability | request IDs, JSON logs, metrics, Grafana | Diagnose failures and validate production readiness |

## Deliberate non-choices

Cypress is not a second full browser suite because it would duplicate the Playwright signal. A migration note is in [`cypress-migration-note.md`](cypress-migration-note.md). Real Jira/QMetry/TestRail/Jenkins connections are not required; import-shaped fictional fixtures demonstrate familiarity without exposing credentials or private systems.
