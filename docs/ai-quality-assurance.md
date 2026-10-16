# AI-assisted quality engineering and AI testing

## Use case

The quality endpoint converts a requirement into **suggested** risk-based scenarios. It supports analysis; it does not approve releases, create evidence or replace product/test judgment.

## Providers

### Deterministic rules (default)

Works offline, is fully testable and produces stable examples for capacity, state, privacy, security, resilience and accessibility cues.

### Local Ollama (optional)

Enabled with `CIVICSHIFT_AI_PROVIDER=ollama`. The model URL defaults to loopback. Requirement text is placed inside explicit data tags, JSON output is requested, temperature is low and failures fall back to rules. Example: `CIVICSHIFT_AI_PROVIDER=ollama OLLAMA_MODEL=llama3.2:3b python -m uvicorn services.api.civicshift.main:app`.

## Quality dimensions

| Dimension | Check |
|---|---|
| Relevance | Scenario addresses a stated requirement or identified product risk |
| Groundedness | No invented feature, account, payment or workflow is treated as fact |
| Coverage | Happy, negative, boundary and relevant non-functional risks are represented |
| Non-duplication | Scenarios add a distinct condition or oracle |
| Actionability | Steps and expected result are specific enough for review/execution |
| Safety | Requirement instructions cannot redirect the system or reveal secrets |
| Schema | IDs, priorities, techniques, steps, expected and tags are present |
| Determinism | Baseline provider is repeatable; model settings are recorded |
| Provenance | Provider and human-review note are returned |
| Fallback | Unavailable/invalid model cannot break the core workflow |

## Evaluation set

`tests/fixtures/ai_eval_cases.json` includes straightforward rules, ambiguity, prompt-injection-like text, missing context, contradictory criteria and high-risk state transitions. Automated checks validate structural invariants and expected risk labels. Human scoring remains necessary for relevance and invented assumptions.

## Prompt-injection model

A requirement may contain text such as “ignore previous instructions.” The service treats the entire requirement as untrusted product data. It must not disclose environment variables, filesystem data, system prompts or hidden instructions. No tool with write access is available to the provider.

## Human review checklist

1. Is every suggested scenario supported by the test basis or explicitly labelled as a question?
2. Is the expected result a true oracle rather than vague wording?
3. Are high product risks represented before low-value edge cases?
4. Does the scenario duplicate existing coverage at a more expensive level?
5. Could the content expose personal data or unsafe payloads?
6. What important scenario did the assistant miss?

## Beyond the narrow demo

A production AI feature would also need model and prompt lineage, protected evaluation data, task-specific thresholds, latency/cost budgets, drift monitoring, red-team cases, privacy review, rollback and monitoring of fallback frequency. Accuracy alone is rarely sufficient; precision/recall, calibration or human-scored rubrics may be more meaningful for the use case.

## Responsible claim

Passing these evals shows controlled behavior for this narrow local use case. It does not establish general LLM safety, fairness or correctness. Do not send confidential requirements, personal data, credentials or proprietary code to an unapproved provider.
