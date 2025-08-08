import os
import pytest
from typing import Dict

# Load .env if available
try:  # pragma: no cover
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

APPIUM_URL = os.getenv("APPIUM_URL") or os.getenv("APPIUM_SERVER_URL")
PLATFORM = (os.getenv("PLATFORM") or os.getenv("PLATFORM_NAME") or "Android").strip()


def _android_caps() -> Dict[str, object]:
    return {
        "platformName": "Android",
        "automationName": os.getenv("AUTOMATION_NAME", "UiAutomator2"),
        "deviceName": os.getenv("DEVICE_NAME", "Android Emulator"),
        "platformVersion": os.getenv("PLATFORM_VERSION", ""),
        "app": os.getenv("APP", ""),
        "appPackage": os.getenv("APP_PACKAGE", ""),
        "appActivity": os.getenv("APP_ACTIVITY", ""),
        "udid": os.getenv("UDID", ""),
        "noReset": os.getenv("NO_RESET", "true").lower() == "true",
        "newCommandTimeout": int(os.getenv("NEW_COMMAND_TIMEOUT", "120")),
    }


def _ios_caps() -> Dict[str, object]:
    return {
        "platformName": "iOS",
        "automationName": os.getenv("AUTOMATION_NAME", "XCUITest"),
        "deviceName": os.getenv("DEVICE_NAME", "iPhone 15"),
        "platformVersion": os.getenv("PLATFORM_VERSION", "17.2"),
        "app": os.getenv("APP", ""),
        "bundleId": os.getenv("BUNDLE_ID", ""),
        "udid": os.getenv("UDID", ""),
        "noReset": os.getenv("NO_RESET", "true").lower() == "true",
        "newCommandTimeout": int(os.getenv("NEW_COMMAND_TIMEOUT", "120")),
    }


@pytest.fixture(scope="session")
def driver():
    if not APPIUM_URL:
        pytest.skip("APPIUM_URL not set; skipping mobile E2E tests")

    try:
        from appium import webdriver  # type: ignore
    except Exception as exc:  # pragma: no cover
        pytest.skip(f"Appium client not available: {exc}")

    caps = _android_caps() if PLATFORM.lower().startswith("android") else _ios_caps()
    driver = webdriver.Remote(APPIUM_URL, caps)

    yield driver

    try:
        driver.quit()
    except Exception:
        pass