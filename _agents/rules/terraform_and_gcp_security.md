---
trigger: glob
globs: "*.tf,*.tfvars"
---

# Enterprise Terraform & Google Cloud Landing Zone Rules

This rule uses `trigger: glob` (`*.tf,*.tfvars`) so it consumes **zero tokens** during general conversations and activates automatically whenever Terraform files are opened or edited.

## Mandatory Security & FinOps Controls
1. **Resource Attribution Labels**: Every Terraform resource that supports `labels` MUST include:
   - `managed_by = "antigravity"`
   - `domain = "<platform|data|security|application>"`
   - `cost_center = var.cost_center`
   - `environment = var.environment`
2. **Cloud Storage Hardening**: Every `google_storage_bucket` resource MUST set:
   - `uniform_bucket_level_access = true`
   - `public_access_prevention = "enforced"`
3. **Zero Static Keys**: Never declare `google_service_account_key` resources. Always use Workload Identity Federation or attached service accounts with least-privilege IAM roles.
4. **VPC Service Controls & Private Access**: Enable `private_ip_google_access = true` on all `google_compute_subnetwork` resources.
