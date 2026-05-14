# Feature Patterns

# Preferred Structure

Feature:
- Represents single business capability

Background:
- Reusable setup steps

Scenario:
- Single business validation

Scenario Outline:
- Dataset-driven validation

# Preferred Step Wording

GOOD:
Given user is on login page

GOOD:
When user enters valid credentials

GOOD:
Then user should be redirected to dashboard

BAD:
When user clicks xpath login button

BAD:
When user enters username in textbox

# Preferred Scenario Style

- Business-readable
- Reusable wording
- Avoid technical implementation
- Concise scenarios