# ADR 001: Keep a checked-in static web build

**Status:** Accepted

## Context

A portfolio reviewer should be able to run the product with one common runtime. Requiring Node installation before seeing the application adds friction unrelated to the quality work.

## Decision

Keep `apps/web/dist/` in version control and serve it from FastAPI. Keep framework-free TypeScript modules and the build script as the maintainable development path. CI rebuilds and tests the generated JavaScript.

## Consequences

- Python alone can run the demonstration after dependencies are installed.
- Source and static build can drift, so repository validation and CI rebuild it.
- The repository is slightly larger, but the generated assets are small and reviewable.
