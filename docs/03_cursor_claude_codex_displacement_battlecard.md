# Competitive Displacement Battlecard: Google Antigravity + Gemini Enterprise vs. Cursor, Claude Code & OpenAI Codex

## 1. Executive Summary for Engineering Leaders, FinOps & Security Architects

Enterprises scaling AI assistance across both technical and non-technical teams face three systemic challenges when evaluating point coding tools like **Cursor**, **Claude Code**, and **OpenAI Codex**:
1. **Per-User Token Burn vs. Enterprise Pooled Economics**: Claude Code and Cursor bill per-seat or per-token with uncapped overages, whereas **Gemini Enterprise Standard ($30/mo) and Plus** automatically fund a **project-wide weekly pooled Antigravity quota** (`$2.50/seat/week` on Standard or `$3.75/seat/week` on Plus) where light business users naturally subsidize heavy engineering workloads.
2. **Governance & Exfiltration Gaps**: Unmanaged local MCP servers, un-sandboxed shell execution, and lack of Google Cloud IAM / Cloud Logging integration create compliance risks in regulated industries.
3. **Developer-Only Silos**: Cursor and Claude Code only serve software engineers, leaving operations, PMO, finance, procurement, product management, and functional QA analysts unable to build or run agents.

---

## 2. Head-to-Head Enterprise Capability Matrix

| Enterprise Dimension | **Google Antigravity + Gemini Enterprise** | **Cursor (Business / Enterprise)** | **Anthropic Claude Code** | **OpenAI Codex (CLI / Cloud)** |
| :--- | :--- | :--- | :--- | :--- |
| **Licensing & Quota Pool Economics** | **Included in Gemini Enterprise** ($10/mo Standard or $15/mo Plus pooled across the GCP project weekly: **$2,500–$3,750/wk per 1,000 seats**). Zero overage by default (`Pay-as-you-go` toggleable). | Separate **$40/user/mo** ($480k/yr per 1,000 seats) + fast-request exhaustion overages. Duplicate cost alongside existing Gemini licenses. | High per-token API burn (`$100–$250+/dev/mo` during multi-agent refactoring loops). No cross-workforce quota pooling. | Requires ChatGPT Enterprise/Pro + API credits; cloud task containers metered separately. |
| **Centralized Admin & IAM Governance** | Native **Google Cloud IAM** (`roles/businessaicode.admin`, `developer`, `viewer`), OS terminal sandbox toggle, Browser URL allow/denylists, and **Admin-overridden MCP JSON**. | Admin dashboard lacks GCP IAM binding, native Cloud Logging prompt/response export, or centralized OS/Browser subagent policy enforcement. | CLI-centric; relies on developer-managed settings files unless custom MDM wrappers are built and maintained by IT. | Cloud sandbox lacks access to internal VPC resources; CLI lacks centralized GCP IAM & MCP override controls. |
| **Multi-Agent & Worktree Architecture** | **Antigravity 2.0 Native Subagents** (`research`, `self`, `browser`, custom `.agents/agents/*.md`), **`New Worktree Mode`** for parallel conflict-free edits, and **`Idle` state warm-context reuse**. | Primarily single-IDE composer thread; background agents require external cloud runners and lack native local Git worktree subagent orchestration. | Supports sub-tasks in CLI, but lacks visual artifact carousels, built-in Chromium `/browser` subagent, and persistent `sidecar.json` daemons. | Runs asynchronous cloud tasks in isolated containers, disconnected from local IDE state, local VPNs, and interactive `/browser` testing. |
| **Deterministic Compliance Gates (`hooks.json`)** | Native `PreToolUse`, `PostToolUse`, `PreInvocation`, `PostInvocation`, and `Stop` hooks (`gate.py`) that can **overwrite** arguments, **force_ask**, or **deny** dangerous commands in code. | Relies primarily on `.cursorrules` (prompt-level suggestions that LLMs can ignore under context pressure). | Supports basic shell hooks, but lacks native `PreInvocation` ephemeral step injection and `LiteRT` on-device model routing. | No local lifecycle hook protocol for cloud-executed tasks. |
| **Business-to-Architect Workforce Span** | Covers **100% of the workforce**: Markdown Citizen Agents, Low-Code Plugins, IDE/CLI Subagents, Python AGY SDK (`google-antigravity`), and 24x7 Sidecars. | Built strictly for IDE developers; non-technical PMO, operations, and finance teams cannot use it. | Terminal-only CLI; alienates non-technical business analysts, PMO, and visual QA teams. | Developer-only CLI/GitHub workflow. |
| **Model Fleet & Local NPU Zero-Egress Option** | **Gemini 3.8/3.7 Flash**, **Gemini 3.1 Pro**, **Nano Banana Pro/2** (UI mockups), **Gemini Omni 1.1 Flash** (video), **Deep Research**, plus **local Gemma 4 (`LiteRTAgentConfig`)** for privacy-sensitive workflows. | Rents third-party models with markup; no native first-party multimodal video/image/deep-research stack or zero-cost local Gemma 4 SDK runtime. | Locked to Claude models; no native image/video generation or first-party GCP Vertex AI data residency integration. | Locked to OpenAI models; no native Vertex AI VPC-SC perimeter integration. |
| **Real-Time Telemetry & Chargeback** | **Developer Tool Metrics** in GCP Console refreshed every **5–15 minutes** (active users, requests, tokens, latency, errors) for departmental chargeback. | Basic CSV usage exports; disconnected from GCP BigQuery billing exports. | API token logs only; lacks unified workspace + IDE developer productivity telemetry in GCP. | Basic dashboard; no native BigQuery cost attribution integration. |

---

## 3. Displacement Playbooks by Competitor

### 3.1 Displacing Cursor in Application Development Teams
- **Why Teams Installed Cursor**: Fast tab-completion and multi-file Composer edits.
- **How Antigravity Wins**:
  1. **Zero Duplicate License Cost**: Organizations already licensing **Gemini Enterprise** receive Antigravity quota automatically. Paying $40/mo/seat for Cursor duplicates existing spend.
  2. **Parallel Git Worktree Subagents (`/teamwork-preview`)**: Instead of watching a single Composer thread edit files sequentially, Antigravity spawns parallel subagents in `New Worktree Mode`—one writing backend code (`gemini-3.8-flash`), one running `/browser` E2E verification, and one running `security-and-finops-auditor.md`.
  3. **Drop-in Rule Migration**: Existing `.cursorrules` files convert in <5 minutes into `_agents/rules/*.md` with `glob` and `model_decision` triggers plus deterministic `_agents/hooks.json` enforcement.

### 3.2 Displacing Claude Code in DevOps / SRE & Modernization Pods
- **Why Teams Installed Claude Code**: Terminal-first agentic loops and strong reasoning on refactoring tasks.
- **How Antigravity Wins**:
  1. **Predictable Weekly Pooled Quota vs. Uncapped API Bills**: A single engineer running Claude Code in an autonomous test loop can burn **$80–$150 in a single afternoon**. Antigravity uses `/goal` with `gemini-3.8-flash` (`Medium` thinking) inside the **pooled Gemini Enterprise allowance**, reserving `gemini-3.1-pro-preview` (`/boost`) strictly for architectural bottlenecks.
  2. **`Idle` Subagent Warm-Context Reuse**: Antigravity 2.0 subagents stay `Idle` after completing an audit so follow-up prompts reuse their warm context window instead of re-indexing the codebase from scratch.
  3. **24x7 Autonomous Sidecar Daemons (`sidecar.json`)**: Claude Code exits when the terminal closes. Antigravity natively runs persistent background sidecars (`restart_policy: "always"`) that monitor incident queues and invoke `agentapi new-conversation` automatically.

### 3.3 Displacing OpenAI Codex in Regulated Enterprise Environments
- **Why Teams Evaluated Codex**: Cloud-hosted asynchronous task execution on GitHub repositories.
- **How Antigravity Wins**:
  1. **VPC Perimeter & On-Device Privacy Compliance**: Regulated enterprises often prohibit uploading proprietary source code to external third-party task containers. Antigravity runs inside the organization's **Google Cloud project boundary** (with `vertex=True` ADC binding) or 100% locally via **Gemma 4 (`LiteRTAgentConfig`)**.
  2. **Interactive Socratic Planning (`/grill-me` + `/plan`)**: Asynchronous black-box PR generation often misses nuanced business logic. Antigravity's `/grill-me` -> `/plan` -> `/goal` workflow aligns human architects before a single line of code is written.

---

## 4. Objection Handling Cheat-Sheet

| Common Developer / Architect Objection | Grounded Technical & Economic Response |
| :--- | :--- |
| *"How do we get maximum reasoning depth on complex multi-file refactoring?"* | Switch `/model` to **`gemini-3.1-pro-preview`** (or `antigravity-preview-05-2026`) with **`High` thinking effort** or run **`/boost`**. Pair it with `/plan` and parallel `New Worktree Mode` subagents (`code-reviewer.md`)—you get deterministic test-verified output without uncapped per-token API bills. |
| *"We already wrote dozens of `CLAUDE.md` and `.cursorrules` files across our repos."* | Antigravity natively supports **`AGENTS.md`** and **`GEMINI.md`** with automatic hierarchical directory-walk loading from the Git root down to subdirectories, plus 4-trigger `_agents/rules/*.md` files. Migration takes less than 10 minutes per repository. |
| *"How do we stop a developer from running a destructive command in Turbo Mode?"* | Prompt rules alone cannot stop mistakes—that is why Antigravity provides **deterministic `_agents/hooks.json` (`PreToolUse`)**. Our [`hooks-scripts/gate.py`](../hooks-scripts/gate.py) intercepts every command in Python and returns `"decision": "deny"` on `terraform destroy`, `rm -rf`, or credential edits before the shell ever sees it. |
| *"Will power users exhaust our quota mid-week?"* | Gemini Enterprise pools quota across all project seats (**$2.50/seat/week Standard** or **$3.75/seat/week Plus**). By routing 80% of subagent exploration to `gemini-3.8-flash` (`Low`/`Medium` effort) and monitoring **Developer Tool Metrics** (5–15 min refresh), power users have substantial headroom while keeping unbudgeted overage at $0.00. |
