# Enterprise Engineering & Multi-Agent Workspace Standards (`AGENTS.md`)

This file is automatically discovered by Google Antigravity's hierarchical directory-walk engine (from the repository root down to the active working directory, up to `100 KB`) to standardize enterprise context, security boundaries, and multi-agent workflows across all teams.

---

## 1. Enterprise Workspace & Security Boundaries
- **Strict Workspace Isolation**: Never read, modify, or execute files outside the active project workspace root.
- **Zero Credential Persistence**: Never commit `.env` files, Cloud Service Account JSON keys, SSH private keys, API tokens, or raw customer PII. Always authenticate using Workload Identity Federation or Application Default Credentials (`gcloud auth application-default login`).
- **Default Permission Preset**: Operate under the **`Default`** permission preset (sandboxed terminal execution with human confirmation for destructive operations). Use **`Turbo`** mode only inside isolated Git worktrees protected by deterministic lifecycle hooks ([`_agents/hooks.json`](_agents/hooks.json)).

---

## 2. Subagent Delegation & Code Quality Standard
Whenever the primary agent delegates work to a built-in subagent (`research`, `self`, `browser`) or a custom subagent (`.agents/agents/*.md`), the delegation prompt **MUST** explicitly define all 4 boundaries:
1. **Target Scope**: Exact directories, files, or modules to inspect.
2. **Permitted Actions**: Specific analysis, refactoring, or verification task and allowed tools.
3. **File Mutation Policy**: Explicitly state *"Do NOT modify any files"* for all discovery, architecture review, and security audit subagents.
4. **Deliverable Contract**:
   - Cite exact file paths, line numbers (`file:///path#L10-L20`), and runtime trigger conditions.
   - Strictly separate **Verified Facts** (confirmed directly in source code or command output) from **Hypotheses / Assumptions**.
5. **Reuse `Idle` Subagents**: When a subagent completes its task and enters the `Idle` state, send follow-up questions to that existing `Idle` subagent via `send_message` rather than spawning a duplicate subagent.
6. **Git Worktree Isolation**: For parallel multi-file modifications, use **New Worktree Mode** (`workspace="share"` or `workspace="branch"`) and verify diffs before merging.

---

## 3. Standard Slash Command (`/`) Engineering Workflow
- **Ambiguous Requirements / Specs**: Run `/grill-me` first so the agent interviews you on edge cases, SLAs, and backward compatibility before planning.
- **Multi-File Changes (3+ files)**: Run `/plan` to produce a reviewable `Implementation Plan` before modifying code.
- **Self-Healing Test & Build Loops**: Run `/goal` with an objective verification command (e.g., *"Run pytest and fix regressions until 100% pass"*).
- **UI & Frontend Verification**: Run `/browser` to verify live DOM rendering and console logs in sandboxed Chromium.
- **Knowledge Capture**: Run `/learn` after solving complex bugs or migrations to codify the pattern into `_agents/rules/*.md` or `_agents/skills/<name>/SKILL.md`.
- **Scheduled Automation**: Run `/schedule` with a 5-field cron expression to automate recurring operational digests and regression checks.
