from __future__ import annotations

import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []

REQUIRED = [
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "apps/web/dist/index.html",
    "apps/web/dist/assets/main.js",
    "services/api/civicshift/main.py",
    "contracts/openapi.json",
    "docs/test-strategy.md",
    "docs/risk-register.md",
    "docs/traceability-matrix.md",
    ".github/workflows/ci.yml",
    "Dockerfile",
]

for relative in REQUIRED:
    if not (ROOT / relative).is_file():
        ERRORS.append(f"missing required file: {relative}")

for path in ROOT.rglob("*.json"):
    if any(part in {"node_modules", ".venv"} for part in path.parts):
        continue
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        ERRORS.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")

for suffix in ("*.xml", "*.jmx"):
    for path in ROOT.rglob(suffix):
        try:
            ET.parse(path)
        except Exception as exc:
            ERRORS.append(f"invalid XML {path.relative_to(ROOT)}: {exc}")

private_patterns = [
    re.compile(r"https?://[^\s\"')]*(?:\.local|\.corp|\.internal)(?:[/:]|$)", re.I),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?:api[_-]?key|password|secret)\s*[=:]\s*[\"'][A-Za-z0-9/+_-]{16,}", re.I),
    re.compile(r"[A-Z]:\\Users\\", re.I),
]
text_suffixes = {
    ".md", ".py", ".ts", ".tsx", ".js", ".cjs", ".json", ".yaml", ".yml",
    ".toml", ".txt", ".sql", ".feature", ".csv", ".xml", ".jmx", ".tf", ".html", ".css"
}
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in text_suffixes:
        continue
    if any(part in {"node_modules", ".venv", ".git"} for part in path.parts):
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    scan_text = text.replace("host.docker.internal", "allowed-docker-host")
    for pattern in private_patterns:
        if pattern.search(scan_text):
            ERRORS.append(
                f"sensitive/private pattern in {path.relative_to(ROOT)}: "
                f"{pattern.pattern}"
            )
    unfinished_marker = "TODO:" + " replace this"
    if unfinished_marker in text:
        ERRORS.append(f"unfinished placeholder in {path.relative_to(ROOT)}")

for forbidden in ("node_modules", ".venv", ".git", "__pycache__", ".pytest_cache"):
    if any(path.is_dir() and path.name == forbidden for path in ROOT.rglob(forbidden)):
        ERRORS.append(f"forbidden generated directory present: {forbidden}")

js_file = ROOT / "apps/web/dist/assets/main.js"
if js_file.exists() and shutil.which("node"):
    result = subprocess.run(["node", "--check", str(js_file)], capture_output=True, text=True)
    if result.returncode:
        ERRORS.append(f"static JavaScript syntax failed: {result.stderr.strip()}")


def report() -> int:
    if ERRORS:
        print("Repository validation failed:")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    file_count = sum(1 for path in ROOT.rglob("*") if path.is_file())
    print(f"Repository validation passed ({file_count} files checked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(report())
