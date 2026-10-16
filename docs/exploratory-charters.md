# Exploratory testing charters

Each charter is time-boxed to 45–60 minutes. Notes should include data, environment, observations, questions and follow-up tests—not only pass/fail.

## Charter A — Last place under pressure

**Explore:** booking around the final available place.  
**Vary:** two browsers, delayed requests, refresh, back button, double-click, reused/new idempotency keys, email case, cancellation during submission.  
**Oracles:** capacity invariant, one active event/email, consistent status, request IDs, DB snapshot.  
**Main risks:** overbooking, duplicate records, stale UI, misleading confirmation.

## Charter B — Wait-list state integrity

Build a queue of at least three records, cancel confirmed and wait-listed records in different orders, repeat cancellation and inspect resulting order/timestamps.

Look for skipped people, double promotion, status resurrection, non-deterministic ordering and incorrect availability counts.

## Charter C — Accessibility and stress

Use keyboard only, 200% zoom, reduced motion, high contrast, browser validation and server validation. Read labels/errors with a screen reader spot check if available.

Look for focus loss after async update, invisible errors, unlabeled controls, color-only state and dialog escape problems.

## Charter D — AI assistant distrust

Submit clear, ambiguous, contradictory and instruction-like requirements. Compare outputs at low/medium/high risk. Ask whether each scenario is supported by the test basis, duplicates another scenario, invents features or omits a critical risk.

The assistant succeeds when it produces reviewable suggestions and fails safely—not when it produces the largest list.

## Charter E — Operability

Stop/restart the service, make the DB read-only, send invalid JSON, exceed the rate limit and inspect health, logs, metrics and client errors.

Look for false-green health, missing correlation IDs, sensitive logs, hanging requests and unrecoverable local state.
