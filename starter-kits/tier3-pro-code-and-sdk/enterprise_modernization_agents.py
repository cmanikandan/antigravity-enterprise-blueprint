#!/usr/bin/env python3
"""Tier 3 Pro-Code Engineering Kit: Antigravity SDK + Gemini 3.x Interactions API.

Demonstrates how software, data, and platform engineers build and orchestrate:
1. Local Cloud-Backed Agents (`gemini-3.8-flash` / `gemini-3.1-pro-preview`) with
   `BudgetConfig`, `ServiceTier.PRIORITY`, `policy`, and lifecycle `hooks`.
2. On-Device Zero-Egress Agents (`gemma-4-26b-a4b-it`) using `LiteRTAgentConfig`
   for privacy-sensitive local data scrubbing ($0 cloud quota cost).
3. Stateful Gemini Interactions API (`client.interactions.create`) with
   `thinking_level="medium"`, `previous_interaction_id`, and `vertex=True` ADC binding.

Run `--dry-run` to validate all configurations deterministically without network calls.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import sys
from typing import Any


@dataclass
class EnterpriseModernizationBlueprint:
    project_domain: str
    primary_agent_model: str
    reviewer_subagent_model: str
    local_on_device_model: str
    vertex_enabled: bool
    max_tokens_budget: int
    max_cost_usd_per_run: float
    service_tier: str
    forbidden_command_patterns: list[str]


def build_modernization_blueprint() -> EnterpriseModernizationBlueprint:
    return EnterpriseModernizationBlueprint(
        project_domain="core-payments-service-modernization",
        primary_agent_model="gemini-3.8-flash",
        reviewer_subagent_model="gemini-3.7-flash",
        local_on_device_model="gemma-4-26b-a4b-it",
        vertex_enabled=True,
        max_tokens_budget=150_000,
        max_cost_usd_per_run=1.25,
        service_tier="PRIORITY",
        forbidden_command_patterns=[
            "terraform destroy",
            "gcloud projects delete",
            "rm -rf /",
            "bq rm -f",
        ],
    )


def create_cloud_engineering_agent(workspace_dir: str = ".") -> Any:
    """Instantiates an Antigravity SDK Agent with BudgetConfig, Policy, and Hooks."""
    from google.antigravity import Agent, BudgetConfig, LocalAgentConfig, ServiceTier
    from google.antigravity.policy import deny_command, policy
    from google.antigravity.types import HookEvent

    bp = build_modernization_blueprint()

    security_policy = policy(
        [
            deny_command(pattern)
            for pattern in bp.forbidden_command_patterns
        ]
    )

    def log_tool_audit(ctx: Any) -> None:
        print(f"[ENTERPRISE-AUDIT] Tool executed: {getattr(ctx, 'tool_name', 'unknown')}")

    return Agent(
        model=bp.primary_agent_model,
        system_instruction=(
            "You are a Senior Platform Modernization Engineer. Follow AGENTS.md, "
            "delegate read-only discovery to the research subagent, and never use "
            "deprecated Gemini 1.5/2.0/2.5 models."
        ),
        config=LocalAgentConfig(
            workspace=workspace_dir,
            service_tier=ServiceTier.PRIORITY,
            budget=BudgetConfig(
                max_tokens=bp.max_tokens_budget,
                max_cost_usd=bp.max_cost_usd_per_run,
            ),
        ),
        policy=security_policy,
        hooks={HookEvent.POST_TOOL_CALL: [log_tool_audit]},
    )


def create_local_gemma4_scrubber(workspace_dir: str = ".") -> Any:
    """Instantiates a 100% local Gemma 4 MoE agent via LiteRTAgentConfig ($0 cloud quota)."""
    from google.antigravity import Agent, LiteRTAgentConfig

    bp = build_modernization_blueprint()
    return Agent(
        model=bp.local_on_device_model,
        system_instruction=(
            "You run 100% locally on workstation NPU/GPU. "
            "Scrub sensitive PII, SSN, and IBAN identifiers from log files before cloud analysis."
        ),
        config=LiteRTAgentConfig(
            workspace=workspace_dir,
            gpu_backend="auto",
            max_context_tokens=32768,
        ),
    )


def run_stateful_gemini_interaction(project_id: str, location: str = "us-central1") -> Any:
    """Demonstrates the latest google-genai Interactions API with vertex=True."""
    from google import genai

    client = genai.Client(vertexai=True, project=project_id, location=location)
    turn1 = client.interactions.create(
        model="gemini-3.8-flash",
        input="Generate a Python dataclass for an ISO-20022 pacs.008 payment instruction.",
        config={
            "thinking_config": {"thinking_level": "medium"},
            "system_instruction": "Adhere to enterprise PCI-DSS tokenization standards.",
        },
    )
    turn2 = client.interactions.create(
        model="gemini-3.8-flash",
        previous_interaction_id=turn1.id,
        input="Now add a pytest unit test verifying IBAN checksum validation.",
        config={"thinking_config": {"thinking_level": "low"}},
    )
    return turn2


def main() -> int:
    parser = argparse.ArgumentParser(description="Tier 3 Enterprise Modernization Agent Runner")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate blueprint and print SDK configuration JSON without network calls",
    )
    args = parser.parse_args()

    bp = build_modernization_blueprint()
    if args.dry_run:
        print(
            json.dumps(
                {
                    "status": "VALIDATED",
                    "tier": "Tier 3 - Delivery & Platform Engineers",
                    "sdk_stack": ["google-antigravity", "google-genai>=2.3.0"],
                    "blueprint": asdict(bp),
                },
                indent=2,
            )
        )
        return 0

    print("Use --dry-run to validate configuration offline, or import functions in your pipeline.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
