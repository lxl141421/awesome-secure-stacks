# Security Audit Report

<!-- 
Instructions: Copy this template to audits/<stack-name>-audit-v<N>.md and
fill in all sections. Delete this comment block when complete.
-->

## Audit Information

| Field | Value |
|-------|-------|
| **Stack** | <!-- e.g., t3-stack --> |
| **Stack Version** | <!-- e.g., 1.0.0 --> |
| **Audit Version** | <!-- e.g., v1 --> |
| **Auditor** | <!-- GitHub username or name --> |
| **Audit Date** | <!-- YYYY-MM-DD --> |
| **Audit Type** | <!-- initial / quarterly / emergency / re-audit --> |
| **Overall Score** | <!-- 0–100 --> |
| **Grade** | <!-- A / B / C / F --> |

---

## Executive Summary

<!-- 2–3 sentence overview of the audit findings and overall assessment. -->

---

## Scope

<!-- What was included in this audit? -->

- Docker Compose configuration
- Dockerfile(s)
- Application configuration
- Security headers
- Network configuration
- Dependency manifest
- Documentation

### Out of Scope

<!-- What was NOT reviewed? E.g., application source code logic, third-party services. -->

---

## Automated Scan Results

### Trivy (Container Vulnerability Scan)

```
<!-- Paste Trivy output here -->
$ trivy image <image:tag>

Total: X (Critical: X, High: X, Medium: X, Low: X)
```

### Hadolint (Dockerfile Linting)

```
<!-- Paste Hadolint output here -->
$ hadolint Dockerfile

No issues found / issues listed
```

### Docker Bench for Security

```
<!-- Paste relevant Docker Bench output here -->
$ docker-bench-security

Score: XX%
```

### Dependency Audit

```
<!-- Paste npm audit / pip-audit / cargo audit output here -->
```

### Secret Scan (gitleaks)

```
<!-- Paste gitleaks output here -->
$ gitleaks detect

No leaks found / findings listed
```

---

## Checklist Results

### Container Security (35 points)

| # | Check | Status | Points | Notes |
|---|-------|--------|--------|-------|
| 1 | Non-root execution | ✅ / ❌ | /5 | |
| 2 | Read-only root filesystem | ✅ / ❌ | /5 | |
| 3 | No new privileges | ✅ / ❌ | /5 | |
| 4 | Resource limits | ✅ / ❌ | /5 | |
| 5 | Dropped capabilities | ✅ / ❌ | /5 | |
| 6 | No privileged mode | ✅ / ❌ | /3 | |
| 7 | Minimal base images | ✅ / ❌ | /4 | |
| 8 | No `latest` tags | ✅ / ❌ | /3 | |

**Subtotal: /35**

### Network Security (20 points)

| # | Check | Status | Points | Notes |
|---|-------|--------|--------|-------|
| 9 | Internal-only networks | ✅ / ❌ | /5 | |
| 10 | No host networking | ✅ / ❌ | /5 | |
| 11 | TLS configured | ✅ / ❌ | /5 | |
| 12 | CORS configured | ✅ / ❌ | /5 | |

**Subtotal: /20**

### Application Security (25 points)

| # | Check | Status | Points | Notes |
|---|-------|--------|--------|-------|
| 13 | No hardcoded secrets | ✅ / ❌ | /5 | |
| 14 | Secure defaults | ✅ / ❌ | /5 | |
| 15 | Input validation | ✅ / ❌ | /3 | |
| 16 | SQL injection prevention | ✅ / ❌ | /4 | |
| 17 | XSS prevention | ✅ / ❌ | /3 | |
| 18 | Security headers | ✅ / ❌ | /5 | |

**Subtotal: /25**

### Dependency Security (10 points)

| # | Check | Status | Points | Notes |
|---|-------|--------|--------|-------|
| 19 | Lockfile present | ✅ / ❌ | /3 | |
| 20 | Lockfile integrity | ✅ / ❌ | /2 | |
| 21 | No known CVEs | ✅ / ❌ | /3 | |
| 22 | Minimal dependencies | ✅ / ❌ | /2 | |

**Subtotal: /10**

### Operational Security (10 points)

| # | Check | Status | Points | Notes |
|---|-------|--------|--------|-------|
| 23 | Health checks defined | ✅ / ❌ | /3 | |
| 24 | Logging configured | ✅ / ❌ | /4 | |
| 25 | Graceful shutdown | ✅ / ❌ | /3 | |

**Subtotal: /10**

### Total Score: /100 — Grade: <!-- A/B/C/F -->

---

## Findings

<!-- List all findings. Use the severity levels: Critical, High, Medium, Low, Informational. -->

### Finding 1: [Title]

| Field | Value |
|-------|-------|
| **Severity** | Critical / High / Medium / Low / Informational |
| **Category** | Container / Network / Application / Dependencies / Operational |
| **CWE** | <!-- e.g., CWE-250 --> |
| **Status** | Open / In Progress / Resolved / Accepted Risk |

**Description:**
<!-- Describe the finding in detail. -->

**Impact:**
<!-- What is the potential impact of this finding? -->

**Evidence:**
<!-- Paste logs, screenshots, or scan output that demonstrates the finding. -->

```
evidence here
```

**Remediation:**
<!-- How should this finding be fixed? -->

**References:**
<!-- Links to CVEs, OWASP, CIS benchmarks, etc. -->

---

### Finding 2: [Title]

<!-- Repeat the above structure for each finding. -->

---

## OWASP Mapping

| OWASP Category | Addressed | Notes |
|---------------|-----------|-------|
| A01: Broken Access Control | ✅ / ⚠️ / ❌ | |
| A02: Cryptographic Failures | ✅ / ⚠️ / ❌ | |
| A03: Injection | ✅ / ⚠️ / ❌ | |
| A04: Insecure Design | ✅ / ⚠️ / ❌ | |
| A05: Security Misconfiguration | ✅ / ⚠️ / ❌ | |
| A06: Vulnerable Components | ✅ / ⚠️ / ❌ | |
| A07: Auth Failures | ✅ / ⚠️ / ❌ | |
| A08: Data Integrity Failures | ✅ / ⚠️ / ❌ | |
| A09: Logging Failures | ✅ / ⚠️ / ❌ | |
| A10: SSRF | ✅ / ⚠️ / ❌ | |

---

## Recommendations

### Must Fix (Before Publication)

<!-- Critical and high findings that block publication. -->

1.

### Should Fix (Within 30 Days)

<!-- Medium findings. -->

1.

### Nice to Have

<!-- Low and informational findings. -->

1.

---

## Conclusion

<!-- Overall assessment. Is this stack ready for publication? -->

**Recommendation:** <!-- Publish / Publish with conditions / Do not publish -->

---

## Sign-off

| Role | Name | Date | Approved? |
|------|------|------|-----------|
| Security Reviewer | | | ✅ / ❌ |
| Maintainer | | | ✅ / ❌ |
