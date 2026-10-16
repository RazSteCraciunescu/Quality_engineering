# Equivalence partitions and boundary values

## Registration input

| Field | Invalid partitions | Valid partition | Key boundaries |
|---|---|---|---|
| Name | absent, blank after normalization, 1 char, over 80 | 2–80 visible chars | 1, 2, 80, 81 |
| Email | absent, missing `@`, missing domain dot, whitespace, over 254 | syntactically acceptable and ≤254 | 4/5 length and 254/255 |
| Age | absent, non-number, below 0, above 120 | integer 0–120 | -1, 0, 120, 121 |
| Event | absent, unknown, draft, cancelled | known and published | state partitions |
| Consent | absent or false | true | boolean decision |
| Idempotency key | absent, 1–7, over 80 | absent or 8–80 | 7, 8, 80, 81 |

## Event eligibility

For minimum age 18, the most useful values are 17, 18 and 19. Testing 1 through 120 individually adds volume without equivalent risk coverage.

## Capacity

With capacity `C`, observe confirmed counts at `C−1`, `C` and `C+1 attempted submission`. The database invariant is `confirmed_count ≤ C`; the extra valid submission changes to wait-listed rather than failing.
