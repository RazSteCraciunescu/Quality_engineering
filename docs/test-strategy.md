# Test strategy

## Quality objective

Demonstrate that a volunteer can discover an event, understand eligibility, register exactly once, receive the correct capacity outcome and recover safely from cancellation or retry—without exposing data, exceeding capacity or excluding keyboard/mobile users.

## Test basis

- Product rules in this repository and the OpenAPI contract.
- Acceptance examples in the Gherkin feature files.
- Security, privacy, accessibility, SEO and performance quality attributes.
- The risk register and architecture trust boundaries.

## Risk-based priorities

**P0 / release blocking**

- Capacity is exceeded or two callers receive the final place.
- Cancellation promotes the wrong record or corrupts state.
- Duplicate/idempotent requests create extra records.
- SQL/script input is executed instead of treated as data.
- Personal data appears in broad list responses or logs.
- AI output escapes its schema or follows injected instructions.

**P1 / normally release blocking**

- Eligibility or consent boundaries are inconsistent between UI and API.
- Critical booking flow cannot be completed with keyboard or mobile viewport.
- Error responses lack actionable detail or correlation ID.
- Performance exceeds the defined API or page budgets.
- Search metadata, robots or canonical configuration is materially broken.

**P2 / evaluated with context**

- Cosmetic layout issues without loss of information.
- Low-frequency browser differences outside the supported matrix.
- Non-critical documentation or optional-tool issues.

## Test levels

### Unit

Pure formatting, scenario generation, risk detection, rate-limiter behavior and release-gate parsing.

### Component/integration

FastAPI handlers with a temporary SQLite database, including transaction and constraint behavior.

### System/API

End-to-end HTTP behavior, status codes, problem detail, headers, OpenAPI, data integrity and observability.

### UI/end-to-end

Representative booking, validation, wait-list and quality-assistant flows in Chromium, Firefox, WebKit and mobile profiles. UI checks focus on high-value journeys rather than duplicating every API branch.

### Acceptance

Gherkin scenarios express capacity, eligibility, duplicate and cancellation behavior in business language.

## Test types

Functional, regression, smoke, sanity, exploratory, accessibility, usability, compatibility, responsive, visual, API, contract, data, schema, security, privacy, performance, load, spike, soak, reliability, recovery, resilience, SEO, observability, installability, deployment and AI evaluation.

## Entry criteria

- Acceptance criteria and risk owner identified.
- Test environment starts from a known seed.
- Schema migration succeeds.
- OpenAPI generation succeeds.
- No unresolved P0 design ambiguity.

## Exit criteria

- All core automated checks pass.
- No open P0/P1 defect without recorded acceptance.
- Critical requirements have automated or explicit manual evidence.
- Data-quality assertions return zero violations.
- Accessibility has no serious/critical automated finding and the keyboard flow is manually reviewed.
- Security baseline has no high-confidence high-severity finding.
- Performance budgets meet the agreed target or a documented waiver exists.
- Evidence bot returns `PASS` or an authorized `CONDITIONAL` decision.

## Environments

| Environment | Purpose | Data |
|---|---|---|
| In-process test app | Fast deterministic API/integration checks | New temp DB per test |
| Local app | Manual exploration and browser automation | Synthetic seed plus test-created records |
| Docker Compose | Container smoke and dependency parity | Disposable volume |
| CI | Repeatable quality gates | Ephemeral fixtures |
| Kubernetes example | Deployment and probe review | No live cluster required |

## Defect handling

Defects include observed/expected behavior, reproducibility, environment, evidence, impact and a risk-based severity. Samples intentionally show uncertainty and follow-up questions rather than pretending every investigation is complete.

## Automation principles

- Test behavior, not implementation trivia.
- Keep one clear assertion theme per test.
- Prefer API/data setup over brittle UI setup.
- Use deterministic identifiers and isolated databases.
- Retry infrastructure only; do not hide product failures with test retries.
- Track quarantined tests with owner, reason and expiry.
- A generated AI suggestion never becomes test evidence until reviewed and executed.
