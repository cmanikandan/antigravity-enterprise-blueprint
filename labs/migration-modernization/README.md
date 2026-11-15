# 🛠️ Legacy Migration, Debugging & Modernization Labs (`labs/migration-modernization/`)

![Swarm vs Workflow Decision Guide](../../assets/headfirst/05_swarm_vs_workflow.jpg)

## Welcome to the Brownfield Trenches at PulsePay

Greenfield demos look magical on stage because there is no history to break. Real enterprise engineering looks like **[`pulsepay-legacy-ledger`](../sandbox-apps/pulsepay-legacy-ledger/README.md)**: an 80-column fixed-width settlement batch parser written in 2019 (`ledger_batch.py`), bolted onto a 2022 receipt notification service (`notification_service.py`), guarded by 7 green unit tests that give everyone a warm, fuzzy, *completely false* sense of security.

In this 5-lab track, you won't just "ask AI to refactor the code." You will practice choosing the **exact orchestration primitive** and **Brain × Thinking Effort** pairing that matches each brownfield hazard:

- **No safety net yet?** Lock down characterization snapshots first with `/plan` + `/goal` (**Lab M1**).
- **Same mechanical upgrade across 20 files?** Encode a `SKILL.md` once and fan out deterministically via `/run-workflow` `parallel()` (**Lab M2**).
- **Mysterious 100x payout discrepancy with green unit tests?** Pit competing hypotheses against each other with `/boost` + `/swarm`, then immunize the repo via `/learn` (**Lab M3**).
- **Hardcoded internal IPs & DSNs blocking Cloud Run?** Refactor to 12-Factor + WIF/ADC under [`_agents/hooks.json`](../../_agents/hooks.json) guardrails (**Lab M4**).
- **Monolith tangled across parser, fees, and notifications?** Run a multi-milestone decomposition with `/teamwork` in `development` integrity mode (**Lab M5**).

---

## 🗺️ Track Catalog & Brain × Squad Matrix

All 5 labs run directly against [`../sandbox-apps/pulsepay-legacy-ledger/`](../sandbox-apps/pulsepay-legacy-ledger/README.md) using standard-library Python 3 (`unittest`).

| Module | Lab Title | Difficulty | Time | Recommended Brain × Squad | Target Seam in `pulsepay-legacy-ledger` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **M1** | [**Golden-File Parity Test Harness Before Rewriting Legacy Code**](migration-test-harness.md) | 🟢 Beginner | 35 min | `Orchestrator (Argon)` (`Medium`) + `@research` + `/plan` + `/goal` | [`sample_settlements.dat`](../sandbox-apps/pulsepay-legacy-ledger/sample_settlements.dat) & [`ledger_batch.py`](../sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py) |
| **M2** | [**Fleet-Scale SDK & Python 3.12 Upgrades**](repetitive-framework-upgrades.md) | 🟡 Intermediate | 45 min | `gemini-4-hydrogen` (`Low`/`Medium`) + `SKILL.md` + `/run-workflow` `parallel()` | Naive `datetime.utcnow()` & untyped payloads across [`ledger_batch.py`](../sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py) & [`notification_service.py`](../sandbox-apps/pulsepay-legacy-ledger/notification_service.py) |
| **M3** | [**Hunting a Cross-Service Monetary Contract Bug**](cross-service-bug-investigation.md) | 🟡 Intermediate | 50 min | `/boost` (`gemini-4-carbon` `High`) + `/swarm` hypotheses + `/learn` | 100x `PART_REFND` cents-vs-dollars mismatch across [`ledger_batch.py`](../sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py) ↔ [`notification_service.py`](../sandbox-apps/pulsepay-legacy-ledger/notification_service.py) |
| **M4** | [**12-Factor Cloud Run & Zero-Secret WIF/ADC Refactor**](cloud-native-refactor.md) | 🟠 Upper-Int | 45 min | `gemini-4-argon` (`High` plan / `Low` edit) + [`_agents/hooks.json`](../../_agents/hooks.json) | `HARDCODED_SPOOL_DIR`, `LEGACY_TREASURY_DSN`, `HARDCODED_SMTP_RELAY` → typed `EnvConfig` + WIF/ADC |
| **M5** | [**Multi-Milestone Monolith Decomposition**](legacy-monolith-decomposition.md) | 🔴 Advanced | 60 min | `/teamwork` (`development` mode): `gemini-4-hydrogen` builders + `gemini-4-carbon` `@verifier` | Decomposing coupled batch parser, 25 bps treasury fee engine, and receipt notifier into isolated packages |

---

## 🧠 Sharpen Your Pencil: Pick `/swarm` vs. `/run-workflow` vs. `/teamwork`

Before jumping into Lab M1, test your instincts against the visual diagram above:

1. **Scenario A**: You need to replace deprecated `datetime.utcnow()` and legacy SDK imports across 18 microservices, and every service must emit a strict `{ "status": "PASS", "files_changed": [...] }` JSON compliance receipt.
   - *Best primitive*: **`/run-workflow` (`parallel()`)** — uniform, independent transformations where peer workers don't need to negotiate interfaces mid-flight.
2. **Scenario B**: Three agents are simultaneously building a REST endpoint, its frontend dashboard, and contract fixtures that must agree on payload field names in real time.
   - *Best primitive*: **`/swarm`** — peer `@workers` coordinating on a shared board in isolated worktrees with a `gemini-4-carbon` `@verifier`.
3. **Scenario C**: You are splitting a 9-year-old settlement monolith into three domain packages over multiple gated milestones where downstream work cannot start until upstream contracts pass verification.
   - *Best primitive*: **`/teamwork`** — Phase 1 Scoping Interview + Phase 2 Exclusive Ownership Milestones.

---

## ⚡ Quick Sandbox Check & Clean Reset

Verify your sandbox is healthy in 2 seconds from the repository root:

```bash
python3 -m unittest discover -s labs/sandbox-apps/pulsepay-legacy-ledger -p "test_*.py" -v
```

Finished a lab and want to reset the sandbox back to its original 2019/2022 brownfield state for the next lab?

```bash
git checkout -- labs/sandbox-apps/pulsepay-legacy-ledger/
```

Ready? Start with **[Lab M1: Golden-File Parity Test Harness Before Rewriting Legacy Code →](migration-test-harness.md)**
