# Selected manual test cases

Automation covers stable repeatable checks. These cases keep human observation where usability, wording, timing or cross-feature judgment matters.

## MAN-001 — Keyboard-only registration

**Priority:** P1  
**Preconditions:** At least one published event with remaining capacity.

1. Load the page and do not use the mouse.
2. Use the skip link, primary navigation and event cards.
3. Open the registration dialog.
4. Move through all controls with Tab and Shift+Tab.
5. Submit blank fields, then valid data.
6. Dismiss the confirmation.

**Expected:** Focus is visible and logical; the dialog has an accessible name; errors identify the affected input; status is announced; no keyboard trap occurs; background controls are not accidentally activated.

## MAN-002 — Capacity information comprehension

Ask a participant unfamiliar with the product to explain the difference between “places available,” “wait-list available” and “full · N waiting,” then complete a wait-list registration.

**Expected:** They can predict whether the result will be confirmed or wait-listed without tester coaching. Record misunderstandings as usability observations, not as user failure.

## MAN-003 — Network interruption during submit

Throttle or interrupt the request after pressing Confirm. Restore the network and retry with the same idempotency key through an API client.

**Expected:** The UI does not claim success without a response. The retry resolves to one persisted registration. Correlation information supports investigation.

## MAN-004 — Mobile zoom and reflow

At 320 CSS pixels, zoom to 200% and complete event discovery, form entry and quality scenario generation.

**Expected:** No required content or action is clipped; horizontal scrolling is not required for normal text; dialog content remains reachable.

## MAN-005 — Exploratory security rendering

Use harmless representative strings containing `<`, `>`, quotes, Unicode direction characters and line breaks in every accepted text field.

**Expected:** Values are treated as data, not executable markup; layout remains understandable; logs remain parseable; no response contains a stack trace.
