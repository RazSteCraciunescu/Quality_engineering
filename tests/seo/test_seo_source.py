from __future__ import annotations

import json
import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
HTML = (ROOT / "apps" / "web" / "dist" / "index.html").read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "pattern",
    [
        r"<title>[^<]{15,60}</title>",
        r'<meta\s+name="description"\s+content="[^"]{50,160}"',
        r'<link\s+rel="canonical"\s+href="https://[^\"]+"',
        r'<meta\s+name="robots"\s+content="index,follow"',
        r'<meta\s+property="og:title"',
    ],
)
def test_required_discovery_metadata(pattern: str) -> None:
    assert re.search(pattern, HTML, re.IGNORECASE)


def test_structured_data_is_valid_json() -> None:
    match = re.search(
        r'<script type="application/ld\+json">\s*(.*?)\s*</script>', HTML, re.DOTALL
    )
    assert match
    data = json.loads(match.group(1))
    assert data["@context"] == "https://schema.org"
    assert data["@type"] == "WebSite"


def test_robots_and_sitemap_agree() -> None:
    robots = (ROOT / "apps" / "web" / "dist" / "robots.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "apps" / "web" / "dist" / "sitemap.xml").read_text(encoding="utf-8")
    assert "Allow: /" in robots
    assert "https://example.invalid/sitemap.xml" in robots
    assert "https://example.invalid/" in sitemap
