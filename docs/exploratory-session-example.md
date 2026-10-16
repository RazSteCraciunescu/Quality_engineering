# Exploratory session example

**Charter:** Capacity and fairness  
**Time box:** 45 minutes  
**Build:** local main branch candidate  
**Environment:** Chromium desktop, FastAPI + SQLite

## Coverage

Filled the four-place food-drive event, added two waiting users, cancelled a confirmed user, repeated cancellation, retried registration with the same key, and submitted two users within the same clock second.

## Findings

1. **BUG-017:** users created within one second could be promoted by random registration ID rather than arrival order. Root cause was second-level timestamp precision. Fixed by storing microseconds and retaining ID only as a deterministic secondary sort.
2. **BUG-021:** rate-limited responses returned the correct body and status but lost the `Retry-After` header because a new response object replaced the decorated response. Fixed and covered at API level.
3. The confirmation reference was clear, but a future real product should also provide a secure retrieval/cancellation link. That feature remains intentionally out of scope.

## New automation

- FIFO promotion assertion with two wait-listed registrations.
- Rate-limit response-header assertion.
- Repeated cancellation assertion.

## Residual questions

A production database would require explicit concurrency tests under the chosen isolation model. SQLite's immediate transaction is suitable for the local reference implementation but is not evidence for PostgreSQL behavior.
