# Prompt: GitHub Open Issue Triage

Purpose: Choose one actionable open issue for automated fix + PR.

## Inputs
- owner
- repo
- branch (must be copilot-branch)

## Process
1. List open issues in owner/repo.
2. Rank by actionability:
   - clear expected vs actual behavior
   - reproducible steps present
   - bounded code impact
   - not blocked by external systems
3. Skip issue if:
   - duplicate/invalid/wontfix/blocked labels
   - missing reproducible details
4. Return exactly one issue.

## Output Contract
- issue_number
- issue_title
- issue_url
- labels
- summary
- acceptance_criteria_inferred
- likely_files
- confidence (HIGH/MEDIUM/LOW)
- status (SUCCESS/FAILED)
- blockers (if any)
