# BUG-024: Encoded path traversal can read repository files

**Severity:** High  
**Priority:** P0  
**Status:** Fixed and confirmed

## Steps

1. Start the local API from the repository root.
2. Request `/%2e%2e/%2e%2e/%2e%2e/README.md`.
3. Inspect the response body and content type.

## Expected

The single-page application fallback serves only files inside `apps/web/dist`; an unknown or unsafe path returns the application shell.

## Actual

The catch-all route joined the decoded path directly to the static directory. Three parent-directory segments reached the repository root and returned `README.md`.

## Root cause and fix

`Path.is_file()` verified existence but not containment. The route now resolves both paths and serves a candidate only when it remains relative to the resolved web root.

## Regression

`test_spa_fallback_cannot_read_files_above_the_web_root` sends the encoded traversal payload and confirms that only the HTML application shell is returned.
