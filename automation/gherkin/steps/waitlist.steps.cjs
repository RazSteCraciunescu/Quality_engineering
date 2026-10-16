const assert = require('node:assert/strict');
const { Before, Given, When, Then } = require('@cucumber/cucumber');

const baseUrl = process.env.CIVICSHIFT_BASE_URL || 'http://127.0.0.1:8000';

Before(function (scenario) {
  this.eventId = scenario.pickle.name.includes('Cancellation')
    ? 'evt-digital-help'
    : 'evt-food-drive';
  this.created = [];
});

async function register(world, suffix) {
  const response = await fetch(`${baseUrl}/api/registrations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      event_id: world.eventId,
      attendee_name: `BDD Volunteer ${suffix}`,
      attendee_email: `bdd-${Date.now()}-${suffix}@example.test`,
      attendee_age: 30,
      consent: true,
    }),
  });
  assert.equal(response.status, 201);
  const registration = await response.json();
  world.created.push(registration);
  return registration;
}

Given('a published event with one place remaining', async function () {
  const event = await fetch(`${baseUrl}/api/events/${this.eventId}`).then((response) => response.json());
  for (let index = event.confirmed_count; index < event.capacity - 1; index += 1) {
    await register(this, `setup-${index}`);
  }
});

When('two eligible volunteers register', async function () {
  await register(this, 'boundary-a');
  await register(this, 'boundary-b');
});

Then('exactly one new registration is confirmed', function () {
  assert.equal(this.created.slice(-2).filter((item) => item.status === 'confirmed').length, 1);
});

Then('exactly one new registration is wait-listed', function () {
  assert.equal(this.created.slice(-2).filter((item) => item.status === 'waitlisted').length, 1);
});

Then('the number of confirmed volunteers does not exceed capacity', async function () {
  const event = await fetch(`${baseUrl}/api/events/${this.eventId}`).then((response) => response.json());
  assert.ok(event.confirmed_count <= event.capacity);
});

Given('a full event with two wait-listed volunteers', async function () {
  const event = await fetch(`${baseUrl}/api/events/${this.eventId}`).then((response) => response.json());
  for (let index = event.confirmed_count; index < event.capacity + 2; index += 1) {
    await register(this, `queue-${index}`);
  }
  this.confirmed = this.created.find((item) => item.status === 'confirmed');
  this.waiting = this.created.filter((item) => item.status === 'waitlisted');
});

When('a confirmed volunteer cancels', async function () {
  const response = await fetch(`${baseUrl}/api/registrations/${this.confirmed.id}/cancel`, { method: 'POST' });
  assert.equal(response.status, 200);
  this.cancellation = await response.json();
});

Then('the oldest wait-listed volunteer is promoted', async function () {
  const promoted = await fetch(`${baseUrl}/api/registrations/${this.waiting[0].id}`).then((response) => response.json());
  assert.equal(promoted.status, 'confirmed');
  assert.equal(this.cancellation.promoted_registration_id, promoted.id);
});

Then('the second wait-listed volunteer remains waiting', async function () {
  const waiting = await fetch(`${baseUrl}/api/registrations/${this.waiting[1].id}`).then((response) => response.json());
  assert.equal(waiting.status, 'waitlisted');
});
