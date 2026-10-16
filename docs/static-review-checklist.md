# Static review checklist

## Requirement review

- Actor and intended value are clear.
- Acceptance criteria are observable and not implementation-only.
- Boundaries, error behavior and state transitions are stated.
- Privacy, accessibility, performance and operability impacts were considered.
- Dependencies, data ownership and out-of-scope behavior are explicit.
- Testability exists without production data or manual database edits.

## Code and automation review

- Business rules are server-side and covered at the lowest useful layer.
- SQL is parameterized and constraints protect critical invariants.
- Tests make one useful claim, use stable selectors and avoid fixed sleep.
- Generated data is unique and cleanup/isolation is understood.
- Logs and failures preserve diagnostic evidence without secrets.
- Retries, skips and quarantines have a narrow purpose and owner.
- Configuration is environment-driven; no machine-specific paths or credentials.
