from __future__ import annotations

import json
from pathlib import Path

import pytest

from services.api.civicshift.quality_assistant import generate_rule_based


CASES = json.loads(
    (Path(__file__).resolve().parents[1] / "fixtures" / "ai_eval_cases.json").read_text(
        encoding="utf-8"
    )
)


@pytest.mark.ai
@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
def test_ai_eval_case_structural_expectations(case: dict[str, object]) -> None:
    result = generate_rule_based(str(case["requirement"]), str(case["risk"]))
    risks = set(result["risks_detected"])
    techniques = {item["technique"] for item in result["scenarios"]}
    assert set(case["expected_risks"]).issubset(risks)
    assert set(case["expected_techniques"]).issubset(techniques)
    assert result["provider"] == "rules"
    assert len(result["scenarios"]) == len({item["id"] for item in result["scenarios"]})
    assert all(item["steps"] and item["expected"] for item in result["scenarios"])
