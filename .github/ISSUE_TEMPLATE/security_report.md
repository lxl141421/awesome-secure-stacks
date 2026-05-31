---
name: Security Report
about: Report a security vulnerability or concern in a stack template
title: '[SECURITY] '
labels: security, triage
assignees: ''
---

> **⚠️ IMPORTANT:** If this is a critical vulnerability that could be actively
> exploited, please email **security@secure-stacks.dev** instead of opening a
> public issue. We will respond within 48 hours.

## Security Report

### Affected Stack

**Stack name:** <!-- e.g., t3-stack, django-stack -->
**Stack version:** <!-- e.g., 1.2.0, or "main branch" -->

### Vulnerability Type

<!-- Check all that apply -->

- [ ] Container misconfiguration
- [ ] Dependency vulnerability (CVE)
- [ ] Hardcoded secret or credential
- [ ] Missing security header
- [ ] Insecure default configuration
- [ ] Privilege escalation
- [ ] Information disclosure
- [ ] Injection vulnerability
- [ ] Authentication/Authorization flaw
- [ ] Supply chain concern
- [ ] Other: <!-- specify -->

### Severity Assessment

<!-- Your assessment of the severity. Our security team will validate. -->

- [ ] **Critical** — Remote code execution, authentication bypass, data breach
- [ ] **High** — Privilege escalation, significant information disclosure
- [ ] **Medium** — Limited impact, requires specific conditions
- [ ] **Low** — Minor issue, defense-in-depth improvement
- [ ] **Informational** — Best practice suggestion

### Description

<!-- Provide a clear description of the vulnerability or security concern. -->

### Steps to Reproduce

<!-- Provide detailed steps to reproduce the issue. -->

1.
2.
3.

### Expected Behavior

<!-- What should happen from a security perspective? -->

### Actual Behavior

<!-- What actually happens? -->

### Impact

<!-- Describe the potential impact if this vulnerability were exploited. -->

### Environment

- **Docker version:**
- **Docker Compose version:**
- **Host OS:**
- **Architecture:** (amd64 / arm64)

### Evidence

<!-- Attach screenshots, logs, scan output, or proof-of-concept if available. -->
<!-- Use code blocks for terminal output: -->

```
paste evidence here
```

### Suggested Fix

<!-- If you have a suggestion for how to fix this issue, please describe it. -->

### References

<!-- Link to CVE, security advisory, OWASP page, or relevant documentation. -->

### Checklist

- [ ] I have verified this issue affects the latest version of the stack
- [ ] I have checked existing issues to ensure this hasn't been reported
- [ ] I have provided enough detail to reproduce the issue
- [ ] I understand this will be triaged within 5 business days
