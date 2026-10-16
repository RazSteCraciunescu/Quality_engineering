# Manual and exploratory testing

Automation protects known behavior. These sessions target ambiguity, trust, unusual sequences and human experience.

## Charter 1: Capacity and fairness

**Mission:** Explore whether people can be overbooked, skipped or promoted unfairly.

**Setup:** One event near capacity; at least three distinct users; browser and API client.

**Tours:** rapid double submission, two browsers, cancellation in different queue positions, refresh/back navigation, retry after a simulated timeout, same email with case/whitespace changes.

**Oracles:** published rules, database counts, API response, timestamps and user-visible status.

## Charter 2: Accessible registration

**Mission:** Complete and recover from errors without a mouse.

**Setup:** Keyboard-only, 200% zoom, reduced motion, one screen-reader smoke pass.

**Focus:** skip link, navigation, dialog entry/exit, logical focus order, visible focus, labels, error association, status announcement and no content loss after validation.

## Charter 3: Untrusted and international input

**Mission:** Find validation, encoding or rendering assumptions.

**Data:** accented names, apostrophes, hyphens, long but valid email, right-to-left text sample, emoji, script-like text, SQL-like text, leading/trailing whitespace and copy/paste line breaks.

**Check:** stored normalization, UI rendering, logs, JSON encoding, database integrity and error clarity.

## Charter 4: AI-assisted test design

**Mission:** Determine whether suggestions are useful, bounded and honest.

**Prompts:** clear criterion, vague criterion, contradictory rule, instruction-like input, very long input, sensitive wording, unavailable Ollama and malformed model JSON.

**Check:** schema, coverage diversity, risk relevance, no claims of execution, no hidden-data disclosure and obvious human-review note.

## Session report template

- Charter and time box
- Environment/build
- Data used
- Areas covered
- Observations and questions
- Defects with evidence
- Risks not covered
- Follow-up automation candidate

A completed example is in [`exploratory-session-example.md`](exploratory-session-example.md).
