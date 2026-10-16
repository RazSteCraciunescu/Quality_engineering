from __future__ import annotations

import json
from pathlib import Path

from automation.rpa.release_evidence_bot import evaluate, markdown


def write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def test_release_gate_passes_clean_evidence(tmp_path: Path) -> None:
    junit = write(
        tmp_path / "junit.xml",
        '<testsuite tests="42" failures="0" skipped="1"></testsuite>',
    )
    lighthouse = tmp_path / "lighthouse.json"
    lighthouse.write_text(
        json.dumps({"categories": {"accessibility": {"score": 0.99}, "seo": {"score": 1}}}),
        encoding="utf-8",
    )
    zap = tmp_path / "zap.json"
    zap.write_text(json.dumps({"site": [{"alerts": []}]}), encoding="utf-8")

    result = evaluate(junit=junit, lighthouse=lighthouse, zap=zap)
    assert result.decision == "PASS"
    assert result.total_tests == 42
    assert "No blocking evidence" in markdown(result)


def test_release_gate_blocks_failures_and_security_alerts(tmp_path: Path) -> None:
    junit = write(
        tmp_path / "junit.xml",
        '<testsuites><testsuite tests="10" failures="2" skipped="0"/></testsuites>',
    )
    lighthouse = tmp_path / "lighthouse.json"
    lighthouse.write_text(
        json.dumps({"accessibility": 0.9, "seo": 0.92}), encoding="utf-8"
    )
    zap = tmp_path / "zap.json"
    zap.write_text(
        json.dumps({"site": [{"alerts": [{"riskcode": "3"}]}]}), encoding="utf-8"
    )

    result = evaluate(junit=junit, lighthouse=lighthouse, zap=zap)
    assert result.decision == "BLOCK"
    assert result.failed_tests == 2
    assert result.high_security_alerts == 1
    assert len(result.reasons) == 4
