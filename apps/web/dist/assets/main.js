import { ApiError, api } from './api.js';
import { escapeHtml } from './format.js';
import { bookingModal, eventCard, scenarioPanel, shell } from './templates.js';
const app = document.querySelector('#app');
if (!app)
    throw new Error('Application root is missing');
app.innerHTML = shell();
let events = [];
let lastModalTrigger = null;
const eventList = document.querySelector('#event-list');
const modalRoot = document.querySelector('#modal-root');
const announcement = document.querySelector('#announcement');
async function loadEvents() {
    try {
        events = await api.events();
        eventList.innerHTML = events.map(eventCard).join('');
        eventList.setAttribute('aria-busy', 'false');
    }
    catch {
        eventList.innerHTML = '<p class="form-error" role="alert">Events are temporarily unavailable. Check that the API is running.</p>';
        eventList.setAttribute('aria-busy', 'false');
    }
}
function closeModal() {
    modalRoot.innerHTML = '';
    lastModalTrigger?.focus();
}
eventList.addEventListener('click', (event) => {
    const target = event.target;
    if (!(target instanceof HTMLElement))
        return;
    const button = target.closest('.book-button');
    if (!button)
        return;
    const selected = events.find((item) => item.id === button.dataset.eventId);
    lastModalTrigger = button;
    if (!selected)
        return;
    modalRoot.innerHTML = bookingModal(selected);
    modalRoot.querySelector('input[name="name"]')?.focus();
});
modalRoot.addEventListener('click', (event) => {
    const target = event.target;
    if (!(target instanceof HTMLElement))
        return;
    if (target.dataset.closeModal === 'true')
        closeModal();
});
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && modalRoot.firstElementChild)
        closeModal();
});
modalRoot.addEventListener('submit', async (event) => {
    if (!(event.target instanceof HTMLFormElement) || event.target.id !== 'booking-form')
        return;
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const error = form.querySelector('#booking-error');
    const submit = form.querySelector('button[type="submit"]');
    error.classList.add('hidden');
    submit.disabled = true;
    submit.textContent = 'Saving…';
    try {
        const registration = await api.register({
            event_id: form.dataset.eventId ?? '',
            attendee_name: String(formData.get('name') ?? ''),
            attendee_email: String(formData.get('email') ?? ''),
            attendee_age: Number(formData.get('age')),
            consent: formData.get('consent') === 'on',
        });
        closeModal();
        announcement.innerHTML = `<section class="confirmation" role="status"><div><span class="eyebrow">Registration saved</span><h2>${registration.status === 'confirmed' ? 'Your place is confirmed.' : 'You joined the wait-list.'}</h2><p>Reference: <strong>${escapeHtml(registration.id)}</strong></p></div><button class="icon-button" type="button" id="dismiss-confirmation" aria-label="Dismiss confirmation">×</button></section>`;
        await loadEvents();
    }
    catch (caught) {
        error.textContent = caught instanceof ApiError ? caught.message : 'The registration could not be saved.';
        error.classList.remove('hidden');
    }
    finally {
        submit.disabled = false;
        submit.textContent = 'Confirm registration';
    }
});
announcement.addEventListener('click', (event) => {
    if (event.target instanceof HTMLElement && event.target.id === 'dismiss-confirmation') {
        announcement.innerHTML = '';
    }
});
document.querySelector('#quality-form')?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const button = form.querySelector('button[type="submit"]');
    const panel = document.querySelector('#scenario-panel');
    const requirement = form.querySelector('#requirement').value;
    const risk = form.querySelector('#risk').value;
    button.disabled = true;
    button.textContent = 'Analysing…';
    try {
        panel.innerHTML = scenarioPanel(await api.scenarios(requirement, risk));
    }
    catch (caught) {
        panel.innerHTML = '<p class="form-error" role="alert"></p>';
        const message = caught instanceof Error ? caught.message : 'Scenario generation failed.';
        panel.querySelector('p').textContent = message;
    }
    finally {
        button.disabled = false;
        button.textContent = 'Suggest test scenarios';
    }
});
void loadEvents();
//# sourceMappingURL=main.js.map