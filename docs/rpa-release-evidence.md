# RPA: release-evidence consolidation

The script `automation/rpa/release_evidence_bot.py` automates a repetitive coordination task: reading independent reports, normalizing their key measures and writing one release-gate result.

## Inputs

- JUnit XML for automated tests;
- Lighthouse JSON for performance/accessibility/SEO scores;
- ZAP-style JSON for security alerts;
- data-quality JSON for duplicate/overbooking violations;
- optional metadata about build and commit.

## Decision rules

`BLOCK` when tests fail, critical/high security alerts exist, critical data violations are non-zero, or required evidence is unreadable. `CONDITIONAL` when tests pass but a warning budget is missed. `PASS` when all required thresholds are met.

## RPA design principles

- Deterministic rules are versioned and reviewable.
- Missing evidence is a failure, not silently treated as zero.
- The bot cannot modify source data or production systems.
- Every output records source file hashes and rule version.
- A human release owner remains accountable for an override.

This is RPA in a useful portfolio context: repetitive evidence handling is automated while the risk decision stays transparent.
