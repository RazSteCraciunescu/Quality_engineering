import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    browse_events: {
      executor: 'ramping-arrival-rate',
      startRate: 2,
      timeUnit: '1s',
      preAllocatedVUs: 10,
      maxVUs: 40,
      stages: [
        { target: 10, duration: '30s' },
        { target: 20, duration: '1m' },
        { target: 0, duration: '20s' },
      ],
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<400', 'p(99)<800'],
  },
};

const baseUrl = __ENV.BASE_URL || 'http://127.0.0.1:8000';

export default function () {
  const response = http.get(`${baseUrl}/api/events`);
  check(response, { 'event browsing succeeds': (result) => result.status === 200 });
  sleep(0.2);
}
