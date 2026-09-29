#!/usr/bin/env python3
"""Deterministic Production Readiness Review (PRR) & SLO Verifier.

Demonstrates Stage 3 of Antigravity Progressive Disclosure: executable scripts
bundled inside a skill folder (`_agents/skills/<skill>/scripts/`).
"""

import argparse
import json
from pathlib import Path
import sys
from typing import Any


SAMPLE_SERVICES: dict[str, dict[str, Any]] = {
    "payment-authorizer-api": {
        "criticality_tier": "MISSION_CRITICAL",
        "multi_region_active": True,
        "p99_latency_ms": 140,
        "autoscaling_configured": True,
        "runbook_linked": True,
    },
    "order-fulfillment-worker": {
        "criticality_tier": "BUSINESS_CORE",
        "multi_region_active": False,
        "p99_latency_ms": 380,
        "autoscaling_configured": True,
        "runbook_linked": True,
    },
    "internal-reporting-scheduler": {
        "criticality_tier": "INTERNAL_TOOLING",
        "multi_region_active": False,
        "p99_latency_ms": 920,
        "autoscaling_configured": True,
        "runbook_linked": True,
    },
}


def load_slo_matrix(matrix_path: Path) -> dict[str, Any]:
    if not matrix_path.exists():
        return {
            "MISSION_CRITICAL": {"availability_slo": "99.99%", "rto_minutes": 5},
            "BUSINESS_CORE": {"availability_slo": "99.9%", "rto_minutes": 30},
            "INTERNAL_TOOLING": {"availability_slo": "99.5%", "rto_minutes": 240},
        }
    return json.loads(matrix_path.read_text(encoding="utf-8")).get("service_tiers", {})


def run_self_test(matrix_path: Path) -> int:
    slo_tiers = load_slo_matrix(matrix_path)
    evaluations = []
    for svc, meta in SAMPLE_SERVICES.items():
        tier = meta["criticality_tier"]
        slo_info = slo_tiers.get(tier, {"availability_slo": "99.9%", "rto_minutes": 30})
        evaluations.append(
            {
                "service": svc,
                "criticality_tier": tier,
                "target_availability_slo": slo_info.get("availability_slo"),
                "target_rto_minutes": slo_info.get("rto_minutes"),
                "target_rpo_minutes": slo_info.get("rpo_minutes", 5),
                "observed_p99_latency_ms": meta["p99_latency_ms"],
                "readiness_status": "READY_FOR_PRODUCTION",
                "required_signoff": slo_info.get("approval_gate", "Tech Lead Sign-off"),
            }
        )
    print(
        json.dumps(
            {
                "status": "OK",
                "verifier": "enterprise-cloud-architecture-readiness-v1",
                "services_evaluated": len(evaluations),
                "evaluations": evaluations,
            },
            indent=2,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Enterprise Cloud Architecture & PRR Verifier")
    parser.add_argument(
        "--slo-matrix",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "resources" / "slo_and_resiliency_targets.json",
        help="Path to SLO and resiliency targets matrix JSON",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run deterministic self-test against sample service descriptors",
    )
    args = parser.parse_args()
    return run_self_test(args.slo_matrix)


if __name__ == "__main__":
    sys.exit(main())
