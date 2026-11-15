# ☁️ Lab M4: 12-Factor Cloud Run & Zero-Secret WIF/ADC Refactor

**Difficulty**: 🟠 Upper-Intermediate | **Duration**: 45 Minutes | **Sandbox**: [`../sandbox-apps/pulsepay-legacy-ledger/`](../sandbox-apps/pulsepay-legacy-ledger/README.md) + [`../../_agents/hooks.json`](../../_agents/hooks.json)

---

## 📖 The Cloud Security Architecture Review Blocker at PulsePay

PulsePay is decommissioning its on-prem VMware settlement hosts next month and moving [`pulsepay-legacy-ledger`](../sandbox-apps/pulsepay-legacy-ledger/README.md) onto **Google Cloud Run Jobs**. Your team containerized the code, deployed to staging, and hit **three immediate brick walls**:

1. **Read-Only Container Root Crash**: `ledger_batch.py` hardcodes `HARDCODED_SPOOL_DIR = "/var/spool/pulsepay/ach_outbox"` — which immediately throws `PermissionError` on hardened Cloud Run Linux sandboxes where only `/tmp` (or Cloud Storage) is writable.
2. **AppSec Red Card**: Security scanning flagged `LEGACY_TREASURY_DSN` (with an inline password and hardcoded `10.240.12.9` IP), `LEGACY_BATCH_HMAC_SEED`, and `HARDCODED_SMTP_RELAY = "10.240.14.22:2525"`.
3. **The "Helpful Agent" Trap**: When an engineer asked an unguarded coding assistant to *"configure Cloud SQL & Vertex AI auth quickly"*, it tried to generate a `service_account.json` key file and run `gcloud run deploy` straight to prod!

In this lab, you will pair **`gemini-4-argon`** (Domain Specialist for Cloud/IaC refactoring) with **deterministic lifecycle guardrails** ([`_agents/hooks.json`](../../_agents/hooks.json) + [`hooks-scripts/gate.py`](../../hooks-scripts/gate.py)) so even an autonomous `/goal` loop is **physically incapable** of writing static credential files or deploying to production without human sign-off.

---

## 🧠 Recommended Brain × Squad + Tokenomics Tip

| Dimension | Recommended Selection | Why This Wins on Speed & Quota |
| :--- | :--- | :--- |
| **Architect & Refactor Brain** | `gemini-4-argon` (`Medium`/`High` for `/plan`, `Low` for edits) *(or `Orchestrator (Argon)`)* | `$2`/`$10` intro (`95%` cache off) — purpose-built for Cloud Run 12-Factor config, IAM/WIF, and clean dependency injection. |
| **Deterministic Guardrail** | [`_agents/hooks.json`](../../_agents/hooks.json) (`PreToolUse` + `Stop` gates) | Prompts are *probabilistic advice*; `PreToolUse` hooks are **deterministic law** (`deny` on `.pem`/`service_account.json`, `force_ask` on `gcloud run deploy`). |
| **Auth Standard** | Workload Identity Federation (`WIF`) / `ADC` (`AGY_ADC_AUTH=true`, `vertex=True`) | Zero long-lived JSON keys in git, containers, or `os.environ`. |
| **💰 Tokenomics Tip** | Don't burn `High` thinking tokens checking formatting or conflict markers at the end of a turn — let the zero-token Python [`Stop` hook](../../hooks-scripts/gate.py) (`git diff --check`) enforce Definition-of-Done deterministically for `$0.00`! |

---

## ⚡ 60-Second Quick Start

1. Audit every 12-Factor violation in `pulsepay-legacy-ledger` AND test the enterprise security gate in 5 seconds:
   ```bash
   grep -rnE "HARDCODED_|LEGACY_" labs/sandbox-apps/pulsepay-legacy-ledger/
   echo '{"toolCall":{"name":"write_to_file","args":{"TargetFile":"labs/sandbox-apps/pulsepay-legacy-ledger/service_account.json"}}}' \
     | python3 hooks-scripts/gate.py --mode=pre-tool
   ```
   Look at that instant deterministic verdict from `gate.py`:
   `{"decision": "deny", "reason": "[ENTERPRISE SECURITY GATE] Modifying sensitive credential file ... is prohibited..."}`!
2. Launch `/plan` with `gemini-4-argon`:
   ```text
   /plan Refactor labs/sandbox-apps/pulsepay-legacy-ledger/ (ledger_batch.py and notification_service.py) to 12-Factor Cloud Run readiness: extract an immutable Settings dataclass loaded from environment variables (with safe stateless defaults like /tmp/pulsepay/ach_outbox for local/test runs), enforce keyless IAM/ADC connection configuration (zero inline DSN passwords, zero .env or service_account.json files), and preserve 100% backward compatibility with test_settlement_flow.py.
   ```

---

## 🔄 Guided 5-Stage Antigravity Loop

### Stage 1: Inspect Your Deterministic Safety Net (`_agents/hooks.json`)
Before refactoring, examine [`_agents/hooks.json`](../../_agents/hooks.json) and [`hooks-scripts/gate.py`](../../hooks-scripts/gate.py). Notice how Antigravity intercepts lifecycle events via stdin/stdout JSON:
- **`PreToolUse` → `"decision": "deny"`**: Blocks writing `.pem`, `.key`, `credentials.json`, or `service_account.json`, and blocks `terraform destroy` or `DROP TABLE`.
- **`PreToolUse` → `"decision": "force_ask"`**: Forces interactive human review on `gcloud run deploy` or `git push` even inside autonomous loops.
- **`PreToolUse` → `"overwrite"`**: Transparently rewrites `bq query` to inject `--label=managed_by:antigravity --label=env:enterprise`.

### Stage 2: Design the Stateless 12-Factor `Settings` Contract (`/plan`)
Review the `Implementation Plan` produced by `gemini-4-argon`. Verify it replaces all 5 module-level hardcoded constants across [`ledger_batch.py`](../sandbox-apps/pulsepay-legacy-ledger/ledger_batch.py) and [`notification_service.py`](../sandbox-apps/pulsepay-legacy-ledger/notification_service.py) with an immutable `PulsePayConfig` dataclass:
- `PULSEPAY_SPOOL_DIR` (default `/tmp/pulsepay/ach_outbox` — writable on Cloud Run's in-memory tmpfs).
- `PULSEPAY_CLOUD_SQL_INSTANCE` + `PULSEPAY_DB_IAM_USER` (`use_iam_authn=True` via ADC/WIF — **zero** password string in code or env!).
- `PULSEPAY_FEE_BPS` (default `25`, validated `0 <= bps <= 5000`).
- `PULSEPAY_WEBHOOK_URL` (validated `https://` in `production` env, overridable in tests via `monkeypatch` / `unittest.mock.patch.dict(os.environ, ...)`).

### Stage 3: Concurrent Socratic Exploration While Agents Work (`/btw`)
While Argon/Hydrogen implements `config.py` and wires dependency injection into `summarize_batch()` and `build_webhook_payload()`, test your security instincts via `/btw`:

- `/btw Why is storing a database password in a plain Cloud Run environment variable still weaker than Cloud SQL IAM Authentication with Workload Identity Federation (ADC)?`
- `/btw In GEMINI.md, how does the Managed Agents Credentials API / agy-plugin-proxy differ from passing GITHUB_TOKEN inside os.environ?`

### Stage 4: Execute & Verify 12-Factor + Hook Compliance (`/goal`)
Drop to `/effort low` and run `/goal` with a dual test + zero-hardcoded-secret verification command:

```text
/goal Implement PulsePayConfig.from_env() for labs/sandbox-apps/pulsepay-legacy-ledger/, remove all hardcoded RFC-1918 IPs, inline DSN passwords, and /var/spool paths, add env-override unit tests in test_settlement_flow.py, and pass:
python3 -m unittest discover -s labs/sandbox-apps/pulsepay-legacy-ledger -p "test_*.py" -v
```

### Stage 5: Simulate All 3 `gate.py` Verdicts (`deny`, `force_ask`, `overwrite`)
Verify your governance gate directly from the CLI so you can demonstrate it live to your CISO:

```bash
# 1. Hard Deny on static JSON key creation
echo '{"toolCall":{"name":"write_to_file","args":{"TargetFile":"credentials.json"}}}' | python3 hooks-scripts/gate.py --mode=pre-tool

# 2. Force Human Approval on Cloud Run prod deploy
echo '{"toolCall":{"name":"run_command","args":{"CommandLine":"gcloud run deploy pulsepay-ledger --region=us-central1"}}}' | python3 hooks-scripts/gate.py --mode=pre-tool

# 3. FinOps Attribution Auto-Overwrite on BigQuery CLI
echo '{"toolCall":{"name":"run_command","args":{"CommandLine":"bq query \"SELECT count(*) FROM ledger.settlements\""}}}' | python3 hooks-scripts/gate.py --mode=pre-tool
```

---

## 🧲 Prompt Magnets: Match Each Governance Layer to Its Job

Match each enterprise requirement (`1–4`) to the **only** Antigravity mechanism (`A–D`) that enforces it reliably:

1. *"Remind the agent of workspace rules at the start of every turn without bloating the permanent conversation transcript."*
2. *"Guarantee an agent in Auto mode can NEVER write a `service_account.json` file, even if prompt-injected."*
3. *"Deploy a Cloud Run service without any static JSON key files on disk or in `os.environ`."*
4. *"Prevent an agent from declaring victory while git merge-conflict markers remain in workspace files."*

- `[ A ]` `PreToolUse` hook returning `{"decision": "deny"}` in [`hooks-scripts/gate.py`](../../hooks-scripts/gate.py)
- `[ B ]` Workload Identity Federation (`WIF`) / Application Default Credentials (`ADC`, `vertex=True`)
- `[ C ]` `PreInvocation` hook injecting transient `ephemeralMessage`
- `[ D ]` `Stop` hook returning `{"decision": "continue"}` when `git diff --check` fails

*(Check your answers in the Facilitator Spoiler below!)*

---

## ✅ Dual-Layer Verification Rubric

| Layer | Check | Pass Criteria |
| :--- | :--- | :--- |
| **Layer 1: Objective `/goal` Command** | `python3 -m unittest discover -s labs/sandbox-apps/pulsepay-legacy-ledger -p "test_*.py" -v && ! grep -rnE "10\.240\.|/var/spool/pulsepay|postgres://.*:.*@" labs/sandbox-apps/pulsepay-legacy-ledger/` | Exit code `0`; zero hardcoded `10.240.*` IPs, inline DSN passwords, or `/var/spool` paths remain; env-var override tests pass. |
| **Layer 2: Security & Hook Gate Proof** | `gate.py` `PreToolUse` + `Stop` verification | `service_account.json` write returns `deny`; `gcloud run deploy` returns `force_ask`; no `.env` or secret files exist in git status. |

---

<details>
<summary>🎓 Facilitator Ground Truth & Root-Cause Spoiler (Click to Expand)</summary>

### 1. Prompt Magnets Solution
- **`1 → [ C ]`** (`PreInvocation` `ephemeralMessage` — enforces rules fresh every turn with zero permanent transcript bloat!).
- **`2 → [ A ]`** (`PreToolUse` `"deny"` — deterministic OS/harness gate outside the model's weights, immune to prompt injection).
- **`3 → [ B ]`** (`WIF / ADC` — short-lived metadata-server / federated tokens; zero static keys to rotate or leak).
- **`4 → [ D ]`** (`Stop` hook — intercepts `terminationReason == "model_stop"` and forces another repair turn if `git diff --check` is non-zero).

### 2. Clean 12-Factor `PulsePayConfig` Reference Pattern
```python
@dataclass(frozen=True)
class PulsePayConfig:
    spool_dir: str
    cloud_sql_instance: str
    db_iam_user: str
    use_iam_authn: bool
    platform_fee_bps: int
    webhook_endpoint: str

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "PulsePayConfig":
        src = env if env is not None else os.environ
        fee_bps = int(src.get("PULSEPAY_FEE_BPS", "25"))
        if not (0 <= fee_bps <= 5000):
            raise ValueError(f"PULSEPAY_FEE_BPS out of bounds: {fee_bps}")
        return cls(
            spool_dir=src.get("PULSEPAY_SPOOL_DIR", "/tmp/pulsepay/ach_outbox"),
            cloud_sql_instance=src.get("PULSEPAY_CLOUD_SQL_INSTANCE", "pulsepay-prod:us-central1:ledger-pg"),
            db_iam_user=src.get("PULSEPAY_DB_IAM_USER", "pulsepay-batch-sa@pulsepay.iam"),
            use_iam_authn=True,
            platform_fee_bps=fee_bps,
            webhook_endpoint=src.get("PULSEPAY_WEBHOOK_URL", "https://notify.pulsepay.internal/v1/receipts"),
        )
```

</details>
