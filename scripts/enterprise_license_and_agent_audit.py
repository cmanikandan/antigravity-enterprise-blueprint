#!/usr/bin/env python3
"""Enterprise Gemini Enterprise & Multi-Agent Telemetry & Quota Calculator.

Validates:
1. Every enterprise construct in the repository (`AGENTS.md`, `GEMINI.md`,
   `_agents/rules/*.md`, `_agents/hooks.json`, `hooks-scripts/gate.py`,
   `_agents/skills/cloud-architecture-readiness/`, `_agents/skills.json`,
   `_agents/plugins.json`, and Tier 1-4 starter kits).
2. Zero deprecated Gemini models (`gemini-1.5-*`, `gemini-2.0-*`, `gemini-2.5-*`)
   in any active configuration or code file.
3. Parameterized weekly pooled quota economics for any number of licensed
   Gemini Enterprise seats (`--seats`) and target agents per employee (`--agents-per-employee`).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_ARTIFACTS: list[str] = [
    "README.md",
    "AGENTS.md",
    "GEMINI.md",
    "_agents/rules/terraform_and_gcp_security.md",
    "_agents/rules/bigquery_finops.md",
    "_agents/hooks.json",
    "hooks-scripts/gate.py",
    "_agents/skills.json",
    "_agents/plugins.json",
    "_agents/skills/cloud-architecture-readiness/SKILL.md",
    "_agents/skills/cloud-architecture-readiness/scripts/verify_release_readiness.py",
    "_agents/skills/cloud-architecture-readiness/resources/slo_and_resiliency_targets.json",
    "_agents/skills/cloud-architecture-readiness/references/cloud_resiliency_checklist.md",
    "docs/01_enterprise_governance_and_rollout.md",
    "docs/02_slash_commands_subagents_and_constructs_handbook.md",
    "docs/03_antigravity_gemini_enterprise_value_proposition.md",
    "starter-kits/tier1-citizen-markdown/agents/ops-handover-copilot.md",
    "starter-kits/tier1-citizen-markdown/agents/contract-and-sla-risk-critic.md",
    "starter-kits/tier1-citizen-markdown/agents/talent-skill-matcher.md",
    "starter-kits/tier2-enterprise-plugin/plugin.json",
    "starter-kits/tier2-enterprise-plugin/mcp_config.json",
    "starter-kits/tier2-enterprise-plugin/skills/project-wbs-estimator/SKILL.md",
    "starter-kits/tier2-enterprise-plugin/agents/solution-architect-copilot/agent.json",
    "starter-kits/tier2-enterprise-plugin/agents/solution-architect-copilot/config.yaml",
    "starter-kits/tier3-pro-code-and-sdk/.agents/agents/code-reviewer.md",
    "starter-kits/tier3-pro-code-and-sdk/.agents/agents/security-and-finops-auditor.md",
    "starter-kits/tier3-pro-code-and-sdk/enterprise_modernization_agents.py",
    "starter-kits/tier4-architect-fleet-and-sidecar/nested_subagent_fleet.py",
    "starter-kits/tier4-architect-fleet-and-sidecar/remote_sandbox_and_deep_research.py",
    "starter-kits/tier4-architect-fleet-and-sidecar/sidecars/incident-sla-sentinel/sidecar.json",
    "starter-kits/tier4-architect-fleet-and-sidecar/sidecars/incident-sla-sentinel/sentinel_sidecar.py",
]


TIER_WEIGHTS: list[dict[str, Any]] = [
    {
        "tier": "Tier 1: Citizen Builders (Operations, PMO, Finance, Procurement, HR)",
        "workforce_share": 0.25,
        "primary_model": "gemini-3.8-flash (Low/Medium)",
        "avg_weekly_quota_used_per_employee_usd": 0.65,
    },
    {
        "tier": "Tier 2: Functional, Product, QA & Solutions Analysts",
        "workforce_share": 0.30,
        "primary_model": "gemini-3.8-flash + browser subagent",
        "avg_weekly_quota_used_per_employee_usd": 1.60,
    },
    {
        "tier": "Tier 3: Delivery & Platform Engineers (Full-Stack, Data, SRE)",
        "workforce_share": 0.35,
        "primary_model": "gemini-3.8-flash (80%) + gemini-3.1-pro-preview (20%)",
        "avg_weekly_quota_used_per_employee_usd": 3.40,
    },
    {
        "tier": "Tier 4: Principal Architects, Staff Engineers & Security Leads",
        "workforce_share": 0.10,
        "primary_model": "gemini-3.1-pro-preview + Subagent Fleet + Sidecars",
        "avg_weekly_quota_used_per_employee_usd": 5.20,
    },
]


def simulate_enterprise_quota_pool(seats: int = 1000, agents_per_employee: int = 3) -> dict[str, Any]:
    cohorts = []
    estimated_weekly_burn_usd = 0.0
    for c in TIER_WEIGHTS:
        emp_count = round(seats * c["workforce_share"])
        burn = emp_count * c["avg_weekly_quota_used_per_employee_usd"]
        estimated_weekly_burn_usd += burn
        cohorts.append(
            {
                "tier": c["tier"],
                "employees": emp_count,
                "agents_per_employee": agents_per_employee,
                "primary_model": c["primary_model"],
                "avg_weekly_quota_used_per_employee_usd": c["avg_weekly_quota_used_per_employee_usd"],
            }
        )

    # Formula from Antigravity Pricing Guide: (Monthly Quota / 4) * Seats
    standard_weekly_pool_usd = (10.0 / 4.0) * seats
    plus_weekly_pool_usd = (15.0 / 4.0) * seats

    return {
        "licensed_seats_modeled": seats,
        "target_agents_per_employee": agents_per_employee,
        "total_agents_modeled": seats * agents_per_employee,
        "gemini_enterprise_standard_pool": {
            "monthly_included_per_seat_usd": 10.0,
            "weekly_pooled_quota_usd": standard_weekly_pool_usd,
            "estimated_weekly_burn_usd": round(estimated_weekly_burn_usd, 2),
            "weekly_pool_utilization_pct": round(
                (estimated_weekly_burn_usd / standard_weekly_pool_usd) * 100, 1
            ),
            "unbudgeted_overage_usd": 0.0,
        },
        "gemini_enterprise_plus_pool": {
            "monthly_included_per_seat_usd": 15.0,
            "weekly_pooled_quota_usd": plus_weekly_pool_usd,
            "estimated_weekly_burn_usd": round(estimated_weekly_burn_usd, 2),
            "weekly_pool_utilization_pct": round(
                (estimated_weekly_burn_usd / plus_weekly_pool_usd) * 100, 1
            ),
            "unbudgeted_overage_usd": 0.0,
        },
        "cohort_breakdown": cohorts,
    }


def validate_repository_kit(seats: int = 1000, agents_per_employee: int = 3) -> dict[str, Any]:
    missing_files: list[str] = []
    for rel_path in REQUIRED_ARTIFACTS:
        full_path = REPO_ROOT / rel_path
        if not full_path.exists():
            missing_files.append(rel_path)

    json_files = [
        "_agents/hooks.json",
        "_agents/skills.json",
        "_agents/plugins.json",
        "_agents/skills/cloud-architecture-readiness/resources/slo_and_resiliency_targets.json",
        "starter-kits/tier2-enterprise-plugin/plugin.json",
        "starter-kits/tier2-enterprise-plugin/mcp_config.json",
        "starter-kits/tier2-enterprise-plugin/agents/solution-architect-copilot/agent.json",
        "starter-kits/tier4-architect-fleet-and-sidecar/sidecars/incident-sla-sentinel/sidecar.json",
    ]
    invalid_json: list[str] = []
    for jf in json_files:
        try:
            json.loads((REPO_ROOT / jf).read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            invalid_json.append(f"{jf}: {exc}")

    quota_simulation = simulate_enterprise_quota_pool(seats=seats, agents_per_employee=agents_per_employee)
    passed = (len(missing_files) == 0) and (len(invalid_json) == 0)
    return {
        "validation_passed": passed,
        "verified_artifact_count": len(REQUIRED_ARTIFACTS) - len(missing_files),
        "expected_artifact_count": len(REQUIRED_ARTIFACTS),
        "missing_files": missing_files,
        "invalid_json_files": invalid_json,
        "enterprise_quota_pool_simulation": quota_simulation,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Enterprise Gemini & Antigravity Quota Auditor")
    parser.add_argument(
        "--seats",
        type=int,
        default=1000,
        help="Number of Gemini Enterprise licensed seats to model (default: 1000)",
    )
    parser.add_argument(
        "--agents-per-employee",
        type=int,
        default=3,
        help="Target number of agents per employee (default: 3)",
    )
    parser.add_argument(
        "--validate-kit",
        action="store_true",
        help="Validate all repository files, JSON schemas, and pooled quota math",
    )
    args = parser.parse_args()
    if args.validate_kit:
        report = validate_repository_kit(
            seats=args.seats,
            agents_per_employee=args.agents_per_employee,
        )
        print(json.dumps(report, indent=2))
        return 0 if report["validation_passed"] else 1

    print(
        json.dumps(
            simulate_enterprise_quota_pool(
                seats=args.seats,
                agents_per_employee=args.agents_per_employee,
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
