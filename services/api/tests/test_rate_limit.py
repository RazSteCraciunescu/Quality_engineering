from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from services.api.civicshift.main import create_app
from services.api.civicshift.rate_limit import SlidingWindowRateLimiter


def test_sliding_window_expires_old_hits() -> None:
    limiter = SlidingWindowRateLimiter(limit=2, window_seconds=10)
    assert limiter.allow("client", now=0)
    assert limiter.allow("client", now=1)
    assert not limiter.allow("client", now=2)
    assert limiter.allow("client", now=11)


def test_registration_rate_limit_returns_retry_after(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("CIVICSHIFT_RATE_LIMIT_PER_MINUTE", "1")
    app = create_app(tmp_path / "rate-limit.db")
    request = {
        "event_id": "evt-park-cleanup",
        "attendee_name": "First Volunteer",
        "attendee_email": "first@example.test",
        "attendee_age": 25,
        "consent": True,
    }
    with TestClient(app) as client:
        first = client.post("/api/registrations", json=request)
        second = client.post(
            "/api/registrations",
            json={**request, "attendee_email": "second@example.test"},
        )
    assert first.status_code == 201
    assert second.status_code == 429
    assert second.headers["retry-after"] == "60"


def test_quality_assistant_has_an_independent_rate_limit(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("CIVICSHIFT_RATE_LIMIT_PER_MINUTE", "1")
    app = create_app(tmp_path / "quality-rate-limit.db")
    payload = {
        "requirement": (
            "When event capacity is reached, additional eligible volunteers should join "
            "a wait-list in submission order."
        ),
        "risk": "high",
    }
    with TestClient(app) as client:
        first = client.post("/api/quality/generate-scenarios", json=payload)
        second = client.post("/api/quality/generate-scenarios", json=payload)
    assert first.status_code == 200
    assert second.status_code == 429
    assert second.headers["retry-after"] == "60"
