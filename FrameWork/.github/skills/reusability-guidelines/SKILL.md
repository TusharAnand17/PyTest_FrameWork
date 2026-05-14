# Step Reusability Analysis Skill

## Purpose
Analyze existing and new steps to maximize reusability and avoid duplication.

## Reusability Checks
- Compare new steps with existing step patterns
- Identify parameterization opportunities
- Detect duplicate or similar step definitions
- Suggest step consolidation opportunities

## Parameterization Rules
- Convert hardcoded button names to parameters
- Convert hardcoded field names to parameters
- Convert hardcoded values to parameters
- Create generic step patterns

## Examples
❌ BAD: `@when('user clicks login button')`
✅ GOOD: `@when('user clicks on "{button_name}" button')`

❌ BAD: `@when('user enters username in username field')`
✅ GOOD: `@when('user enters "{value}" in "{field_name}" field')`