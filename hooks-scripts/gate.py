#!/usr/bin/env python3
"""Deterministic Enterprise Security, FinOps Attribution, and Definition-of-Done Gate.

Implements the Antigravity `hooks.json` stdin/stdout protojson (camelCase) contract across
all 5 lifecycle events:
  1. PreToolUse     -> Blocks destructive commands ("deny"), forces human review on prod
                       mutations ("force_ask"), and rewrites `bq query` commands via
                       "overwrite" to inject mandatory FinOps attribution labels.
  2. PostToolUse    -> Logs audit telemetry after tool completion (returns `{}`).
  3. PreInvocation  -> Injects a transient `ephemeralMessage` reminding the agent of workspace rules.
  4. PostInvocation -> Optionally controls loop continuation (`terminationBehavior`).
  5. Stop           -> Blocks premature agent exit ("decision": "continue") if git conflict
                       markers or formatting errors remain in the workspace.
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
from typing import Any, Dict

DESTRUCTIVE_PATTERNS = (
    "terraform destroy",
    "rm -rf /",
    "rm -rf ~",
    "DROP TABLE",
    "DROP DATABASE",
    "TRUNCATE TABLE",
    "gcloud projects delete",
    "gsutil rm -r",
    "gcloud storage rm --recursive",
)

FORCE_ASK_PATTERNS = (
    "terraform apply",
    "git push",
    "kubectl delete",
    "gcloud run deploy",
    "gcloud sql instances patch",
)

SENSITIVE_FILE_SUFFIXES = (
    ".pem",
    ".key",
    "id_rsa",
    "credentials.json",
    "service_account.json",
)


def handle_pre_tool(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluates PreToolUse payload and returns allow, deny, force_ask, or overwrite."""
    tool_call = payload.get("toolCall", {})
    tool_name = tool_call.get("name", "")
    args = tool_call.get("args") or tool_call.get("arguments") or {}

    # 1. Guard file mutation tools against writing sensitive key files
    if tool_name in ("write_to_file", "replace_file_content"):
        target_file = str(args.get("TargetFile", ""))
        for suffix in SENSITIVE_FILE_SUFFIXES:
            if target_file.endswith(suffix):
                return {
                    "decision": "deny",
                    "reason": (
                        f"[ENTERPRISE SECURITY GATE] Modifying sensitive credential file "
                        f"'{target_file}' is prohibited by workspace security policy."
                    ),
                }

    # 2. Guard shell command execution
    if tool_name == "run_command":
        cmd = str(args.get("CommandLine", ""))

        # 2a. Hard-block destructive commands immediately
        for pattern in DESTRUCTIVE_PATTERNS:
            if pattern.lower() in cmd.lower():
                return {
                    "decision": "deny",
                    "reason": (
                        f"[ENTERPRISE SECURITY GATE] Blocked destructive command pattern: '{pattern}'. "
                        "Explicit human execution outside the agent is required."
                    ),
                }

        # 2b. Force interactive human confirmation for production mutations
        for pattern in FORCE_ASK_PATTERNS:
            if pattern.lower() in cmd.lower():
                return {
                    "decision": "force_ask",
                    "reason": (
                        f"[ENTERPRISE CHANGE CONTROL] Command contains production mutation '{pattern}'. "
                        "Explicit human approval is required (ignoring cached permissions)."
                    ),
                }

        # 2c. Shallow Argument Overwrite: Auto-inject FinOps labels into BigQuery CLI queries
        stripped = cmd.strip()
        if stripped.startswith("bq query") and "--label" not in stripped:
            rewritten_cmd = cmd.replace(
                "bq query",
                "bq query --label=managed_by:antigravity --label=env:enterprise",
                1,
            )
            return {
                "decision": "allow",
                "reason": "Auto-injected mandatory FinOps attribution labels into bq query.",
                "overwrite": {"CommandLine": rewritten_cmd},
            }

    return {
        "decision": "allow",
        "reason": "Passed Enterprise PreToolUse security gate.",
    }


def handle_post_tool(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handles PostToolUse event and writes an audit entry if audit log path is set."""
    audit_log_path = os.environ.get("ENTERPRISE_AUDIT_LOG")
    if audit_log_path:
        entry = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "conversationId": payload.get("conversationId", "unknown"),
            "stepIdx": payload.get("stepIdx", -1),
            "error": payload.get("error", ""),
            "modelName": payload.get("modelName", "auto"),
        }
        try:
            with open(audit_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except OSError:
            pass
    return {}


def handle_pre_invocation(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Injects an ephemeral compliance reminder into the turn without polluting transcript."""
    _ = payload
    return {
        "injectSteps": [
            {
                "ephemeralMessage": (
                    "[ENTERPRISE GOVERNANCE] Follow AGENTS.md and GEMINI.md: strictly separate "
                    "verified facts from hypotheses, use Gemini 3.x models, and do not modify "
                    "files outside the workspace."
                )
            }
        ]
    }


def handle_post_invocation(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Allows normal turn completion after model response."""
    _ = payload
    return {}


def handle_stop_gate(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Deterministic Definition-of-Done gate before the agent finishes its loop."""
    termination_reason = payload.get("terminationReason", "")
    fully_idle = payload.get("fullyIdle", True)

    if termination_reason == "model_stop" and fully_idle:
        workspaces = payload.get("workspacePaths", [])
        for ws in workspaces:
            if os.path.isdir(os.path.join(ws, ".git")):
                res = subprocess.run(
                    ["git", "-C", ws, "diff", "--check"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if res.returncode != 0:
                    return {
                        "decision": "continue",
                        "reason": (
                            "[DEFINITION-OF-DONE GATE] `git diff --check` detected conflict "
                            f"markers or whitespace errors:\n{res.stdout}\n"
                            "Please clean up these issues before finishing."
                        ),
                    }

    return {"decision": "stop"}


def main() -> None:
    valid_modes = ["pre-tool", "post-tool", "pre-invocation", "post-invocation", "stop-gate"]
    parser = argparse.ArgumentParser(description="Enterprise Antigravity Lifecycle Hook Gate")
    parser.add_argument(
        "positional_mode",
        nargs="?",
        choices=valid_modes,
        help="Hook lifecycle mode (positional)",
    )
    parser.add_argument(
        "--mode",
        dest="flag_mode",
        choices=valid_modes,
        help="Hook lifecycle mode (--mode flag)",
    )
    args = parser.parse_args()
    mode = args.flag_mode or args.positional_mode
    if not mode:
        parser.error("Provide hook mode either positionally or via --mode")

    raw_stdin = sys.stdin.read().strip()
    payload: Dict[str, Any] = json.loads(raw_stdin) if raw_stdin else {}

    if mode == "pre-tool":
        response = handle_pre_tool(payload)
    elif mode == "post-tool":
        response = handle_post_tool(payload)
    elif mode == "pre-invocation":
        response = handle_pre_invocation(payload)
    elif mode == "post-invocation":
        response = handle_post_invocation(payload)
    else:
        response = handle_stop_gate(payload)

    sys.stdout.write(json.dumps(response) + "\n")


if __name__ == "__main__":
    main()
