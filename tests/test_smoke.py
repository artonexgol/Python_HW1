import os
import pytest

from typing import Optional

CHECK_AID: Optional[str] = os.getenv("CHECK_AID")  # accessibility id to assert is present
CHECK_ID: Optional[str] = os.getenv("CHECK_ID")    # native id (Android resource-id or iOS name)


@pytest.mark.smoke
@pytest.mark.usefixtures("driver")
def test_app_launches_and_shows_first_screen(driver):
    assert driver.session_id

    # Optionally wait for a specific element if env vars provided
    if not (CHECK_AID or CHECK_ID):
        pytest.skip("No CHECK_AID/CHECK_ID provided; launch verified via session only")

    try:
        from appium.webdriver.common.appiumby import AppiumBy  # type: ignore
        from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
        from selenium.webdriver.support import expected_conditions as EC  # type: ignore
    except Exception:
        pytest.skip("Selenium/Appium extras not available to perform element assertions")

    locator = None
    if CHECK_AID:
        locator = (AppiumBy.ACCESSIBILITY_ID, CHECK_AID)
    else:
        # For Android, resource-id like com.example:id/title; for iOS, use name
        locator = (AppiumBy.ID, CHECK_ID)

    el = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
    assert el.is_displayed()