from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("attendee_name", " "),
        ("attendee_email", "not-an-email"),
        ("attendee_age", -1),
        ("attendee_age", 121),
        ("event_id", "x"),
    ],
)
def test_invalid_partitions_are_rejected(
    client: TestClient,
    registration_payload: dict[str, object],
    field: str,
    value: object,
) -> None:
    request = {**registration_payload, field: value}
    response = client.post("/api/registrations", json=request)
    assert response.status_code == 422
    assert response.json()["title"] == "Validation failed"


def test_unknown_fields_do_not_affect_persisted_shape(
    client: TestClient, registration_payload: dict[str, object]
) -> None:
    response = client.post(
        "/api/registrations", json={**registration_payload, "is_admin": True}
    )
    assert response.status_code == 201
    assert "is_admin" not in response.json()
