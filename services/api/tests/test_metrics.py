from __future__ import annotations

from fastapi.testclient import TestClient


def test_metrics_are_prometheus_compatible(client: TestClient) -> None:
    client.get("/api/health")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert "civicshift_http_requests_total" in response.text
    assert "civicshift_data_quality_violations 0" in response.text
