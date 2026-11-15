#!/usr/bin/env python3
"""Tier 4 Principal Architect Fleet: Gemini 4 Carbon + Hydrogen Multi-Agent Orchestration.

Demonstrates how a Principal Architect orchestrates a Lead Planner (`gemini-4-carbon`)
that delegates parallel execution and read-only research to `gemini-4-hydrogen` workers
and adversarial security audits to `gemini-4-argon` / `gemini-4-carbon` using `agent.as_tool()`
and the 4-Part Subagent Prompt Contract:
1. `legacy_ast_researcher` (`gemini-4-hydrogen`, `low` effort — Read-only AST & SQL scan)
2. `terraform_iac_builder` (`gemini-4-hydrogen`, `high` effort — Isolated Git Worktree IaC writer)
3. `zero_trust_security_critic` (`gemini-4-carbon`, `high` effort — CWE chain & FinOps verifier)
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


FLEET_SPEC: dict[str, Any] = {
    "lead_orchestrator": {
        "name": "principal_modernization_orchestrator",
        "model": "gemini-4-carbon",
        "thinking_level": "high",
        "role": "Plans milestones, enforces re-planning triggers, and keeps parent context lean (<8K tokens).",
    },
    "subagents": [
        {
            "name": "legacy_ast_researcher",
            "model": "gemini-4-hydrogen",
            "thinking_level": "low",
            "workspace_mode": "inherit (Read-Only Local Mode)",
            "contract": {
                "target_scope": "legacy-sql/ and services/core-ledger/",
                "permitted_actions": "view_file, grep_search, find_by_name only",
                "no_file_modify_guard": True,
                "output_format": "Verified Facts (with file:line links) vs. Hypotheses",
            },
        },
        {
            "name": "terraform_iac_builder",
            "model": "gemini-4-hydrogen",
            "thinking_level": "high",
            "workspace_mode": "share (Isolated Git Worktree Mode)",
            "contract": {
                "target_scope": "infra/terraform/modules/",
                "permitted_actions": "write_to_file, replace_file_content, terraform validate",
                "no_file_modify_guard": False,
                "output_format": "Validated HCL diff + terraform validate exit code",
            },
        },
        {
            "name": "zero_trust_security_critic",
            "model": "gemini-4-argon",
            "thinking_level": "high",
            "workspace_mode": "inherit (Read-Only Local Mode)",
            "contract": {
                "target_scope": "All modified .py, .tf, and .sql files",
                "permitted_actions": "Read-only CWE/OWASP & BigQuery FinOps verification",
                "no_file_modify_guard": True,
                "output_format": "Severity Table (BLOCKER/HIGH/MEDIUM) with CWE IDs",
            },
        },
    ],
}


def instantiate_nested_fleet(workspace_dir: str = ".") -> Any:
    """Builds the nested multi-agent hierarchy using google.antigravity Agent.as_tool()."""
    from google.antigravity import Agent, BudgetConfig, LocalAgentConfig

    subagent_tools = []
    for sub in FLEET_SPEC["subagents"]:
        sub_agent = Agent(
            model=sub["model"],
            system_instruction=(
                f"Role: {sub['name']}. Workspace Mode: {sub['workspace_mode']}. "
                f"Contract: {json.dumps(sub['contract'])}"
            ),
            config=LocalAgentConfig(
                workspace=workspace_dir,
                budget=BudgetConfig(max_tokens=60_000, max_cost_usd=0.35),
            ),
        )
        subagent_tools.append(
            sub_agent.as_tool(
                name=sub["name"],
                description=f"Subagent {sub['name']} ({sub['model']})",
            )
        )

    lead = FLEET_SPEC["lead_orchestrator"]
    return Agent(
        model=lead["model"],
        system_instruction=(
            "You are the Principal Modernization Orchestrator on Gemini 4 Carbon. "
            "Never read >5 raw files directly in your own context; delegate exploration "
            "to legacy_ast_researcher, IaC authoring to terraform_iac_builder, and final "
            "verification to zero_trust_security_critic. Reuse Idle subagents for follow-ups."
        ),
        tools=subagent_tools,
        config=LocalAgentConfig(
            workspace=workspace_dir,
            budget=BudgetConfig(max_tokens=200_000, max_cost_usd=2.00),
        ),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Tier 4 Nested Subagent Fleet Orchestrator")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Output the nested fleet topology and 4-part subagent contracts as JSON",
    )
    args = parser.parse_args()
    if args.dry_run:
        print(json.dumps({"status": "VALIDATED", "fleet_topology": FLEET_SPEC}, indent=2))
        return 0
    print("Run with --dry-run to inspect the nested fleet specification.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
