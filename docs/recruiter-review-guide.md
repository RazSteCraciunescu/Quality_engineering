# Ten-minute review guide

## Minute 1–2: see the product

Run the service, open the page and register for an event. The app is intentionally small enough to understand quickly.

## Minute 3–4: inspect one hard rule

Read `FR-04` and `FR-07` in `test-basis.md`, then open:

- `services/api/civicshift/database.py`
- `services/api/tests/test_business_rules.py`
- `docs/test-design/decision-table.md`
- `automation/gherkin/features/waitlist.feature`

## Minute 5–6: look beyond happy-path automation

Review security, accessibility, data and AI tests under `tests/`, plus the threat model and AI evaluation dataset.

## Minute 7–8: examine delivery thinking

Open `.github/workflows/ci.yml`, `Dockerfile`, Kubernetes deployment, metrics endpoint and `devops-for-testers.md`.

## Minute 9–10: judge test leadership

Read the risk register, exploratory session, DMAIC case study and release report. These show prioritisation, defect learning and communication rather than framework familiarity alone.
