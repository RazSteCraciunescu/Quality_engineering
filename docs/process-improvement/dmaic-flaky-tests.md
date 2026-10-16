# Lean Six Sigma DMAIC: reducing flaky UI automation

This is a portfolio case study using synthetic measurements. It demonstrates the method without pretending the numbers came from an employer.

## Define

**Problem:** A critical browser suite has an 8.7% rerun rate. Engineers distrust failures, CI feedback is delayed and real regressions risk being dismissed.

**Customer/CTQ:** A pull-request result should be reproducible and actionable within 12 minutes. A failed test should represent a product or controlled-environment issue, not random timing.

**Scope:** Critical booking UI tests from test start through result publication. Product defect resolution is outside the process-improvement project.

## Measure

Four weeks, 1,200 synthetic executions:

| Failure category | Count | Share |
|---|---:|---:|
| Shared test data/collision | 39 | 37.1% |
| Arbitrary waits/timing | 28 | 26.7% |
| Unstable selector | 17 | 16.2% |
| Environment startup | 12 | 11.4% |
| Genuine product defect | 9 | 8.6% |

Baseline rerun rate: 8.7%. First-pass yield: 91.3%. Median feedback: 14.8 minutes. P95 feedback: 28.4 minutes.

Measurement-system check: one failure taxonomy, required trace/screenshot/request ID and independent review of 10% of classifications.

## Analyze

The Pareto view shows 63.8% of flaky outcomes came from data collision and timing. Five-why analysis linked data collision to shared static emails and timing to UI sleeps instead of observable state. Retries masked both causes and inflated runtime.

## Improve

- Generate unique test identities and reset state through API/temp DB.
- Replace sleeps with assertions on response or visible state.
- Introduce stable semantic selectors.
- Start the environment once per worker with a readiness probe.
- Disallow automatic retry for product assertions; allow one documented infrastructure retry at pipeline level.
- Quarantine only with owner, defect, reason and expiry date.

Synthetic pilot target: rerun rate below 2%, first-pass yield above 98%, median feedback below 10 minutes, no reduction in escaped-defect detection.

## Control

| Metric | Green | Amber | Red/action |
|---|---:|---:|---|
| Weekly flaky rerun rate | <2% | 2–3% | >3%: root-cause review |
| Quarantined critical tests | 0 | 1 | >1 or expired: block merge |
| Median PR feedback | <10 min | 10–12 min | >12 min: pipeline review |
| Failures with complete evidence | >98% | 95–98% | <95%: fix reporter |

A weekly control chart and monthly Pareto review detect drift. The control plan owns the process, not just the individual test files.
