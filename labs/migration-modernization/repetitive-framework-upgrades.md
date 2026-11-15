# 🏭 Lab M2: Fleet-Scale SDK & Python 3.12 Upgrades

**Difficulty**: 🟡 Intermediate | **Duration**: 45 Minutes | **Sandbox**: [`../sandbox-apps/pulsepay-legacy-ledger/`](../sandbox-apps/pulsepay-legacy-ledger/README.md)

---

## 📖 The Monday 9:00 AM Platform Ticket Avalanche at PulsePay

PulsePay's Python runtime upgrade to **Python 3.12+** (alongside the enterprise mandate in [`GEMINI.md`](../../GEMINI.md) banning deprecated SDKs and enforcing structured UTC telemetry) just flagged **42 services** across Core Payments:
- Naive `datetime.datetime.utcnow()` calls littered across [`ledger_batch.py`](../sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py) and [`notification_service.py`](../sandbox-apps/pulsepay-legacy-ledger/notification_service.py) emit `DeprecationWarning` and produce timezone-naive datetimes with manually glued `"Z"` suffixes.
- Ad-hoc `dict[str, Any]` audit summaries lack strict typed schemas and standardized ISO-8601 timezone-aware UTC helpers.

Here is how most teams blow their weekly token quota on fleet upgrades: they open 42 chat tabs, paste slightly different prose instructions into a frontier reasoning model (`gemini-4-carbon`), and get **42 slightly incompatible date formats** (`+00:00` in one service, `Z` in another, broken tests in three).

**The Antigravity Way**: Teach the upgrade recipe **once** inside a reusable `_agents/skills/python312-utc-modernizer/SKILL.md`, then fan it out deterministically across independent modules via `/run-workflow` (`parallel()` + JSON-Schema validated verdicts) powered by `gemini-4-hydrogen`!

---

## 🧠 Recommended Brain × Squad + Tokenomics Tip

| Dimension | Recommended Selection | Why This Wins on Speed & Quota |
| :--- | :--- | :--- |
| **Skill Authoring Brain** | `gemini-4-argon` (`Medium` effort) | Drafts a crystal-clear, edge-case-proof `SKILL.md` transformation spec once. |
| **Fleet Fan-Out Workers** | `gemini-4-hydrogen` (`Low` / `Medium` effort) | `$1.50` in / `$7.50` out (`$0.075` cached) — deterministic mechanical AST/code upgrades run fast and cheap on Hydrogen. |
| **Orchestration Primitive** | `/run-workflow` (`phase()`, `parallel()`, `pipeline()`) | Independent modules do **not** need peer chat negotiation (`/swarm`). `parallel()` fans out cleanly and validates each worker's JSON-Schema receipt! |
| **💰 Tokenomics Tip** | Why **not** `/swarm` here? `/swarm` shines when workers must negotiate shared interfaces mid-flight. For uniform fleet upgrades, `/run-workflow` eliminates peer-chatter overhead and reuses the cached `SKILL.md` prefix across every worker (`95%` cache discount). |

---

## ⚡ 60-Second Quick Start

1. Scan every deprecated `utcnow()` occurrence in the PulsePay sandbox right now:
   ```bash
   grep -rn "utcnow" labs/sandbox-apps/pulsepay-legacy-ledger/
   ```
   *(You should see **3 hits** across 2 independent modules: 2 in `ledger_batch.py` and 1 in `notification_service.py`!)*
2. Preview the target workflow architecture you are about to build:
   ```text
   SKILL.md (Single Source of Truth)
      └── /run-workflow pipeline()
            ├── Phase 1: parallel() [Worker A: ledger_batch.py]  [Worker B: notification_service.py]
            └── Phase 2: Verification Gate (zero utcnow hits + unittest exit 0 + JSON Schema receipt)
   ```

---

## 🔄 Guided 5-Stage Antigravity Loop

### Stage 1: Codify the Upgrade Recipe Once (`SKILL.md`)
Instead of repeating prose rules in every prompt, create a workspace skill at `_agents/skills/python312-utc-modernizer/SKILL.md` (or ask `gemini-4-argon` to generate it within your lab branch — remember to keep lab artifacts clean when done!):

```markdown
---
name: python312-utc-modernizer
description: Upgrade deprecated Python datetime.utcnow() calls to timezone-aware datetime.now(datetime.timezone.utc) while preserving exact ISO-8601 trailing-Z wire format compatibility.
---
## Transformation Rules
1. Replace `datetime.datetime.utcnow().isoformat() + "Z"` with:
   `datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")`
2. Replace `datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")` with:
   `datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")`
3. Never alter business math, public function signatures, or wire JSON keys.
4. Run `python3 -W error::DeprecationWarning -m unittest` to prove zero deprecation warnings remain.
```

> **💡 Brain Power**: Look closely at Rule #1! `datetime.now(timezone.utc).isoformat()` returns `'2026-11-15T15:45:00.123456+00:00'`. If an eager junior prompt naively glues `+ "Z"` onto the end, downstream COBOL/Java parsers receive `'...+00:00Z'` and crash at midnight! Encoding `.replace("+00:00", "Z")` in `SKILL.md` prevents that bug across all 42 services simultaneously.

### Stage 2: Define the Deterministic `/run-workflow` Fan-Out
Create a compact workflow spec (or run via `/run-workflow`) that fans `gemini-4-hydrogen` workers across disjoint file scopes (`ledger_batch.py` and `notification_service.py`) and enforces a strict **JSON-Schema Verdict** per module:

```python
# Conceptual /run-workflow specification for deterministic fleet upgrades
UPGRADE_VERDICT_SCHEMA = {
    "type": "object",
    "required": ["module", "utcnow_removed_count", "wire_format_preserved", "status"],
    "properties": {
        "module": {"type": "string"},
        "utcnow_removed_count": {"type": "integer", "minimum": 1},
        "wire_format_preserved": {"type": "boolean", "const": True},
        "status": {"type": "string", "enum": ["PASS", "FAIL"]},
    },
    "additionalProperties": False,
}

workflow = pipeline(
    name="pulsepay-py312-utc-fleet-upgrade",
    steps=[
        parallel(
            phase(
                name="upgrade-ledger-batch",
                model="gemini-4-hydrogen",
                effort="low",
                skill="python312-utc-modernizer",
                prompt="Apply python312-utc-modernizer ONLY to labs/sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py.",
                output_schema=UPGRADE_VERDICT_SCHEMA,
            ),
            phase(
                name="upgrade-notification-service",
                model="gemini-4-hydrogen",
                effort="low",
                skill="python312-utc-modernizer",
                prompt="Apply python312-utc-modernizer ONLY to labs/sandbox-apps/pulsepay-legacy-ledger/notification_service.py.",
                output_schema=UPGRADE_VERDICT_SCHEMA,
            ),
        ),
        phase(
            name="strict-deprecation-gate",
            model="gemini-4-hydrogen",
            effort="low",
            prompt="Run python3 -W error::DeprecationWarning -m unittest discover -s labs/sandbox-apps/pulsepay-legacy-ledger -p 'test_*.py' -v and add a unit test asserting trailing 'Z' without '+00:00Z'.",
            output_schema=UPGRADE_VERDICT_SCHEMA,
        ),
    ],
)
```

### Stage 3: Concurrent Socratic Exploration While Workers Run (`/btw`)
While the parallel `gemini-4-hydrogen` workers execute their disjoint file scopes, fire `/btw` side questions without interrupting them:

- `/btw Why must parallel() workers in /run-workflow own strictly non-overlapping files (ledger_batch.py vs notification_service.py) when running in the same workspace?`
- `/btw If we also needed to migrate a legacy LLM call in pulsepay from deprecated google-generativeai to google-genai >= 2.3.0 with vertex=True, what exact rule would we add to SKILL.md?`

### Stage 4: Promote `DeprecationWarning` to a Hard Error (`/goal`)
Notice how standard `python3 -m unittest` hides `DeprecationWarning` in some configurations unless `-W error::DeprecationWarning` is passed! Run `/goal` with strict warning-as-error promotion:

```text
/goal Apply the Python 3.12 timezone-aware UTC upgrade across ledger_batch.py and notification_service.py, add test_timestamps_are_utc_iso_z() to test_settlement_flow.py, and pass with zero warnings:
python3 -W error::DeprecationWarning -m unittest discover -s labs/sandbox-apps/pulsepay-legacy-ledger -p "test_*.py" -v
```

### Stage 5: Audit the Structured Receipts
Inspect the JSON verdicts emitted by each phase (`utcnow_removed_count: 2` for `ledger_batch.py`, `utcnow_removed_count: 1` for `notification_service.py`) — ready to drop straight into a Platform Engineering compliance dashboard!

---

## 🕵️ Spot the Anti-Pattern: Why Did Team Rocket's Fleet Upgrade Fail?

Team Rocket tried to upgrade 30 services on Friday afternoon using the setup below. **Circle all 4 anti-patterns** hiding in their approach:

> *"We launched a `/swarm` of 8 `gemini-4-carbon` (`xhigh` effort) workers in the same shared working tree with the prompt: `'Update all Python files in the repo to modern Python 3.12 datetime best practices and clean up anything else that looks outdated.'` Half the workers overwrote each other's edits, two services switched timestamps from `Z` to `+00:00` breaking downstream Kafka consumers, and our weekly shared quota pool dropped by 18% in 20 minutes!"*

*(Compare your 4 catches against the Facilitator Spoiler below!)*

---

## ✅ Dual-Layer Verification Rubric

| Layer | Check | Pass Criteria |
| :--- | :--- | :--- |
| **Layer 1: Objective `/goal` Command** | `python3 -W error::DeprecationWarning -m unittest discover -s labs/sandbox-apps/pulsepay-legacy-ledger -p "test_*.py" -v && ! grep -rn "utcnow" labs/sandbox-apps/pulsepay-legacy-ledger/` | Exit code `0`; `0` `DeprecationWarning`s; `0` remaining `utcnow` occurrences; timestamps end cleanly in `"Z"` (never `"+00:00Z"`). |
| **Layer 2: Fleet Governance Artifacts** | Reusable `SKILL.md` + JSON-Schema `UPGRADE_VERDICT_SCHEMA` receipts | Disjoint worker file ownership enforced; wire format backward compatibility explicitly tested. |

---

<details>
<summary>🎓 Facilitator Ground Truth & Root-Cause Spoiler (Click to Expand)</summary>

### 1. Spot the Anti-Pattern — All 4 Catches
1. **Wrong Orchestration Primitive (`/swarm` instead of `/run-workflow` `parallel()`)**: Uniform, independent file upgrades don't need peer board chatter — deterministic `parallel()` with JSON-Schema output is cleaner, faster, and auditable.
2. **Wrong Brain × Effort (`gemini-4-carbon` at `xhigh` instead of `gemini-4-hydrogen` at `Low`)**: Paying frontier reasoning output rates (`5x` input rate on thinking tokens) for mechanical `utcnow()` replacements wastes pooled quota for zero quality benefit.
3. **Shared File Collision (No Disjoint File Scope or Git Worktree Isolation)**: Letting 8 writers edit overlapping files without strict `Target Scope` boundaries or `workspace="share"`/`"branch"` causes lost writes and merge thrash.
4. **Unbounded "Clean Up Anything Outdated" Prompt Without a `SKILL.md` Wire Contract**: Caused silent wire-format drift (`Z` → `+00:00`) because backward-compatible `.replace("+00:00", "Z")` wasn't codified in a reusable skill!

### 2. Exact Sandbox Upgrade Locations
- [`ledger_batch.py`](../sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py) `parse_settlement_line()`:
  `datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")`
- [`ledger_batch.py`](../sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py) `summarize_batch()`:
  `datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")`
- [`notification_service.py`](../sandbox-apps/pulsepay-legacy-ledger/notification_service.py) `build_webhook_payload()`:
  `datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")`

</details>
