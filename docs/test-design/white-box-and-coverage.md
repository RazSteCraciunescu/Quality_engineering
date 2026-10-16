# White-box coverage notes

Coverage is used to find unexercised logic, not as proof of product quality.

High-value branches include:

- idempotency key present/absent/replayed;
- published event found/not found;
- eligible/ineligible age;
- consent accepted/rejected;
- duplicate present/absent;
- capacity available/full;
- cancellation from confirmed/wait-listed/already-cancelled;
- waiting user present/absent for promotion;
- rules/Ollama/fallback provider paths;
- rate-limit allow/reject and expired-window cleanup.

The project gate uses branch-aware coverage with an 85% floor for the compact backend. Risk coverage and assertions remain more important than optimising the percentage.
