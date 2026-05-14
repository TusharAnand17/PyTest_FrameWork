Feature: Search and view books in catalog table
  As a user
  I want to search and view books from the web table
  So that I can find books based on subject, author, and price

  Background:
    Given user is viewing the books catalog table

  # ========================
  # POSITIVE SCENARIOS
  # ========================

  Scenario: View all books with required details
    When user views all books in the catalog table
    Then user should see one or more books
    And every listed book should include "Book Name", "Author", "Subject", and "Price"

  Scenario Outline: Identify books by subject with case-insensitive comparison
    Given books exist for subject "<subject>"
    When user searches books by subject "<search_term>"
    Then user should see books for subject "<subject>"

    Examples:
      | subject | search_term |
      | Science | science     |
      | Science | SCIENCE     |
      | Science | ScIeNcE     |

  Scenario Outline: Verify books written by a specific author
    Given books exist for author "<author>"
    When user searches books by author "<author>"
    Then user should see books written by "<author>"

    Examples:
      | author        |
      | R. K. Narayan |
      | Jane Austen   |

  Scenario: Identify books whose price is greater than 1000
    When user filters books with price greater than "1000"
    Then user should see only books with price greater than "1000"

  Scenario: Verify total number of books available
    When user checks total number of books in the table
    Then displayed total should match the number of listed books

  # ========================
  # NEGATIVE SCENARIOS
  # ========================

  Scenario Outline: Show no matching records when no books match search filters
    When user searches books by "<filter_type>" using "<value>"
    Then user should see "No matching books found"
    And no books should be displayed in the results

    Examples:
      | filter_type | value               |
      | subject     | UnknownSubject      |
      | author      | Author Not In Table |

  Scenario: Show no matching records for very high price threshold
    When user filters books with price greater than "999999"
    Then user should see "No matching books found"
    And no books should be displayed in the results

  # ========================
  # EDGE CASES
  # ========================

  Scenario Outline: Subject search handles leading and trailing spaces
    Given books exist for subject "Science"
    When user searches books by subject "<search_term>"
    Then user should see books for subject "Science"

    Examples:
      | search_term |
      |  Science    |
      | Science     |

  Scenario: Price boundary excludes books priced exactly 1000
    When user filters books with price greater than "1000"
    Then user should not see books priced exactly "1000"

  Scenario: Handle empty subject input gracefully
    When user searches books by subject ""
    Then system should handle empty subject input gracefully
