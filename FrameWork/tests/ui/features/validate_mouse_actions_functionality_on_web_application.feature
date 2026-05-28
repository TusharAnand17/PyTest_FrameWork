Feature: Validate mouse actions functionality on web application
  As a user of the web application
  I want to interact with UI elements using mouse actions
  So that I can access dropdown options, copy text between fields, and move elements successfully

  Background:
    Given user is on "Mouse Actions" page

  Scenario: Show dropdown options on hover
    When user hovers on "Point Me" button
    Then dropdown "Point Me options" should be visible
    And dropdown "Point Me options" should contain options "Mobiles", "Laptops"

  Scenario: Hide dropdown options after hover is removed
    Given user hovers on "Point Me" button
    And dropdown "Point Me options" should be visible
    When user moves mouse away from "Point Me" button
    Then dropdown "Point Me options" should not be visible

  Scenario: Copy text from Field1 to Field2 on double click
    Given "Field1" field contains "Hello World!"
    And "Field2" field is empty
    When user double clicks on "Copy Text" button
    Then "Field2" field should contain "Hello World!"

  Scenario: Do not copy text on single click
    Given "Field1" field contains "Hello World!"
    And "Field2" field is empty
    When user clicks on "Copy Text" button
    Then "Field2" field should be empty

  Scenario: Complete drag and drop successfully
    Given draggable element "Drag me to my target" is visible
    And drop target "Drop here" is visible
    When user drags "Drag me to my target" and drops on "Drop here"
    Then drop area should show "Dropped!"
    And draggable element "Drag me to my target" should be inside target "Drop here"

  Scenario: Drop target remains unchanged for invalid drop
    Given draggable element "Drag me to my target" is visible
    And drop target "Drop here" is visible
    When user drags "Drag me to my target" and drops outside target "Drop here"
    Then drop area should show "Drop here"

  Scenario: Preserve exact copied text on repeated double click
    Given "Field1" field contains "Hello World!"
    And "Field2" field is empty
    When user double clicks on "Copy Text" button 2 times
    Then "Field2" field should contain exactly "Hello World!"
