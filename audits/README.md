# Secure Stacks — Security Audits

This directory contains security audit reports for each stack template. Every
stack must pass a security audit before being published.

## Audit Process

### 1. Automated Scanning (CI)

Every push triggers automated security scanning:

| Tool | Purpose | Gate |
|------|---------|------|
| Trivy | Container image vulnerability scanning | No critical/high CVEs |
| Grype | SBOM-based vulnerability matching | No critical CVEs |
| Hadolint | Dockerfile best practices | No errors |
| Docker Bench | CIS Docker Benchmark | Score ≥ 80% |
| gitleaks | Secret detection | Zero findings |
| npm audit / pip-audit | Dependency vulnerabilities | No critical/high |

### 2. Manual Security Review

A security reviewer evaluates each stack against the 25-point checklist
defined in [CONTRIBUTING.md](../CONTRIBUTING.md#security-audit-checklist).

The review covers:
- Container configuration hardening
- Network isolation
- Application security defaults
- Dependency management
- Operational readiness

### 3. Audit Report

The reviewer produces an audit report using the template in
[audit-template.md](audit-template.md). Reports include:

- Overall security score (0–100)
- Findings categorized by severity
- Remediation steps for each finding
- Compliance mapping (OWASP, CIS)

### 4. Remediation & Re-audit

Critical and high findings must be resolved before the stack is published.
Medium findings should be resolved within 30 days. Low and informational
findings are tracked as improvements.

---

## Scoring System

Each stack receives a security score from 0–100:

| Score | Grade | Status |
|-------|-------|--------|
| 90–100 | A | Excellent — Published |
| 80–89 | B | Good — Published with notes |
| 70–79 | C | Acceptable — Published with improvement plan |
| Below 70 | F | Failing — Not published |

### Score Calculation

| Category | Weight | Max Points |
|----------|--------|------------|
| Container Security | 35% | 35 |
| Network Security | 20% | 20 |
| Application Security | 25% | 25 |
| Dependency Security | 10% | 10 |
| Operational Security | 10% | 10 |

---

## Current Audit Status

| Stack | Version | Audit Date | Score | Grade | Report |
|-------|---------|-----------|-------|-------|--------|
| t3-stack | 1.0.0 | — | — | — | Pending initial audit |
| django-stack | 1.0.0 | — | — | — | Pending initial audit |
| fastapi-stack | 1.0.0 | — | — | — | Pending initial audit |
| express-mongo-stack | 1.0.0 | — | — | — | Pending initial audit |
| rails-stack | 1.0.0 | — | — | — | Pending initial audit |

---

## Audit Schedule

- **New stacks** — Audited before first publication
- **Major updates** — Re-audited when framework major version changes
- **Quarterly reviews** — All published stacks reviewed every 90 days
- **Emergency audits** — Triggered when a critical CVE affects a dependency

---

## Becoming a Security Reviewer

We welcome security-minded contributors! To become a reviewer:

1. Have at least 3 merged contributions to the project
2. Demonstrate security knowledge (certifications, blog posts, or prior work)
3. Shadow an existing reviewer for 2 audits
4. Complete your first solo audit with reviewer oversight

Contact **security@secure-stacks.dev** to express interest.

---

## Reports Index

Reports are named: `{stack-name}-audit-v{version}.md`

```
audits/
├── README.md                   # This file
├── audit-template.md           # Template for new audit reports
├── t3-stack-audit-v1.md        # (pending)
├── django-stack-audit-v1.md    # (pending)
└── ...
```
