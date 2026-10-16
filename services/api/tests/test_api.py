from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_describes_ready_service(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "civicshift-api",
        "version": "1.0.0",
        "database": "ready",
    }


def test_events_are_publicly_browsable_and_capacity_is_derived(client: TestClient) -> None:
    response = client.get("/api/events")
    assert response.status_code == 200
    events = response.json()
    assert len(events) == 3
    assert events[0]["remaining_seats"] == events[0]["capacity"]
    assert all(event["status"] == "published" for event in events)


def test_unknown_event_uses_problem_details(client: TestClient) -> None:
    response = client.get("/api/events/evt-missing")
    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["title"] == "Not found"
    assert response.json()["request_id"] == response.headers["x-request-id"]


def test_valid_registration_is_confirmed(
    client: TestClient, registration_payload: dict[str, object]
) -> None:
    response = client.post(
        "/api/registrations",
        json=registration_payload,
        headers={"Idempotency-Key": "booking-0001"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "confirmed"
    assert body["attendee_email"] == "alex@example.test"
    assert body["replayed"] is False

    fetched = client.get(f"/api/registrations/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == body["id"]


def test_idempotent_replay_returns_original_registration(
    client: TestClient, registration_payload: dict[str, object]
) -> None:
    headers = {"Idempotency-Key": "booking-retry-01"}
    first = client.post("/api/registrations", json=registration_payload, headers=headers)
    second = client.post("/api/registrations", json=registration_payload, headers=headers)

    assert first.status_code == 201
    assert second.status_code == 200
    assert second.headers["idempotent-replayed"] == "true"
    assert second.json()["id"] == first.json()["id"]
    assert second.json()["replayed"] is True


def test_idempotency_key_cannot_replay_a_different_request(
    client: TestClient, registration_payload: dict[str, object]
) -> None:
    headers = {"Idempotency-Key": "booking-payload-01"}
    first = client.post("/api/registrations", json=registration_payload, headers=headers)
    changed = {
        **registration_payload,
        "attendee_email": "different@example.test",
    }
    second = client.post("/api/registrations", json=changed, headers=headers)

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["detail"] == (
        "Idempotency key was already used for a different request"
    )
    assert client.get("/api/quality/snapshot").json()["registrations"] == 1


def test_duplicate_active_email_is_rejected_case_insensitively(
    client: TestClient, registration_payload: dict[str, object]
) -> None:
    first = client.post("/api/registrations", json=registration_payload)
    duplicate = {**registration_payload, "attendee_email": "ALEX@EXAMPLE.TEST"}
    second = client.post("/api/registrations", json=duplicate)

    assert first.status_code == 201
    assert second.status_code == 409
    assert "active registration" in second.json()["detail"]


def test_invalid_idempotency_key_is_rejected_before_write(
    client: TestClient, registration_payload: dict[str, object]
) -> None:
    response = client.post(
        "/api/registrations",
        json=registration_payload,
        headers={"Idempotency-Key": "short"},
    )
    assert response.status_code == 400
    assert response.json()["title"] == "Invalid idempotency key"


def test_request_id_is_echoed_and_length_bounded(client: TestClient) -> None:
    supplied = "trace-123"
    response = client.get("/api/health", headers={"X-Request-ID": supplied})
    assert response.headers["x-request-id"] == supplied
    assert float(response.headers["x-response-time-ms"]) >= 0
