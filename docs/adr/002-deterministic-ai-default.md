# ADR 002: Deterministic AI-assistance default

**Status:** Accepted

## Context

A portfolio should work without tokens, subscriptions, model downloads or network access. Generative output also complicates repeatable tests.

## Decision

Use a deterministic risk-and-technique engine by default. Provide an optional Ollama adapter behind the same response model, with timeout and fallback.

## Consequences

- Core demonstrations and evaluations are repeatable.
- The default is not marketed as a general reasoning model.
- Optional model usefulness must be evaluated per model/version.
