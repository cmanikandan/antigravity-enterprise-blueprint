# Enterprise Gemini 4 & 3.x Model, Tokenomics & SDK Governance Standard (`GEMINI.md`)

This file is automatically loaded by Antigravity across the workspace hierarchy to enforce model selection, thinking-effort tokenomics, SDK standards, and Gemini Enterprise pooled quota efficiency across all teams.

---

## 1. Approved Gemini 4 & Gemini 3.x Model Routing Standard

> [!CAUTION]
> **Strict Deprecation Block**: Legacy models (`gemini-1.5-*`, `gemini-2.0-*`, `gemini-2.5-*`) and legacy SDKs (`google-generativeai`, `@google/generative-ai`) are **deprecated and prohibited**. Always use `google-genai >= 2.3.0` (Interactions & Managed Agents API) and `google-antigravity`.

Route workloads along the **Two-Axis Operating Model** (Model Brain × Thinking Effort) to maximize velocity and preserve your **Weekly Shared Quota Pool** (and take advantage of **95% implicit cached-input discounts**):

| Agent Archetype / Workload | Approved Model Identifier | Thinking Effort Tier | Tokenomics & Target Role |
| :--- | :--- | :--- | :--- |
| **Recommended Default: Intra-Turn Planner + Executor** *(Feature builds, multi-file debugging, refactors)* | `Orchestrator (Carbon)` / `Orchestrator (Argon)` *(Pro/Ultra)*<br>or SDK `Carbon/Argon` + `Hydrogen` | Fixed Dynamic Handoff *(Carbon/Argon plans; Hydrogen executes)* | **-24% quota, +19% faster** vs. standalone Carbon; auto re-plans on 2x test failure |
| **Agent #1: High-Speed Agentic Executor & Daily Copilot** *(Everyday coding, PR triage, unit tests, `/swarm` & `/run-workflow` workers)* | `gemini-4-hydrogen` *(or `gemini-3.8-flash`)* | `Low` / `Medium` (Fast edits)<br>`High` (Default) / `Extra` (`xhigh`) | `$1.50` in / `$7.50` out (`$0.075` cached) — All Employees & Worker Fleets |
| **Agent #2A: Frontier Engineering & Domain Specialist** *(Large refactors, distributed systems, RFCs, complex SQL/IaC)* | `gemini-4-argon` *(or `gemini-3.1-pro-preview`)* | `Medium` / `High` | `$2/$10` intro (`$4/$20` standard; 95% cache off) — Senior Engineers & Architects |
| **Agent #2B: Peak Frontier Reasoning, Cyber & Verifier** *(Hardest multi-package architecture, CWE chains, `/swarm` `@verifier`, `/boost`)* | `gemini-4-carbon` | `High` (Deep Exploration)<br>`Low` / `Medium` (Fast Audit) | `$2/$10` intro (`$4/$20` standard; 95% cache off) — Principal Architects & Security |
| **Agent #3: Background Sentinel & High-Volume Scanner** *(`/automation`, `/schedule` cron, `sidecar.json`, log triage)* | `gemini-3.5-flash-lite` / `gemini-3.7-flash` | `Minimal` / `Low` | `$0.30` in / `$2.50` out — Automated Quality, FinOps & SRE Sentinels |
| **Multimodal UI, Architecture Visuals & Video** *(`/generative_ui`, UI mockups, video walkthroughs)* | • `Nano Banana 2` (`gemini-3.1-flash-image-preview`)<br>• `gemini-omni-1.2-flash` / `1.1-flash`<br>• `gemini-embedding-2` | Standard | Product Managers, UX Designers, Enablement & QA |
| **Managed Remote Sandboxes & Deep Research** *(Zero-laptop Issue-to-PR, repo-scale audits)* | • `antigravity-preview-09-2026` *(default `gemini-4-hydrogen`)*<br>• `deep-research-preview-04-2026` (`background=True`) | Managed Linux Sandbox + Credentials API | CI/CD Issue-to-PR Pipelines, Strategy & Security Teams |
| **On-Device Zero-Cost Local Execution** *(PII scrubbing, offline AST filtering)* | • `gemma-4-31b-it` (Dense)<br>• `gemma-4-26b-a4b-it` (MoE) | Local `LiteRTAgentConfig` | `$0.00` Cloud Quota — Privacy-Sensitive Local Workflows |

---

## 2. Gemini Enterprise Authentication, Credentials API & Seat Binding (`vertex=True`)
All Python SDK agents (`google-antigravity` and `google-genai`) and headless CLI pipelines (`AGY_ADC_AUTH=true`) must authenticate cleanly without hardcoding secrets:
1. **Standard Enterprise Mode (ADC / WIF — Recommended)**: `LocalAgentConfig(vertex=True, project=os.environ["GOOGLE_CLOUD_PROJECT"], location="global")`
2. **Managed Sandbox Wire-Level Secrets**: Use the **Managed Agents Credentials API** (or Remote Agents `agy-plugin-proxy`) so GitHub/SaaS OAuth tokens are injected at the egress proxy and never exposed inside `os.environ`.
3. **Remember Thinking Token Economics**: Thinking tokens are billed at **output token rates** (`5x` input rate). Dial `/effort low` or `medium` on routine steps and reserve `high` / `xhigh` / `gemini-4-carbon` for genuine ambiguity, architecture, and adversarial verification.
