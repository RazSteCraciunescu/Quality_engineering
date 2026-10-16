from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4


class ClosingConnection(sqlite3.Connection):
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            return super().__exit__(exc_type, exc_value, traceback)
        finally:
            self.close()


class ConflictError(Exception):
    pass


class NotFoundError(Exception):
    pass


class BusinessRuleError(Exception):
    pass


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds")


class Store:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.database_path,
            timeout=10,
            isolation_level=None,
            factory=ClosingConnection,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 5000")
        return connection

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        connection = self.connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _initialize(self) -> None:
        schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
        with self.connect() as connection:
            connection.executescript(schema)
            existing = connection.execute("SELECT COUNT(*) FROM events").fetchone()[0]
            if existing == 0:
                self._seed(connection)

    def _seed(self, connection: sqlite3.Connection) -> None:
        # Fixed fixture dates keep visual regression and API examples reproducible.
        created_at = "2026-08-15T09:00:00+00:00"
        rows = [
            (
                "evt-park-cleanup",
                "riverside-park-cleanup",
                "Riverside park cleanup",
                "A two-hour cleanup and sorting session for the riverside walking path.",
                "Riverside Community Gate",
                "2027-04-18T08:30:00+00:00",
                12,
                16,
                "published",
                created_at,
            ),
            (
                "evt-food-drive",
                "neighbourhood-food-drive",
                "Neighbourhood food-drive sorting",
                "Sort donated pantry items and prepare labelled household boxes.",
                "North Hall, Community Centre",
                "2027-05-02T10:00:00+00:00",
                4,
                18,
                "published",
                created_at,
            ),
            (
                "evt-digital-help",
                "digital-help-desk",
                "Digital help desk",
                "Help residents with basic device setup, accounts and online public services.",
                "Library learning room",
                "2027-05-16T13:00:00+00:00",
                8,
                18,
                "published",
                created_at,
            ),
        ]
        connection.executemany(
            """
            INSERT INTO events (
                id, slug, title, summary, location, starts_at, capacity,
                minimum_age, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

    @staticmethod
    def _row_dict(row: sqlite3.Row) -> dict[str, Any]:
        return {key: row[key] for key in row.keys()}

    def list_events(self) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT e.*,
                    SUM(CASE WHEN r.status = 'confirmed' THEN 1 ELSE 0 END) AS confirmed_count,
                    SUM(CASE WHEN r.status = 'waitlisted' THEN 1 ELSE 0 END) AS waitlist_count
                FROM events e
                LEFT JOIN registrations r ON r.event_id = e.id
                WHERE e.status = 'published'
                GROUP BY e.id
                ORDER BY e.starts_at
                """
            ).fetchall()
        events = []
        for row in rows:
            item = self._row_dict(row)
            item["confirmed_count"] = int(item["confirmed_count"] or 0)
            item["waitlist_count"] = int(item["waitlist_count"] or 0)
            item["remaining_seats"] = max(0, item["capacity"] - item["confirmed_count"])
            events.append(item)
        return events

    def get_event(self, event_id: str) -> dict[str, Any]:
        for event in self.list_events():
            if event["id"] == event_id:
                return event
        raise NotFoundError("Event not found")

    def create_registration(
        self,
        *,
        event_id: str,
        attendee_name: str,
        attendee_email: str,
        attendee_age: int,
        consent: bool,
        idempotency_key: str | None,
    ) -> tuple[dict[str, Any], bool]:
        now = utc_now()
        normalized_name = " ".join(attendee_name.split())
        normalized_email = attendee_email.strip().lower()
        with self.transaction() as connection:
            if idempotency_key:
                existing = connection.execute(
                    "SELECT * FROM registrations WHERE idempotency_key = ?",
                    (idempotency_key,),
                ).fetchone()
                if existing:
                    same_request = (
                        existing["event_id"] == event_id
                        and existing["attendee_name"] == normalized_name
                        and existing["attendee_email"] == normalized_email
                        and existing["attendee_age"] == attendee_age
                        and existing["consent"] == int(consent)
                    )
                    if not same_request:
                        raise ConflictError(
                            "Idempotency key was already used for a different request"
                        )
                    return self._row_dict(existing), True

            event = connection.execute(
                "SELECT * FROM events WHERE id = ?", (event_id,)
            ).fetchone()
            if not event or event["status"] != "published":
                raise NotFoundError("Published event not found")
            if attendee_age < event["minimum_age"]:
                raise BusinessRuleError(
                    f"Attendee must be at least {event['minimum_age']} years old"
                )
            if not consent:
                raise BusinessRuleError("Consent is required")

            active = connection.execute(
                """
                SELECT 1 FROM registrations
                WHERE event_id = ? AND lower(attendee_email) = lower(?)
                  AND status IN ('confirmed', 'waitlisted')
                """,
                (event_id, attendee_email),
            ).fetchone()
            if active:
                raise ConflictError("An active registration already exists for this email")

            confirmed_count = connection.execute(
                """
                SELECT COUNT(*) FROM registrations
                WHERE event_id = ? AND status = 'confirmed'
                """,
                (event_id,),
            ).fetchone()[0]
            status = "confirmed" if confirmed_count < event["capacity"] else "waitlisted"
            registration_id = f"reg-{uuid4().hex[:12]}"
            connection.execute(
                """
                INSERT INTO registrations (
                    id, event_id, attendee_name, attendee_email, attendee_age,
                    consent, status, idempotency_key, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    registration_id,
                    event_id,
                    normalized_name,
                    normalized_email,
                    attendee_age,
                    int(consent),
                    status,
                    idempotency_key,
                    now,
                    now,
                ),
            )
            created = connection.execute(
                "SELECT * FROM registrations WHERE id = ?", (registration_id,)
            ).fetchone()
        return self._row_dict(created), False

    def get_registration(self, registration_id: str) -> dict[str, Any]:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM registrations WHERE id = ?", (registration_id,)
            ).fetchone()
        if not row:
            raise NotFoundError("Registration not found")
        return self._row_dict(row)

    def cancel_registration(self, registration_id: str) -> dict[str, Any]:
        now = utc_now()
        with self.transaction() as connection:
            row = connection.execute(
                "SELECT * FROM registrations WHERE id = ?", (registration_id,)
            ).fetchone()
            if not row:
                raise NotFoundError("Registration not found")
            if row["status"] == "cancelled":
                return self._row_dict(row)

            previous_status = row["status"]
            connection.execute(
                "UPDATE registrations SET status = 'cancelled', updated_at = ? WHERE id = ?",
                (now, registration_id),
            )
            promoted_id = None
            if previous_status == "confirmed":
                waitlisted = connection.execute(
                    """
                    SELECT id FROM registrations
                    WHERE event_id = ? AND status = 'waitlisted'
                    ORDER BY created_at, id
                    LIMIT 1
                    """,
                    (row["event_id"],),
                ).fetchone()
                if waitlisted:
                    promoted_id = waitlisted["id"]
                    connection.execute(
                        "UPDATE registrations SET status = 'confirmed', "
                        "updated_at = ? WHERE id = ?",
                        (now, promoted_id),
                    )

            cancelled = connection.execute(
                "SELECT * FROM registrations WHERE id = ?", (registration_id,)
            ).fetchone()
        result = self._row_dict(cancelled)
        result["promoted_registration_id"] = promoted_id
        return result

    def quality_snapshot(self) -> dict[str, Any]:
        with self.connect() as connection:
            event_count = connection.execute("SELECT COUNT(*) FROM events").fetchone()[0]
            registration_count = connection.execute(
                "SELECT COUNT(*) FROM registrations"
            ).fetchone()[0]
            duplicate_count = connection.execute(
                """
                SELECT COUNT(*) FROM (
                    SELECT event_id, lower(attendee_email), COUNT(*) AS total
                    FROM registrations
                    WHERE status IN ('confirmed', 'waitlisted')
                    GROUP BY event_id, lower(attendee_email)
                    HAVING total > 1
                )
                """
            ).fetchone()[0]
            overbooked_count = connection.execute(
                """
                SELECT COUNT(*) FROM (
                    SELECT e.id, e.capacity,
                        SUM(CASE WHEN r.status = 'confirmed' THEN 1 ELSE 0 END) AS confirmed
                    FROM events e LEFT JOIN registrations r ON r.event_id = e.id
                    GROUP BY e.id
                    HAVING confirmed > e.capacity
                )
                """
            ).fetchone()[0]
        return {
            "events": event_count,
            "registrations": registration_count,
            "active_duplicates": duplicate_count,
            "overbooked_events": overbooked_count,
        }
