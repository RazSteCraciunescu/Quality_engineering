export class ApiError extends Error {
    status;
    constructor(message, status) {
        super(message);
        this.status = status;
        this.name = 'ApiError';
    }
}
async function request(path, options = {}) {
    const response = await fetch(path, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
    });
    if (!response.ok) {
        const body = (await response.json().catch(() => null));
        throw new ApiError(body?.detail ?? `Request failed with status ${response.status}`, response.status);
    }
    return (await response.json());
}
export const api = {
    events: () => request('/api/events'),
    register: (payload) => request('/api/registrations', {
        method: 'POST',
        headers: { 'Idempotency-Key': crypto.randomUUID() },
        body: JSON.stringify(payload),
    }),
    scenarios: (requirement, risk) => request('/api/quality/generate-scenarios', {
        method: 'POST',
        body: JSON.stringify({ requirement, risk }),
    }),
};
//# sourceMappingURL=api.js.map