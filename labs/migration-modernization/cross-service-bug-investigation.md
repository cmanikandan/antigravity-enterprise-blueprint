# 🕵️ Lab M3: Hunting a Cross-Service Monetary Contract Bug

**Difficulty**: 🟡 Intermediate | **Duration**: 50 Minutes | **Sandbox**: [`../sandbox-apps/pulsepay-legacy-ledger/`](../sandbox-apps/pulsepay-legacy-ledger/README.md)

---

## 📖 The 2:14 AM Merchant Escalation at PulsePay

Your PagerDuty phone buzzes with an urgent Sev-1 ticket from **Acme Outfitters (`MCH_ACME_001`)** and **Kite Mobility (`MCH_KITE_108`)**:

> *"Our overnight settlement batch processed a `$1,250.00` card batch with a `$250.00` customer partial refund. Our bank account received the right `$1,000.00` wire from Treasury, **but your merchant receipt email and accounting webhook reported `Net Payout: USD 10.00`!** Our ERP auto-booked a `$990.00` reconciliation variance and froze morning payouts!"*

You rub your eyes and run [`test_settlement_flow.py`](../sandbox-apps/pulsepay-legacy-ledger/test_settlement_flow.py). **All 7 tests pass (`OK`) in `0.003s`!** Standard settled payouts (`USD 1250.50`, `USD 4800.00`, `EUR 999.99`) and compliance holds (`GBP 7500.00`) are 100% accurate.

Why are **only** partial-refund (`PART_REFND`) receipts shrinking by **100x** while Treasury batch totals stay accurate? Time to unleash `/boost` (`DeepInvestigator`), pit competing hypotheses against each other in a read-only `/swarm`, prove the bug with a failing regression test, fix it via `/goal`, and permanently immunize PulsePay's codebase with `/learn`!

---

## 🧠 Recommended Brain × Squad + Tokenomics Tip

| Dimension | Recommended Selection | Why This Wins on Speed & Quota |
| :--- | :--- | :--- |
| **Root-Cause Investigator** | `/boost` (`DeepInvestigator` on `gemini-4-carbon`, `High` effort) | Adversarial challenge rounds excel at subtle cross-module type/unit contract mismatches where baseline tests are green. |
| **Competing Hypothesis Squad** | Read-only `/swarm` (`2 × gemini-4-hydrogen` scouts + `gemini-4-carbon` `@verifier`) | Scout A investigates fixed-width COBOL parsing & integer rounding; Scout B traces cross-service helper unit contracts (`cents` vs. `dollars`). |
| **Fix & Regression Loop** | `gemini-4-hydrogen` (`Low` effort) inside `/goal` | Once Carbon pinpoints the exact 3-line contract bug, switch down to Hydrogen (`$1.50`/`$7.50`) to write the regression test and surgical fix! |
| **Institutional Memory** | `/learn` → `_agents/rules/monetary_minor_units.md` | Ensures no future agent or engineer ever mixes float dollars and integer cents across module boundaries again. |
| **💰 Tokenomics Tip** | Spend `gemini-4-carbon` (`High` effort) **only** on the 60-second root-cause diagnosis where ambiguity is high, then drop to `gemini-4-hydrogen` (`Low` effort) for test writing and cleanup! |

---

## ⚡ 60-Second Quick Start

1. Reproduce the merchant's exact Sev-1 symptom right now in your terminal:
   ```bash
   python3 -c "import sys; sys.path.insert(0, 'labs/sandbox-apps/pulsepay-legacy-ledger'); from ledger_batch import load_settlement_batch; from notification_service import format_receipt; [print(format_receipt(e)) for e in load_settlement_batch()]"
   ```
   Look at line 3 (`STL20261115C`) and line 6 (`STL20261115F`) of the output — `USD 10.00` and `EUR 20.00`!
2. Launch `/boost` in strictly read-only investigation mode first:
   ```text
   /boost Investigate why PART_REFND records (STL20261115C and STL20261115F) in labs/sandbox-apps/pulsepay-legacy-ledger/ emit receipts and webhook payouts 100x too small (USD 10.00 instead of USD 1000.00) while summarize_batch() net_cents_by_currency is accurate and all 7 baseline tests pass. Do NOT modify any files yet. Cite exact file paths and line numbers, separating Verified Facts from Hypotheses.
   ```

---

## 🔄 Guided 5-Stage Antigravity Loop

### Stage 1: Competing Hypotheses via Read-Only `/swarm` or `/boost`
In real production incidents, single-thread debugging often latches onto the first plausible suspect (*"Maybe the 80-char COBOL slice for `REFUND_CENTS` is off by two zeros!"*). Pit two read-only scouts against each other under [`AGENTS.md`](../../AGENTS.md)'s 4-boundary contract:

- **`@scout-parser` (`ledger_batch.py` + `sample_settlements.dat`)**: Verify whether `STL20261115C` (`000000125000` gross, `000000025000` refund) parses into accurate minor units and inspect all properties on `SettlementEvent`. *Do NOT modify any files.*
- **`@scout-notifier` (`notification_service.py` + `test_settlement_flow.py`)**: Trace every call path from `SettlementEvent` → `resolve_payout_units()` → `_cents_to_major_units()` → `format_receipt()` and `build_webhook_payload()`, plus why `test_settlement_flow.py` missed it. *Do NOT modify any files.*
- **`@verifier` (`gemini-4-carbon`)**: Cross-examine both scouts' findings and deliver a Verified Root-Cause Verdict with exact line numbers.

### Stage 2: Write the Red Regression Test *Before* Touching `notification_service.py`
Never fix a Sev-1 bug without first watching a new test fail for the exact reason the customer reported! Ask Antigravity to add `test_partial_refund_receipt_and_webhook_preserve_exact_payout()` to `test_settlement_flow.py` asserting:
- `STL20261115C` (`125000` cents gross − `25000` cents refund) → `Net Payout: USD 1000.00` and webhook `"payout_amount": "1000.00"`.
- `STL20261115F` (`245000` cents gross − `45000` cents refund) → `Net Payout: EUR 2000.00` and webhook `"payout_amount": "2000.00"`.

Run `unittest` and savor the deterministic `FAIL: 'USD 10.00' != 'USD 1000.00'`!

### Stage 3: Concurrent Socratic Exploration While Agents Work (`/btw`)
While your agent executes the investigation and regression test, probe deeper architectural questions via `/btw` (zero context window bloat!):

- `/btw Look at the type annotation on resolve_payout_units(event) -> int | float in notification_service.py. How could mypy or strict integer-only minor-unit typing (NewType('Cents', int)) have caught this at compile time?`
- `/btw Is build_webhook_payload() suffering from the exact same 100x bug as format_receipt(), or is only email formatting broken?`

### Stage 4: Surgical Contract Fix via `/goal`
Switch down to `/effort low` and run `/goal` to align the cross-service contract cleanly (returning integer `event.net_amount_cents` from `resolve_payout_units(event: SettlementEvent) -> int` and tightening `_cents_to_major_units(amount_in_cents: int)`):

```text
/goal Fix the cross-service monetary unit contract in labs/sandbox-apps/pulsepay-legacy-ledger/notification_service.py so resolve_payout_units() strictly returns integer minor units (cents), keep ledger_batch.py backward-compatible, and verify all baseline + partial-refund regression tests pass via:
python3 -m unittest discover -s labs/sandbox-apps/pulsepay-legacy-ledger -p "test_*.py" -v
```

### Stage 5: Immunize the Codebase Permanently (`/learn`)
Fixing one line fixes today's outage; running `/learn` prevents next quarter's outage! Run `/learn` to codify the lesson into a concise workspace rule or skill (e.g., **Monetary Minor-Unit Boundary Rule**: *All cross-service functions exchanging currency values MUST pass `int` minor units (`*_cents`) or `Decimal` with explicit unit suffixes; union return types `int | float` on monetary helpers are prohibited*).

---

## 🕵️ Spot the Anti-Pattern: Trace the 3-Line Crime Scene

Look at these two snippets from [`ledger_batch.py`](../sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py) and [`notification_service.py`](../sandbox-apps/pulsepay-legacy-ledger/notification_service.py). **Without peeking at the spoiler**, circle the exact line where dollars masquerade as cents AND identify the type-hint smell that let it slip through code review:

```python
# In ledger_batch.py (SettlementEvent)
@property
def net_amount_cents(self) -> int:
    return self.amount_cents - self.refund_cents

@property
def net_settlement_dollars(self) -> float:
    return (self.amount_cents - self.refund_cents) / 100.0
```

```python
# In notification_service.py
def resolve_payout_units(event: SettlementEvent) -> int | float:
    if event.status in ("HELD", "CHARGEBACK"):
        return 0
    if event.status == "PART_REFND" or event.refund_cents > 0:
        return event.net_settlement_dollars
    return event.amount_cents
```

---

## ✅ Dual-Layer Verification Rubric

| Layer | Check | Pass Criteria |
| :--- | :--- | :--- |
| **Layer 1: Objective `/goal` Command** | `python3 -m unittest discover -s labs/sandbox-apps/pulsepay-legacy-ledger -p "test_*.py" -v` | Exit code `0`; `STL20261115C` asserts `USD 1000.00` and `STL20261115F` asserts `EUR 2000.00` in both `format_receipt()` and `build_webhook_payload()`. |
| **Layer 2: Prevention Artifacts** | Root-cause report (Verified Facts vs. Hypotheses) + `/learn` rule capture | `resolve_payout_units()` signature tightened to `-> int`; no `int | float` monetary union remains. |

---

<details>
<summary>🎓 Facilitator Ground Truth & Root-Cause Spoiler (Click to Expand)</summary>

### 1. Exact Root Cause (`file://` Line-by-Line Trace)
1. **Verified Fact #1 ([`ledger_batch.py`](../sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py) `SettlementEvent.net_settlement_dollars`)**: Computes `(self.amount_cents - self.refund_cents) / 100.0` — returning **major currency units (float dollars/euros)** (`1000.0` for `STL20261115C`, `2000.0` for `STL20261115F`). Meanwhile, `SettlementEvent.net_amount_cents` returns integer cents (`100000` and `200000`).
2. **Verified Fact #2 ([`notification_service.py`](../sandbox-apps/pulsepay-legacy-ledger/notification_service.py) `resolve_payout_units()`)**: Returns `event.amount_cents` (`int` cents) on normal `SETTLED` rows, **but returns `event.net_settlement_dollars` (`float` dollars) on `PART_REFND` rows!** Notice the code-review smell: `-> int | float` masked two incompatible monetary units behind a single vague word (`units`).
3. **Verified Fact #3 ([`notification_service.py`](../sandbox-apps/pulsepay-legacy-ledger/notification_service.py) `format_receipt()` & `build_webhook_payload()`)**: Both pass `raw_units` into `_cents_to_major_units(raw_units)`, dividing by `100.0` **a second time** (`1000.0 / 100.0 = 10.00`, `2000.0 / 100.0 = 20.00`)!
4. **Why Baseline Tests Missed It**: [`test_settlement_flow.py`](../sandbox-apps/pulsepay-legacy-ledger/test_settlement_flow.py) tested `format_receipt()` on `self.events[0]` (`SETTLED`) and `self.events[4]` (`HELD`), and tested `PART_REFND` **only** via `summarize_batch()` (which properly used `ev.net_amount_cents`!).

### 2. Clean 3-Line Surgical Fix in `notification_service.py`
```python
def _cents_to_major_units(amount_in_cents: int) -> float:
    """Converts integer minor units (cents) into major currency units (dollars/euros/pounds)."""
    return round(amount_in_cents / 100.0, 2)


def resolve_payout_units(event: SettlementEvent) -> int:
    """Determines the payout figure in integer minor units (cents) for a merchant receipt."""
    if event.status in ("HELD", "CHARGEBACK"):
        return 0
    if event.status == "PART_REFND" or event.refund_cents > 0:
        return event.net_amount_cents
    return event.amount_cents
```

</details>
