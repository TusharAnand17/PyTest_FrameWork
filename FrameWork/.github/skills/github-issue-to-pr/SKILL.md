---
name: github-issue-to-pr
description: "Use when: user wants automatic GitHub workflow to pick an open issue, fix code on copilot-branch, and create a pull request without touching master/main"
---

# GitHub Issue To PR Skill

## Purpose
Run an end-to-end issue remediation workflow against:
- repository: TusharAnand17/PyTest_FrameWork
- working branch: copilot-branch

## Use When
- User says: find an open issue and fix it automatically
- User asks for: auto PR from issue
- User requires: never touch master/main

## Invocation
Use agent:
- .github/agents/github-issue-fix-pr-orchestrator.agent.md

Optional input:
- issue_number
- dry_run (true|false, default: false)

## Required Assets
- .github/agents/github-issue-fix-pr-orchestrator.agent.md
- .github/agents/github-issue-triage.agent.md
- .github/agents/github-fix-pr-executor.agent.md
- .github/prompts/github-issue-triage.prompt.md
- .github/prompts/github-fix-pr.prompt.md
- .github/context/github-issue-fix-workflow.md
- .github/hooks/branch-guard.json

## Outcome
- One issue triaged
- Code fixed on copilot-branch
- PR created from copilot-branch (dry_run=false)
- PR preview returned without push/PR creation (dry_run=true)
- Pipeline summary artifact written
