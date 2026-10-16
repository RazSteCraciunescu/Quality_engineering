# Observability and testability

## Signals

- `/api/health` provides a small readiness-oriented response.
- `/metrics` exposes request, registration and data-quality measures in Prometheus text format.
- Every response includes `X-Request-ID` and `X-Response-Time-Ms`.
- Structured logs include method, path, status, timing and request ID, but not attendee name/email.

## Test uses

Correlation IDs connect UI/API failures to server logs. Metrics support post-deployment smoke and synthetic monitoring. Data-quality gauges detect invariants that normal uptime checks miss.

## Alert concepts

- elevated 5xx rate;
- registration latency above SLO;
- non-zero data-quality violations;
- repeated rate-limit events beyond expected traffic;
- health failure or absent metrics scrape.

The sample Grafana dashboard is infrastructure evidence, not a claim that live production monitoring is running.
