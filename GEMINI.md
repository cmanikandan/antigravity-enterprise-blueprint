# Enterprise Gemini Model & SDK Governance Standard (`GEMINI.md`)

This file is automatically loaded by Antigravity across the workspace hierarchy to enforce model selection, SDK standards, and Gemini Enterprise pooled quota efficiency across all teams.

---

## 1. Approved Gemini 3.x Model Routing Standard

> [!CAUTION]
> **Strict Deprecation Block**: Legacy models (`gemini-1.5-*`, `gemini-2.0-*`, `gemini-2.5-*`) and legacy SDKs (`google-generativeai`, `@google/generative-ai`) are **deprecated and prohibited**. Always use `google-genai >= 2.3.0` (Interactions API) and `google-antigravity`.

Route workloads to the appropriate model and **Thinking Effort Tier (`Low`, `Medium`, `High`)** to maximize your project's **Gemini Enterprise Weekly Shared Quota Pool**:

| Agent Archetype / Workload | Approved Model Identifier | Thinking Effort Tier | Target Persona / Role |
| :--- | :--- | :--- | :--- |
| **Agent #1: Daily Role Copilot** *(Interactive coding, specs, status digests, operational checklists)* | `gemini-3.8-flash` *(or SDK default `gemini-3.7-flash`)* | `Low` / `Medium` (Tier 1–2)<br>`High` (Tier 3–4 Coding) | All Employees (Business & Technical) |
| **Agent #2: Domain & Architecture Specialist** *(Complex refactoring, distributed systems design, `/boost`)* | `gemini-3.1-pro-preview` | `High` (Deep Reasoning)<br>`Low` (Fast Review) | Senior Engineers & Systems Architects |
| **Agent #3: Automated Critic & Background Sentinel** *(`/schedule` cron, `every()`, `on_file_change()`, Sidecars)* | `gemini-3.5-flash-lite` / `gemini-3.7-flash` | `Low` (Ultra-Fast / Lowest Quota Cost) | Automated Quality, Security & Ops Agents |
| **Multimodal Visuals, Video & Audio** *(Architecture diagrams, UI mockups, enablement videos, transcription)* | • `gemini-3-pro-image-preview` (*Nano Banana Pro*)<br>• `gemini-3.1-flash-image-preview` (*Nano Banana 2*)<br>• `gemini-omni-1.1-flash` *(Video up to 40s)*<br>• `gemini-embedding-2` | Standard | Product, Design, Enablement & QA Teams |
| **Managed Remote Sandboxes & Deep Research** | • `antigravity-preview-05-2026` (`environment="remote"`)<br>• `deep-research-preview-04-2026` (`background=True`) | Managed Agent | Architecture, Security & Strategy Teams |
| **On-Device Zero-Cost Local Execution** | • `gemma-4-31b-it` (Dense)<br>• `gemma-4-26b-a4b-it` (MoE) | Local `LiteRTAgentConfig` | Privacy-Sensitive & High-Frequency Local Workflows |

---

## 2. Gemini Enterprise Authentication & Seat Binding (`vertex=True`)
All Python SDK agents (`google-antigravity` and `google-genai`) must authenticate through **Gemini Enterprise / Vertex AI** so usage attributes cleanly to the organization's governed Google Cloud project:
1. **Standard Enterprise Mode (ADC — Recommended)**: `LocalAgentConfig(vertex=True, project=os.environ["GOOGLE_CLOUD_PROJECT"], location="us-central1")`
2. **Express / Prototyping Mode (API Key)**: `LocalAgentConfig(vertex=True, api_key=os.environ["GEMINI_ENTERPRISE_API_KEY"])`
