# Advanced UI Control Patterns Skill

## Purpose
Provide reusable patterns and best practices for implementing common advanced UI control scenarios in page objects: frames, alerts, windows, dropdowns, modals, and complex state management.

## Universal Control Patterns

### Pattern 1: Locator Composition and Reuse
**Principle**: Define base locators once, compose child/relative locators from them.

**Good Practice**:
```python
# Define base locator once
SECTION_XPATH = "//section[@id='preferences']"
OPTION_BY_LABEL_XPATH = f".//*[contains(@class, 'option') and normalize-space()='{{label}}']"

# Compose when needed
def find_option_in_section(self, label):
    section = self.driver.find_element(By.XPATH, self.SECTION_XPATH)
    return section.find_element(By.XPATH, self.OPTION_BY_LABEL_XPATH.format(label=label))
```

**Anti-Pattern**:
```python
# Repeating full XPath everywhere
def get_option_1(self):
    return self.driver.find_element(By.XPATH, "//section[@id='preferences']//*[contains(@class, 'option')]")

def get_option_2(self):
    return self.driver.find_element(By.XPATH, "//section[@id='preferences']//*[contains(@class, 'option')]")
```

---

### Pattern 2: Selenium API-based State Checking (Preferred)
**Principle**: Use Selenium element state APIs instead of attribute-based XPath checks.

**Good Practice** (Simple and Reliable):
```python
def is_radio_selected(self, locator):
    """Check if radio button is selected using element state API."""
    element = self.driver.find_element(*locator)
    return element.is_selected()

def is_element_visible(self, locator):
    """Check visibility using element display check."""
    element = self.driver.find_element(*locator)
    return element.is_displayed()

def is_button_enabled(self, locator):
    """Check if button is enabled."""
    element = self.driver.find_element(*locator)
    return element.is_enabled()
```

**Anti-Pattern** (Fragile Attribute Checks):
```python
def is_radio_selected(self):
    """Avoid using @checked attribute in XPath."""
    selected = self.driver.find_elements(
        By.XPATH,
        "//input[@type='radio' and @checked]"  # ❌ Fragile
    )
    return len(selected) > 0
```

---

### Pattern 3: Helper Methods for Common Operations
**Principle**: Create small, focused helper methods to reduce duplication and improve readability.

**Example: Select from Dropdown**:
```python
def _find_select_element(self, field_name):
    """Locate and wait for select element."""
    locator = self.FIELD_LOCATORS.get(field_name)
    if not locator:
        raise ValueError(f"Unsupported field: {field_name}")
    return self.wait.until(EC.visibility_of_element_located(locator))

def select_option(self, field_name, option_text):
    """Generic select operation."""
    select = Select(self._find_select_element(field_name))
    select.select_by_visible_text(option_text.strip())
```

---

## Control-Specific Patterns

### Frames
```python
# Switch to frame by locator
def switch_to_frame(self, frame_locator):
    """Switch to named/indexed frame."""
    frame_element = self.wait.until(EC.frame_to_be_available_and_switch_to_it(frame_locator))
    return frame_element

# Switch back to main content
def switch_to_default_content(self):
    """Return focus to main page content."""
    self.driver.switch_to.default_content()

# Nested frame handling
def switch_to_nested_frame(self, parent_locator, child_locator):
    """Navigate nested frame hierarchy."""
    self.switch_to_frame(parent_locator)
    self.wait.until(EC.frame_to_be_available_and_switch_to_it(child_locator))
```

### Alerts
```python
# Simple alert handling
def accept_alert(self):
    """Accept JavaScript alert."""
    alert = self.wait.until(EC.alert_is_present())
    alert.accept()

# Alert with message capture
def get_alert_text_and_accept(self):
    """Capture alert message and accept."""
    alert = self.wait.until(EC.alert_is_present())
    text = alert.text
    alert.accept()
    return text

# Dismiss alert
def dismiss_alert(self):
    """Dismiss/cancel alert."""
    alert = self.wait.until(EC.alert_is_present())
    alert.dismiss()

# Alert with input
def send_text_to_alert(self, text):
    """Send text to prompt alert."""
    alert = self.wait.until(EC.alert_is_present())
    alert.send_keys(text)
    alert.accept()
```

### Windows and Tabs
```python
# Switch to new window
def switch_to_new_window(self):
    """Switch to most recently opened window."""
    main_window = self.driver.current_window_handle
    for handle in self.driver.window_handles:
        if handle != main_window:
            self.driver.switch_to.window(handle)
            break

# Close current and return to main
def close_window_and_switch_to_main(self):
    """Close active window and return to first/main window."""
    self.driver.close()
    self.driver.switch_to.window(self.driver.window_handles[0])

# Switch by window title
def switch_to_window_by_title(self, title):
    """Find and switch to window matching title."""
    for handle in self.driver.window_handles:
        self.driver.switch_to.window(handle)
        if title in self.driver.title:
            return
    raise ValueError(f"Window with title '{title}' not found")
```

### Dropdowns
```python
# Select by visible text
def select_from_dropdown(self, locator, visible_text):
    """Select option from dropdown by visible text."""
    dropdown = Select(self.wait.until(EC.visibility_of_element_located(locator)))
    dropdown.select_by_visible_text(visible_text.strip())

# Select by value
def select_by_value(self, locator, value):
    """Select option by value attribute."""
    dropdown = Select(self.wait.until(EC.visibility_of_element_located(locator)))
    dropdown.select_by_value(value)

# Get all options
def get_dropdown_options(self, locator):
    """Return list of visible option texts."""
    dropdown = Select(self.wait.until(EC.visibility_of_element_located(locator)))
    return [opt.text.strip() for opt in dropdown.options]

# Multi-select
def select_multiple(self, locator, option_texts):
    """Select multiple options in multi-select."""
    dropdown = Select(self.wait.until(EC.visibility_of_element_located(locator)))
    for text in option_texts:
        dropdown.select_by_visible_text(text.strip())

def deselect_all(self, locator):
    """Clear all selections in multi-select."""
    dropdown = Select(self.wait.until(EC.visibility_of_element_located(locator)))
    dropdown.deselect_all()
```

### Modals and Overlays
```python
# Wait for modal to appear
def wait_for_modal(self, modal_locator):
    """Wait for modal/overlay to be visible."""
    return self.wait.until(EC.visibility_of_element_located(modal_locator))

# Close modal by button
def close_modal(self, close_button_locator):
    """Click close button on modal."""
    button = self.wait.until(EC.element_to_be_clickable(close_button_locator))
    button.click()

# Wait for modal to disappear
def wait_modal_to_disappear(self, modal_locator):
    """Wait for modal to be removed from DOM."""
    self.wait.until(EC.invisibility_of_element_located(modal_locator))
```

### Complex Selection (Radio, Checkbox, Custom Buttons)
```python
# Radio button selection using state API
def select_radio_option(self, option_locator):
    """Select radio button by locator."""
    radio = self.wait.until(EC.element_to_be_clickable(option_locator))
    if not radio.is_selected():
        radio.click()

# Checkbox with state verification
def check_option(self, checkbox_locator):
    """Check checkbox if not already checked."""
    checkbox = self.wait.until(EC.element_to_be_clickable(checkbox_locator))
    if not checkbox.is_selected():
        checkbox.click()

def uncheck_option(self, checkbox_locator):
    """Uncheck checkbox if checked."""
    checkbox = self.wait.until(EC.element_to_be_clickable(checkbox_locator))
    if checkbox.is_selected():
        checkbox.click()

# Verify state using is_selected()
def is_option_selected(self, locator):
    """Return True if option is selected."""
    try:
        element = self.driver.find_element(*locator)
        return element.is_selected()
    except:
        return False
```

---

## Best Practices Summary

1. **Define Once, Compose Many**: Extract base locators into constants; build variations from them.
2. **Prefer State APIs**: Use `is_selected()`, `is_displayed()`, `is_enabled()` instead of XPath attribute checks.
3. **Small Helpers**: Create focused helper methods for common operations (find, wait, select).
4. **Explicit Waits**: Always use waits for dynamic elements (dropdowns, frames, alerts).
5. **Error Clarity**: Raise meaningful errors for unsupported fields/options.
6. **Idempotency**: Design methods so running them twice has the same effect (avoid flaky toggles).
7. **Normalize Inputs**: Trim and lowercase field/option names for robust matching.
8. **Control-Agnostic Helpers**: Build methods that work across different control types where possible.

---

## Implementation Checklist
- [ ] All base locators defined once at class level
- [ ] No hardcoded full XPath repeated in multiple methods
- [ ] State checking uses `is_selected()`, `is_displayed()`, `is_enabled()`
- [ ] No `@checked`, `@selected` attribute checks in XPath
- [ ] All dynamic element access uses explicit waits
- [ ] Helper methods reduce duplication
- [ ] Input normalization (strip, lowercase) present
- [ ] Error messages are descriptive
- [ ] Methods are idempotent where applicable
- [ ] Imports are minimal and correct
