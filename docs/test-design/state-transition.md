# Registration state transitions

```mermaid
stateDiagram-v2
  [*] --> confirmed: valid and capacity available
  [*] --> waitlisted: valid and event full
  confirmed --> cancelled: volunteer cancels
  waitlisted --> cancelled: volunteer cancels
  waitlisted --> confirmed: older confirmed registration cancels
  cancelled --> cancelled: repeated cancellation (no-op)
```

Invalid transitions include direct client selection of status, promotion without a released place, return from cancelled to active using the same record, and promotion that skips an older waiting record.

Tests cover every valid transition and representative invalid paths. A future coordinator override would need authorization, audit and additional transitions rather than directly editing the column.
