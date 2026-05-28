from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.env_config import Config
from pages.BasePage import BasePage


class MouseActionsPage(BasePage):
    """Page object for mouse interactions: hover, clicks, and drag and drop."""

    POINT_ME_BUTTON_LOCATORS = [
        (By.XPATH, "//button[normalize-space()='Point Me']"),
        (By.XPATH, "//*[self::button or self::a][contains(normalize-space(), 'Point Me')]"),
    ]

    COPY_TEXT_BUTTON_LOCATORS = [
        (By.XPATH, "//button[normalize-space()='Copy Text']"),
        (By.XPATH, "//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'copy text')]"),
        (By.XPATH, "//button[contains(@ondblclick, 'copy')]"),
    ]

    DROPDOWN_LOCATORS = {
        "point me options": [
            (By.XPATH, "//*[contains(@class, 'dropdown-content') and .//*[normalize-space()='Mobiles' or normalize-space()='Laptops']]"),
            (By.XPATH, "//a[normalize-space()='Mobiles']/ancestor::*[contains(@class, 'dropdown-content')][1]"),
        ]
    }

    FIELD_LOCATORS = {
        "field1": [
            (By.ID, "field1"),
            (By.XPATH, "//input[contains(@id,'field1') or contains(@name,'field1') or contains(@placeholder,'Field1')]")
        ],
        "field2": [
            (By.ID, "field2"),
            (By.XPATH, "//input[contains(@id,'field2') or contains(@name,'field2') or contains(@placeholder,'Field2')]")
        ],
    }

    DRAGGABLE_LOCATORS = {
        "drag me to my target": [
            (By.ID, "draggable"),
            (By.XPATH, "//*[contains(@id, 'draggable') and contains(normalize-space(), 'Drag me to my target')]"),
            (By.XPATH, "//*[contains(normalize-space(), 'Drag me to my target')]")
        ]
    }

    DROP_TARGET_LOCATORS = {
        "drop here": [
            (By.ID, "droppable"),
            (By.XPATH, "//*[contains(@id, 'droppable') or contains(@class, 'droppable')][contains(normalize-space(), 'Drop here') or contains(normalize-space(), 'Dropped!')]"),
            (By.XPATH, "//*[contains(normalize-space(), 'Drop here') or contains(normalize-space(), 'Dropped!')]")
        ]
    }

    def __init__(self, driver):
        super().__init__(driver)

    def _normalize(self, text):
        return " ".join(str(text).strip().lower().split())

    def _wait(self, timeout=10):
        return WebDriverWait(self.driver, timeout)

    def _resolve_from_map(self, name, locator_map, control_type):
        key = self._normalize(name)
        if key not in locator_map:
            raise ValueError(f"Unsupported {control_type} name: {name}")
        return locator_map[key]

    def _find_visible_from_candidates(self, candidates, timeout=10):
        last_error = None
        for locator in candidates:
            try:
                return self._wait(timeout).until(EC.visibility_of_element_located(locator))
            except TimeoutException as exc:
                last_error = exc
        raise TimeoutException(f"Unable to locate visible element from candidates: {candidates}") from last_error

    def _find_clickable_from_candidates(self, candidates, timeout=10):
        last_error = None
        for locator in candidates:
            try:
                return self._wait(timeout).until(EC.element_to_be_clickable(locator))
            except TimeoutException as exc:
                last_error = exc
        raise TimeoutException(f"Unable to locate clickable element from candidates: {candidates}") from last_error

    def _get_button(self, button_name, clickable=True):
        key = self._normalize(button_name)
        button_map = {
            "point me": self.POINT_ME_BUTTON_LOCATORS,
            "copy text": self.COPY_TEXT_BUTTON_LOCATORS,
        }
        candidates = self._resolve_from_map(button_name, button_map, "button")
        if clickable:
            return self._find_clickable_from_candidates(candidates)
        return self._find_visible_from_candidates(candidates)

    def _get_field(self, field_name, clickable=False):
        candidates = self._resolve_from_map(field_name, self.FIELD_LOCATORS, "field")
        if clickable:
            return self._find_clickable_from_candidates(candidates)
        return self._find_visible_from_candidates(candidates)

    def _get_drag_element(self, draggable_name):
        candidates = self._resolve_from_map(draggable_name, self.DRAGGABLE_LOCATORS, "draggable")
        return self._find_visible_from_candidates(candidates)

    def _get_drop_target(self, target_name):
        candidates = self._resolve_from_map(target_name, self.DROP_TARGET_LOCATORS, "drop target")
        return self._find_visible_from_candidates(candidates)

    def _reset_hover_state(self):
        body = self._find_visible_from_candidates([(By.TAG_NAME, "body")])
        ActionChains(self.driver).move_to_element_with_offset(body, 1, 1).perform()

    def open_page(self, page_name):
        if self._normalize(page_name) != "mouse actions":
            raise ValueError(f"Unsupported page name: {page_name}")

        config = Config()
        qa_config = config.get("qa", {})
        base_url = qa_config.get("base_url")
        if not base_url:
            raise ValueError("Base URL not configured in config/config.yaml under qa.base_url")

        self.logger.info(f"Navigating to: {base_url}")
        self.driver.get(base_url)
        self._find_visible_from_candidates(self.POINT_ME_BUTTON_LOCATORS)
        self._find_visible_from_candidates(self.COPY_TEXT_BUTTON_LOCATORS)
        self._get_drag_element("Drag me to my target")
        self._get_drop_target("Drop here")

    def hover_on_button(self, button_name):
        button = self._get_button(button_name, clickable=False)
        ActionChains(self.driver).move_to_element(button).perform()

    def move_mouse_away_from_button(self, button_name):
        self._get_button(button_name, clickable=False)
        self._reset_hover_state()
        dropdown_candidates = self._resolve_from_map("Point Me options", self.DROPDOWN_LOCATORS, "dropdown")
        self._wait(5).until(EC.invisibility_of_element_located(dropdown_candidates[0]))

    def is_dropdown_visible(self, dropdown_name):
        candidates = self._resolve_from_map(dropdown_name, self.DROPDOWN_LOCATORS, "dropdown")
        for locator in candidates:
            try:
                element = self._wait(2).until(EC.visibility_of_element_located(locator))
                if element.is_displayed():
                    return True
            except TimeoutException:
                continue
        return False

    def get_dropdown_options(self, dropdown_name):
        dropdown = self._find_visible_from_candidates(
            self._resolve_from_map(dropdown_name, self.DROPDOWN_LOCATORS, "dropdown")
        )
        option_elements = dropdown.find_elements(By.XPATH, ".//*[self::a or self::button or self::li or self::span]")
        texts = [el.text.strip() for el in option_elements if el.text.strip()]
        unique_texts = []
        for text in texts:
            if text not in unique_texts:
                unique_texts.append(text)
        return unique_texts

    def set_field_value(self, field_name, value):
        field = self._get_field(field_name, clickable=True)
        field.click()
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(Keys.DELETE)
        field.send_keys(value)

    def clear_field(self, field_name):
        field = self._get_field(field_name, clickable=True)
        field.click()
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(Keys.DELETE)
        field.clear()

    def is_field_empty(self, field_name):
        return self.get_field_value(field_name) == ""

    def double_click_button(self, button_name, times=1):
        if times < 1:
            raise ValueError(f"times must be >= 1, got: {times}")

        button = self._get_button(button_name, clickable=True)
        for _ in range(times):
            ActionChains(self.driver).double_click(button).perform()

    def click_button(self, button_name):
        button = self._get_button(button_name, clickable=True)
        button.click()

    def get_field_value(self, field_name):
        field = self._get_field(field_name, clickable=False)
        tag_name = field.tag_name.lower()
        if tag_name in {"input", "textarea"}:
            return (field.get_attribute("value") or "").strip()
        return field.text.strip()

    def is_element_visible(self, element_name):
        key = self._normalize(element_name)
        try:
            if key in self.DRAGGABLE_LOCATORS:
                return self._get_drag_element(element_name).is_displayed()
            if key in self.DROP_TARGET_LOCATORS:
                return self._get_drop_target(element_name).is_displayed()
            return False
        except (TimeoutException, NoSuchElementException):
            return False

    def drag_and_drop_to_target(self, draggable_name, target_name):
        source = self._get_drag_element(draggable_name)
        target = self._get_drop_target(target_name)
        actions = ActionChains(self.driver)
        actions.drag_and_drop(source, target).perform()
        self._wait(5).until(lambda d: "Dropped!" in self.get_drop_area_text())

    def drag_and_drop_outside_target(self, draggable_name, target_name):
        source = self._get_drag_element(draggable_name)
        target = self._get_drop_target(target_name)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", source)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", target)

        # Use viewport-relative coordinates to avoid out-of-bounds moves on scrolled pages.
        geometry = self.driver.execute_script(
            """
            const src = arguments[0].getBoundingClientRect();
            const tgt = arguments[1].getBoundingClientRect();
            return {
                source: {left: src.left, top: src.top, width: src.width, height: src.height},
                target: {left: tgt.left, top: tgt.top, right: tgt.right, width: tgt.width, height: tgt.height},
                viewport: {w: window.innerWidth, h: window.innerHeight}
            };
            """,
            source,
            target,
        )

        source_center_x = float(geometry["source"]["left"]) + (float(geometry["source"]["width"]) / 2)
        source_center_y = float(geometry["source"]["top"]) + (float(geometry["source"]["height"]) / 2)
        target_center_y = float(geometry["target"]["top"]) + (float(geometry["target"]["height"]) / 2)
        viewport_w = float(geometry["viewport"]["w"])
        viewport_h = float(geometry["viewport"]["h"])

        margin = 10
        outside_x = min(viewport_w - margin, float(geometry["target"]["right"]) + 40)
        if outside_x <= float(geometry["target"]["right"]) + 5:
            outside_x = max(margin, float(geometry["target"]["left"]) - 40)
        outside_y = max(margin, min(target_center_y, viewport_h - margin))

        dx = int(outside_x - source_center_x)
        dy = int(outside_y - source_center_y)
        if dx == 0 and dy == 0:
            dx = 20

        ActionChains(self.driver).click_and_hold(source).move_by_offset(dx, dy).release().perform()

        self._wait(5).until(lambda d: self.get_drop_area_text() in {"Drop here", "Dropped!"})

    def get_drop_area_text(self):
        drop_target = self._get_drop_target("Drop here")
        return drop_target.text.strip()

    def is_element_inside_target(self, draggable_name, target_name):
        source = self._get_drag_element(draggable_name)
        target = self._get_drop_target(target_name)

        try:
            is_descendant = self.driver.execute_script("return arguments[0].contains(arguments[1]);", target, source)
            if bool(is_descendant):
                return True
        except Exception:
            pass

        source_rect = source.rect
        target_rect = target.rect

        source_center_x = source_rect["x"] + (source_rect["width"] / 2)
        source_center_y = source_rect["y"] + (source_rect["height"] / 2)

        within_x = target_rect["x"] <= source_center_x <= (target_rect["x"] + target_rect["width"])
        within_y = target_rect["y"] <= source_center_y <= (target_rect["y"] + target_rect["height"])
        return within_x and within_y


