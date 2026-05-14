# Gherkin Step Parsing Skill

## Purpose
Parse Gherkin steps from feature files to extract actionable information for step definition generation.

## Parsing Capabilities
- Extract step type (Given/When/Then/And/But)
- Identify parameters and variables in steps
- Categorize step intent (navigation, input, validation, wait)
- Extract UI element references (buttons, fields, dropdowns)
- Identify data patterns and table structures

## Step Categorization
- **Navigation steps**: "user navigates to", "user is on", "user opens"
- **Input steps**: "user enters", "user selects", "user clicks", "user chooses"
- **Validation steps**: "user should see", "page should display", "system should"
- **Wait steps**: "user waits", "system processes"

## Parameter Extraction
- Quoted parameters: "Login" button
- Table data parameters
- Dynamic values and variables
- Optional parameters