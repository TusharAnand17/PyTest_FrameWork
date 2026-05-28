# Prompt: GitHub Issue Fix and PR

Purpose: Fix a selected issue on copilot-branch and create a PR.

Mode:
- dry_run=false (default): full flow including push + PR
- dry_run=true: execute fix + validation only, then return PR preview without push/PR

## Mandatory Constraints
- Target repository: TusharAnand17/PyTest_FrameWork
- Working branch: copilot-branch only
- Never touch master/main

## Process
1. Ensure branch is copilot-branch.
2. Reproduce issue with minimal test command(s).
3. Implement smallest safe fix.
4. Run validation commands.
5. Commit with issue-linked message.
6. If dry_run=false: push copilot-branch.
7. If dry_run=false: create PR from head copilot-branch to base default branch.
8. If dry_run=true: skip push/PR and return PR title/body preview.

## PR Body Template
- Issue: #<issue_number>
- Summary
- Root cause
- Changes made
- Validation (commands + result)
- Risk / rollback
- Closes #<issue_number>

## Output Contract
- issue_number
- dry_run
- changed_files
- commit_sha
- branch
- pr_number
- pr_url
- pr_preview_body
- validation_summary
- status (SUCCESS/FAILED)
- blockers (if any)
