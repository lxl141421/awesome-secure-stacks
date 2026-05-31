# DevOps & Infrastructure — Secure Stacks

> Last updated: 2026-05-31
> Review cadence: Monthly

---

## 1. Container Runtime ⭐

**Security Grade: A**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Docker Engine | 25.0.6 | Apache-2.0 | 1 moderate (patched) |
| containerd | 1.7.22 | Apache-2.0 | 0 critical |
| BuildKit | 0.16.0 | Apache-2.0 | 0 |
| runc | 1.2.1 | Apache-2.0 | 0 |

**Security Hardening:**
```jsonc
// /etc/docker/daemon.json
{
  "userns-remap": "default",
  "no-new-privileges": true,
  "live-restore": true,
  "log-driver": "json-file",
  "log-opts": { "max-size": "10m", "max-file": "3" },
  "default-ulimits": { "nofile": { "Name": "nofile", "Hard": 65536, "Soft": 65536 } }
}
```

**Best Practices:**
- Use distroless or scratch base images
- Scan images with Trivy 0.57.x or Grype 0.82.x
- Never run containers as root (`USER 1000`)
- Pin base image digests: `FROM node:20.18.0-alpine@sha256:abc...`

**Known CVEs:**
- CVE-2024-41110: Docker AuthZ plugin bypass (patched in 25.0.6)

---

## 2. Orchestration: Kubernetes

**Security Grade: A**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Kubernetes | 1.29.10 | Apache-2.0 | 1 moderate (patched) |
| etcd | 3.5.16 | Apache-2.0 | 0 |
| containerd | 1.7.22 | Apache-2.0 | 0 |

**Security Configuration:**
```yaml
# Pod Security Standards (restricted)
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

**Hardening Checklist:**
- [ ] Enable Pod Security Admission (restricted profile)
- [ ] Use RBAC with least-privilege roles
- [ ] Enable audit logging to SIEM
- [ ] Network policies for all namespaces
- [ ] Encrypt secrets at rest (KMS provider)
- [ ] Rotate kubelet certificates (auto-rotation)
- [ ] Scan with kube-bench (CIS benchmark)

**Known CVEs:**
- CVE-2024-5321: Ingress NGINX path traversal (patched)

---

## 3. CI/CD Pipelines

### GitHub Actions

**Security Grade: A-**

```yaml
# .github/workflows/ci.yml — pinned actions
name: CI
on: [push, pull_request]
permissions:
  contents: read    # minimum permissions
  packages: write

jobs:
  build:
    runs-on: ubuntu-22.04  # pin runner version
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1 (SHA pin)
      - uses: actions/setup-node@60edb5dd545a775178f52524783378180af0d1f8  # v4.0.2
```

**Security Practices:**
- Pin all actions to SHA (not tag)
- Set `permissions: { contents: read }` minimum
- Use OIDC for cloud authentication (no long-lived secrets)
- Enable Dependabot for Actions updates

### GitLab CI

**Security Grade: A**

```yaml
# .gitlab-ci.yml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
```

---

## 4. Infrastructure as Code

### Terraform

**Security Grade: A-**

| Component | Pinned Version | License |
|-----------|---------------|---------|
| Terraform | 1.7.5 | BSL-1.1 |
| OpenTofu | 1.8.2 | MPL-2.0 (open fork) |
| tflint | 0.53.0 | MPL-2.0 |
| checkov | 3.2.302 | Apache-2.0 |

```hcl
# versions.tf — pin providers
terraform {
  required_version = ">= 1.7.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.76.0"
    }
  }
  # Remote state with encryption
  backend "s3" {
    encrypt = true
    kms_key_id = "arn:aws:kms:..."
  }
}
```

**Security Practices:**
- Use OpenTofu if BSL license is a concern
- Enable state encryption (S3 SSE-KMS or GCS CMEK)
- Run `checkov` and `tfsec` in CI
- Use `.terraform.lock.hcl` with provider hashes

### Pulumi

| Component | Pinned Version | License |
|-----------|---------------|---------|
| Pulumi | 3.137.0 | Apache-2.0 |
| Pulumi AI | Latest | Apache-2.0 |

---

## 5. Monitoring Stack

**Security Grade: A**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Prometheus | 2.54.1 | Apache-2.0 | 0 |
| Grafana | 10.4.10 | AGPL-3.0 | 1 low |
| Alertmanager | 0.27.0 | Apache-2.0 | 0 |
| Loki | 3.2.1 | AGPL-3.0 | 0 |
| Node Exporter | 1.8.2 | Apache-2.0 | 0 |

**Security Configuration:**
```yaml
# prometheus.yml — secure config
global:
  scrape_interval: 15s
  evaluation_interval: 15s

# Disable admin API
web:
  enable_admin_api: false
  enable_lifecycle: false
```

**Grafana Hardening:**
- Disable anonymous access
- Enable LDAP/OAuth for auth
- Set `cookie_secure = true`, `cookie_samesite = strict`
- Use `GF_SECURITY_ANTI_FORGERY=true`

---

## 6. Service Mesh

### Istio

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Istio | 1.21.6 | Apache-2.0 | 1 moderate |

**Security Features:** mTLS by default, authorization policies, JWT validation

### Linkerd

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Linkerd | 2.14.10 | Apache-2.0 | 0 |

**Security Features:** mTLS (always-on), zero-config, minimal overhead

**Recommendation:** Linkerd for simplicity, Istio for advanced policy control

---

## 7. Secrets Management

**Security Grade: A+**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| HashiCorp Vault | 1.15.9 | BSL-1.1 | 0 critical |

**Security Features:**
- Dynamic secrets (database credentials, AWS keys)
- Auto-unseal with cloud KMS
- Lease-based secret rotation
- Audit logging (every access logged)
- Shamir's Secret Sharing for unsealing

**Alternatives:**
| Tool | Version | License | Notes |
|------|---------|---------|-------|
| OpenBao | 2.1.0 | MPL-2.0 | Open-source Vault fork |
| AWS Secrets Manager | N/A | Proprietary | Cloud-native |
| SOPS + Age | 3.9.1 | MPL-2.0 | File-based, GitOps-friendly |

---

## Security Comparison Matrix

| Feature | Docker | K8s | GitHub Actions | Terraform | Prometheus/Grafana | Vault |
|---------|--------|-----|----------------|-----------|-------------------|-------|
| RBAC | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Audit Log | ⚠️ | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| TLS | ✅ | ✅ | N/A | ✅ | ✅ | ✅ |
| Secrets Mgmt | ❌ | ⚠️ | ✅ | ❌ | ❌ | ✅ |
| **Grade** | **A** | **A** | **A-** | **A-** | **A** | **A+** |
