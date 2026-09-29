---
trigger: model_decision
description: "Apply these BigQuery SQL and Dataform FinOps optimization rules whenever writing, reviewing, or migrating SQL queries, views, or warehouse pipelines."
---

# Enterprise Data Platform: BigQuery SQL & FinOps Optimization Rules

This rule uses `trigger: model_decision` (progressive disclosure). Only its 1-line description is loaded by default; the model reads this file only when working on SQL or BigQuery tasks.

## Mandatory SQL Quality & Cost Guardrails
1. **No `SELECT *` on Partitioned Tables**: Explicitly project required columns and always filter on the partition column (e.g., `WHERE _PARTITIONDATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)`).
2. **CLI Attribution Labels**: Every `bq query` command executed via `run_command` MUST include `--label=managed_by:antigravity --label=env:enterprise` (also enforced deterministically by `_agents/hooks.json` `PreToolUse` `overwrite`).
3. **Legacy Database Type Mapping**:
   - Map `NUMBER(p, s)` with financial precision to `NUMERIC` or `BIGNUMERIC` (never `FLOAT64`).
   - Replace correlated subqueries with window functions (`QUALIFY ROW_NUMBER() OVER (...) = 1`).
