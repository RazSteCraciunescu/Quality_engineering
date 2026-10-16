from __future__ import annotations

import json
from pathlib import Path

from automation.rpa.release_evidence_bot import build_evidence


def copy_samples(tmp_path: Path) -> Path:
    source = Path(__file__).resolve().parents[2] / "reports" / "samples"
    for name in ("junit.xml", "lighthouse.json", "zap.json", "data-quality.json"):
        (tmp_path / name).write_bytes((source / name).read_bytes())
    return tmp_path


def test_green_evidence_passes(tmp_path: Path) -> None:
    result = build_evidence(copy_samples(tmp_path))
    assert result["decision"] == "PASS"
    assert result["metrics"]["tests"]["tests"] == 74
    assert len(result["sources"]["junit"]["sha256"]) == 64


def test_test_failure_blocks_release(tmp_path: Path) -> None:
    directory = copy_samples(tmp_path)
    junit = (directory / "junit.xml").read_text(encoding="utf-8")
    (directory / "junit.xml").write_text(
        junit.replace('failures="0"', 'failures="1"', 1), encoding="utf-8"
    )
    result = build_evidence(directory)
    assert result["decision"] == "BLOCK"
    assert any(finding["source"] == "junit" for finding in result["findings"])


def test_performance_budget_miss_is_conditional(tmp_path: Path) -> None:
    directory = copy_samples(tmp_path)
    report = json.loads((directory / "lighthouse.json").read_text(encoding="utf-8"))
    report["categories"]["performance"]["score"] = 0.82
    (directory / "lighthouse.json").write_text(json.dumps(report), encoding="utf-8")
    result = build_evidence(directory)
    assert result["decision"] == "CONDITIONAL"


def test_missing_evidence_blocks_release(tmp_path: Path) -> None:
    result = build_evidence(tmp_path)
    assert result["decision"] == "BLOCK"
    assert len(result["findings"]) == 4
