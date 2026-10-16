from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.mark.contract
def test_required_api_operations_are_described(client: TestClient) -> None:
    schema = client.get("/api/openapi.json").json()
    paths = schema["paths"]
    expected = {
        "/api/health",
        "/api/events",
        "/api/events/{event_id}",
        "/api/registrations",
        "/api/registrations/{registration_id}",
        "/api/registrations/{registration_id}/cancel",
        "/api/quality/generate-scenarios",
        "/api/quality/snapshot",
        "/metrics",
    }
    assert expected.issubset(paths)


@pytest.mark.contract
def test_operation_ids_are_unique(client: TestClient) -> None:
    schema = client.get("/api/openapi.json").json()
    operation_ids = [
        operation["operationId"]
        for path in schema["paths"].values()
        for operation in path.values()
        if isinstance(operation, dict) and "operationId" in operation
    ]
    assert len(operation_ids) == len(set(operation_ids))


@pytest.mark.contract
def test_checked_in_openapi_snapshot_matches_runtime(client: TestClient) -> None:
    runtime = client.get("/api/openapi.json").json()
    snapshot_path = Path(__file__).resolve().parents[2] / "contracts" / "openapi.json"
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    assert runtime == snapshot


@pytest.mark.contract
def test_problem_detail_contract_on_negative_request(client: TestClient) -> None:
    response = client.get("/api/events/unknown")
    assert response.status_code == 404
    body = response.json()
    assert set(body) == {"type", "title", "status", "detail", "request_id"}
    assert body["status"] == response.status_code
