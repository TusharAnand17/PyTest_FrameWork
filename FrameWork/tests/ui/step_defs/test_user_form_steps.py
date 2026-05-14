# steps/test_user_form_steps.py
from pytest_bdd import scenarios, given, when, parsers
from pages.FormPage import UserFormPage
from core.utils.logger import MyLogger
from config.env_config import Config

scenarios("ui/features/user_form.feature")

logger = MyLogger().get_logger()


@given("user is on form page")
def open_form_page(browser):
    config = Config()
    base_url = config.get("qa").get("base_url")
    logger.info(f"Navigating to: {base_url}")
    browser.get(base_url)


@when("user fills the form with valid data")
def fill_form(browser):
    form = UserFormPage(browser)
    form.fill_form(
        name="Tushar",
        email="tushar@test.com",
        phone="9999999999",
        address="Bangalore"
    )


@when(parsers.parse('user selects "{day}" from days checkbox'))
def select_day(browser, day):
    form = UserFormPage(driver)
    form.select_day(day)