#!/usr/bin/env python3

import json
import re
import subprocess
import sys
from typing import Any, Dict

PROTECTED_BRANCHES = {"master", "main"}
ALLOWED_WORK_BRANCH = "copilot-branch"
REPO_SLUG = "TusharAnand17/PyTest_FrameWork"


def parse_payload(raw_input: str) -> Dict[str, Any]:
    if not raw_input.strip():
        return {}
    try:
        data = json.loads(raw_input)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def current_branch() -> str:
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def block(reason: str) -> int:
    print(json.dumps({"continue": False, "reason": reason}))
    return 0


def allow() -> int:
    print(json.dumps({"continue": True}))
    return 0


def command_mentions_protected_branch(command: str) -> bool:
    return bool(re.search(r"\b(master|main)\b", command, flags=re.IGNORECASE))


def command_mentions_allowed_branch(command: str) -> bool:
    return bool(re.search(r"\bcopilot-branch\b", command, flags=re.IGNORECASE))


def protects_pull_request_command(command: str) -> bool:
    normalized = command.lower()

    # Block PRs that explicitly use protected branches as head/base.
    if "gh pr create" in normalized:
        if re.search(r"--head\s+(master|main)\b", normalized):
            return True
        if re.search(r"--base\s+(master|main)\b", normalized):
            return True
        if "--repo" in normalized and REPO_SLUG.lower() not in normalized:
            return True

    return False


def main() -> int:
    payload = parse_payload(sys.stdin.read())
    if payload.get("hook_event_name") != "PreToolUse":
        return allow()

    tool_name = str(payload.get("tool_name", ""))
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        tool_input = {}

    # Enforce branch for terminal git operations.
    if tool_name == "run_in_terminal":
        command = str(tool_input.get("command", ""))
        lowered = command.lower()

        if "git" in lowered and command_mentions_protected_branch(command):
            return block(
                "Blocked: references to master/main are not allowed. Use only copilot-branch."
            )

        if protects_pull_request_command(command):
            return block(
                "Blocked: PR command targets protected/invalid branch or repo. Use --head copilot-branch and repo TusharAnand17/PyTest_FrameWork."
            )

        if any(x in lowered for x in ["git commit", "git push", "git merge", "git rebase", "git checkout", "git switch"]):
            branch = current_branch()
            if branch and branch in PROTECTED_BRANCHES:
                return block(
                    "Blocked: current branch is protected (master/main). Switch to copilot-branch first."
                )
            if branch and branch != ALLOWED_WORK_BRANCH and not command_mentions_allowed_branch(command):
                return block(
                    "Blocked: workflow is restricted to copilot-branch. Include/switch to copilot-branch before running git operations."
                )

    return allow()


if __name__ == "__main__":
    raise SystemExit(main())
