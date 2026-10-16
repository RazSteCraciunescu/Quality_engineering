# Security policy

CivicShift is a fictional portfolio application and must not be used to collect real personal data. The default database and all checked-in fixtures are synthetic.

## Reporting

For a public fork, use the repository owner's preferred private reporting channel. Do not place exploit payloads, tokens or personal information in a public issue.

## Supported version

Only the latest revision of the default branch is maintained.

## Security boundaries

- There are no production credentials or live enterprise integrations.
- Public registration is the intended use case; no administrative API is exposed.
- The optional Ollama adapter is local-only by default and receives untrusted requirements inside explicit data delimiters.
- Dependency, container and dynamic scans are defense-in-depth checks, not proof that the application is vulnerability-free.
