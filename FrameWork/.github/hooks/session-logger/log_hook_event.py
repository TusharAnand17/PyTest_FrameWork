#!/usr/bin/env python3

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def parse_input(raw_input: str):
    if not raw_input.strip():
        return {}
    try:
        return json.loads(raw_input)
    except json.JSONDecodeError as exc:
        return {
            "_raw_input": raw_input,
            "_parse_error": str(exc),
        }


def detect_event_name(payload: dict) -> str:
    for key in ("hookEventName", "eventName", "event", "hook_event_name"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return "UnknownEvent"


def main() -> int:
    payload_raw = sys.stdin.read()
    payload = parse_input(payload_raw)

    event_name = detect_event_name(payload if isinstance(payload, dict) else {})

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event_name,
        "cwd": os.getcwd(),
        "payload": payload,
    }

    log_dir = Path("logs") / "copilot"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "chat-events.log"

    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=True) + "\n")

    print(json.dumps({"continue": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
