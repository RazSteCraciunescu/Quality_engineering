from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from fastapi.testclient import TestClient

from services.api.civicshift.database import Store


def payload(email: str, event_id: str = "evt-food-drive", age: int = 30) -> dict[str, object]:
    return {
        "event_id": event_id,
        "attendee_name": "Community Volunteer",
        "attendee_email": email,
        "attendee_age": age,
        "consent": True,
    }


def test_minimum_age_boundary(client: TestClient) -> None:
    below = client.post("/api/registrations", json=payload("young@example.test", age=17))
    at_boundary = client.post("/api/registrations", json=payload("adult@example.test", age=18))

    assert below.status_code == 422
    assert "at least 18" in below.json()["detail"]
    assert at_boundary.status_code == 201


def test_consent_is_a_business_requirement(client: TestClient) -> None:
    request = payload("privacy@example.test")
    request["consent"] = False
    response = client.post("/api/registrations", json=request)
    assert response.status_code == 422
    assert response.json()["detail"] == "Consent is required"


def test_capacity_boundary_waitlist_and_fifo_promotion(client: TestClient) -> None:
    created = []
    for index in range(6):
        response = client.post(
            "/api/registrations",
            json=payload(f"capacity-{index}@example.test"),
        )
        assert response.status_code == 201
        created.append(response.json())

    assert [item["status"] for item in created[:4]] == ["confirmed"] * 4
    assert [item["status"] for item in created[4:]] == ["waitlisted"] * 2

    cancelled = client.post(f"/api/registrations/{created[0]['id']}/cancel")
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"
    assert cancelled.json()["promoted_registration_id"] == created[4]["id"]

    promoted = client.get(f"/api/registrations/{created[4]['id']}")
    still_waiting = client.get(f"/api/registrations/{created[5]['id']}")
    assert promoted.json()["status"] == "confirmed"
    assert still_waiting.json()["status"] == "waitlisted"


def test_cancelling_twice_is_safe_and_does_not_promote_twice(client: TestClient) -> None:
    registration = client.post(
        "/api/registrations", json=payload("cancel-once@example.test")
    ).json()
    first = client.post(f"/api/registrations/{registration['id']}/cancel")
    second = client.post(f"/api/registrations/{registration['id']}/cancel")
    assert first.status_code == 200
    assert second.status_code == 200
    assert second.json()["status"] == "cancelled"
    assert second.json()["promoted_registration_id"] is None


def test_cancel_unknown_registration(client: TestClient) -> None:
    response = client.post("/api/registrations/reg-does-not-exist/cancel")
    assert response.status_code == 404


def test_cancelled_email_can_register_again(client: TestClient) -> None:
    first = client.post(
        "/api/registrations",
        json=payload("returning@example.test", event_id="evt-park-cleanup"),
    )
    assert first.status_code == 201

    cancelled = client.post(f"/api/registrations/{first.json()['id']}/cancel")
    assert cancelled.status_code == 200

    replacement = client.post(
        "/api/registrations",
        json=payload("RETURNING@EXAMPLE.TEST", event_id="evt-park-cleanup"),
    )
    assert replacement.status_code == 201
    assert replacement.json()["id"] != first.json()["id"]


def test_concurrent_submissions_do_not_overbook(tmp_path: Path) -> None:
    store = Store(tmp_path / "concurrency.db")

    def register(index: int) -> str:
        registration, _ = store.create_registration(
            event_id="evt-food-drive",
            attendee_name=f"Concurrent Volunteer {index}",
            attendee_email=f"concurrent-{index}@example.test",
            attendee_age=30,
            consent=True,
            idempotency_key=None,
        )
        return str(registration["status"])

    with ThreadPoolExecutor(max_workers=8) as executor:
        statuses = list(executor.map(register, range(10)))

    assert statuses.count("confirmed") == 4
    assert statuses.count("waitlisted") == 6
    snapshot = store.quality_snapshot()
    assert snapshot["overbooked_events"] == 0

