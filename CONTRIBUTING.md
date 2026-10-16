# Contributing

1. Create a focused branch.
2. Add or update tests with the behavior change.
3. Run `python -m pytest -m "not browser"`, `npm run test:node` and `python scripts/validate_repository.py`.
4. Update the OpenAPI snapshot, traceability or release evidence when applicable.
5. Keep fixtures fictional and remove secrets, internal URLs and machine-specific paths.

Pull requests should explain the product risk being changed, the test evidence collected and any accepted residual risk.
