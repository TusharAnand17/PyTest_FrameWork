from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

class WebDriverFactory(ABC):

    @abstractmethod
    def create_driver(self, headless=True):
        pass

class ChromeDriverFactory(WebDriverFactory):
    def create_driver(self, headless=True):
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver


class FirefoxDriverFactory(WebDriverFactory):
    def create_driver(self, headless=True):
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")

        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        return driver


class EdgeDriverFactory(WebDriverFactory):
    def create_driver(self, headless=True):
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")

        driver = webdriver.Edge(options=options)
        driver.maximize_window()
        return driver


class BrowserFactory:

    @staticmethod
    def get_driver_factory(browser_type):
        factories = {
            "chrome": ChromeDriverFactory,
            "firefox": FirefoxDriverFactory,
            "edge": EdgeDriverFactory
        }

        factory_class = factories.get(browser_type.lower())
        if not factory_class:
            raise ValueError(f"Unsupported browser: {browser_type}")

        return factory_class()