# ADR 002: SQLite for the portfolio runtime

**Status:** Accepted

## Context

The booking rules need real constraints and transactions, but the public repository should run on Windows, macOS and Linux without a service subscription or container prerequisite.

## Decision

Use SQLite with foreign keys, check constraints, partial unique indexes and immediate transactions. Document PostgreSQL/distributed-production differences explicitly.

## Consequences

Local setup and isolated tests are simple. Multi-instance concurrency, online migration and managed backup behavior are not proven by this design.
