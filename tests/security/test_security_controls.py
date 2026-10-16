from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.mark.security
def test_security_headers_cover_success_and_error(client: TestClient) -> None:
    for path in ("/api/health", "/api/events/not-found"):
        response = client.get(path)
        assert response.headers["x-content-type-options"] == "nosniff"
        assert response.headers["x-frame-options"] == "DENY"
        assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"
        assert "object-src 'none'" in response.headers["content-security-policy"]
        assert "camera=()" in response.headers["permissions-policy"]


@pytest.mark.security
def test_untrusted_origin_is_not_reflected(client: TestClient) -> None:
    response = client.options(
        "/api/registrations",
        headers={
            "Origin": "https://attacker.example",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert response.headers.get("access-control-allow-origin") != "https://attacker.example"


@pytest.mark.security
def test_sql_like_event_identifier_is_data_not_query(client: TestClient) -> None:
    response = client.get("/api/events/'%20OR%201=1--")
    assert response.status_code == 404
    assert len(client.get("/api/events").json()) == 3


@pytest.mark.security
def test_validation_response_avoids_stack_trace_and_echoed_payload(
    client: TestClient,
) -> None:
    payload = {
        "event_id": "evt-park-cleanup",
        "attendee_name": "<script>alert(1)</script>",
        "attendee_email": "invalid",
        "attendee_age": 30,
        "consent": True,
    }
    response = client.post("/api/registrations", json=payload)
    assert response.status_code == 422
    body = response.text.lower()
    assert "traceback" not in body
    assert "<script>" not in body
    assert "services/api" not in body


@pytest.mark.security
def test_event_list_does_not_expose_registration_personal_data(
    client: TestClient, registration_payload: dict[str, object]
) -> None:
    assert client.post("/api/registrations", json=registration_payload).status_code == 201
    body = client.get("/api/events").text
    assert str(registration_payload["attendee_email"]) not in body
    assert str(registration_payload["attendee_name"]) not in body
