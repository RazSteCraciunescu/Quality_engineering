# DevOps understanding for testers

A quality engineer does not need to own the platform to test delivery risk intelligently.

## Pipeline flow

1. Static repository and secret checks.
2. TypeScript build and Node unit tests.
3. Python lint, unit/API/data/security/AI tests and coverage.
4. Build the container once.
5. Start the built artifact and run smoke/contract tests.
6. Run browser/accessibility tests against that artifact.
7. Run non-functional checks on schedule or release candidate.
8. Aggregate evidence and publish a release decision.

## Tester review points

- Does CI test the same artifact that is deployed?
- Are environment variables explicit and secrets injected securely?
- Do readiness/liveness probes prove different things?
- Can a migration and old application version overlap safely?
- Are failures diagnosable through request ID, logs and retained reports?
- Are test retries hiding nondeterminism?
- Is rollback tested, and what happens to data written by the new version?
- Are security and performance checks placed where they provide timely feedback?

## Kubernetes probes

Liveness answers “should this process be restarted?” Readiness answers “should traffic be sent here?” The sample uses `/api/health` for both because the demo has one local dependency; a production design should expose separate semantics and include database readiness without making liveness depend on a transient external service.

## Infrastructure as code

Kubernetes, Helm and Terraform examples are reviewable and lintable without deploying. The portfolio tests configuration for non-root execution, resource limits, read-only filesystem where practical, probe paths and explicit environment configuration.
