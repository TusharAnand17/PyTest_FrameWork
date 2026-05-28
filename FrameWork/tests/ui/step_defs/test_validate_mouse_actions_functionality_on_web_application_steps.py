from importlib import import_module

from pytest_bdd import given, parsers, scenarios, then, when


scenarios("ui/features/validate_mouse_actions_functionality_on_web_application.feature")


def _page(driver):
    """Resolve mouse actions page object from common module naming variants."""
    candidates = [
        ("pages.mouse_actions_page", "MouseActionsPage"),
        (
            "pages.validate_mouse_actions_functionality_on_web_application_page",
            "ValidateMouseActionsFunctionalityOnWebApplicationPage",
        ),
    ]

    for module_name, class_name in candidates:
        try:
            module = import_module(module_name)
            page_cls = getattr(module, class_name, None)
            if page_cls is not None:
                return page_cls(driver)
        except ModuleNotFoundError:
            continue

    raise ModuleNotFoundError(
        "Mouse actions page object not found. Expected one of: "
        "pages.mouse_actions_page.MouseActionsPage or "
        "pages.validate_mouse_actions_functionality_on_web_application_page."
        "ValidateMouseActionsFunctionalityOnWebApplicationPage"
    )


@given(parsers.parse('user is on "{page_name}" page'))
def user_is_on_page(driver, page_name):
    page = _page(driver)
    page.open_page(page_name)


@given(parsers.parse('user hovers on "{button_name}" button'))
@when(parsers.parse('user hovers on "{button_name}" button'))
def user_hovers_on_button(driver, button_name):
    page = _page(driver)
    page.hover_on_button(button_name)


@when(parsers.parse('user moves mouse away from "{button_name}" button'))
def user_moves_mouse_away_from_button(driver, button_name):
    page = _page(driver)
    page.move_mouse_away_from_button(button_name)


@given(parsers.parse('dropdown "{dropdown_name}" should be visible'))
@then(parsers.parse('dropdown "{dropdown_name}" should be visible'))
def dropdown_should_be_visible(driver, dropdown_name):
    page = _page(driver)
    assert page.is_dropdown_visible(dropdown_name), (
        f'Expected dropdown "{dropdown_name}" to be visible.'
    )


@given(parsers.parse('dropdown "{dropdown_name}" should not be visible'))
@then(parsers.parse('dropdown "{dropdown_name}" should not be visible'))
def dropdown_should_not_be_visible(driver, dropdown_name):
    page = _page(driver)
    assert not page.is_dropdown_visible(dropdown_name), (
        f'Expected dropdown "{dropdown_name}" to be hidden.'
    )


@then(
    parsers.parse(
        'dropdown "{dropdown_name}" should contain options "{first_option}", "{second_option}"'
    )
)
def dropdown_should_contain_options(driver, dropdown_name, first_option, second_option):
    page = _page(driver)
    options = page.get_dropdown_options(dropdown_name)
    assert first_option in options, f'Expected option "{first_option}" in {options}.'
    assert second_option in options, f'Expected option "{second_option}" in {options}.'


@given(parsers.parse('"{field_name}" field contains "{value}"'))
def field_contains_value(driver, field_name, value):
    page = _page(driver)
    page.set_field_value(field_name, value)


@given(parsers.parse('"{field_name}" field is empty'))
def field_is_empty(driver, field_name):
    page = _page(driver)
    page.clear_field(field_name)
    assert page.is_field_empty(field_name), f'Expected field "{field_name}" to be empty.'


@when(parsers.parse('user double clicks on "{button_name}" button'))
def user_double_clicks_button(driver, button_name):
    page = _page(driver)
    page.double_click_button(button_name)


@when(parsers.parse('user double clicks on "{button_name}" button {times:d} times'))
def user_double_clicks_button_multiple_times(driver, button_name, times):
    page = _page(driver)
    page.double_click_button(button_name, times=times)


@when(parsers.parse('user clicks on "{button_name}" button'))
def user_clicks_on_button(driver, button_name):
    page = _page(driver)
    page.click_button(button_name)


@then(parsers.parse('"{field_name}" field should contain "{expected_value}"'))
def field_should_contain(driver, field_name, expected_value):
    page = _page(driver)
    actual = page.get_field_value(field_name)
    assert actual == expected_value, (
        f'Expected field "{field_name}" value "{expected_value}", got "{actual}".'
    )


@then(parsers.parse('"{field_name}" field should be empty'))
def field_should_be_empty(driver, field_name):
    page = _page(driver)
    assert page.is_field_empty(field_name), f'Expected field "{field_name}" to be empty.'


@then(parsers.parse('"{field_name}" field should contain exactly "{expected_value}"'))
def field_should_contain_exactly(driver, field_name, expected_value):
    page = _page(driver)
    actual = page.get_field_value(field_name)
    assert actual == expected_value, (
        f'Expected exact value "{expected_value}" in "{field_name}", got "{actual}".'
    )


@given(parsers.parse('draggable element "{draggable_name}" is visible'))
def draggable_element_is_visible(driver, draggable_name):
    page = _page(driver)
    assert page.is_element_visible(draggable_name), (
        f'Expected draggable element "{draggable_name}" to be visible.'
    )


@given(parsers.parse('drop target "{target_name}" is visible'))
def drop_target_is_visible(driver, target_name):
    page = _page(driver)
    assert page.is_element_visible(target_name), (
        f'Expected drop target "{target_name}" to be visible.'
    )


@when(parsers.parse('user drags "{draggable_name}" and drops on "{target_name}"'))
def user_drags_and_drops_on_target(driver, draggable_name, target_name):
    page = _page(driver)
    page.drag_and_drop_to_target(draggable_name, target_name)


@when(
    parsers.parse(
        'user drags "{draggable_name}" and drops outside target "{target_name}"'
    )
)
def user_drags_and_drops_outside_target(driver, draggable_name, target_name):
    page = _page(driver)
    page.drag_and_drop_outside_target(draggable_name, target_name)


@then(parsers.parse('drop area should show "{expected_text}"'))
def drop_area_should_show_text(driver, expected_text):
    page = _page(driver)
    actual = page.get_drop_area_text()
    assert actual == expected_text, (
        f'Expected drop area text "{expected_text}", got "{actual}".'
    )


@then(
    parsers.parse(
        'draggable element "{draggable_name}" should be inside target "{target_name}"'
    )
)
def draggable_should_be_inside_target(driver, draggable_name, target_name):
    page = _page(driver)
    assert page.is_element_inside_target(draggable_name, target_name), (
        f'Expected "{draggable_name}" to be inside "{target_name}".'
    )
