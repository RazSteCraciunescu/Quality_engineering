# Release readiness report

**Candidate:** CivicShift 1.0.0 portfolio baseline  
**Decision:** Ready for local/public portfolio demonstration  
**Decision owner:** human reviewer; automation supplies evidence only

## Evidence summary

- Core business rules have unit/API regression coverage.
- Capacity, duplicate and wait-list integrity have database constraints and zero-row queries.
- OpenAPI snapshot and response-schema checks are present.
- Public UI has browser, mobile, accessibility, SEO and visual test paths.
- Security controls include threat model, response headers, CORS, injection checks, SAST/DAST configurations and secret scanning.
- AI suggestions have deterministic behavior, fallback and adversarial eval cases.
- Deployment examples include health/readiness, resources and security context.

## Verified local baseline — 31 August 2026

This repository snapshot was checked as a release candidate rather than presented as production evidence:

| Check | Result |
|---|---:|
| Python API, repository, security, data and AI tests | 70 passed |
| Backend branch-aware coverage | 95.20% |
| Concurrent capacity stress loop | Passed in repeated local runs |
| Dependency-free Node web tests | 3 passed |
| Live booking smoke | 1 passed in Chromium |
| Python compilation and source syntax checks | Passed |
| JSON, YAML, XML and JMeter asset parsing | Passed |
| Public-safety and repository-structure validator | Passed |

The full Playwright browser/device matrix, axe scan, Lighthouse, ZAP and load jobs remain CI or scheduled gates. Generated output belongs in `reports/generated/`; the small checked-in report files are explicitly labelled format examples.

## Residual risks

- SQLite behavior is not proof of production database concurrency semantics.
- No real identity, email delivery or admin workflow is implemented.
- Manual screen-reader and real-device evidence should be collected before a real public launch.
- Optional Ollama behavior depends on the selected model and requires its own measured evaluation.
- Performance thresholds are reference assumptions, not production capacity claims.

## Release conditions

Portfolio release is acceptable when core pytest and repository validation pass, the application smoke test succeeds, and no credentials/private data are present. A real production release would additionally require the browser matrix, DAST, load test, infrastructure review, manual accessibility evidence and approved operational ownership.
