import pytest
import os
from datetime import datetime
from core.driver.driver_manager import WebDriverManagerSingleton

if not os.path.exists("ScreenShots"):
    os.makedirs("ScreenShots")

def pytest_bdd_before_scenario(request, feature, scenario):
    print(f"\n[START] Scenario: {scenario.name}")


def pytest_bdd_after_scenario(request, feature, scenario):
    print(f"[END] Scenario: {scenario.name}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        try:
            driver = WebDriverManagerSingleton().get_driver()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{item.name}_{timestamp}.png"
            file_path = os.path.join("ScreenShots", file_name)

            driver.save_screenshot(file_path)
            print(f"\nScreenshot saved at: {file_path}")

        except Exception as e:
            print(f"\n Could not capture screenshot: {e}")