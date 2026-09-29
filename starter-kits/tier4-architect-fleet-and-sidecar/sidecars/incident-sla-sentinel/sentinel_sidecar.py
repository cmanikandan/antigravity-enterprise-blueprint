#!/usr/bin/env python3
"""Enterprise 24x7 SRE & Operations Incident & SLA Sentinel Sidecar.

Runs continuously under `<configDir>/sidecars/incident-sla-sentinel/sidecar.json`
(`restart_policy: "always"`). Persists processed incident IDs inside
`ANTIGRAVITY_EXECUTABLE_DATA_DIR` and invokes `agentapi new-conversation`
whenever a new P1/Sev-1 incident arrives.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any


SAMPLE_INCIDENT_QUEUE: list[dict[str, Any]] = [
    {
        "incident_id": "INC-2026-88412",
        "severity": "P1",
        "service_domain": "Core-Payments-Platform",
        "summary": "Cloud Run payment-settlement latency > 2500ms after release v2026.09.2",
        "sla_minutes_remaining": 45,
    }
]


def get_data_dir() -> Path:
    env_dir = os.environ.get("ANTIGRAVITY_EXECUTABLE_DATA_DIR")
    if env_dir:
        path = Path(env_dir)
    else:
        path = Path(__file__).resolve().parent / "data"
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_agentapi_command(incident: dict[str, Any]) -> list[str]:
    model_tier = os.environ.get("INCIDENT_DEFAULT_MODEL", "flash")
    title = f"[SRE-{incident['severity']}] Auto-RCA: {incident['incident_id']} ({incident['service_domain']})"
    prompt = (
        f"/plan Perform an immediate read-only Root Cause Analysis for {incident['incident_id']}: "
        f"'{incident['summary']}'. Spawn the research subagent to inspect recent commits and "
        f"Cloud Run config diffs, and produce an emergency mitigation plan within the "
        f"{incident['sla_minutes_remaining']}-minute SLA window."
    )
    return [
        "agentapi",
        "new-conversation",
        f"--model={model_tier}",
        f"--title={title}",
        prompt,
    ]


def process_once(dry_run: bool = False) -> dict[str, Any]:
    data_dir = get_data_dir()
    state_file = data_dir / "processed_incidents.json"
    if state_file.exists():
        processed: dict[str, str] = json.loads(state_file.read_text(encoding="utf-8"))
    else:
        processed = {}

    triggered_commands: list[list[str]] = []
    for inc in SAMPLE_INCIDENT_QUEUE:
        inc_id = inc["incident_id"]
        cmd = build_agentapi_command(inc)
        triggered_commands.append(cmd)
        if not dry_run and inc_id not in processed:
            subprocess.run(cmd, check=False)
            processed[inc_id] = datetime.now(timezone.utc).isoformat()

    if not dry_run:
        state_file.write_text(json.dumps(processed, indent=2), encoding="utf-8")

    return {
        "status": "OK",
        "sidecar": "incident-sla-sentinel",
        "data_dir": str(data_dir),
        "incidents_evaluated": len(SAMPLE_INCIDENT_QUEUE),
        "agentapi_commands_prepared": triggered_commands,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Enterprise 24x7 Incident & SLA Sentinel Sidecar")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single evaluation cycle and exit (for verification/testing)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Prepare agentapi commands without invoking subprocess",
    )
    args = parser.parse_args()

    if args.once or args.dry_run:
        result = process_once(dry_run=args.dry_run or args.once)
        print(json.dumps(result, indent=2))
        return 0

    poll_seconds = int(os.environ.get("INCIDENT_POLL_INTERVAL_SECONDS", "300"))
    while True:
        process_once(dry_run=False)
        time.sleep(poll_seconds)


if __name__ == "__main__":
    sys.exit(main())
