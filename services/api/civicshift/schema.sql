PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL CHECK(length(title) BETWEEN 3 AND 120),
    summary TEXT NOT NULL CHECK(length(summary) BETWEEN 10 AND 500),
    location TEXT NOT NULL,
    starts_at TEXT NOT NULL,
    capacity INTEGER NOT NULL CHECK(capacity BETWEEN 1 AND 500),
    minimum_age INTEGER NOT NULL DEFAULT 16 CHECK(minimum_age BETWEEN 0 AND 100),
    status TEXT NOT NULL CHECK(status IN ('draft', 'published', 'cancelled')),
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS registrations (
    id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL REFERENCES events(id),
    attendee_name TEXT NOT NULL CHECK(length(attendee_name) BETWEEN 2 AND 80),
    attendee_email TEXT NOT NULL,
    attendee_age INTEGER NOT NULL CHECK(attendee_age BETWEEN 0 AND 120),
    consent INTEGER NOT NULL CHECK(consent IN (0, 1)),
    status TEXT NOT NULL CHECK(status IN ('confirmed', 'waitlisted', 'cancelled')),
    idempotency_key TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_registration_idempotency
    ON registrations(idempotency_key)
    WHERE idempotency_key IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_active_event_email
    ON registrations(event_id, lower(attendee_email))
    WHERE status IN ('confirmed', 'waitlisted');

CREATE INDEX IF NOT EXISTS idx_registration_event_status
    ON registrations(event_id, status, created_at);
