# BUG-025: Reused idempotency key can replay a different payload

**Severity:** High  
**Priority:** P0  
**Status:** Fixed and confirmed

## Steps

1. Create a registration with an idempotency key.
2. Reuse that key with a different email or event.
3. Inspect the response and stored row count.

## Expected

An exact retry returns the original response. A different request using the same key is rejected as a conflict.

## Actual

Any request carrying an existing key received the first registration, even when the business payload differed.

## Root cause and fix

The replay lookup compared only the key. The store now normalizes the relevant fields and verifies the payload before returning an existing result.

## Regression

`test_idempotency_key_cannot_replay_a_different_request` verifies HTTP 409 and confirms that no second row is created.
