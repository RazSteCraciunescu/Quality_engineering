from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml


def test_json_assets_parse() -> None:
    roots = [Path("automation/postman"), Path("contracts"), Path("integrations")]
    files = [path for root in roots for path in root.rglob("*.json")]
    assert files
    for path in files:
        json.loads(path.read_text(encoding="utf-8"))


def test_xml_assets_parse() -> None:
    files = list(Path("automation").rglob("*.xml")) + list(Path("automation").rglob("*.jmx"))
    assert files
    for path in files:
        ET.parse(path)


def test_yaml_assets_parse() -> None:
    roots = [
        Path(".github/workflows"),
        Path("automation/security/zap"),
        Path("infrastructure/kubernetes"),
    ]
    files = [path for root in roots for path in root.rglob("*.y*ml")]
    files.extend([Path("compose.yaml"), Path("azure-pipelines.yml")])
    files.extend(Path("infrastructure/helm/civicshift").glob("*.yaml"))
    assert files
    for path in files:
        list(yaml.safe_load_all(path.read_text(encoding="utf-8")))


def test_core_portfolio_documents_exist() -> None:
    required = [
        "README.md",
        "docs/test-strategy.md",
        "docs/traceability-matrix.md",
        "docs/risk-register.md",
        "docs/test-design/decision-table.md",
        "docs/process-improvement/dmaic-flaky-tests.md",
        "docs/rpa-release-evidence.md",
        "docs/ai-quality-assurance.md",
        "SECURITY.md",
    ]
    missing = [item for item in required if not Path(item).is_file()]
    assert not missing, missing
