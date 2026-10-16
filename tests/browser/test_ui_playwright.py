from __future__ import annotations

import os
import shutil

import pytest

playwright = pytest.importorskip("playwright.sync_api")


@pytest.mark.browser
def test_critical_booking_flow_with_python_playwright() -> None:
    base_url = os.getenv("CIVICSHIFT_BASE_URL", "http://127.0.0.1:8000")
    with playwright.sync_playwright() as runtime:
        launch_options: dict[str, object] = {"headless": True}
        system_chromium = os.getenv("CHROMIUM_EXECUTABLE") or shutil.which("chromium")
        if system_chromium:
            launch_options["executable_path"] = system_chromium
        browser = runtime.chromium.launch(**launch_options)
        page = browser.new_page(viewport={"width": 1366, "height": 900})
        page.goto(base_url)
        page.get_by_role("heading", name="Choose a volunteer shift").wait_for()
        page.get_by_role("button", name="Reserve a place").first.click()
        page.get_by_label("Full name").fill("Browser Volunteer")
        page.get_by_label("Email address").fill("browser@example.test")
        page.get_by_label("Age").fill("30")
        page.get_by_label("I agree to the fictional demo privacy notice.").check()
        page.get_by_role("button", name="Confirm registration").click()
        page.get_by_role("heading", name="Your place is confirmed.").wait_for()
        browser.close()
