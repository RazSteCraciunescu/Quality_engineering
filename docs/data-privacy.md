# Privacy and test-data handling

CivicShift uses synthetic data only. Addresses end in `.test`, a reserved non-deliverable namespace.

## Data inventory

| Field | Purpose | Sensitivity | Test handling |
|---|---|---|---|
| Name | Identify volunteer registration | Personal | Synthetic values; not logged |
| Email | Duplicate identity/contact placeholder | Personal | `.test`; not exposed in event lists |
| Age | Eligibility | Personal | Integer boundaries only |
| Consent | Record agreement | Personal decision | Boolean, server enforced |
| Event/status/timestamps | Service operation | Operational | Safe for synthetic analytics |

## Production test ideas

Consent versioning, retention expiry, deletion/export requests, email delivery minimization, access auditing, backup deletion, analytics anonymization and environment separation. They remain outside the demo implementation and are not falsely marked complete.
