import assert from 'node:assert/strict';
import test from 'node:test';

import { availabilityLabel, escapeHtml, formatEventDate } from '../../apps/web/dist/assets/format.js';

test('availability labels cover open, final-seat and wait-list states', () => {
  assert.equal(availabilityLabel(3, 0), '3 places available');
  assert.equal(availabilityLabel(1, 0), '1 place available');
  assert.equal(availabilityLabel(0, 0), 'Wait-list available');
  assert.equal(availabilityLabel(0, 2), 'Full · 2 waiting');
});

test('event date rendering is deterministic and invalid-safe', () => {
  assert.match(formatEventDate('2026-10-15T09:30:00+00:00'), /15 Oct 2026/);
  assert.equal(formatEventDate('not-a-date'), 'Date unavailable');
});

test('untrusted event text is escaped before template insertion', () => {
  assert.equal(escapeHtml('<img src=x onerror=alert(1)>'), '&lt;img src=x onerror=alert(1)&gt;');
});
