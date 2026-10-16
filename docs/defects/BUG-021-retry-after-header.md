# BUG-021: Rate-limit response omits Retry-After

**Severity:** Medium  
**Priority:** P1  
**Status:** Fixed and confirmed

## Steps

1. Configure registration limit to one request per minute.
2. Submit two registrations from the same client.
3. Inspect the second response.

## Expected

HTTP 429 with problem details and `Retry-After: 60`.

## Actual

HTTP 429 and body were correct, but the header was absent.

## Root cause and fix

The route added the header to FastAPI's injected response, then returned a new `JSONResponse`. The header is now attached to the returned object. API regression asserts status, body and header.
