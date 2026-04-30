from pytest_bdd import scenarios, given, when, then,parsers
from core.utils.logger import MyLogger
logger = MyLogger().get_logger()
from pages.FormPage import UserFormPage
import time
from config.env_config import Config

scenarios("ui/features/user_form.feature")


logger = MyLogger().get_logger()

@given("user is on form page")
def open_form_page(driver):
    logger.info("Opening page")
    config = Config()
    base_url = config.get("qa").get("base_url")
    logger.info(f"Navigating to: {base_url}")
    driver.get(base_url)


@when("user fills the form with valid data")
def fill_form():
    form = UserFormPage()
    form.fill_form(
        name="Tushar",
        email="tushar@test.com",
        phone="9999999999",
        address="Bangalore"
    )

@when(parsers.parse('user selects "{day}" from days checkbox'))
def select_checkbox(day):
    form = UserFormPage()
    form.select_day(day)
    time.sleep(5)