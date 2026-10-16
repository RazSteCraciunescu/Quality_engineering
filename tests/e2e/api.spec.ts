import { expect, test } from '@playwright/test';

test('API prevents business duplicates and echoes a trace identifier', async ({ request }) => {
  const email = `api-${Date.now()}@example.test`;
  const body = {
    event_id: 'evt-park-cleanup',
    attendee_name: 'API Volunteer',
    attendee_email: email,
    attendee_age: 35,
    consent: true,
  };
  const created = await request.post('/api/registrations', {
    data: body,
    headers: { 'Idempotency-Key': `pw-${Date.now()}` },
  });
  expect(created.status()).toBe(201);
  expect(created.headers()['x-request-id']).toBeTruthy();

  const duplicate = await request.post('/api/registrations', { data: body });
  expect(duplicate.status()).toBe(409);
  expect(await duplicate.json()).toMatchObject({ title: 'Conflict', status: 409 });
});
