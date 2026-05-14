# Generate Step Definitions Prompt

## Objective
Generate function-based step definitions that follow existing codebase patterns exactly.

## Input Analysis
1. Parse Gherkin steps from feature file
2. Analyze existing step definition patterns
3. Identify reusable vs new step requirements
4. Extract UI elements and actions

## Generation Rules
1. Follow detected naming conventions exactly
2. Use existing import patterns
3. Create parameterized steps for reusability
4. Generate page object integration points
5. Add locator placeholders with XPath > ID preference
6. Ensure function-based structure

## Output Requirements
- Complete step definition file
- Proper imports following existing patterns
- Parameterized step functions
- Page object integration
- Locator variable placeholders
- Implementation documentation