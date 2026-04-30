import pytest
from core.driver.driver_manager import WebDriverManagerSingleton

@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    manager = WebDriverManagerSingleton()
    driver = manager.get_driver(browser, headless)

    yield driver

    manager.quit_driver()