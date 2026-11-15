# 🧪 Lab M1: Golden-File Parity Test Harness Before Rewriting Legacy Code

**Difficulty**: 🟢 Beginner | **Duration**: 35 Minutes | **Sandbox**: [`../sandbox-apps/pulsepay-legacy-ledger/`](../sandbox-apps/pulsepay-legacy-ledger/README.md)

---

## 📖 The Friday 4:45 PM Story Hook at PulsePay

The VP of Core Payments just dropped by your desk with "great news":
*"We're replacing [`ledger_batch.py`](../sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py)'s crusty 80-column COBOL slice parser (`line[24:36]`) with a clean, declarative copybook schema parser before Monday's audit!"*

There is just one tiny problem. Nobody who wrote `ledger_batch.py` in 2019 still works at PulsePay, `sample_settlements.dat` processes millions in `USD`, `EUR`, and `GBP` every night, and the existing [`test_settlement_flow.py`](../sandbox-apps/pulsepay-legacy-ledger/test_settlement_flow.py) checks only a handful of fields on 2 of the 8 records. If your shiny rewrite shifts a column slice by **one character** (`line[24:35]` instead of `line[24:36]`), every merchant payout silently shrinks by `10x`.

**Rule #1 of Agentic Legacy Modernization**: *Never ask an agent to rewrite legacy code until an agent has locked its observable behavior inside a deterministic Golden-File Parity Harness.*

---

## 🧠 Recommended Brain × Squad + Tokenomics Tip

| Dimension | Recommended Selection | Why This Wins on Speed & Quota |
| :--- | :--- | :--- |
| **Primary Brain** | `Orchestrator (Argon)` *(or `gemini-4-argon` + `gemini-4-hydrogen`)* | Intra-turn handoff: Argon designs the characterization test matrix; Hydrogen writes the test fixture and refactored parser (`-24%` quota, `+19%` faster). |
| **Discovery Helper** | `@research` *(Read-Only Subagent)* | Scans all 80-byte slice boundaries and callers without cluttering your main coding context window. |
| **Thinking Effort** | `Medium` for `/plan` → `Low` during `/goal` test execution | Thinking tokens bill at **output rates (`5x` input)**. Characterization snapshots are deterministic once planned — drop to `/effort low` for implementation! |
| **Core Slash Loop** | `/plan` → `/goal` | `/plan` lets you review edge cases before file edits; `/goal` loops autonomously until byte-for-byte golden parity exits `0`. |
| **💰 Tokenomics Tip** | Keep `sample_settlements.dat` + `AGENTS.md` stable at the top of context to capture **95% implicit cached-input discounts** (`$0.075`/1M cached on `gemini-4-hydrogen`). |

---

## ⚡ 60-Second Quick Start

1. Confirm baseline tests pass right now from the repository root:
   ```bash
   python3 -m unittest discover -s labs/sandbox-apps/pulsepay-legacy-ledger -p "test_*.py" -v
   ```
2. Kick off your read-only discovery + characterization plan in Antigravity:
   ```text
   /plan Inspect labs/sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py and sample_settlements.dat. Before we refactor any slice indices in parse_settlement_line(), design a deterministic golden-file parity test harness (deterministic clock injection + all 8 records + per-currency fee & net-cents snapshots) so any 1-byte column drift fails immediately. Do NOT modify notification_service.py.
   ```

---

## 🔄 Guided 5-Stage Antigravity Loop

### Stage 1: Delegate Read-Only Copybook Discovery (`@research`)
Ask `@research` to map every slice offset and non-deterministic side effect in `ledger_batch.py` following the 4-boundary subagent contract in [`AGENTS.md`](../../AGENTS.md):

```text
Invoke @research on Target Scope: labs/sandbox-apps/pulsepay-legacy-ledger/.
Permitted Actions: Map exact column slices in ledger_batch.py, all statuses/currencies in sample_settlements.dat, and any non-deterministic fields (timestamps, environment state) that would break golden-file snapshot comparisons.
File Mutation Policy: Do NOT modify any files.
Deliverable Contract: Cite exact line numbers and separate Verified Facts from Assumptions.
```

> **💡 Brain Power**: Look at what `@research` spots immediately in `parse_settlement_line()` and `summarize_batch()`! Both stamp `datetime.datetime.utcnow()` on every run. What happens to a naive JSON golden snapshot if `generated_at` changes every millisecond?

### Stage 2: Lock the Plan Before Writing Code (`/plan`)
Run `/plan` to produce an `Implementation Plan` artifact covering 3 files:
1. `labs/sandbox-apps/pulsepay-legacy-ledger/golden_batch_snapshot.json` — canonical frozen output for all 8 records in `sample_settlements.dat` (with `ingested_at_iso` and `generated_at` pinned via an optional `now_utc` clock parameter or normalized in the harness).
2. `labs/sandbox-apps/pulsepay-legacy-ledger/test_golden_parity.py` — asserts exact field-by-field parity across all 8 parsed `SettlementEvent` rows, all 4 statuses (`SETTLED`, `PART_REFND`, `HELD`, `CHARGEBACK`), `calculate_platform_fee_cents()` per row, and malformed width rejection (`79` chars, `81` chars, non-numeric cents).
3. `labs/sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py` — refactored from magic slice numbers (`line[24:36]`) to a declarative `COPYBOOK_SPEC` tuple table while preserving 100% backward-compatible signatures.

### Stage 3: Concurrent Socratic Exploration While Agents Work (`/btw` & `/context`)
While Hydrogen generates the snapshot fixture and refactored parser, open `/btw` so you can interrogate design trade-offs with **zero trajectory pollution**:

- `/btw Why is characterization testing different from correctness testing? If ledger_batch.py currently rounds platform fees with floor division (// 10_000), should Lab M1 change that rounding or freeze it?`
- `/btw What would happen on row STL20261115D (000000099999 EUR) if someone accidentally changed slice [24:36] to [24:35]?`
- Run `/context` afterward — verify that your `/btw` tangent added **0 tokens** to the active agent trajectory!

### Stage 4: Self-Healing Refactor Gate (`/goal`)
Switch to `/effort low` and execute the refactor inside a deterministic `/goal` loop:

```text
/goal Refactor parse_settlement_line() in labs/sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py to use a named declarative COPYBOOK_FIELDS specification instead of magic slice literals, add optional clock injection for deterministic snapshots, and verify 100% golden parity by passing:
python3 -m unittest discover -s labs/sandbox-apps/pulsepay-legacy-ledger -p "test_*.py" -v
```

### Stage 5: Sabotage Check (Prove the Harness Catches Drift!)
A safety net isn't real until you watch it catch a fall. Temporarily nudge `AMOUNT_CENTS` slice `(24, 36)` → `(24, 35)` in `ledger_batch.py`, re-run `unittest`, watch `test_golden_parity.py` scream on `STL20261115A` (`12505 != 125050`), and restore `(24, 36)` (or `/rewind` the sabotage turn!).

---

## 🧲 Prompt Magnets: Assemble the Safe Brownfield Prompt

Unscramble the 5 prompt magnets below into the **exact order** that prevents "rewrite-and-pray" regressions when modernizing legacy batch code:

- `[ A ]` *"Do NOT change rounding rules or notification_service.py; preserve exact backward-compatible function signatures."*
- `[ B ]` *"First capture a deterministic golden snapshot across all 8 rows of sample_settlements.dat by injecting a fixed clock."*
- `[ C ]` *"Verify exit code 0 via python3 -m unittest discover -s labs/sandbox-apps/pulsepay-legacy-ledger -p 'test_*.py' -v."*
- `[ D ]` *"/plan Target Scope: labs/sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py and test_golden_parity.py."*
- `[ E ]` *"Only after the parity suite is green on the untouched legacy parser, replace magic slice indices with COPYBOOK_FIELDS."*

*(Check your sequence inside the Facilitator Spoiler at the bottom!)*

---

## ✅ Dual-Layer Verification Rubric

| Layer | Check | Pass Criteria |
| :--- | :--- | :--- |
| **Layer 1: Objective `/goal` Command** | `python3 -m unittest discover -s labs/sandbox-apps/pulsepay-legacy-ledger -p "test_*.py" -v` | Exit code `0`; baseline 7 tests + new golden parity tests all pass in `< 0.05s`. |
| **Layer 2: Engineering Artifacts** | `Implementation Plan` + `golden_batch_snapshot.json` + `test_golden_parity.py` | Clock non-determinism isolated; all 8 records (`USD`, `EUR`, `GBP`) and `79`/`81`-char boundary errors asserted; `notification_service.py` untouched. |

---

<details>
<summary>🎓 Facilitator Ground Truth & Root-Cause Spoiler (Click to Expand)</summary>

### 1. Prompt Magnets Solution
**Correct Sequence**: **`[ D ]` → `[ B ]` → `[ A ]` → `[ E ]` → `[ C ]`**
1. Scope the target files and trigger `/plan` (`D`).
2. Freeze current behavior in a deterministic snapshot *before* editing implementation (`B`).
3. Bound mutation scope and preserve bug-for-bug / rounding parity (`A`).
4. Refactor magic slices to declarative `COPYBOOK_FIELDS` (`E`).
5. Gate completion on an objective CLI pass command (`C`).

### 2. Why Characterization != Bug Fixing
Notice that in [`notification_service.py`](../sandbox-apps/pulsepay-legacy-ledger/notification_service.py), `PART_REFND` receipts currently emit `USD 10.00` instead of `USD 1000.00` (the bug you will hunt in **Lab M3**). Meanwhile, `ledger_batch.py` itself parses `amount_cents=125000` and `refund_cents=25000` (`net_amount_cents=100000`) **correctly**! By scoping Lab M1 strictly to `ledger_batch.py`'s copybook parser and golden snapshot, learners prove `ledger_batch.py`'s integer cents math is solid — which becomes a critical clue when debugging `notification_service.py` in Lab M3.

### 3. Clean Declarative Copybook Pattern
```python
COPYBOOK_FIELDS: tuple[tuple[str, int, int], ...] = (
    ("record_id", 0, 12),
    ("merchant_id", 12, 24),
    ("amount_cents", 24, 36),
    ("currency", 36, 39),
    ("status", 39, 49),
    ("refund_cents", 49, 61),
    ("value_date", 61, 69),
    ("channel", 69, 80),
)
```
 Adding `assert COPYBOOK_FIELDS[-1][2] == RECORD_WIDTH` and contiguous offset assertions makes off-by-one COBOL copybook bugs structurally impossible!

</details>
