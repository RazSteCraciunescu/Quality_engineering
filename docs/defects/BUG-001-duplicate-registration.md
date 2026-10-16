# BUG-001 — Double submission can create two active registrations

**Status:** Resolved in baseline  
**Severity:** High  
**Priority:** P0

## Observed

Two near-identical registration requests with the same event/email could both return success in an early implementation.

## Expected

At most one active registration exists per event and normalized email. A keyed retry returns the original response; an unkeyed business duplicate returns 409.

## Reproduction

1. Prepare an event with capacity.
2. Send two requests concurrently using the same email and different/no idempotency keys.
3. Query stored active records.

## Impact

Capacity and communications become inaccurate; cancellation/promotion order may be corrupted.

## Resolution/evidence

Added a partial unique database index, transaction handling, normalized email and API tests for keyed replay and case-insensitive duplicate conflict.
