---
name: Locator Strategy Agent
description: Creates locator variables and method signatures for page objects with XPath > ID preference
mode: agent
tools:
  - search/codebase
  - read/readFile
  - writeFile
  - edit/createFile
  - searchFiles
---

# Locator Strategy Agent

## Responsibility
- Receive UI elements list from Step Definition Generator
- Scan existing page objects for locator and method patterns
- Generate locator variables and method signatures for page classes
- Create page object templates with XPath > ID preference
- Save page object templates for manual completion
- Return page object mapping for step definition integration

---

## On Activation

Receive from Step Definition Generator:
ui_elements: ["Login button", "Username field", "Password field", "Country dropdown"] feature_name: "user_login" page_name: "LoginPage"


DO NOT ask user for anything.
Process UI elements directly.

---

## Step 1 - Extract Element Information

From UI elements list, identify:
"Login button" → type: button, name: "Login", action: click "Username field" → type: input_field, name: "Username", action: enter_text "Password field" → type: input_field, name: "Password", action: enter_text "Country dropdown" → type: dropdown, name: "Country", action: select_option

---

## Step 2 - Scan Existing Page Object Patterns

Search existing page objects:
Search: pages/**/*Page.py Look for patterns like:

class SomePageName: # Locators login_button_xpath = "//button[@id='login']" username_field_id = "username"

# Methods
def click_login_button(self):
def enter_username(self, username):
def select_country(self, country):

Extract patterns:
- Locator naming: `<element>_<type>_<strategy>`
- Method naming: `<action>_<element>` or `<action>_<element>_<type>`
- Class structure and imports

---

## Step 3 - Generate Page Object Template

Create complete page object class:
```python
class LoginPage:
    """Page object for Login Page - Manual completion required"""
    
    def __init__(self, driver):
        self.driver = driver
    
    # Locators (XPath preferred, ID fallback)
    login_button_xpath = "# TODO: Add XPath for Login button"
    login_button_id = "# TODO: Add ID for Login button"
    
    username_field_xpath = "# TODO: Add XPath for Username field"

    username_field_id = "# TODO: Add ID for Username field"
    
    password_field_xpath = "# TODO: Add XPath for Password field"
    password_field_id = "# TODO: Add ID for Password field"
    
    country_dropdown_xpath = "# TODO: Add XPath for Country dropdown"
    country_dropdown_id = "# TODO: Add ID for Country dropdown"
    
    # Methods
    def click_login_button(self):
        """Click on Login button"""
        # TODO: Implement click action using login_button_xpath
        pass
    
    def enter_username(self, username):
        """Enter text in Username field"""
        # TODO: Implement text input using username_field_xpath
        pass
    
    def enter_password(self, password):
        """Enter text in Password field"""
        # TODO: Implement text input using password_field_xpath
        pass
    
    def select_country(self, country):
        """Select option from Country dropdown"""
        # TODO: Implement dropdown selection using country_dropdown_xpath
        pass


Step 4 - Save Page Object Template
Save to:
pages/<feature_name>_page.py
Step 5 - Return Page Object Mapping
Return to Step Definition Generator:



✅ LOCATOR_STRATEGY COMPLETE
page_object_file: pages/<feature_name>_page.py
page_class_name: <FeatureName>Page
method_mapping: {
  "click Login button": "click_login_button",
  "enter Username": "enter_username",
  "enter Password": "enter_password", 
  "select Country": "select_country"
}
locator_mapping: {
  "Login button": "login_button_xpath",
  "Username field": "username_field_xpath",
  "Password field": "password_field_xpath",
  "Country dropdown": "country_dropdown_xpath"
}


---

## Rules

Always create complete page object class in single file
Always use XPath as primary locator strategy
Always provide ID as fallback locator
Always generate method signatures with TODO comments
Always follow detected naming patterns
Always include proper class structure and imports

--- 

## Skills Required

skills/repository-search-rules/SKILL.md
skills/reusability-guidelines/SKILL.md

---
## Context Required

context/naming-conventions.md
context/framework-overview.md