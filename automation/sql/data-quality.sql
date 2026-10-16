-- Every query should return zero rows in a releasable environment.

-- Confirmed registrations must never exceed event capacity.
SELECT e.id, e.capacity, COUNT(r.id) AS confirmed_count
FROM events e
JOIN registrations r ON r.event_id = e.id AND r.status = 'confirmed'
GROUP BY e.id, e.capacity
HAVING COUNT(r.id) > e.capacity;

-- One active registration per event and normalized email.
SELECT event_id, lower(attendee_email) AS normalized_email, COUNT(*) AS active_count
FROM registrations
WHERE status IN ('confirmed', 'waitlisted')
GROUP BY event_id, lower(attendee_email)
HAVING COUNT(*) > 1;

-- Wait-listed records only make sense when the event is currently full.
SELECT r.id, r.event_id
FROM registrations r
JOIN events e ON e.id = r.event_id
WHERE r.status = 'waitlisted'
  AND (
    SELECT COUNT(*) FROM registrations confirmed
    WHERE confirmed.event_id = e.id AND confirmed.status = 'confirmed'
  ) < e.capacity;
