import { availabilityLabel, escapeHtml, formatEventDate } from './format.js';
export function shell() {
    return `
    <header class="site-header">
      <a class="brand" href="#top" aria-label="CivicShift home">
        <span class="brand-mark" aria-hidden="true">C</span><span>CivicShift</span>
      </a>
      <nav aria-label="Primary navigation">
        <a href="#events">Events</a><a href="#quality-lab">Quality lab</a><a href="/api/docs">API</a>
      </nav>
    </header>
    <main id="main-content">
      <section class="hero" id="top">
        <div class="hero__copy">
          <span class="eyebrow">Local action, clearly organised</span>
          <h1>Volunteer where your time makes a visible difference.</h1>
          <p>Browse community events, check eligibility and reserve a place. Capacity and wait-list status remain transparent from registration through cancellation.</p>
          <a class="button button--primary" href="#events">Browse upcoming events</a>
        </div>
        <aside class="hero__proof" aria-label="Service qualities">
          <div><strong>Accessible</strong><span>Keyboard-first forms and clear status messages</span></div>
          <div><strong>Reliable</strong><span>Idempotent booking and capacity protection</span></div>
          <div><strong>Transparent</strong><span>Published eligibility and wait-list rules</span></div>
        </aside>
      </section>
      <div id="announcement" aria-live="polite"></div>
      <section class="events-section" id="events" aria-labelledby="events-title">
        <div class="section-heading"><div><span class="eyebrow">Upcoming opportunities</span><h2 id="events-title">Choose a volunteer shift</h2></div><p>All names, locations and registrations in this project are fictional.</p></div>
        <div id="event-list" class="event-grid" aria-busy="true"><p>Loading events…</p></div>
      </section>
      <section class="quality-lab" id="quality-lab" aria-labelledby="quality-lab-title">
        <div class="section-heading"><div><span class="eyebrow">AI-assisted quality engineering</span><h2 id="quality-lab-title">Requirement-to-risk test design</h2></div><p>The default provider is deterministic and local. An optional Ollama adapter is isolated behind the same schema and falls back safely when unavailable.</p></div>
        <div class="quality-grid">
          <form class="quality-form" id="quality-form">
            <label>Requirement or acceptance criterion<textarea id="requirement" name="requirement" minlength="20" maxlength="2000" rows="8" required>When a volunteer event reaches capacity, additional eligible registrations should join a wait-list. Cancelling a confirmed registration should promote the oldest wait-listed registration.</textarea></label>
            <label>Product risk<select id="risk" name="risk"><option value="low">Low</option><option value="medium">Medium</option><option value="high" selected>High</option></select></label>
            <button class="button button--primary" type="submit">Suggest test scenarios</button>
          </form>
          <div class="scenario-panel" id="scenario-panel" aria-live="polite"><div class="empty-state"><div><strong>No generated scenarios yet</strong><p>Submit the example requirement to see risk-based suggestions.</p></div></div></div>
        </div>
      </section>
    </main>
    <footer><p>CivicShift is a fictional system built as a public quality-engineering capstone.</p><a href="/api/health">Service health</a></footer>
    <div id="modal-root"></div>`;
}
export function eventCard(event) {
    const full = event.remaining_seats === 0;
    return `<article class="event-card" aria-labelledby="event-${escapeHtml(event.id)}">
    <div class="event-card__topline"><span class="status-pill ${full ? 'status-pill--wait' : ''}">${escapeHtml(availabilityLabel(event.remaining_seats, event.waitlist_count))}</span><span class="event-card__age">Age ${event.minimum_age}+</span></div>
    <h3 id="event-${escapeHtml(event.id)}">${escapeHtml(event.title)}</h3><p>${escapeHtml(event.summary)}</p>
    <dl class="event-meta"><div><dt>When</dt><dd>${escapeHtml(formatEventDate(event.starts_at))}</dd></div><div><dt>Where</dt><dd>${escapeHtml(event.location)}</dd></div></dl>
    <button class="button button--primary book-button" type="button" data-event-id="${escapeHtml(event.id)}">${full ? 'Join the wait-list' : 'Reserve a place'}</button>
  </article>`;
}
export function bookingModal(event) {
    return `<div class="modal-backdrop" data-close-modal="true"><section class="modal-card" role="dialog" aria-modal="true" aria-labelledby="booking-title">
    <div class="modal-card__header"><div><span class="eyebrow">Registration</span><h2 id="booking-title">${escapeHtml(event.title)}</h2></div><button class="icon-button" type="button" data-close-modal="true" aria-label="Close form">×</button></div>
    <p class="modal-card__hint">Places are confirmed in submission order. When an event is full, a registration joins the wait-list automatically.</p>
    <form id="booking-form" data-event-id="${escapeHtml(event.id)}">
      <label>Full name<input name="name" minlength="2" maxlength="80" autocomplete="name" required /></label>
      <label>Email address<input name="email" type="email" maxlength="254" autocomplete="email" required /></label>
      <label>Age<input name="age" type="number" min="0" max="120" required /></label>
      <label class="checkbox-row"><input name="consent" type="checkbox" required /><span>I agree to the fictional demo privacy notice.</span></label>
      <p id="booking-error" class="form-error hidden" role="alert"></p>
      <div class="button-row"><button class="button button--quiet" type="button" data-close-modal="true">Cancel</button><button class="button button--primary" type="submit">Confirm registration</button></div>
    </form>
  </section></div>`;
}
export function scenarioPanel(result) {
    const scenarios = result.scenarios
        .map((scenario) => `<li><div class="scenario-list__topline"><strong>${escapeHtml(scenario.title)}</strong><span>${scenario.priority}</span></div><p>${escapeHtml(scenario.technique)}</p></li>`)
        .join('');
    return `<div class="scenario-summary"><span>Provider: ${escapeHtml(result.provider)}</span><span>${result.scenarios.length} scenarios</span></div>
    <p class="risk-line"><strong>Risks:</strong> ${escapeHtml(result.risks_detected.join(', '))}</p>
    <ol class="scenario-list">${scenarios}</ol><p class="review-note">${escapeHtml(result.review_note)}</p>`;
}
//# sourceMappingURL=templates.js.map