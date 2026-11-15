# Lab S2 `[Level 300]`: Parallel Cross-Stack Feature Build with `/swarm`, `Alt+S` Board TUI & Cross-Model `Carbon` `@verifier`

> [!IMPORTANT]
> **Unofficial Guide Disclaimer**: This lab is part of an **unofficial, community-authored guide** and is not affiliated with or endorsed by Google. Always consult the **[Official Google Antigravity Documentation](https://antigravity.google/docs)** and **[Google Cloud Gemini Enterprise Documentation](https://docs.cloud.google.com/gemini/enterprise/docs/overview)** for authoritative product specifications.

**Navigation**: [← Lab S1: PRD to Prototype](prd-to-clickable-prototype.md) | [Agentic SDLC Hub](README.md) | **Next Lab**: [Lab S3: Self-Healing QA & Browser →](self-healing-qa-and-browser.md)

| Lab Metadata | Specification |
| :--- | :--- |
| **Difficulty & Track** | **`[Level 300]`** — Agentic SDLC Stage 3 (Parallel Implementation & Fan-Out) |
| **Estimated Duration** | `45 minutes` |
| **Active Personas** | **Alex** *(Full-Stack Tech Lead)* + **Sam** *(Staff Security Verifier)* |
| **Antigravity Surface** | **Antigravity App** (`Board` / `Members` / `Graph` views) & **CLI** (`Alt+S` Swarm Board + `Ctrl+O` Workflow) |
| **Optimal `(Brain × Squad)`** | `gemini-4-hydrogen (medium/high/xhigh)` `@workers` + `gemini-4-carbon (high)` `@verifier` × **`/swarm`** & **`/run-workflow`** |

---

## 🎬 Stage 1 — The PulsePay Story & Broken Status Quo

**Priya** just stamped `APPROVED!` on `implementation_plan.md` from [Lab S1](prd-to-clickable-prototype.md). Now the baton lands on **Alex** (Full-Stack Tech Lead).

Alex's pod has two distinct parallel jobs to ship **PulsePay Instant Refund Guard** before Friday's code freeze:
1. **Job A — Coupled Cross-Stack Feature Build**: Implement atomic partial-refund velocity scoring (`ledger`), extend the accounting webhook JSON schema (`webhooks`), and wire the Ops Override UI (`console`)—where changing a field name in the ledger payload immediately affects the webhook serializer and UI table!
2. **Job B — Uniform Repo-Wide Compliance Audit**: Check 12 downstream merchant adapter modules to verify zero legacy unauthenticated webhook calls remain, emitting a strict JSON compliance table.

In single-thread CLI tools, engineers try to brute-force Job A by opening three separate terminal tabs on the same folder—triggering `git` file-write collisions, burning 3x cold-start prompt tokens, and leaving nobody to verify cross-boundary security bugs. Conversely, if you use a chatty peer mesh for Job B, 12 agents waste thousands of tokens saying *"Hey guys, I checked module 7!"*

**Let's see how Antigravity v2.32 solves BOTH shapes cleanly.**

---

## 🧠 Stage 2 — Pick Your `(Brain × Squad)` Combo: `/swarm` vs. `/run-workflow`

Burn this visual distinction into your engineering instincts:

![Swarm Live Peer Collaboration vs Run-Workflow Deterministic Python Fan-Out](../../assets/visuals/05_swarm_vs_workflow.jpg)

| Decision Dimension | **`/swarm`** (`@[plugin:swarm]`) — *Live Peer Collaboration* | **`/run-workflow`** *(v2.32+)* — *Deterministic Python Fan-Out* |
| :--- | :--- | :--- |
| **Do parallel workers need to talk mid-flight?** | **YES!** `@api-worker` posts finalized JSON field names to the **Shared Append-Only Message Board** via `@ui-worker` or `@all`. | **NO! Zero peer chatter.** A readable Python script dispatches `parallel(items, fn)` across isolated workers. |
| **File Collision Protection** | Optional **isolated working copies** (Git worktrees) per `@worker`, merged cleanly by the Coordinator. | Read-only fan-out (`type_name="research"`) or strictly non-overlapping per-item file scopes. |
| **Quality & Security Gate** | Dedicated **`@verifier`** (1 per 2–4 workers) **pinned to `gemini-4-carbon`** inspecting `git diff` + running tests! | Strict **`schema={...}` JSON Schema** validation on every `agent()` return value + optional Stage 2 escalation. |
| **Idle Token Economics** | `@monitor` and any worker in **`Waiting`** state consume **`0` tokens** while parked! | Workers spin up per item, validate against JSON Schema, and exit cleanly (`Ctrl+O` live tree). |

> **🙋 There Are No Dumb Questions**
>
> **Q: *Wait—in `05_swarm_vs_workflow.jpg`, `@monitor` is literally snoring (`ZZZ — 0 Tokens!`). What is `@monitor` actually doing if it costs zero tokens?***
>
> **A:** `@monitor` stays parked in the **`Waiting`** lifecycle state—meaning zero LLM calls are made while your workers make healthy progress on the message board. The runtime only wakes `@monitor` if board heartbeats stall, two workers deadlock waiting on each other, or a loop spins without progress!
>
> **Q: *Why pin `@verifier` to `gemini-4-carbon` while keeping `@api-worker` and `@ui-worker` on `gemini-4-hydrogen`?***
>
> **A:** Two reasons—**Tokenomics** and **Cross-Model Adversarial Diversity**:
> 1. `Hydrogen` (`$1.50/1M` input, **`$0.075/1M` cached input**, plus `xhigh` surgical thinking at `$7.50/1M` output) writes code and runs test loops ~3x faster and dramatically cheaper than running four `Carbon` writers.
> 2. Having **`gemini-4-carbon`** (`#1` on `SEC-bench Pro` & `CWE-bench v1`) audit a diff written by `Hydrogen` eliminates same-model blind spots—catching subtle integer-cents overflows, BOLA/IDOR tenant spoofing, or weakened test assertions before merge!

---

## 🛠️ Stage 3 — Hands-On Execution

### Step 3.1 — Launch a Cross-Stack `/swarm` Following the 4-Part Delegation Contract

Per [`AGENTS.md`](../../AGENTS.md), every multi-agent delegation **must** define (1) **Target Scope**, (2) **Permitted Actions**, (3) **File Mutation Policy**, and (4) **Deliverable Contract**.

First, create a scratch branch if you plan to merge edits locally (`git checkout -b lab/s2-swarm-demo`), then run this copy-pasteable `/swarm` prompt in the Antigravity App or CLI:

```text
/swarm Implement the "PulsePay Instant Refund Guard" velocity & webhook v2 upgrade across isolated working copies per worker, strictly following our AGENTS.md 4-Part Delegation Contract:

1. @ledger-worker (model: gemini-4-hydrogen, effort: xhigh):
   - Target Scope: labs/sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py
   - Permitted Actions: Add evaluate_refund_guard(event, cumulative_refund_cents) enforcing integer-cents cumulative cap (refund_cents + cumulative <= amount_cents) and auto-HOLD when refund_cents >= 50000 USD-equivalent minor units. Post the exact function signature & return dict fields to @webhook-worker on the board!

2. @webhook-worker (model: gemini-4-hydrogen, effort: high):
   - Target Scope: labs/sandbox-apps/pulsepay-legacy-ledger/notification_service.py
   - Permitted Actions: Wait for @ledger-worker's contract on the board, then extend build_webhook_payload() with net_payout_cents (fixing PART_REFND gross-vs-net calculation!) and guard_status ("AUTO_APPROVED" | "HELD_FOR_OPS"). Post finalized JSON payload example to @test-worker.

3. @test-worker (model: gemini-4-hydrogen, effort: medium):
   - Target Scope: labs/sandbox-apps/pulsepay-legacy-ledger/test_settlement_flow.py
   - Permitted Actions: Add unit tests covering <50000 auto-approval, >=50000 HELD routing, 3x partial-refund overflow rejection, and PART_REFND net_payout_cents accuracy without weakening any of the 7 existing tests.

4. @verifier (PIN MODEL TO gemini-4-carbon, effort: high):
   - File Mutation Policy: Do NOT modify any production files.
   - Deliverable Contract: Run `python3 -m unittest discover -s labs/sandbox-apps/pulsepay-legacy-ledger -p "test_*.py" -v`, audit all worker git diffs for CWE-190 integer overflow, floating-point currency bugs, and weakened test assertions, and post a Verified Facts vs. Hypotheses sign-off before Coordinator merges!
```

### Step 3.2 — Drive the Live `/swarm` Cockpit (`Alt+S` CLI TUI & App Graph View)

While your swarm executes in parallel, practice steering it like a seasoned Lead Engineer:

- **In the Antigravity CLI** — Press **`Alt+S`** (or type `/swarm board`) to open the interactive Swarm Board TUI:
  | Shortcut | Live Action in `/swarm board` |
  | :--- | :--- |
  | `j` / `k` *(or `↑` / `↓`)* | Step chronologically through `@mention` contract handoffs between `@ledger-worker` and `@webhook-worker` |
  | `f` | Follow live message tail as workers post discoveries |
  | `p` | Filter board messages by participant — select **`@verifier`** to read `gemini-4-carbon`'s security diff audit! |
  | `z` | Zoom into a full message or diff payload |
  | `o` | Open the selected worker's full step-by-step tool transcript |
  | `Alt+J` → `Ctrl+K` | Jump straight to any worker awaiting sandboxed command confirmation and fast-approve |

- **In the Antigravity Desktop / Web App** — Toggle across the three Swarm tabs:
  1. **Board**: Live `@mention` stream showing contract negotiation.
  2. **Members**: Real-time model badge (`Hydrogen` vs. `Carbon`) and state (`Running` vs. `Waiting (0 tokens)`).
  3. **Graph**: Visual communication topology with a **timeline replay slider** so you can scrub backward and show your team how `@webhook-worker` adapted to `@ledger-worker`'s schema!

### Step 3.3 — Contrast with `/run-workflow` (Zero-Chatter Deterministic Python Fan-Out)

Now tackle **Job B**: auditing every Python file across PulsePay's sandbox and starter kits in parallel with **zero inter-agent chatter** and **100% JSON-Schema validated output**.

Run `/run-workflow` in Antigravity (and press **`Ctrl+O`** in the CLI to watch the generated Python `phase()` / `parallel()` tree execute live):

```text
/run-workflow Audit these 4 repository modules in parallel using read-only research agents on gemini-4-hydrogen (low effort) — Do NOT modify any files:
1. labs/sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py
2. labs/sandbox-apps/pulsepay-legacy-ledger/notification_service.py
3. starter-kits/tier3-pro-code-and-sdk/enterprise_modernization_agents.py
4. starter-kits/tier4-architect-fleet-and-sidecar/issue_to_pr_pipeline.py

Stage 1: Use parallel() + agent(..., schema=...) to return strict JSON {file_path, naive_utc_calls, hardcoded_endpoints, monetary_float_risk, risk_level}.
Stage 2: Filter only files where risk_level == "HIGH" and dispatch a single gemini-4-carbon research agent to produce remediation citations with exact line numbers.
```

You can also inspect and run our standalone Python SDK multi-worktree fleet blueprint directly in your terminal right now:

```bash
python3 starter-kits/tier4-architect-fleet-and-sidecar/nested_subagent_fleet.py --dry-run
```

---

## 🔬 Stage 4 — Verify Telemetry, Context & Guardrails

1. **Verify All Sandbox Tests Pass Cleanly**:
   ```bash
   python3 -m unittest discover -s labs/sandbox-apps/pulsepay-legacy-ledger -p "test_*.py" -v
   ```
   *(Tip: If you want to restore the original brownfield seam in `pulsepay-legacy-ledger` for Lab S3, run `git checkout -- labs/sandbox-apps/pulsepay-legacy-ledger/`.)*

2. **Check the Cross-Model Tokenomics Win**:
   Compare the quota math of Alex's **Hydrogen Workers + Carbon `@verifier`** topology vs. a naive all-Carbon swarm (using post-intro `Dec 1+` standard rates from [`GEMINI.md`](../../GEMINI.md)):
   - **Naive 4x Carbon Swarm**: 4 agents reading/editing on `Carbon` (`$4.00/1M` in, `$20.00/1M` out) ≈ **`$1.45`**.
   - **Smart Hydrogen + Carbon `@verifier` Swarm**: 3 `Hydrogen` workers (`$1.50/1M` in, **`$0.075/1M` cached**, `$7.50/1M` out) + 1 `Carbon` `@verifier` reading only the final `git diff` + `@monitor` sleeping at **`$0.00`** ≈ **`$0.44`** (**~70% quota saved** with *higher* cross-model security rigor!).

> **💥 Watch Out! Two Deadly Swarm Mistakes**
> 1. **Overlapping File Ownership Without Isolated Copies**: Never assign two concurrent `@workers` to edit `ledger_batch.py` in the same shared working tree! Give each worker non-overlapping files **and** request isolated per-worker working copies.
> 2. **Using `/swarm` for Embarrassingly Parallel Batch Jobs**: If 30 workers don't need to talk to each other mid-flight, `/swarm` board messages are pure overhead—reach for **`/run-workflow`** (`parallel()` + `schema=...`) every single time!

---

## 🎓 Stage 5 — Sharpen Your Pencil & Facilitator Ground Truth

### 🕵️ Be the Swarm Coordinator — Spot the 3 Flaws in This Prompt!

A developer on Alex's team wrote the prompt below and complained that it burned too much quota, corrupted a test file, and missed an authorization bug:

> ❌ **Broken Prompt**:
> *"`/swarm` Everybody use `gemini-4-carbon` and edit `ledger_batch.py` and `test_settlement_flow.py` together to add instant refunds fast. Fix any failing tests however you want and merge when done."*

**Write down the 3 governance & orchestration bugs hiding in those two sentences!**

<details>
<summary><b>🔑 Click to Reveal the 3 Bugs & Facilitator Ground Truth</b></summary>

1. **Bug #1 — Shared-File Collision & Missing Scope Boundaries**: Assigning *"everybody"* to edit `ledger_batch.py` and `test_settlement_flow.py` simultaneously violates [`AGENTS.md`](../../AGENTS.md) Rule #2 (*Target Scope* + *Git Worktree Isolation*), causing concurrent edits to clobber each other.
2. **Bug #2 — Quota Burn & Zero Cross-Model Diversity**: Running every worker on `gemini-4-carbon` burns `~3x` the output/thinking rate on routine coding turns while omitting a dedicated read-only `@verifier` role. Fast `gemini-4-hydrogen` workers paired with a read-only `gemini-4-carbon` `@verifier` is both cheaper and safer.
3. **Bug #3 — "Fix Failing Tests However You Want" Reward-Hacking Hole**: Without an explicit prohibition against weakening or deleting existing assertions (plus a read-only `@verifier` checking `git diff` on `test_settlement_flow.py`), an eager worker might change `assertEqual(expected, actual)` to pass a broken implementation!

</details>

---

**Next Stop: How do we test the live UI in Chromium, loop tests to 100% convergence, and enforce pure-Python security gates even in Turbo mode?**
👉 **[Continue to Lab S3 `[Level 300–400]`: Self-Healing QA, `/browser` E2E & Deterministic `hooks.json` Gates →](self-healing-qa-and-browser.md)**
