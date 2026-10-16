from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from services.api.civicshift.database import Store


@pytest.mark.data
def test_seed_data_has_valid_capacity_and_iso_dates(tmp_path: Path) -> None:
    store = Store(tmp_path / "quality.db")
    events = store.list_events()
    assert len(events) == 3
    assert all(event["capacity"] > 0 for event in events)
    assert all("T" in event["starts_at"] for event in events)
    assert store.quality_snapshot()["active_duplicates"] == 0
    assert store.quality_snapshot()["overbooked_events"] == 0


@pytest.mark.data
def test_database_check_constraint_rejects_zero_capacity(tmp_path: Path) -> None:
    store = Store(tmp_path / "constraints.db")
    with store.connect() as connection, pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            """
            INSERT INTO events (
              id, slug, title, summary, location, starts_at,
              capacity, minimum_age, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "evt-invalid",
                "invalid",
                "Invalid event",
                "This row intentionally violates the capacity constraint.",
                "Test location",
                "2026-12-01T10:00:00+00:00",
                0,
                18,
                "published",
                "2026-08-31T00:00:00+00:00",
            ),
        )


@pytest.mark.data
def test_partial_unique_index_allows_cancelled_history_but_not_two_active_rows(
    tmp_path: Path,
) -> None:
    store = Store(tmp_path / "duplicates.db")
    first, _ = store.create_registration(
        event_id="evt-park-cleanup",
        attendee_name="Data Tester",
        attendee_email="data@example.test",
        attendee_age=30,
        consent=True,
        idempotency_key=None,
    )
    store.cancel_registration(first["id"])
    second, _ = store.create_registration(
        event_id="evt-park-cleanup",
        attendee_name="Data Tester",
        attendee_email="DATA@example.test",
        attendee_age=30,
        consent=True,
        idempotency_key=None,
    )
    assert first["id"] != second["id"]
    assert store.quality_snapshot()["active_duplicates"] == 0
