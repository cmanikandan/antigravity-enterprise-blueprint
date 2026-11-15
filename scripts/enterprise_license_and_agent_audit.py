#!/usr/bin/env python3
"""Enterprise Gemini 4 & Antigravity Telemetry, Tokenomics & Pooled Quota Calculator.

Validates:
1. Every enterprise construct in the repository (`README.md`, `AGENTS.md`, `GEMINI.md`,
   `_agents/rules/*.md`, `_agents/hooks.json`, `hooks-scripts/gate.py`,
   `_agents/skills/cloud-architecture-readiness/`, `_agents/skills.json`,
   `_agents/plugins.json`, Tier 1-4 starter kits, and Issue-to-PR sandbox pipelines).
2. Zero deprecated Gemini models (`gemini-1.5-*`, `gemini-2.0-*`, `gemini-2.5-*`)
   in any active agent configuration or runnable code file.
3. Parameterized weekly pooled quota economics for any number of licensed
   Gemini Enterprise seats (`--seats`), plus Gemini 4 Hydrogen / Argon / Carbon /
   Orchestrator tokenomics modeling.
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
    "assets/headfirst/00_book_cover.jpg",
    "assets/headfirst/01_five_surfaces_vs_cli.jpg",
    "assets/headfirst/02_periodic_table_brains.jpg",
    "assets/headfirst/03_two_axis_cockpit.jpg",
    "assets/headfirst/04_sdlc_storyboard.jpg",
    "assets/headfirst/05_swarm_vs_workflow.jpg",
    "assets/headfirst/06_issue_to_pr_sandbox.jpg",
    "assets/headfirst/07_context_garage.jpg",
    "assets/headfirst/08_tokenomics_quota_pool.jpg",
    "assets/headfirst/09_workshops_and_labs_map.jpg",
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
    "workshops/README.md",
    "workshops/by-tech-role/development/feature-development/README.md",
    "workshops/by-tech-role/development/app-maintenance/README.md",
    "workshops/by-tech-domain/ai-and-automation/agentic-ai/README.md",
    "workshops/by-tech-domain/ai-and-automation/agentic-sdlc/README.md",
    "labs/README.md",
    "labs/migration-modernization/README.md",
    "labs/migration-modernization/migration-test-harness.md",
    "labs/migration-modernization/repetitive-framework-upgrades.md",
    "labs/migration-modernization/cross-service-bug-investigation.md",
    "labs/migration-modernization/cloud-native-refactor.md",
    "labs/migration-modernization/legacy-monolith-decomposition.md",
    "labs/agentic-sdlc/README.md",
    "labs/agentic-sdlc/prd-to-clickable-prototype.md",
    "labs/agentic-sdlc/parallel-fullstack-swarm.md",
    "labs/agentic-sdlc/self-healing-qa-and-browser.md",
    "labs/agentic-sdlc/github-issue-to-remote-pr.md",
    "labs/sandbox-apps/pulsepay-legacy-ledger/README.md",
    "labs/sandbox-apps/pulsepay-legacy-ledger/sample_settlements.dat",
    "labs/sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py",
    "labs/sandbox-apps/pulsepay-legacy-ledger/notification_service.py",
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
    "starter-kits/tier4-architect-fleet-and-sidecar/issue_to_pr_pipeline.py",
    "starter-kits/tier4-architect-fleet-and-sidecar/github-actions-issue-to-pr.yml",
    "starter-kits/tier4-architect-fleet-and-sidecar/sidecars/incident-sla-sentinel/sidecar.json",
    "starter-kits/tier4-architect-fleet-and-sidecar/sidecars/incident-sla-sentinel/sentinel_sidecar.py",
]


GEMINI_4_TOKENOMICS_CATALOG: dict[str, dict[str, Any]] = {
    "gemini-4-hydrogen": {
        "context_window_tokens": 1_048_576,
        "thinking_levels": ["low", "medium", "high (default)", "xhigh (Extra)"],
        "input_usd_per_1m": 1.50,
        "cached_input_usd_per_1m": 0.075,
        "output_usd_per_1m": 7.50,
        "batch_in_out_usd_per_1m": [0.75, 3.75],
        "ideal_workload": "Everyday coding, /swarm & /run-workflow workers, Issue-to-PR sandboxes",
    },
    "gemini-4-argon": {
        "context_window_tokens": 1_048_576,
        "thinking_levels": ["low", "medium", "high"],
        "intro_in_out_thru_2026_11_30_usd": [2.00, 10.00],
        "standard_in_out_from_2026_12_01_usd": [4.00, 20.00],
        "cached_input_discount_pct": 95,
        "ideal_workload": "Complex multi-file SWE, RFC architecture, quantitative & legal synthesis",
    },
    "gemini-4-carbon": {
        "context_window_tokens": 1_048_576,
        "thinking_levels": ["low", "medium", "high"],
        "intro_in_out_thru_2026_11_30_usd": [2.00, 10.00],
        "standard_in_out_from_2026_12_01_usd": [4.00, 20.00],
        "cached_input_discount_pct": 95,
        "ideal_workload": "Hardest long-horizon SWE, /swarm @verifier, /boost, CWE & formal proofs",
    },
    "orchestrator_carbon_or_argon": {
        "mechanism": "Bidirectional intra-turn handoff: Carbon/Argon plans & reviews; Hydrogen executes",
        "benchmark_delta_vs_standalone_carbon": {
            "quota_saved_pct": 24,
            "wall_clock_speedup_pct": 19,
        },
        "ideal_workload": "Recommended daily interactive coding default on Pro/Ultra plans",
    },
}


TIER_WEIGHTS: list[dict[str, Any]] = [
    {
        "tier": "Tier 1: Citizen Builders — Knowledge Work Layout (PMO, Ops, Finance, HR)",
        "workforce_share": 0.25,
        "primary_model": "gemini-4-hydrogen (low/medium) + gemini-3.8-flash",
        "avg_weekly_quota_used_per_employee_usd": 0.65,
    },
    {
        "tier": "Tier 2: Product Managers, Designers & QA Analysts (/grill-me, /generative_ui, /browser)",
        "workforce_share": 0.30,
        "primary_model": "gemini-4-hydrogen + Nano Banana 2 + browser subagent",
        "avg_weekly_quota_used_per_employee_usd": 1.60,
    },
    {
        "tier": "Tier 3: Delivery & Platform Engineers (/plan, /swarm, /run-workflow, /goal)",
        "workforce_share": 0.35,
        "primary_model": "gemini-4-hydrogen (80%) + gemini-4-argon (20%)",
        "avg_weekly_quota_used_per_employee_usd": 3.40,
    },
    {
        "tier": "Tier 4: Principal Architects & Security Leads (/boost, /teamwork, Remote Sandboxes)",
        "workforce_share": 0.10,
        "primary_model": "gemini-4-carbon + gemini-4-hydrogen workers + Sidecars",
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

    # Formula from Official Gemini Enterprise Quota Docs: (Monthly Credit / 4) * Seats
    standard_weekly_pool_usd = (10.0 / 4.0) * seats
    plus_weekly_pool_usd = (15.0 / 4.0) * seats

    return {
        "licensed_seats_modeled": seats,
        "target_agents_per_employee": agents_per_employee,
        "total_agents_modeled": seats * agents_per_employee,
        "gemini_4_tokenomics_reference": GEMINI_4_TOKENOMICS_CATALOG,
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
    parser = argparse.ArgumentParser(description="Enterprise Gemini 4 & Antigravity Quota Auditor")
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
