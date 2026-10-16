import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 1,
  iterations: 10,
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<250'],
  },
};

const baseUrl = __ENV.BASE_URL || 'http://127.0.0.1:8000';

export default function () {
  const response = http.get(`${baseUrl}/api/events`, {
    headers: { 'X-Request-ID': `k6-${__VU}-${__ITER}` },
  });
  check(response, {
    'status is 200': (result) => result.status === 200,
    'returns event list': (result) => Array.isArray(result.json()),
    'request id is returned': (result) => Boolean(result.headers['X-Request-Id']),
  });
}
