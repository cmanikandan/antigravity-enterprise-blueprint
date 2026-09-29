# Cloud Resiliency & Production Readiness Reference Checklist

## 1. Idempotency & Retry Safety
- **Requirement**: All mutating REST/gRPC endpoints must accept an `Idempotency-Key` header and enforce exponential backoff with jitter on upstream calls.
- **Anti-Pattern**: Unbounded immediate retries that trigger cascading retry storms during downstream brownouts.

## 2. Graceful Degradation & Circuit Breaking
- **Requirement**: Configure explicit connection and read timeouts on all external HTTP/database clients and define fallback behavior when non-critical dependencies are unavailable.
- **Database Pooling**: Bound maximum open connections per container instance to prevent connection exhaustion during rapid autoscaling events.

## 3. Cloud IAM & Workload Identity
- **Requirement**: Authenticate workloads using Workload Identity Federation (WIF) or attached Cloud Run / GKE service accounts with least-privilege IAM roles—never static JSON service account keys.
