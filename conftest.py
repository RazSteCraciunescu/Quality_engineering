from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from services.api.civicshift.main import create_app


@pytest.fixture
def app(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("CIVICSHIFT_RATE_LIMIT_PER_MINUTE", "200")
    monkeypatch.setenv("CIVICSHIFT_AI_PROVIDER", "rules")
    return create_app(tmp_path / "test.db")


@pytest.fixture
def client(app) -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def registration_payload() -> dict[str, object]:
    return {
        "event_id": "evt-park-cleanup",
        "attendee_name": "Alex Sample",
        "attendee_email": "alex@example.test",
        "attendee_age": 28,
        "consent": True,
    }
