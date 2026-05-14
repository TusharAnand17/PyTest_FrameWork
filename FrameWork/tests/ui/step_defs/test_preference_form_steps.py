"""Step definitions for preference_form.feature.

These steps intentionally route through a page object and keep wording generic
for reuse across future preference-like forms.
"""

from pytest_bdd import given, parsers, scenarios, then, when

from pages.preference_form_page import PreferenceFormPage
scenarios("ui/features/preference_form.feature")

def _page(driver):
    return PreferenceFormPage(driver)


@given("user is on the preference form")
def user_is_on_preference_form(driver):
    page = _page(driver)
    page.open_preference_form()


@when("user views the preference sections")
def user_views_preference_sections(driver):
    page = _page(driver)
    page.wait_for_preference_sections()


@then(parsers.parse('"{field_name}" should show radio options "{options_csv}"'))
def field_should_show_radio_options(driver, field_name, options_csv):
    page = _page(driver)
    expected_options = [item.strip() for item in options_csv.split(",")]
    actual_options = page.get_field_options(field_name)
    assert actual_options == expected_options


@then(parsers.parse('"{field_name}" should show options "{options_csv}"'))
def field_should_show_options(driver, field_name, options_csv):
    page = _page(driver)
    expected_options = [item.strip() for item in options_csv.split(",")]
    actual_options = page.get_field_options(field_name)
    assert actual_options == expected_options


@then(parsers.parse('"{field_name}" should list "{options_csv}"'))
def field_should_list_options(driver, field_name, options_csv):
    page = _page(driver)
    expected_options = [item.strip() for item in options_csv.split(",")]
    actual_options = page.get_field_options(field_name)
    assert actual_options == expected_options


@then(parsers.parse('"{field_name}" options should be unselected by default'))
def field_options_should_be_unselected_by_default(driver, field_name):
    page = _page(driver)
    assert page.are_all_options_unselected(field_name)


@given(parsers.parse('user selects "{value}" in "{field_name}" field'))
@when(parsers.parse('user selects "{value}" in "{field_name}" field'))
def user_selects_value_in_field(driver, value, field_name):
    page = _page(driver)
    page.select_value(field_name, value)


@given(parsers.parse('user checks "{value}" in "{field_name}" options'))
@when(parsers.parse('user checks "{value}" in "{field_name}" options'))
def user_checks_option(driver, value, field_name):
    page = _page(driver)
    page.check_option(field_name, value)


@given(parsers.parse('user unchecks "{value}" in "{field_name}" options'))
@when(parsers.parse('user unchecks "{value}" in "{field_name}" options'))
def user_unchecks_option(driver, value, field_name):
    page = _page(driver)
    page.uncheck_option(field_name, value)


@then(parsers.parse('"{value}" in "{field_name}" should be selected'))
def value_in_field_should_be_selected(driver, value, field_name):
    page = _page(driver)
    assert page.is_option_selected(field_name, value)


@then(parsers.parse('"{value}" in "{field_name}" should be unselected'))
def value_in_field_should_be_unselected(driver, value, field_name):
    page = _page(driver)
    assert not page.is_option_selected(field_name, value)


@then(parsers.parse('"{field_name}" should display "{value}" as selected'))
def field_should_display_value_as_selected(driver, field_name, value):
    page = _page(driver)
    assert page.get_selected_value(field_name) == value


@then(parsers.parse('"{field_name}" should display "{value}"'))
def field_should_display_value(driver, field_name, value):
    page = _page(driver)
    assert page.get_displayed_value(field_name) == value


@when(parsers.parse('user opens "{field_name}" dropdown'))
def user_opens_dropdown(driver, field_name):
    page = _page(driver)
    page.open_dropdown(field_name)


@when(parsers.parse('user opens "{field_name}" multi-select'))
def user_opens_multi_select(driver, field_name):
    page = _page(driver)
    page.open_multi_select(field_name)


@then(parsers.parse('"{field_name}" should indicate selected values "{values_csv}"'))
def field_should_indicate_selected_values(driver, field_name, values_csv):
    page = _page(driver)
    expected_values = [item.strip() for item in values_csv.split(",")]
    assert page.get_selected_values(field_name) == expected_values


@when(parsers.parse('user deselects "{value}" in "{field_name}" field'))
def user_deselects_value_in_field(driver, value, field_name):
    page = _page(driver)
    page.deselect_value(field_name, value)


@when(parsers.parse('user changes "{field_name}" to "{value}"'))
def user_changes_field_to_value(driver, field_name, value):
    page = _page(driver)
    page.change_selection(field_name, value)


@when("user submits the preference form")
def user_submits_the_preference_form(driver):
    page = _page(driver)
    page.submit_form()


@then("preferences should be captured with current selections")
def preferences_should_be_captured(driver):
    page = _page(driver)
    assert page.preferences_captured_successfully()


@then("preferences should be processed and stored correctly")
def preferences_should_be_processed_and_stored(driver):
    page = _page(driver)
    assert page.preferences_processed_and_stored()


@given(parsers.parse('"{field_name}" is required in preference form'))
def field_is_required(driver, field_name):
    page = _page(driver)
    assert page.is_field_required(field_name)


@given(parsers.parse('user leaves "{field_name}" with no selection'))
def user_leaves_field_without_selection(driver, field_name):
    page = _page(driver)
    page.clear_selection(field_name)


@then(parsers.parse('user should see validation message "{message}"'))
def user_should_see_validation_message(driver, message):
    page = _page(driver)
    assert page.get_validation_message() == message


@then("form submission should be blocked")
def form_submission_should_be_blocked(driver):
    page = _page(driver)
    assert page.is_submission_blocked()


@when(parsers.parse('user leaves all options unselected in "{field_name}"'))
def user_leaves_all_options_unselected(driver, field_name):
    page = _page(driver)
    page.clear_all_options(field_name)


@then(parsers.parse('no options in "{field_name}" should be selected'))
def no_options_in_field_should_be_selected(driver, field_name):
    page = _page(driver)
    assert page.get_selected_values(field_name) == []


@when(parsers.parse('user selects all options in "{field_name}"'))
def user_selects_all_options_in_field(driver, field_name):
    page = _page(driver)
    page.select_all_options(field_name)


@then(parsers.parse('all options in "{field_name}" should be selected'))
def all_options_in_field_should_be_selected(driver, field_name):
    page = _page(driver)
    assert page.are_all_options_selected(field_name)


@when(parsers.parse('user scrolls "{field_name}" options list'))
def user_scrolls_options_list(driver, field_name):
    page = _page(driver)
    page.scroll_options_list(field_name)


@given(parsers.parse('"{field_name}" selection boundary is "{boundary}"'))
def field_selection_boundary_is(driver, field_name, boundary):
    page = _page(driver)
    page.set_boundary_context(field_name, boundary)


@when(parsers.parse('user applies selection set "{selection_set}" in "{field_name}"'))
def user_applies_selection_set(driver, selection_set, field_name):
    page = _page(driver)
    page.apply_selection_set(field_name, selection_set)


@then("system should accept the selection state")
def system_should_accept_the_selection_state(driver):
    page = _page(driver)
    assert page.is_selection_state_accepted()
