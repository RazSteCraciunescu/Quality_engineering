from __future__ import annotations

import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

RULE_VERSION = "1.0"


@dataclass(frozen=True)
class Finding:
    source: str
    level: str
    message: str


@dataclass(frozen=True)
class GateResult:
    decision: str
    total_tests: int
    failed_tests: int
    skipped_tests: int
    accessibility_score: float
    seo_score: float
    high_security_alerts: int
    reasons: tuple[str, ...]


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_junit(path: Path) -> tuple[dict[str, int], list[Finding]]:
    root = ET.parse(path).getroot()
    totals = {key: 0 for key in ("tests", "failures", "errors", "skipped")}
    if root.tag == "testsuites" and "tests" in root.attrib:
        for key in totals:
            totals[key] = int(float(root.attrib.get(key, "0")))
    else:
        suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
        for suite in suites:
            for key in totals:
                totals[key] += int(float(suite.attrib.get(key, "0")))
    findings: list[Finding] = []
    if totals["failures"] or totals["errors"]:
        findings.append(
            Finding(
                "junit",
                "block",
                f"{totals['failures']} failed and {totals['errors']} errored tests",
            )
        )
    if totals["tests"] == 0:
        findings.append(Finding("junit", "block", "No tests were reported"))
    return totals, findings


def parse_lighthouse(path: Path) -> tuple[dict[str, float], list[Finding]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    categories = raw.get("categories", raw)
    scores = {
        name: float(value["score"] if isinstance(value, dict) else value)
        for name, value in categories.items()
        if name in {"performance", "accessibility", "best-practices", "seo"}
    }
    required = {
        "performance": 0.90,
        "accessibility": 0.95,
        "best-practices": 0.90,
        "seo": 0.95,
    }
    findings = []
    for name, threshold in required.items():
        score = scores.get(name)
        if score is None:
            findings.append(Finding("lighthouse", "block", f"Missing {name} score"))
        elif score < threshold:
            level = "block" if name == "accessibility" and score < 0.90 else "warn"
            findings.append(
                Finding(
                    "lighthouse",
                    level,
                    f"{name} score {score:.2f} is below {threshold:.2f}",
                )
            )
    return scores, findings


def parse_zap(path: Path) -> tuple[dict[str, int], list[Finding]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    alerts = list(raw.get("alerts", []))
    sites = raw.get("site", [])
    if isinstance(sites, dict):
        sites = [sites]
    if isinstance(sites, list):
        for site in sites:
            if isinstance(site, dict):
                alerts.extend(site.get("alerts", []))
    counts = {"high": 0, "medium": 0, "low": 0, "informational": 0}
    findings: list[Finding] = []
    risk_code_map = {"3": "high", "2": "medium", "1": "low", "0": "informational"}
    for alert in alerts:
        if "riskcode" in alert:
            normalized = risk_code_map.get(str(alert.get("riskcode")), "informational")
        else:
            risk = str(alert.get("risk", alert.get("riskdesc", "informational"))).lower()
            normalized = next((key for key in counts if key in risk), "informational")
        counts[normalized] += 1
    if counts["high"]:
        findings.append(Finding("zap", "block", f"{counts['high']} high-risk alert(s)"))
    if counts["medium"]:
        findings.append(Finding("zap", "warn", f"{counts['medium']} medium-risk alert(s)"))
    return counts, findings


def parse_data_quality(path: Path) -> tuple[dict[str, int], list[Finding]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    measures = {
        "active_duplicates": int(raw.get("active_duplicates", -1)),
        "overbooked_events": int(raw.get("overbooked_events", -1)),
    }
    findings = []
    for name, value in measures.items():
        if value < 0:
            findings.append(Finding("data-quality", "block", f"Missing measure: {name}"))
        elif value > 0:
            findings.append(
                Finding("data-quality", "block", f"{name} has {value} violation(s)")
            )
    return measures, findings


def evaluate(*, junit: Path, lighthouse: Path, zap: Path) -> GateResult:
    test_metrics, _ = parse_junit(junit)
    lighthouse_scores, _ = parse_lighthouse(lighthouse)
    security_counts, _ = parse_zap(zap)
    failed = test_metrics["failures"] + test_metrics["errors"]
    accessibility = float(lighthouse_scores.get("accessibility", 0.0))
    seo = float(lighthouse_scores.get("seo", 0.0))
    high_alerts = security_counts["high"]
    reasons: list[str] = []
    if failed:
        reasons.append(f"{failed} automated test(s) failed or errored")
    if high_alerts:
        reasons.append(f"{high_alerts} high-risk security alert(s)")
    if accessibility < 0.95:
        reasons.append(f"Accessibility score {accessibility:.2f} is below 0.95")
    if seo < 0.95:
        reasons.append(f"SEO score {seo:.2f} is below 0.95")
    return GateResult(
        decision="BLOCK" if reasons else "PASS",
        total_tests=test_metrics["tests"],
        failed_tests=failed,
        skipped_tests=test_metrics["skipped"],
        accessibility_score=accessibility,
        seo_score=seo,
        high_security_alerts=high_alerts,
        reasons=tuple(reasons),
    )


def markdown(result: GateResult) -> str:
    reasons = (
        "\n".join(f"- {reason}" for reason in result.reasons)
        if result.reasons
        else "- No blocking evidence was found."
    )
    return (
        "# Release evidence summary\n\n"
        f"**Decision:** {result.decision}\n\n"
        f"- Tests: {result.total_tests} total, {result.failed_tests} failed, "
        f"{result.skipped_tests} skipped\n"
        f"- Accessibility score: {result.accessibility_score:.2f}\n"
        f"- SEO score: {result.seo_score:.2f}\n"
        f"- High security alerts: {result.high_security_alerts}\n\n"
        "## Reasons\n\n"
        f"{reasons}\n"
    )


def build_evidence(input_dir: Path) -> dict[str, Any]:
    required = {
        "junit": input_dir / "junit.xml",
        "lighthouse": input_dir / "lighthouse.json",
        "zap": input_dir / "zap.json",
        "data_quality": input_dir / "data-quality.json",
    }
    missing = [str(path) for path in required.values() if not path.is_file()]
    if missing:
        return {
            "rule_version": RULE_VERSION,
            "decision": "BLOCK",
            "findings": [
                asdict(Finding("evidence", "block", f"Missing required evidence: {path}"))
                for path in missing
            ],
            "sources": {},
            "metrics": {},
        }

    junit, junit_findings = parse_junit(required["junit"])
    lighthouse, lighthouse_findings = parse_lighthouse(required["lighthouse"])
    zap, zap_findings = parse_zap(required["zap"])
    data_quality, data_findings = parse_data_quality(required["data_quality"])
    findings = junit_findings + lighthouse_findings + zap_findings + data_findings
    decision = "BLOCK" if any(item.level == "block" for item in findings) else (
        "CONDITIONAL" if any(item.level == "warn" for item in findings) else "PASS"
    )
    return {
        "rule_version": RULE_VERSION,
        "decision": decision,
        "findings": [asdict(item) for item in findings],
        "metrics": {
            "tests": junit,
            "lighthouse": lighthouse,
            "security_alerts": zap,
            "data_quality": data_quality,
        },
        "sources": {
            name: {"file": path.name, "sha256": file_hash(path)}
            for name, path in required.items()
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Consolidate release evidence into a gate decision")
    parser.add_argument("--input", type=Path, required=True, help="Directory containing required reports")
    parser.add_argument("--output", type=Path, required=True, help="JSON evidence output")
    parser.add_argument("--markdown", type=Path, help="Optional human-readable summary")
    args = parser.parse_args()
    evidence = build_evidence(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    if args.markdown:
        tests = evidence.get("metrics", {}).get("tests", {})
        lighthouse_scores = evidence.get("metrics", {}).get("lighthouse", {})
        security = evidence.get("metrics", {}).get("security_alerts", {})
        summary = GateResult(
            decision=evidence["decision"],
            total_tests=int(tests.get("tests", 0)),
            failed_tests=int(tests.get("failures", 0)) + int(tests.get("errors", 0)),
            skipped_tests=int(tests.get("skipped", 0)),
            accessibility_score=float(lighthouse_scores.get("accessibility", 0.0)),
            seo_score=float(lighthouse_scores.get("seo", 0.0)),
            high_security_alerts=int(security.get("high", 0)),
            reasons=tuple(item["message"] for item in evidence["findings"]),
        )
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(markdown(summary), encoding="utf-8")
    print(f"Release gate: {evidence['decision']}")
    for finding in evidence["findings"]:
        print(f"- {finding['level'].upper()}: {finding['message']}")
    return 1 if evidence["decision"] == "BLOCK" else 0


if __name__ == "__main__":
    raise SystemExit(main())
