from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    environment: str
    database_path: Path
    allowed_origins: tuple[str, ...]
    rate_limit_per_minute: int
    ai_provider: str
    ollama_base_url: str
    ollama_model: str

    @classmethod
    def from_env(cls, database_path: str | Path | None = None) -> "Settings":
        db_path = Path(database_path or os.getenv("CIVICSHIFT_DB", "var/civicshift.db"))
        origins = tuple(
            origin.strip()
            for origin in os.getenv(
                "CIVICSHIFT_ALLOWED_ORIGINS",
                "http://127.0.0.1:5173,http://localhost:5173",
            ).split(",")
            if origin.strip()
        )
        return cls(
            environment=os.getenv("CIVICSHIFT_ENV", "development"),
            database_path=db_path,
            allowed_origins=origins,
            rate_limit_per_minute=max(
                1, int(os.getenv("CIVICSHIFT_RATE_LIMIT_PER_MINUTE", "30"))
            ),
            ai_provider=os.getenv("CIVICSHIFT_AI_PROVIDER", "rules").lower(),
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/"),
            ollama_model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
        )
