from __future__ import annotations

import os
import sys
from pathlib import Path

import uvicorn


def main() -> None:
    repository_root = Path(__file__).resolve().parents[1]
    os.chdir(repository_root)
    sys.path.insert(0, str(repository_root))

    database = repository_root / "var" / "playwright.db"
    database.parent.mkdir(parents=True, exist_ok=True)
    database.unlink(missing_ok=True)
    os.environ["CIVICSHIFT_DB"] = str(database)
    os.environ.setdefault("CIVICSHIFT_ENV", "test")
    os.environ.setdefault("CIVICSHIFT_RATE_LIMIT_PER_MINUTE", "200")
    uvicorn.run(
        "services.api.civicshift.main:app",
        host="127.0.0.1",
        port=8000,
        log_level="warning",
    )


if __name__ == "__main__":
    main()
