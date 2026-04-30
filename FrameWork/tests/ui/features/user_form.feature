Feature: User Form Submission

  Scenario: Submit form with valid details
    Given user is on form page
    When user fills the form with valid data
    And user selects "monday" from days checkbox