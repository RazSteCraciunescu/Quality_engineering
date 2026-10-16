# Browser and device compatibility

| Target | Automated project | Manual emphasis |
|---|---|---|
| Chromium desktop | `chromium` | Core flow, CSP and DevTools diagnostics |
| Firefox desktop | `firefox` | Form/date differences and focus behavior |
| WebKit | `webkit` | Safari-like dialog, input and layout behavior |
| Android viewport | `mobile-chrome` | Touch targets, reflow and virtual keyboard |
| iPhone viewport | `mobile-safari` | WebKit mobile layout and zoom |
| Microsoft Edge | Chromium evidence plus spot check | Windows high contrast and enterprise policies |

Support means the critical flow is operable and content is available. Pixel identity across engines is not a requirement.
