"""Small Selenium example for teams maintaining a Python browser stack.

Run the API first, then: pytest automation/selenium/test_smoke.py --browser
"""

from __future__ import annotations

import pytest

selenium = pytest.importorskip("selenium")
from selenium import webdriver  # noqa: E402
from selenium.webdriver.common.by import By  # noqa: E402


@pytest.mark.browser
def test_homepage_heading() -> None:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("http://127.0.0.1:8000")
        assert "CivicShift" in driver.title
        assert "Volunteer where" in driver.find_element(By.TAG_NAME, "h1").text
    finally:
        driver.quit()
