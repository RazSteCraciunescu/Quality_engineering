from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ".pytest_cache",
    ".coverage",
    "coverage.xml",
    "htmlcov",
    "playwright-report",
    "test-results",
    "reports/generated",
]

for target in TARGETS:
    path = ROOT / target
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()

for path in (ROOT / "var").glob("*.db*"):
    if path.is_file():
        path.unlink()

for path in sorted(ROOT.rglob("__pycache__"), reverse=True):
    if path.is_dir():
        shutil.rmtree(path)

for pattern in ("*.pyc", "*.pyo"):
    for path in ROOT.rglob(pattern):
        if path.is_file():
            path.unlink()

(ROOT / "reports/generated").mkdir(parents=True, exist_ok=True)
(ROOT / "reports/generated/.gitkeep").touch()
print("Generated files removed.")
