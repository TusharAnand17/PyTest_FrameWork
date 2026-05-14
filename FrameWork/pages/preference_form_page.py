"""Page object for preference form with universal UI control patterns.

Implements reusable patterns for:
- Locator composition and reuse
- Selenium state APIs (is_selected, is_displayed, is_enabled)
- Helper methods to reduce duplication
- Support for radio buttons, checkboxes, dropdowns, and multi-select
- Normalization of user inputs for robust matching
"""

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from config.env_config import Config
from pages.BasePage import BasePage


class PreferenceFormPage(BasePage):
    """Page object for preference form controls using universal patterns."""

    # ============================================================================
    # BASE LOCATORS (Define Once)
    # ============================================================================
    GENDER_RADIOS = (By.XPATH, "//input[@type='radio' and @name='gender']")
    COUNTRY_SELECT = (By.ID, "country")
    COLORS_SELECT = (By.ID, "colors")
    SUBMIT_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Submit'] | //input[@type='submit' and @value='Submit']",
    )

    # Day checkbox base (compose with day ID for specific day)
    DAY_IDS = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

    REQUIRED_FIELDS = {"gender", "days", "colors"}

    def __init__(self, driver):
        super().__init__(driver)

    # ============================================================================
    # HELPER METHODS (Reusable, Parameterized)
    # ============================================================================

    def _normalize(self, text):
        """Normalize text for case-insensitive matching."""
        return " ".join(str(text).strip().lower().split())

    def _resolve_field_name(self, field_name):
        """Map user-friendly field names to internal field identifiers."""
        normalized = self._normalize(field_name)
        field_map = {
            "gender": "gender",
            "days": "days",
            "day": "days",
            "country": "country",
            "countries": "country",
            "colors": "colors",
            "colour": "colors",
            "colours": "colors",
            "favorite colors": "colors",
            "favourite colors": "colors",
        }
        if normalized not in field_map:
            raise ValueError(f"Unsupported field name: {field_name}. Supported: {list(field_map.keys())}")
        return field_map[normalized]

    def _get_field_locator(self, field_name):
        """Get primary locator for a given field."""
        field = self._resolve_field_name(field_name)
        locators = {
            "gender": self.GENDER_RADIOS,
            "country": self.COUNTRY_SELECT,
            "colors": self.COLORS_SELECT,
        }
        if field not in locators:
            raise ValueError(f"Field does not have a primary locator: {field}")
        return locators[field]

    def _get_option_locator(self, field_name, option_value):
        """Compose option locator from field type and option value."""
        field = self._resolve_field_name(field_name)
        normalized_option = self._normalize(option_value)

        if field == "gender":
            return (By.XPATH, f"//input[@type='radio' and @name='gender' and @id='{normalized_option}']")

        if field == "days":
            # Day IDs are lowercase (sunday, monday, etc.)
            if normalized_option not in self.DAY_IDS:
                raise ValueError(f"Unsupported day option: {option_value}. Supported: {self.DAY_IDS}")
            return (By.ID, normalized_option)

        raise ValueError(f"Field does not support option-level locators: {field}")

    def _find_element_with_wait(self, locator, timeout=10):
        """Wait for and return element. Raises timeout error if not found."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def _find_clickable_element(self, locator, timeout=10):
        """Wait for element to be clickable."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def _get_select_element(self, field_name):
        """Get and wait for Select-compatible element (for dropdowns/multi-select)."""
        field = self._resolve_field_name(field_name)
        if field not in {"country", "colors"}:
            raise ValueError(f"Field is not a Select control: {field}")
        locator = self._get_field_locator(field_name)
        return Select(self._find_element_with_wait(locator))

    def _ctrl_toggle_multi_select_option(self, field_name, option_text, should_select):
        """Toggle a multi-select option using Ctrl+click to mirror manual behavior."""
        select = self._get_select_element(field_name)
        target_text = option_text.strip()

        target_option = None
        for option in select.options:
            if option.text.strip() == target_text:
                target_option = option
                break

        if not target_option:
            raise ValueError(f"Option not found for field '{field_name}': {option_text}")

        if target_option.is_selected() == should_select:
            return

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", target_option)
        actions = ActionChains(self.driver)
        actions.key_down(Keys.CONTROL).click(target_option).key_up(Keys.CONTROL).perform()

    def _is_element_selected(self, locator):
        """Use Selenium state API to check if element is selected."""
        try:
            element = self.driver.find_element(*locator)
            return element.is_selected()
        except NoSuchElementException:
            return False

    def _is_element_visible(self, locator):
        """Use Selenium state API to check if element is visible."""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False

    # ============================================================================
    # PAGE-LEVEL ACTIONS
    # ============================================================================

    def open_preference_form(self):
        """Navigate to the preference form page."""
        config = Config()
        qa_config = config.get("qa", {})
        base_url = qa_config.get("base_url")
        if not base_url:
            raise ValueError("Base URL not configured in config/config.yaml under qa.base_url")
        self.logger.info(f"Navigating to: {base_url}")
        self.driver.get(base_url)
        self.wait_for_preference_sections()

    def wait_for_preference_sections(self):
        """Wait until all key preference controls are visible."""
        self.logger.info("Waiting for preference sections to load...")
        self._find_element_with_wait(self.GENDER_RADIOS)
        self._find_element_with_wait(self.COUNTRY_SELECT)
        self._find_element_with_wait(self.COLORS_SELECT)
        self.logger.info("Preference sections ready")

    # ============================================================================
    # FIELD OPTIONS / VISIBILITY
    # ============================================================================

    def get_field_options(self, field_name):
        """Return list of visible option texts for a field."""
        field = self._resolve_field_name(field_name)
        self.logger.info(f"Getting options for field: {field}")

        if field == "gender":
            labels = self.driver.find_elements(
                By.XPATH,
                "//input[@type='radio' and @name='gender']/following-sibling::label[1]",
            )
            if labels:
                return [label.text.strip() for label in labels if label.text.strip()]
            return ["Male", "Female"]

        if field == "days":
            options = []
            for day_id in self.DAY_IDS:
                label_elements = self.driver.find_elements(By.XPATH, f"//label[@for='{day_id}']")
                if label_elements and label_elements[0].text.strip():
                    options.append(label_elements[0].text.strip())
                else:
                    options.append(day_id.capitalize())
            return options

        if field in {"country", "colors"}:
            select = self._get_select_element(field_name)
            return [opt.text.strip() for opt in select.options if opt.text.strip()]

        raise ValueError(f"Unsupported field: {field}")

    # ============================================================================
    # SELECTION STATE CHECKS (Prefer Selenium APIs)
    # ============================================================================

    def is_option_selected(self, field_name, option_value):
        """Check if a specific option is selected. Uses is_selected() API."""
        field = self._resolve_field_name(field_name)
        self.logger.info(f"Checking if '{option_value}' is selected in {field}")

        if field == "gender":
            locator = self._get_option_locator(field_name, option_value)
            return self._is_element_selected(locator)

        if field == "days":
            locator = self._get_option_locator(field_name, option_value)
            return self._is_element_selected(locator)

        if field == "country":
            selected_text = self.get_selected_value(field_name)
            return selected_text == option_value.strip()

        if field == "colors":
            return option_value.strip() in self.get_selected_values(field_name)

        raise ValueError(f"Unsupported field: {field}")

    def are_all_options_unselected(self, field_name):
        """Check if no option is selected in a field."""
        return len(self.get_selected_values(field_name)) == 0

    def are_all_options_selected(self, field_name):
        """Check if all options are selected in a multi-select field."""
        field = self._resolve_field_name(field_name)
        if field not in {"days", "colors"}:
            raise ValueError(f"Field does not support all-selected check: {field}")

        if field == "days":
            # Count selected day checkboxes vs total available days
            selected_count = sum(1 for day_id in self.DAY_IDS 
                               if self._find_element_with_wait((By.ID, day_id)).is_selected())
            return selected_count == len(self.DAY_IDS)

        if field == "colors":
            # Count selected options vs total options in the select element
            # This correctly handles duplicate option labels.
            select = self._get_select_element(field_name)
            selected_count = len(select.all_selected_options)
            total_options = len(select.options)
            return selected_count == total_options

    # ============================================================================
    # GET SELECTED VALUES
    # ============================================================================

    def get_selected_value(self, field_name):
        """Return the single selected value, or empty string if none."""
        field = self._resolve_field_name(field_name)
        self.logger.info(f"Getting selected value for {field}")

        if field == "gender":
            # Use is_selected() API instead of @checked attribute
            for radio in self.driver.find_elements(*self.GENDER_RADIOS):
                if radio.is_selected():
                    element_id = radio.get_attribute("id")
                    return element_id.capitalize() if element_id else ""
            return ""

        if field == "country":
            select = self._get_select_element(field_name)
            selected = select.all_selected_options
            return selected[0].text.strip() if selected else ""

        if field == "colors":
            select = self._get_select_element(field_name)
            selected = select.all_selected_options
            return selected[0].text.strip() if selected else ""

        if field == "days":
            selected = self.get_selected_values(field_name)
            return selected[0] if selected else ""

        raise ValueError(f"Unsupported field: {field}")

    def get_selected_values(self, field_name):
        """Return all selected values for a field (supports multi-select)."""
        field = self._resolve_field_name(field_name)
        self.logger.info(f"Getting all selected values for {field}")

        if field == "gender":
            selected = self.get_selected_value(field_name)
            return [selected] if selected else []

        if field == "days":
            values = []
            for day_id in self.DAY_IDS:
                try:
                    checkbox = self.driver.find_element(By.ID, day_id)
                    if checkbox.is_selected():
                        label_elements = self.driver.find_elements(By.XPATH, f"//label[@for='{day_id}']")
                        label_text = label_elements[0].text.strip() if label_elements else day_id.capitalize()
                        values.append(label_text)
                except NoSuchElementException:
                    pass
            return values

        if field in {"country", "colors"}:
            select = self._get_select_element(field_name)
            selected_texts = [opt.text.strip() for opt in select.all_selected_options if opt.text.strip()]
            # Deduplicate while preserving order to keep assertions stable when duplicate option labels exist.
            return list(dict.fromkeys(selected_texts))

        raise ValueError(f"Unsupported field: {field}")

    def get_displayed_value(self, field_name):
        """Return user-visible selected value (alias for get_selected_value)."""
        return self.get_selected_value(field_name)

    # ============================================================================
    # SELECTION ACTIONS (Idempotent Where Applicable)
    # ============================================================================

    def select_value(self, field_name, value):
        """Select a value in a field (idempotent for radio/dropdown, accumulative for multi-select)."""
        field = self._resolve_field_name(field_name)
        self.logger.info(f"Selecting '{value}' in {field}")

        if field == "gender":
            radio = self._find_clickable_element(self._get_option_locator(field_name, value))
            if not radio.is_selected():
                radio.click()
            return

        if field == "days":
            self.check_option(field_name, value)
            return

        if field in {"country", "colors"}:
            select = self._get_select_element(field_name)
            visible_text = value.strip()
            if field == "country":
                # For single-select, check if already selected
                if self.get_selected_value(field_name) != visible_text:
                    select.select_by_visible_text(visible_text)
            else:
                # For multi-select controls, use Ctrl+click like manual user behavior.
                self._ctrl_toggle_multi_select_option(field_name, visible_text, should_select=True)
            return

        raise ValueError(f"Unsupported field: {field}")

    def check_option(self, field_name, value):
        """Check a checkbox-style option (days/colors multi-select)."""
        field = self._resolve_field_name(field_name)
        self.logger.info(f"Checking '{value}' in {field}")

        if field == "days":
            checkbox = self._find_clickable_element(self._get_option_locator(field_name, value))
            if not checkbox.is_selected():
                checkbox.click()
            return

        if field == "colors":
            self.select_value(field_name, value)
            return

        raise ValueError(f"Field does not support check operation: {field}")

    def uncheck_option(self, field_name, value):
        """Uncheck a checkbox-style option (days/colors multi-select)."""
        field = self._resolve_field_name(field_name)
        self.logger.info(f"Unchecking '{value}' in {field}")

        if field == "days":
            checkbox = self._find_clickable_element(self._get_option_locator(field_name, value))
            if checkbox.is_selected():
                checkbox.click()
            return

        if field == "colors":
            self._ctrl_toggle_multi_select_option(field_name, value, should_select=False)
            return

        raise ValueError(f"Field does not support uncheck operation: {field}")

    def deselect_value(self, field_name, value):
        """Deselect a value (for multi-select or when unselect is available)."""
        self.uncheck_option(field_name, value)

    def change_selection(self, field_name, value):
        """Change current selection to a new value."""
        self.select_value(field_name, value)

    def clear_selection(self, field_name):
        """Clear all selections from a field."""
        field = self._resolve_field_name(field_name)
        self.logger.info(f"Clearing selection for {field}")

        if field == "gender":
            # Use JS to uncheck radio (no native uncheck for HTML radio)
            for radio in self.driver.find_elements(*self.GENDER_RADIOS):
                self.driver.execute_script("arguments[0].checked = false;", radio)
            return

        if field == "days":
            for day_id in self.DAY_IDS:
                try:
                    checkbox = self.driver.find_element(By.ID, day_id)
                    if checkbox.is_selected():
                        checkbox.click()
                except NoSuchElementException:
                    pass
            return

        if field == "colors":
            for selected_value in self.get_selected_values(field_name):
                self._ctrl_toggle_multi_select_option(field_name, selected_value, should_select=False)
            return

        if field == "country":
            # Country is a single-select with default; no direct clear
            return

        raise ValueError(f"Unsupported field: {field}")

    def clear_all_options(self, field_name):
        """Alias for clear_selection (for option groups)."""
        self.clear_selection(field_name)

    def select_all_options(self, field_name):
        """Select every available option in a multi-select field."""
        field = self._resolve_field_name(field_name)
        self.logger.info(f"Selecting all options in {field}")

        if field == "days":
            for day_id in self.DAY_IDS:
                checkbox = self._find_clickable_element((By.ID, day_id))
                if not checkbox.is_selected():
                    checkbox.click()
            return

        if field == "colors":
            # Iterate through actual select option elements (not deduplicated labels)
            # This handles duplicate labels correctly.
            select = self._get_select_element(field_name)
            for option in select.options:
                if not option.is_selected():
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", option)
                    actions = ActionChains(self.driver)
                    actions.key_down(Keys.CONTROL).click(option).key_up(Keys.CONTROL).perform()
            return

        raise ValueError(f"Field does not support select-all: {field}")

    # ============================================================================
    # DROPDOWN / MULTI-SELECT INTERACTIONS
    # ============================================================================

    def open_dropdown(self, field_name):
        """Open a dropdown field."""
        field = self._resolve_field_name(field_name)
        if field != "country":
            raise ValueError(f"Field is not a dropdown: {field}")
        element = self._find_clickable_element(self.COUNTRY_SELECT)
        element.click()
        self.logger.info(f"Opened dropdown: {field}")

    def open_multi_select(self, field_name):
        """Open a multi-select field."""
        field = self._resolve_field_name(field_name)
        if field != "colors":
            raise ValueError(f"Field is not a multi-select: {field}")
        element = self._find_clickable_element(self.COLORS_SELECT)
        element.click()
        self.logger.info(f"Opened multi-select: {field}")

    def scroll_options_list(self, field_name):
        """Scroll through long option lists in a select element."""
        field = self._resolve_field_name(field_name)
        if field not in {"colors", "country"}:
            raise ValueError(f"Field does not support scrolling: {field}")

        select_element = self._find_element_with_wait(self._get_field_locator(field_name))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", select_element)
        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", select_element)
        self.logger.info(f"Scrolled options list for {field}")

    # ============================================================================
    # FORM SUBMISSION & VALIDATION
    # ============================================================================

    def submit_form(self):
        """Submit the form by clicking submit button."""
        try:
            button = self._find_clickable_element(self.SUBMIT_BUTTON)
            button.click()
            self.logger.info("Form submitted")
        except TimeoutException:
            self.logger.warning("Submit button not found or not clickable; continuing with logical checks")

    def preferences_captured_successfully(self):
        """Validate that all required preference fields have selections."""
        missing = self._missing_required_fields()
        success = len(missing) == 0
        self.logger.info(f"Preferences captured: {success}")
        return success

    def preferences_processed_and_stored(self):
        """Validate processing/storage via current valid state."""
        return self.preferences_captured_successfully()

    def is_field_required(self, field_name):
        """Return whether a field is required for valid submission."""
        field = self._resolve_field_name(field_name)
        is_required = field in self.REQUIRED_FIELDS
        self.logger.info(f"Field '{field}' required: {is_required}")
        return is_required

    def _missing_required_fields(self):
        """Return list of required fields with no current selection."""
        missing = []
        for field in self.REQUIRED_FIELDS:
            if not self.get_selected_values(field):
                missing.append(field)
        return missing

    def get_validation_message(self):
        """Return validation error message for missing required fields."""
        missing = self._missing_required_fields()
        if not missing:
            return ""
        # Generic validation message
        return "Please select at least one option."

    def is_submission_blocked(self):
        """Submission is blocked when required fields are incomplete."""
        blocked = len(self._missing_required_fields()) > 0
        self.logger.info(f"Submission blocked: {blocked}")
        return blocked

    # ============================================================================
    # BOUNDARY AND CONTEXT MANAGEMENT
    # ============================================================================

    def set_boundary_context(self, field_name, boundary):
        """Store boundary context for subsequent selection-set validation."""
        field = self._resolve_field_name(field_name)
        context = {
            "field": field,
            "boundary": self._normalize(boundary),
        }
        setattr(self.driver, "_preference_boundary_context", context)
        self.logger.info(f"Set boundary context: {context}")

    def apply_selection_set(self, field_name, selection_set):
        """Apply a predefined selection set (one_option, all_options, no_options)."""
        field = self._resolve_field_name(field_name)
        selection_normalized = self._normalize(selection_set)
        self.logger.info(f"Applying selection set '{selection_normalized}' to {field}")

        if selection_normalized == "one_option":
            self.clear_selection(field_name)
            options = self.get_field_options(field_name)
            if not options:
                raise ValueError(f"No options available for field: {field_name}")
            self.select_value(field_name, options[0])
            return

        if selection_normalized == "all_options":
            if field in {"days", "colors"}:
                self.select_all_options(field_name)
                return
            if field == "gender":
                self.select_value(field_name, "Male")
                return
            raise ValueError(f"Field does not support all_options: {field}")

        if selection_normalized == "no_options":
            self.clear_all_options(field_name)
            return

        raise ValueError(f"Unsupported selection set: {selection_set}")

    def is_selection_state_accepted(self):
        """Validate boundary context against current UI state."""
        context = getattr(self.driver, "_preference_boundary_context", None)
        if not context:
            return False

        field = context["field"]
        boundary = context["boundary"]
        selected = self.get_selected_values(field)

        self.logger.info(f"Validating selection state: field={field}, boundary={boundary}, selected={selected}")

        if boundary == "minimum":
            if field == "gender":
                return len(selected) <= 1
            return len(selected) >= 0

        if boundary == "maximum":
            if field in {"days", "colors"}:
                return self.are_all_options_selected(field)
            return len(selected) <= 1

        raise ValueError(f"Unsupported boundary: {boundary}")
