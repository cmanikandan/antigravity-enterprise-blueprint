---
name: cloud-architecture-readiness
description: Deterministic Production Readiness Review (PRR), SLO resiliency verification, and cloud architecture audit workflow for enterprise engineering teams. Use when validating services before production cutover, auditing SLO targets, or checking multi-zone high availability.
---

# Cloud Architecture & Release Readiness Skill (Enterprise Standard)

This skill demonstrates **3-Stage Progressive Disclosure** so agents keep context overhead low (~100 tokens at startup) and only load auxiliary verification scripts, JSON SLO matrices, or architecture checklists when a Production Readiness Review (PRR) task is actively triggered.

## Stage 1: Deterministic Release Readiness & SLO Verification

Before approving a production release or architecture blueprint, run the deterministic readiness verifier in `scripts/verify_release_readiness.py`:

```bash
python3 _agents/skills/cloud-architecture-readiness/scripts/verify_release_readiness.py \
  --slo-matrix _agents/skills/cloud-architecture-readiness/resources/slo_and_resiliency_targets.json \
  --self-test
```

### Mandatory Readiness Rules
1. **Multi-Zone Resiliency Check**: Verify whether stateful and stateless services define health checks, autoscaling bounds, and retry budgets.
2. **Service Tier SLO Lookup**: Read [`resources/slo_and_resiliency_targets.json`](resources/slo_and_resiliency_targets.json) to classify the required availability, RTO/RPO, and error budget policy (`MISSION_CRITICAL` = 99.99%, `BUSINESS_CORE` = 99.9%, `INTERNAL_TOOLING` = 99.5%).
3. **Isolated Validation**: If configuration changes are required, spawn the `research` subagent or a builder subagent in `New Worktree Mode` to validate changes before touching the primary branch.

## Stage 2: Resiliency & Observability Pattern Lookup

When reviewing service configurations (e.g., circuit breakers, idempotency keys, dead-letter queues, or distributed tracing), read [`references/cloud_resiliency_checklist.md`](references/cloud_resiliency_checklist.md) for enterprise reference patterns.

## Stage 3: Production Readiness Sign-Off

Every Production Readiness Review must output a structured markdown table containing:
- **Service Name & Criticality Tier**
- **Availability SLO & Error Budget Policy**
- **RTO / RPO Targets**
- **Observability & Alerting Coverage**
- **Verification Command & Exit Code**
