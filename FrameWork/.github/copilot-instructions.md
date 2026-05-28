# AI Automation Framework Instructions

You are working inside an enterprise-grade Python test automation framework.

## Mission

Produce high-quality, reusable, and execution-ready UI automation assets with minimal rework.
Always prefer deterministic file outputs over chat-only responses.

## Stack And Architecture

- Language: Python
- Test framework: pytest + pytest-bdd
- UI automation: Selenium
- API support exists in repo, but story-driven orchestrator flow is UI-first
- Pattern: Page Object Model (POM)
- Design: fixture-based + config-driven + reusable utilities

## Real Project Layout

Use actual repo structure and do not assume alternate paths:

- Tests root: tests/
- UI tests: tests/ui/
- UI feature files: tests/ui/features/
- UI step definitions: tests/ui/step_defs/
- Page objects: pages/
- Core utilities: core/
- Fixtures/plugins: fixtures/
- Environment config: config/
- BDD docs: docs/bdd/

BDD documentation folders currently used:

- docs/bdd/analysis/
- docs/bdd/validation/
- docs/bdd/pipeline/
- docs/bdd/step-definitions/
- docs/bdd/page-objects/

## Active Copilot Assets

### Agents

- .github/agents/orchestrator.agent.md
- .github/agents/requirement-analyst.agent.md
- .github/agents/feature-generator.agent.md
- .github/agents/validator.agent.md
- .github/agents/stepdef-generator.agent.md
- .github/agents/stepdef-pom-orchestrator.agent.md
- .github/agents/pom-implementation.agent.md
- .github/agents/locator-strategy.agent.md
- .github/agents/code-structure.agent.md

### Prompts

- .github/prompts/generate-feature-file.prompt.md
- .github/prompts/generate-step-definitions.prompt.md
- .github/prompts/implement-page-object-methods.prompt.md

### Context

- .github/context/framework-overview.md
- .github/context/feature-patterns.md
- .github/context/naming-conventions.md

### Hooks

- .github/hooks/logger.json

The UI story validator hook is blocking and enforces:

- Minimum story length
- UI automation relevance
- Acceptance criteria presence
- API-story blocking for orchestrator flow

## Input Contract

For story-driven generation, collect and pass full Confluence page content.
User story and acceptance criteria are mandatory, and any additional relevant sections must also be included (for example: title, description, business value, expected outcome, assumptions, notes, data points, preconditions).

Minimum required extracted inputs:

- User story (mandatory)
- Acceptance criteria (mandatory)
- Additional context sections (mandatory when present)
- Full page content/raw body (mandatory pass-through)

Do not ask for feature_name or file paths when orchestration rules can derive them.
Derive feature_name from user story in snake_case.

## Path Contract

When running the requirement-to-feature pipeline, use these canonical outputs:

- Analysis: docs/bdd/analysis/<feature_name>_analysis.md
- Feature: tests/ui/features/<feature_name>.feature
- Validation: docs/bdd/validation/<feature_name>_validation.md
- Pipeline: docs/bdd/pipeline/<feature_name>_pipeline.md

For step-definition and POM pipeline:

- Step definitions: tests/ui/step_defs/<feature_name>_steps.py (or caller-provided exact path)
- Step-def analysis: docs/bdd/step-definitions/<feature_name>_stepdef_analysis.md
- POM report: docs/bdd/page-objects/<feature_name>_implementation.md

Important compatibility note:

- Existing repo also contains test_*.py naming in step definitions.
- Never rename existing files just to force conventions.
- For new files, follow caller/orchestrator exact target path first.

## Mandatory Pipeline Order

### Pipeline A: Story To Validated Feature

1. Orchestrator
2. Requirement Analyst
3. Feature Generator
4. Validator
5. Pipeline summary write

### Pipeline B: Feature To StepDefs To POM

1. StepDef to POM Orchestrator
2. Step Definition Generator
3. POM Implementation Agent

Do not skip phase ordering.
Stop immediately on hard validation failure and return precise reason.

## Authoring Standards (Gherkin)

- Use business-readable language.
- Avoid Selenium, locators, XPath, CSS, technical internals in feature text.
- Keep step wording reusable and parameterized.
- Use Background only for truly shared setup.
- Use Scenario Outline only for dataset-driven behavior.
- Cover positive, negative, edge, and boundary scenarios from analysis.
- Avoid duplicate scenarios inside file and against existing repository features.

Good reusable patterns:

- When user clicks on "{button}" button
- When user enters "{value}" in "{field}" field
- When user selects "{value}" in "{field}" field

Avoid:

- Step text with XPath/locator terms
- Hardcoded credentials or secrets
- Framework/tool implementation wording in scenarios

## Step Definition Standards

- Prefer function-based pytest-bdd step definitions.
- Reuse existing decorators and import style from tests/ui/step_defs/.
- Use generic, parameterized parser-based steps where possible.
- Route UI actions through page objects, not inline Selenium in steps.
- Keep helper factory pattern acceptable when consistent (for example _page(driver)).

Quality and reliability checks before saving:

- No undefined variables in step definitions.
- Page object class names and imports are valid.
- Scenario links are correct for bdd_features_base_dir.

## POM Implementation Standards

- Follow pages/BasePage.py interaction patterns (click, send_keys, waits).
- Prefer reusable, control-agnostic methods.
- Use explicit waits for dynamic UI interactions.
- Handle context switches explicitly for frame/window/alert flows.
- Keep methods readable, minimal, and deterministic.
- Do not leave pass/TODO in generated runnable methods.

Locator strategy:

- Prefer stable locators and shared locator composition.
- XPath can be used for complex/grouped controls.
- ID is preferred when uniquely stable.
- Avoid repeating long locator strings across multiple methods.

## Execution Awareness

Repository pytest defaults include verbose output, short tracebacks, and allure results path.
Environment and browser controls are provided via pytest options and fixtures.

Respect existing runtime options:

- --env
- --browser
- --headless

## Output Contract For Every Agent Action

Always return concise structured completion details:

- input file(s) used
- output file(s) written
- status (SUCCESS/FAILED)
- verdict (when validator runs)
- blockers/assumptions (if any)

Never return chat-only outputs when file artifacts are required.

## Hard Rules

- Always pass exact file paths between agents.
- Never ask downstream agents to discover files already known.
- Always save artifacts at each phase and confirm save path.
- Reuse repository terminology and step patterns first.
- Avoid duplicate assets and unnecessary new files.
- Follow DRY across scenarios, step definitions, and page objects.
- Keep generated docs concise but complete.

## Fast Quality Checklist (Run Before Final Response)

- Paths follow active tests/ui and docs/bdd structure.
- Feature language is business-facing and non-technical.
- Coverage includes positive, negative, edge, boundary where required.
- Step definitions compile logically and reference valid page methods.
- POM methods are implemented and reusable.
- Validation report has explicit verdict and status.
- Pipeline summary includes all created/updated files.