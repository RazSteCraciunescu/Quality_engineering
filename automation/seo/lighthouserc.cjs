module.exports = {
  ci: {
    collect: {
      url: ['http://127.0.0.1:8000/'],
      numberOfRuns: 2,
      settings: { chromeFlags: '--headless --no-sandbox' },
    },
    assert: {
      assertions: {
        'categories:performance': ['warn', { minScore: 0.85 }],
        'categories:accessibility': ['error', { minScore: 0.95 }],
        'categories:best-practices': ['error', { minScore: 0.9 }],
        'categories:seo': ['error', { minScore: 0.95 }],
        'document-title': 'error',
        'meta-description': 'error',
        'html-has-lang': 'error',
        'link-text': 'error'
      },
    },
    upload: { target: 'filesystem', outputDir: 'reports/generated/lighthouse' },
  },
};
