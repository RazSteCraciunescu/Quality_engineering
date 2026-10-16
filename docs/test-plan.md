# Test plan: CivicShift 1.0

## Scope

### In scope

Event discovery, eligibility, booking, wait-list behavior, cancellation promotion, duplicate handling, idempotent retries, public error contract, web accessibility, API/security headers, data integrity, AI-assisted test design, observability and deployment smoke behavior.

### Out of scope

Email delivery, payment, identity provider integration, privileged administration, real personal data, production disaster recovery and third-party analytics. These do not exist in the demo product and are not represented as tested.

## Milestones

| Stage | Main activity | Evidence |
|---|---|---|
| Design review | Ambiguity, risk, API/schema and threat review | Comments, updated criteria, risk register |
| Build validation | Unit, static and migration tests | CI results |
| Feature validation | API, integration, BDD and exploratory sessions | JUnit, notes, defects |
| Non-functional | Accessibility, security, performance, SEO and compatibility | Tool reports + manual review |
| Release decision | Evidence consolidation and residual-risk review | Gate JSON and completion report |

## Responsibilities

| Role | Responsibility |
|---|---|
| Product owner | Clarify business outcomes and accept residual product risk |
| Developer | Implement, unit test, review logs and resolve defects |
| Quality engineer | Own test analysis, automation strategy, exploratory work and evidence quality |
| DevOps/platform | Maintain pipeline, environment, deployment and observability controls |
| Security/accessibility specialists | Review high-risk findings when specialist judgment is needed |

A small team may combine roles, but the decisions remain visible.

## Test data

Synthetic `.test` email addresses and fictional names only. Tests create unique values and use temporary databases. No production export is required.

## Suspension/resumption

Suspend the affected suite when the environment cannot preserve data isolation, the migration fails, more than 20% of tests fail from one confirmed infrastructure incident, or a P0 defect makes downstream results meaningless. Resume after a targeted smoke check proves the blocker is removed.

## Deliverables

Test strategy, risk register, traceability matrix, automated results, exploratory notes, accessibility/security/performance/SEO evidence, defect reports, AI eval report, release evidence and completion summary.
