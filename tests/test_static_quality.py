from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path


class HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_title = False
        self.meta: dict[str, str] = {}
        self.links: dict[str, str] = {}
        self.html_lang = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "html":
            self.html_lang = data.get("lang", "") or ""
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            key = data.get("name") or data.get("property")
            if key and data.get("content"):
                self.meta[key] = data["content"] or ""
        if tag == "link" and data.get("rel"):
            self.links[data["rel"] or ""] = data.get("href", "") or ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data


def test_static_frontend_has_baseline_seo_metadata() -> None:
    parser = HeadParser()
    parser.feed(Path("apps/web/dist/index.html").read_text(encoding="utf-8"))
    assert parser.html_lang == "en"
    assert 10 <= len(parser.title.strip()) <= 60
    assert 70 <= len(parser.meta["description"]) <= 160
    assert parser.meta["robots"] == "index,follow"
    assert parser.links["canonical"] == "https://example.invalid/"


def test_manifest_and_sitemap_are_valid_and_public_safe() -> None:
    manifest = json.loads(Path("apps/web/dist/manifest.webmanifest").read_text())
    assert manifest["name"] == "CivicShift"
    sitemap = Path("apps/web/dist/sitemap.xml").read_text()
    assert "https://example.invalid/" in sitemap
    assert "localhost" not in sitemap


def test_no_remote_runtime_scripts_or_trackers() -> None:
    html = Path("apps/web/dist/index.html").read_text(encoding="utf-8")
    assert "googletagmanager" not in html.lower()
    assert "analytics" not in html.lower()
    assert 'src="http' not in html.lower()
