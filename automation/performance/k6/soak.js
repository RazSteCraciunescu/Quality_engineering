import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    sustained_browse: {
      executor: 'constant-arrival-rate',
      rate: 5,
      timeUnit: '1s',
      duration: __ENV.SOAK_DURATION || '15m',
      preAllocatedVUs: 8,
      maxVUs: 20,
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<400'],
    checks: ['rate>0.99'],
  },
};

const baseUrl = __ENV.BASE_URL || 'http://127.0.0.1:8000';

export default function () {
  const response = http.get(`${baseUrl}/api/events`);
  check(response, {
    'event list remains available': (result) => result.status === 200,
    'response contains events': (result) => Array.isArray(result.json()) && result.json().length > 0,
  });
  sleep(0.1);
}
