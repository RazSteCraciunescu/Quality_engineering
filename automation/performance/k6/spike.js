import http from 'k6/http';

export const options = {
  stages: [
    { duration: '10s', target: 5 },
    { duration: '10s', target: 75 },
    { duration: '20s', target: 75 },
    { duration: '20s', target: 5 },
  ],
  thresholds: { http_req_failed: ['rate<0.03'], http_req_duration: ['p(95)<750'] },
};

export default function () {
  http.get(`${__ENV.BASE_URL || 'http://127.0.0.1:8000'}/api/events`);
}
