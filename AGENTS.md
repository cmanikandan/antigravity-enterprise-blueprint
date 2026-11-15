# Enterprise Engineering & Multi-Agent Workspace Standards (`AGENTS.md`)

This file is automatically discovered by Google Antigravity's hierarchical directory-walk engine (from the repository root down to the active working directory, up to `100 KB`) to standardize enterprise context, security boundaries, context hygiene, and multi-agent workflows across all teams.

---

## 1. Enterprise Workspace & Security Boundaries
- **Strict Workspace Isolation**: Never read, modify, or execute files outside the active project workspace root.
- **Zero Credential Persistence**: Never commit `.env` files, Cloud Service Account JSON keys, SSH private keys, API tokens, or raw customer PII. Always authenticate using Workload Identity Federation (`BYOID / WIF`), Application Default Credentials (`AGY_ADC_AUTH=true`), or proxy-injected Managed Agent credentials.
- **Default Permission Preset**: Operate under **`Default`** (OS-sandboxed terminal execution) or **`Request Review`** on production repositories. Use **`Auto`** or **`Turbo`** mode only inside isolated Git worktrees, ephemeral Remote Agent sandboxes, or CI containers protected by deterministic lifecycle hooks ([`_agents/hooks.json`](_agents/hooks.json)).

---

## 2. Multi-Agent Orchestration & Subagent Delegation Standard
Choose the lightest coordination primitive that fits the task:
- **Focused Background Errand**: Built-in subagents (`@research`, `@browser`, `self`) or custom `.agents/agents/*.md`.
- **Deep Vertical Bug / Concurrency / Algorithm**: `/boost` (`DeepCoder` / `DeepInvestigator` + adversarial challenge rounds).
- **Parallel Multi-File Build with Peer Coordination**: `/swarm` (named `@workers` in non-overlapping scopes/worktrees + `@verifier` pinned to `gemini-4-carbon` or `gemini-4-argon` on the shared board).
- **Deterministic Fan-Out / Staged Map-Reduce**: `/run-workflow` (Python `phase()`, `parallel()`, `pipeline()` returning JSON-schema validated verdicts).
- **Multi-Day Repo Migration / Simulation**: `/teamwork` (Phase 1 scoping interview + Phase 2 milestone gates in `~/teamwork_projects/{NAME}`).

Whenever delegating to a subagent or worker, the prompt **MUST** define all 4 boundaries:
1. **Target Scope**: Exact directories, files, or modules owned.
2. **Permitted Actions**: Specific analysis, refactoring, or verification task and allowed tools.
3. **File Mutation Policy**: Explicitly state *"Do NOT modify any files"* for all discovery, architecture review, and security audit agents.
4. **Deliverable Contract**: Cite exact file paths and line numbers (`file:///path#L10-L20`), and strictly separate **Verified Facts** from **Hypotheses / Assumptions**.
5. **Warm Context Reuse**: Reuse `Idle` subagents (`send_message`) and let `/swarm` workers sleep in `Waiting` (`0` tokens) rather than respawning cold contexts.
6. **Git Worktree Isolation**: For concurrent writers, isolate each worker via `workspace="share"` or `workspace="branch"` (`New Worktree Mode`).

---

## 3. Standard Slash Command (`/`) & Context Hygiene Workflow
- **Ambiguous Requirements / PRDs**: Run `/grill-me` (or stack `/plan /grill-me`) for one-question-at-a-time alignment with `(Recommended)` options.
- **Multi-File Changes (3+ files)**: Run `/plan` to produce a reviewable `Implementation Plan` artifact before modifying code.
- **Interactive Diagrams & Clickable Prototypes**: Run `/generative_ui` to build sandboxed HTML explainers and mockups.
- **Self-Healing Build & Test Loops**: Run `/goal` with an objective pass/fail verification command.
- **Live UI & Console Verification**: Run `/browser` to validate DOM rendering, network requests, and console logs.
- **Context Engineering Discipline**: Monitor token breakdown with `/context`, ask side questions via `/btw` (zero trajectory pollution), `/rewind` or `/fork` failed experiments instead of arguing with a bloated window, and `/clear` between unrelated tasks.
- **Knowledge Capture & Scheduled Sentinels**: Run `/learn` to codify fixes into `_agents/rules/*.md` or `_agents/skills/<name>/SKILL.md`, and automate recurring checks with `/automation` (`CRON_TZ` `sidecar.json`) or `/schedule`.
