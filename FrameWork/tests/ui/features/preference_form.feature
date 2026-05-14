Feature: Preference form captures user preferences correctly
  As a user filling out a preference form
  I want to select my gender, preferred days, country, and favorite colors
  So that my preferences are accurately captured and stored in the system

  Background:
    Given user is on the preference form

  # ========================
  # POSITIVE SCENARIOS
  # ========================

  Scenario: Display all sections with expected defaults
    When user views the preference sections
    Then "Gender" should show radio options "Male, Female"
    And "Gender" options should be unselected by default
    And "Days" should show options "Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday"
    And "Days" options should be unselected by default
    And "Country" should display "United States"
    And "Colors" should list "Red, Blue, Green, Yellow, Red, White, Green"
    And "Colors" options should be unselected by default

  Scenario: Select one gender at a time
    When user selects "Male" in "Gender" field
    Then "Gender" should display "Male" as selected
    And "Female" in "Gender" should be unselected
    When user selects "Female" in "Gender" field
    Then "Gender" should display "Female" as selected
    And "Male" in "Gender" should be unselected

  Scenario Outline: Check and uncheck days independently
    When user checks "<day>" in "Days" options
    Then "<day>" in "Days" should be selected
    When user unchecks "<day>" in "Days" options
    Then "<day>" in "Days" should be unselected

    Examples:
      | day       |
      | Sunday    |
      | Wednesday |
      | Saturday  |

  Scenario: Change selected country
    When user opens "Country" dropdown
    And user selects "Canada" in "Country" field
    Then "Country" should display "Canada"

  Scenario: Select and deselect multiple colors
    When user opens "Colors" multi-select
    And user leaves all options unselected in "Colors"
    And user selects "Red" in "Colors" field
    And user selects "Blue" in "Colors" field
    Then "Colors" should indicate selected values "Red, Blue"
    When user deselects "Red" in "Colors" field
    Then "Colors" should indicate selected values "Blue"

  Scenario: Keep selections while interacting across sections
    Given user selects "Female" in "Gender" field
    And user checks "Monday" in "Days" options
    And user selects "India" in "Country" field
    And user selects "Green" in "Colors" field
    When user changes "Country" to "Germany"
    Then "Gender" should display "Female" as selected
    And "Monday" in "Days" should be selected
    And "Colors" should indicate selected values "Green"

  Scenario: Submit completed preferences successfully
    Given user selects "Female" in "Gender" field
    And user checks "Tuesday" in "Days" options
    And user selects "United States" in "Country" field
    And user selects "Yellow" in "Colors" field
    When user submits the preference form
    Then preferences should be captured with current selections
    And preferences should be processed and stored correctly

  # # ========================
  # # NEGATIVE SCENARIOS
  # # ========================

  # Scenario Outline: Show validation for missing required selections
  #   Given "<field>" is required in preference form
  #   And user leaves "<field>" with no selection
  #   When user submits the preference form
  #   Then user should see validation message "<message>"
  #   And form submission should be blocked

  #   Examples:
  #     | field  | message                                |
  #     | Gender | Please select at least one option.    |
  #     | Days   | Please select at least one option.    |
  #     | Colors | Please select at least one option.    |

  # # ========================
  # # EDGE CASES
  # # ========================

  Scenario: Support no-day and all-day selections
    When user leaves all options unselected in "Days"
    Then no options in "Days" should be selected
    When user selects all options in "Days"
    Then all options in "Days" should be selected

  Scenario: Scroll colors and select from deeper list positions
    When user opens "Colors" multi-select
    And user scrolls "Colors" options list
    And user selects "Green" in "Colors" field
    Then "Colors" should indicate selected values "Green"

  Scenario: Preserve latest gender after repeated changes
    When user selects "Male" in "Gender" field
    And user selects "Female" in "Gender" field
    And user selects "Male" in "Gender" field
    Then "Gender" should display "Male" as selected

  # # ========================
  # # BOUNDARY CONDITIONS
  # # ========================

  Scenario Outline: Respect minimum and maximum selection boundaries
    Given "<field>" selection boundary is "<boundary>"
    When user applies selection set "<selection_set>" in "<field>"
    Then system should accept the selection state

    Examples:
      | field  | boundary | selection_set |
      | Gender | minimum  | one_option    |
      | Days   | maximum  | all_options   |
      | Colors | maximum  | all_options   |
      | Days   | minimum  | no_options    |
