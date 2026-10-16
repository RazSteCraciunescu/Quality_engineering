export type EventItem = {
  id: string;
  slug: string;
  title: string;
  summary: string;
  location: string;
  starts_at: string;
  capacity: number;
  minimum_age: number;
  status: string;
  confirmed_count: number;
  waitlist_count: number;
  remaining_seats: number;
};

export type Registration = {
  id: string;
  event_id: string;
  attendee_name: string;
  attendee_email: string;
  attendee_age: number;
  consent: number;
  status: 'confirmed' | 'waitlisted' | 'cancelled';
  created_at: string;
  updated_at: string;
  replayed?: boolean;
};

export type GeneratedScenario = {
  id: string;
  title: string;
  technique: string;
  priority: 'P0' | 'P1' | 'P2';
  steps: string[];
  expected: string;
  tags: string[];
};

export type ScenarioResult = {
  provider: string;
  requirement_summary: string;
  risks_detected: string[];
  scenarios: GeneratedScenario[];
  review_note: string;
};
