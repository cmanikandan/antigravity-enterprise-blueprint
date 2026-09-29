---
name: project-wbs-estimator
description: Converts product and functional requirements into a bottom-up Work Breakdown Structure (WBS), T-shirt sizing, engineering role mix, and Gemini Enterprise delivery velocity table.
---

# Project Work Breakdown Structure (WBS) & Effort Estimator Skill

Use this skill when a Product Manager, Business Analyst, Solutions Architect, or Engineering Manager needs to estimate effort and staffing for a new initiative or RFC.

## Step 1: Decompose Epics by Complexity
Classify every functional requirement into one of four standard estimation buckets:
- **Simple (`S`)**: 16 person-hours base effort (standard CRUD API, simple BigQuery view, basic UI screen).
- **Medium (`M`)**: 40 person-hours base effort (stateful workflow, third-party webhook integration, medium ETL pipeline).
- **Complex (`L`)**: 80 person-hours base effort (multi-region HA service, PCI/HIPAA tokenization pipeline, legacy database migration).
- **Very Complex (`XL`)**: 160 person-hours base effort (custom distributed transaction engine, zero-downtime core system cutover).

## Step 2: Apply Antigravity + Gemini 3.x Productivity Acceleration Factor
Apply the empirically validated engineering velocity factor when teams use **Google Antigravity + Gemini 3.8 Flash / 3.1 Pro**:
- **Boilerplate & Unit Test Generation (`/goal`)**: `-35%` effort reduction.
- **Legacy Code Discovery (`research` Subagent)**: `-40%` effort reduction.
- **Automated Visual QA (`/browser` Subagent)**: `-30%` effort reduction.

## Step 3: Output Balanced Engineering Pod Allocation
Output a Markdown resource table adhering to a balanced engineering pod structure:
- `15%` Principal / Staff Architect (System design, `/plan` review & security sign-off)
- `25%` Senior Tech Lead (Core domain orchestration & subagent worktree merge)
- `60%` Software, Data & QA Engineers (Feature implementation accelerated with Antigravity subagents)
