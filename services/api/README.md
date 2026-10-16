# CivicShift API

FastAPI service with a small SQLite data layer and deliberately testable business rules:
capacity, wait-listing, eligibility, cancellation promotion, duplicate prevention and idempotent retries.

From the repository root:

```bash
python -m uvicorn services.api.civicshift.main:app --reload --port 8000
```
