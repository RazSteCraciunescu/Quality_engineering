# BUG-003 — Placeholder canonical URL would block a real SEO release

**Status:** Known configuration item  
**Severity:** Low locally / High before public deployment  
**Priority:** P1 at deployment

## Observed

The checked-in canonical and sitemap use `https://example.invalid/` so the public repository never points to a real owner-controlled domain.

## Expected before deployment

Build-time configuration replaces the placeholder consistently in canonical, Open Graph and sitemap output.

## Decision

Accepted for the local portfolio baseline. The SEO test flags inconsistency or a missing canonical, while the release checklist requires replacing the reserved placeholder for a real environment.
