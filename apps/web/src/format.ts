export function formatEventDate(iso: string, locale = 'en-GB'): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return 'Date unavailable';
  return new Intl.DateTimeFormat(locale, {
    dateStyle: 'medium',
    timeStyle: 'short',
    timeZone: 'UTC',
  }).format(date);
}

export function availabilityLabel(remainingSeats: number, waitlistCount: number): string {
  if (remainingSeats > 1) return `${remainingSeats} places available`;
  if (remainingSeats === 1) return '1 place available';
  if (waitlistCount === 0) return 'Wait-list available';
  return `Full · ${waitlistCount} waiting`;
}

export function escapeHtml(value: string): string {
  return value.replace(
    /[&<>'"]/g,
    (character) =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' })[character] ??
      character,
  );
}
