# GitHub Issue Fix Workflow Context

## Target Repository
- URL: https://github.com/TusharAnand17/PyTest_FrameWork
- Owner: TusharAnand17
- Repository: PyTest_FrameWork

## Branch Safety Contract
- Never checkout, commit to, merge into, or push to master/main.
- Always work on copilot-branch.
- Always open PRs from head copilot-branch.
- If base branch is unknown, discover default branch first and use it as PR base.

## Dry-Run Contract
- Use dry_run=true for safe trial execution.
- In dry-run, perform issue triage, local code fix, and validation.
- In dry-run, do not push and do not create PR.
- In dry-run output, include PR preview title/body and changed file summary.

## Issue Selection Rules
- Select open issue only.
- Prefer labels: bug, defect, regression.
- Skip issues with labels: wontfix, duplicate, invalid, blocked.
- Skip issues without actionable reproduction details.
- Prefer smallest safe change first.

## Fix Quality Rules
- Reproduce issue before changing code when possible.
- Keep edits minimal and localized.
- Do not refactor unrelated code.
- Run targeted tests first, then broader suite if needed.
- Capture evidence for PR body.

## PR Requirements
- PR title format: Fix #<issue_number>: <summary>
- PR body must include:
  - issue summary
  - root cause
  - change list
  - verification commands/results
  - risk/rollback note
  - Closes #<issue_number>
