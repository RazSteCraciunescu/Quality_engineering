import type { EventItem, Registration, ScenarioResult } from './types.js';

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(path, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new ApiError(body?.detail ?? `Request failed with status ${response.status}`, response.status);
  }
  return (await response.json()) as T;
}

export const api = {
  events: () => request<EventItem[]>('/api/events'),
  register: (payload: {
    event_id: string;
    attendee_name: string;
    attendee_email: string;
    attendee_age: number;
    consent: boolean;
  }) =>
    request<Registration>('/api/registrations', {
      method: 'POST',
      headers: { 'Idempotency-Key': crypto.randomUUID() },
      body: JSON.stringify(payload),
    }),
  scenarios: (requirement: string, risk: string) =>
    request<ScenarioResult>('/api/quality/generate-scenarios', {
      method: 'POST',
      body: JSON.stringify({ requirement, risk }),
    }),
};
