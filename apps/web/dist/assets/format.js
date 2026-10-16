export function formatEventDate(iso, locale = 'en-GB') {
    const date = new Date(iso);
    if (Number.isNaN(date.getTime()))
        return 'Date unavailable';
    return new Intl.DateTimeFormat(locale, {
        dateStyle: 'medium',
        timeStyle: 'short',
        timeZone: 'UTC',
    }).format(date);
}
export function availabilityLabel(remainingSeats, waitlistCount) {
    if (remainingSeats > 1)
        return `${remainingSeats} places available`;
    if (remainingSeats === 1)
        return '1 place available';
    if (waitlistCount === 0)
        return 'Wait-list available';
    return `Full · ${waitlistCount} waiting`;
}
export function escapeHtml(value) {
    return value.replace(/[&<>'"]/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' })[character] ??
        character);
}
//# sourceMappingURL=format.js.map