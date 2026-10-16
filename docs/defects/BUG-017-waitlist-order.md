# BUG-017: Wait-list promotion can ignore arrival order

**Severity:** High  
**Priority:** P0  
**Status:** Fixed and confirmed

## Environment

Local API, SQLite, six registrations submitted within one second.

## Steps

1. Fill a four-place event.
2. Submit two additional valid registrations quickly.
3. Cancel the first confirmed registration.
4. Retrieve both waiting registrations.

## Expected

The first wait-listed registration becomes confirmed.

## Actual

Either waiting registration could be promoted because both `created_at` values had second-level precision and random IDs acted as the tie-breaker.

## Root cause and fix

Arrival timestamps were truncated to seconds. Store microseconds and order by timestamp, then ID only as a deterministic secondary key.

## Regression

`test_capacity_boundary_waitlist_and_fifo_promotion` creates two waiting users and asserts the first is promoted.
