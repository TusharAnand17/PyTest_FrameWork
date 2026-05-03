from selenium.webdriver.common.by import By
from pages.BasePage import BasePage

class UserFormPage(BasePage):
    # Locators
    NAME = (By.ID, "name")
    EMAIL = (By.ID, "email")
    PHONE = (By.ID, "phone")
    ADDRESS = (By.ID, "textarea")
    
    def day_checkbox(self, day):
        return (By.XPATH, f"//input[@type='checkbox' and @id='{day}']")
    
    
    def __init__(self, driver):
        super().__init__(driver)


    # Actions
    def enter_name(self, name):
        self.send_keys(self.NAME, name)

    def enter_email(self, email):
        self.send_keys(self.EMAIL, email)

    def enter_phone(self, phone):
        self.send_keys(self.PHONE, phone)

    def enter_address(self, address):
        self.send_keys(self.ADDRESS, address)

    def fill_form(self, name, email, phone, address):
        self.enter_name(name)
        self.enter_email(email)
        self.enter_phone(phone)
        self.enter_address(address)

    def select_day(self,day):
        self.logger.info(f"Selecting day checkbox: {day}")
        self.click(self.day_checkbox(day))
