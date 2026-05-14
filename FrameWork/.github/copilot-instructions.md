# AI Automation Framework Instructions

You are working inside an enterprise-grade Python test automation framework.

---

## Technology Stack

- Python
- pytest
- pytest-bdd
- Selenium
- Requests

---

## Framework Architecture

- Page Object Model (POM)
- Fixture-based design
- Reusable automation utilities
- Config-driven execution

---

## Folder Structure
project/
├── .github/
│   ├── agents/
│   │   ├── orchestrator.agent.md
│   │   ├── requirement-analyst.agent.md
│   │   ├── feature-generator.agent.md
│   │   └── validator.agent.md
│   ├── prompts/
│   │   └── generate-feature-file.prompt.md
│   ├── context/
│   │   ├── feature-patterns.md
│   │   ├── framework-overview.md
│   │   └── naming-conventions.md
│   ├── skills/
│   │   ├── bdd-rules/SKILL.md
│   │   ├── edge-case-generation/SKILL.md
│   │   ├── gherkin-best-practices/SKILL.md
│   │   ├── repository-search-rules/SKILL.md
│   │   ├── reusability-guidelines/SKILL.md
│   │   └── scenario-design/SKILL.md
│   └── copilot-instructions.md
├── docs/
│   └── bdd/
│       ├── analysis/
│       │   └── <feature_name>_analysis.md
│       ├── validation/
│       │   └── <feature_name>_validation.md
│       └── pipeline/
│           └── <feature_name>_pipeline.md
├── pages/
├── tests/
│   ├── features/
│   │   └── <feature_name>.feature
│   └── step_defs/
├── fixtures/
├── core/
├── api/
└── config/




---

## Agent Definitions

### Orchestrator Agent
- File: .github/agents/orchestrator.agent.md
- Role: Run full pipeline automatically
- Input: User story + Acceptance criteria only
- Invoke: Always use this as entry point

### Requirement Analyst Agent
- File: .github/agents/requirement-analyst.agent.md
- Role: Analyze user story and save analysis file
- Input: Received from Orchestrator
- Saves to: docs/bdd/analysis/<feature_name>_analysis.md

### Feature Generator Agent
- File: .github/agents/feature-generator.agent.md
- Role: Read analysis file and generate feature file
- Input: Exact analysis file path from Orchestrator
- Reads from: docs/bdd/analysis/<feature_name>_analysis.md
- Saves to: tests/ui/features/<feature_name>.feature
- Uses: .github/prompts/generate-feature-file.prompt.md

### Validator Agent
- File: .github/agents/validator.agent.md
- Role: Validate feature file and save report
- Input: Exact feature file path from Orchestrator
- Reads from: tests/ui/features/<feature_name>.feature
- Saves to: docs/bdd/validation/<feature_name>_validation.md

---

## Agent Pipeline
YOU PROVIDE User Story + Acceptance Criteria │ ▼ @orchestrator │ ├─ Extracts feature_name ├─ Builds all file paths │ ▼ requirement-analyst │ ├─ Analyzes user story ├─ Saves analysis file ├─ Returns exact path │ ▼ feature-generator │ ├─ Reads analysis file ├─ Loads prompt as guide ├─ Generates feature file ├─ Returns exact path │ ▼ validator │ ├─ Reads feature file ├─ Validates all rules ├─ Fixes issues ├─ Saves validation report ├─ Returns verdict │ ▼ orchestrator │ └─ Saves pipeline log Shows final summary

---

## File Path Conventions
Given feature_name = user_login

Analysis : docs/bdd/analysis/user_login_analysis.md Feature : tests/ui/features/user_login.feature Validation : docs/bdd/validation/user_login_validation.md Pipeline : docs/bdd/pipeline/user_login_pipeline.md

---

## BDD Standards

- Use business-readable language
- Avoid implementation details
- Avoid Selenium-specific wording
- Prefer reusable step wording
- Use Scenario Outline for datasets
- Use Background for common setup

---

## Step Reusability Rules
✅ GOOD: When user clicks on "{button}" button 
✅ GOOD: When user enters "{value}" in "{field}" field

❌ BAD: When user clicks login button 
❌ BAD: When user enters username in username textbox

---

## Naming Conventions
Feature files : snake_case.feature 
Step definitions : snake_case_steps.py 
Page objects : Page.py 
Analysis files : <feature_name>_analysis.md 
Validation files : <feature_name>_validation.md 
Pipeline files : <feature_name>_pipeline.md


---

## Mandatory Rules

- Always use Orchestrator as entry point
- Always derive feature_name from user story
- Always pass exact file paths between agents
- Never let agents search for files
- Never output only to chat
- Always save all outputs to files
- Always confirm file saved after each phase
- Search repository before generating new steps
- Reuse existing feature patterns
- Avoid duplicate scenarios
- Avoid hardcoded values
- Follow DRY principle

---