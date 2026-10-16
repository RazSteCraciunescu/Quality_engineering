# Cypress-to-Playwright migration note

A team inheriting Cypress tests should migrate by business capability, not file count:

1. Map custom commands and fixtures to typed Playwright helpers.
2. Replace CSS-first selectors with roles, labels and explicit test IDs only where semantics cannot help.
3. Move API setup out of UI steps.
4. Recreate one critical journey and compare failure diagnostics before broad conversion.
5. Run old and new suites briefly in parallel; remove duplicated coverage after confidence is established.
6. Record unsupported assumptions such as direct browser internals, implicit retries or plugin behavior.

This repository uses Playwright as the primary browser framework and keeps Selenium as a small compatibility example. That is a maintainable portfolio choice, not a claim that other frameworks are inferior.
