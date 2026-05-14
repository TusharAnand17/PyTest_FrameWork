
---
mode: prompt
description: Generation guide for feature-generator agent to create pytest-bdd feature files
---

# Generate Feature File Guide

## Purpose
This prompt is used by feature-generator.agent.md
as a generation guide.
All inputs come from analysis file.
Do not ask user for anything.

---

## Step 1 - Read Analysis File

Read from exact path received:
read_from = docs/bdd/analysis/<feature_name>_analysis.md


Extract:
Actor : for Feature header 
Goal : for Feature header 
Benefit : for Feature header 
Positive Scenarios : PS-01, PS-02... 
Negative Scenarios : NS-01, NS-02... 
Edge Cases : EC-01, EC-02... 
Validations : VAL-01, VAL-02... 
Boundary Conditions : BC-01, BC-02... 
Reusable Steps : use in scenarios 
Existing Terminology: use in wording

---

## Step 2 - Search Repository
Search : tests/features/ → reusable steps 
Search : tests/step_defs/ → existing terminology 
Reuse : steps from analysis file 
Avoid : duplicate scenarios

---

## Step 3 - Generate Feature File

### Language Rules
✅ Business-readable wording 
✅ Reusable parameterized steps 
✅ Existing repository terminology

❌ No XPath or locator references 
❌ No Selenium actions 
❌ No hardcoded values 
❌ No technical details



### Examples
✅ GOOD: When user logs in with valid credentials 
❌ BAD : When user clicks login xpath

✅ GOOD: When user enters "{value}" in "{field}" field 
❌ BAD : When user enters username in username textbox

✅ GOOD: Then user should be redirected to dashboard 
❌ BAD : Then Selenium validates dashboard

✅ GOOD: When user submits the form 
❌ BAD : When user clicks submit button xpath



### Structure Rules
✅ Feature header with As a/I want/So that 
✅ Background for common setup steps 
✅ Scenario for single behavior 
✅ Scenario Outline for multiple datasets 
✅ Examples table for data-driven tests 
✅ Section comments to separate scenarios


### Coverage Rules
Must include ALL from analysis file: 
✅ All Positive Scenarios 
✅ All Negative Scenarios 
✅ All Edge Cases 
✅ All Boundary Conditions

---

## Step 4 - Output Format

Generate using this exact structure:

```gherkin
Feature: <Feature Title>
  As a <actor>
  I want to <goal>
  So that <benefit>

  Background:
    Given <common setup>

  # ========================
  # POSITIVE SCENARIOS
  # ========================

  Scenario: <PS-01 title>
    Given <precondition>
    When <action>
    Then <outcome>

  Scenario: <PS-02 title>
    Given <precondition>
    When <action>
    Then <outcome>

  # ========================
  # NEGATIVE SCENARIOS
  # ========================

  Scenario Outline: <NS title>
    Given <precondition>
    When user enters "<value>" in "<field>" field
    Then user should see "<message>"

    Examples:
      | value | field | message |
      | ...   | ...   | ...     |

  # ========================
  # EDGE CASES
  # ========================

  Scenario Outline: <EC title>
    Given <precondition>
    When user leaves "<field>" field empty
    Then user should see "<message>"

    Examples:
      | field | message |
      | ...   | ...     |

Step 5 - Save File
Save to exact path received:
save_to = tests/ui/features/<feature_name>.feature

Never output only to chat.
Always save as physical file.
Always confirm file saved.
Anti-Patterns To Avoid


❌ NEVER: When user clicks submit button xpath
❌ NEVER: Then Selenium validates dashboard
❌ NEVER: When user enters username in username textbox
❌ NEVER: Hardcoded values in steps
❌ NEVER: XPath wording
❌ NEVER: Locator references
❌ NEVER: Technical implementation details