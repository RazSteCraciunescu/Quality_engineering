# Non-functional quality model

## Accessibility

Target WCAG 2.2 AA for the critical public flow. Automated axe checks are a safety net; manual keyboard, zoom/reflow, focus, error comprehension and screen-reader spot checks remain required.

Release blockers include an unreachable action, keyboard trap, missing accessible name on a critical control, serious/critical axe finding or status change that is not exposed to assistive technology.

## Performance and scalability

Local SLO-oriented budgets:

- health p95 below 150 ms at 20 VUs;
- event-list p95 below 300 ms at 20 VUs;
- registration p95 below 600 ms at 10 VUs;
- HTTP error rate below 1%, excluding deliberate negative requests;
- Lighthouse performance score at least 0.90 on the static landing path;
- compressed initial web assets below 250 KB.

These are regression budgets for the demo, not a production capacity forecast. Load, spike and soak scripts use synthetic unique identities.

## Security

Focus areas: injection, XSS, data exposure, duplicate abuse, rate limiting, error leakage, dependency risk, secrets, container configuration and optional-model prompt injection. Dynamic scanners are tuned to avoid claiming exploitability from unverified alerts.

## Reliability/recoverability

Idempotency, transaction atomicity and stable cancellation make retries safe. Recovery testing checks that a failed operation leaves no partial registration and that a restored service can continue with the same data.

## Compatibility

Primary: latest stable Chromium, Firefox and WebKit-compatible Safari behavior; Android/iPhone viewport profiles; keyboard and touch input. Secondary manual spot checks cover Edge and high-contrast Windows behavior.

## SEO

The public page includes title, description, canonical, robots, sitemap, Open Graph and JSON-LD. A real deployment must replace `example.invalid` and verify indexing rules per environment.

## Privacy

Only name, email, age, consent and event relationship are collected. The demo does not implement production retention/deletion workflows; corresponding test ideas remain documented as a known gap.

## Maintainability

Quality includes test readability, isolated fixtures, clear failure messages, source maps, typed contracts, deterministic seed data, repository validation and a small number of deliberate dependencies.
