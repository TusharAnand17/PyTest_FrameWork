import threading
from core.driver.browser_factory import BrowserFactory

class WebDriverManagerSingleton:
    _instance = None
    _lock = threading.Lock()
    _thread_local = threading.local()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(WebDriverManagerSingleton, cls).__new__(cls)
        return cls._instance

    def get_driver(self, browser_type="chrome", headless=False):
        if not hasattr(self._thread_local, "driver"):
            factory = BrowserFactory.get_driver_factory(browser_type)
            self._thread_local.driver = factory.create_driver(headless=headless)
        return self._thread_local.driver

    def quit_driver(self):
        if hasattr(self._thread_local, "driver"):
            self._thread_local.driver.quit()
            del self._thread_local.driver