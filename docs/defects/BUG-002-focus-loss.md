# BUG-002 — Booking dialog originally opened without moving focus

**Status:** Resolved in baseline  
**Severity:** Medium  
**Priority:** P1

## Observed

Keyboard focus remained on the event-card button while the dialog appeared later in the DOM.

## Expected

Focus moves into the dialog, remains visibly navigable, and returns to a logical control when the dialog closes.

## Risk

Keyboard and screen-reader users may not discover the form. Automated role checks alone may miss the confusion.

## Resolution/evidence

The first input receives focus on open. The keyboard charter and Playwright accessibility path verify the critical interaction. A production component would also implement full focus containment and focus return; that limitation is retained as a review item rather than hidden.
