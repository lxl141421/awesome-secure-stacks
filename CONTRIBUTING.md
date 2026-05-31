# Contributing to Secure Stacks

Thank you for your interest in making web development more secure! This guide
covers everything you need to contribute a new stack, improve an existing one,
or help with audits.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Submitting a New Stack](#submitting-a-new-stack)
- [Required Information](#required-information)
- [Security Audit Checklist](#security-audit-checklist)
- [Review Process](#review-process)
- [Quality Standards](#quality-standards)
- [Development Setup](#development-setup)

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
By participating, you agree to uphold a welcoming, inclusive, and harassment-free
environment. Report unacceptable behavior to **security@secure-stacks.dev**.

---

## How to Contribute

### Types of Contributions

| Type | Description |
|------|-------------|
| **New Stack** | Add a full-stack template with security hardening |
| **Stack Update** | Update dependencies or configurations for an existing stack |
| **Audit** | Perform or review a security audit for a stack |
| **Documentation** | Improve guides, fix typos, add examples |
| **Tooling** | Improve validation scripts, CI pipelines, or automation |
| **Bug Report** | Report issues with existing stacks or tooling |

### Quick Start

1. Fork the repository
2. Create a feature branch: `git checkout -b add/stack-name`
3. Make your changes
4. Run the validation script: `python scripts/validate-stack.py stacks/your-stack/stack.yml`
5. Submit a Pull Request

---

## Submitting a New Stack

### Step 1: Propose the Stack

Open a [Stack Request](https://github.com/lxl141421/awesome-secure-stacks/issues/new?template=stack_request.md)
issue before starting work. This avoids duplicate effort and allows early feedback
on scope and approach.

### Step 2: Create the Stack Directory

```
stacks/your-stack-name/
├── stack.yml              # Stack metadata and dependency manifest
├── README.md              # Setup and usage documentation
├── docker-compose.yml     # Production-ready Docker Compose
├── docker-compose.dev.yml # Development overrides (optional)
├── Dockerfile             # Custom images if needed
├── .env.example           # Environment variable template
├── lockfile.sha256        # SHA-256 checksums for lockfiles
├── security-config/       # Security configuration files
│   ├── nginx.conf         # Reverse proxy config
│   ├── headers.conf       # Security headers
│   └── cors.conf          # CORS policy
└── tests/
    ├── smoke-test.sh      # Basic health checks
    └── security-test.sh   # Security validation tests
```

### Step 3: Fill in `stack.yml`

```yaml
name: your-stack-name
version: 1.0.0
description: Brief description of the stack
category: fullstack | backend | frontend | infra
license: MIT

framework:
  name: FrameworkName
  version: "X.Y.Z"
  url: https://framework.dev

components:
  - name: app
    image: your-app:tag
    role: application
  - name: db
    image: postgres:16-alpine
    role: database

security:
  last_audit: null
  audit_score: null
  cve_exceptions: []
  hardening:
    - non-root-user
    - read-only-filesystem
    - resource-limits
    - no-new-privileges

dependencies:
  - name: dependency
    version: "X.Y.Z"
    source: npm | pypi | crates | go
    checksum: "sha256:..."

maintainers:
  - github: your-username
    name: Your Name
```

### Step 4: Write Documentation

Your `README.md` must include:

- **Prerequisites** — required tools and versions
- **Quick Start** — get running in under 5 minutes
- **Configuration** — all environment variables documented
- **Security Features** — what hardening is applied
- **Customization** — how to adapt for production
- **Troubleshooting** — common issues and solutions

### Step 5: Submit the Pull Request

Use the [PR template](.github/PULL_REQUEST.md) and ensure all checklist items
are completed.

---

## Required Information

Every stack submission **must** include:

### Mandatory

- [ ] `stack.yml` with all required fields populated
- [ ] Working `docker-compose.yml` that starts successfully
- [ ] `README.md` with setup instructions
- [ ] `.env.example` listing all required environment variables
- [ ] All containers run as non-root users
- [ ] All containers have resource limits defined
- [ ] All containers have health checks
- [ ] Security headers configured (CSP, HSTS, X-Frame-Options, etc.)
- [ ] No hardcoded secrets, passwords, or API keys
- [ ] Lockfile included and checksum recorded in `lockfile.sha256`

### Recommended

- [ ] Development docker-compose override
- [ ] Smoke tests that verify the stack starts correctly
- [ ] Security test script
- [ ] CI/CD pipeline example
- [ ] Logging configuration
- [ ] Backup/restore scripts for stateful services

---

## Security Audit Checklist

Every stack must pass this 25-point security checklist before merging. Auditors
check each item and document findings in `audits/`.

### Container Security

1. **Non-root execution** — All containers specify a non-root `USER` with a
   specific UID/GID (not just username)
2. **Read-only root filesystem** — `read_only: true` is set; writable paths use
   `tmpfs` mounts
3. **No new privileges** — `security_opt: [no-new-privileges:true]` on every
   service
4. **Resource limits** — CPU and memory limits are defined to prevent resource
   exhaustion
5. **Dropped capabilities** — `cap_drop: [ALL]` with only required capabilities
   added back
6. **No privileged mode** — No container runs with `privileged: true`
7. **Minimal base images** — Alpine, distroless, or scratch-based images preferred
8. **No `latest` tags** — All images pinned to specific versions or digests

### Network Security

9. **Internal-only networks** — Backend services not exposed to host unless
   explicitly required
10. **No host networking** — Containers do not use `network_mode: host`
11. **TLS everywhere** — All inter-service and external communication encrypted
12. **CORS configured** — Explicit origin allowlist, no wildcard `*`

### Application Security

13. **No hardcoded secrets** — All secrets via environment variables or Docker
    secrets/vaults
14. **Secure defaults** — Debug mode off, secure cookies, CSRF protection enabled
15. **Input validation** — All user inputs validated at API boundary
16. **SQL injection prevention** — Parameterized queries or ORM used exclusively
17. **XSS prevention** — Output encoding, Content-Security-Policy headers set
18. **Security headers** — HSTS, X-Content-Type-Options, X-Frame-Options,
    Referrer-Policy configured

### Dependency Security

19. **Lockfile present** — `package-lock.json`, `requirements.txt` (pinned),
    `go.sum`, `Cargo.lock`, etc.
20. **Lockfile integrity** — SHA-256 checksum of lockfile recorded
21. **No known CVEs** — Dependencies scanned with `npm audit`, `pip-audit`,
    `govulncheck`, or equivalent
22. **Minimal dependencies** — No unused or unnecessary dependencies included

### Operational Security

23. **Health checks defined** — Every service has a Docker health check with
    appropriate intervals and timeouts
24. **Logging configured** — Structured logging with no sensitive data in logs
25. **Graceful shutdown** — Containers handle SIGTERM and shut down cleanly

---

## Review Process

### Phase 1: Automated Checks (CI)

When you open a PR, GitHub Actions automatically runs:

- **YAML validation** — `stack.yml` schema check
- **Docker Compose validation** — `docker compose config` succeeds
- **Container build** — All images build without errors
- **Linting** — Hadolint for Dockerfiles, yamllint for YAML
- **Secret scanning** — TruffleHog / gitleaks scan for leaked credentials
- **Dependency audit** — `npm audit --production`, `pip-audit`, etc.
- **SBOM generation** — Software Bill of Materials generated for each image
- **Vulnerability scan** — Trivy scans all container images
- **Configuration analysis** — Docker Bench for Security checks

All automated checks must pass before human review begins.

### Phase 2: Maintainer Review

A project maintainer reviews:

1. **Architecture** — Is the stack well-structured and idiomatic for the
   framework?
2. **Security posture** — Does it meet or exceed the audit checklist?
3. **Documentation** — Is the README complete and accurate?
4. **Testing** — Do the smoke and security tests cover key scenarios?
5. **License compatibility** — Are all dependencies compatible with MIT?

### Phase 3: Security Review (for new stacks)

For new stack submissions, a security-focused reviewer performs:

1. Manual review of all configuration files
2. Runs the full audit checklist against the stack
3. Attempts common attack vectors (OWASP Top 10)
4. Documents findings in `audits/stack-name-audit-v1.md`
5. Issues must be resolved before merge; findings noted for future improvement

### Merge Criteria

- [ ] All CI checks pass (green)
- [ ] At least 1 maintainer approval
- [ ] At least 1 security reviewer approval (new stacks)
- [ ] All review comments resolved
- [ ] Audit score ≥ 65/100 (new stacks)
- [ ] No critical or high severity findings unresolved

---

## Quality Standards

### Code Quality

- Dockerfiles use multi-stage builds where appropriate
- Shell scripts pass `shellcheck`
- YAML files pass `yamllint`
- Python scripts pass `ruff` linting and type checking
- No TODO/FIXME/HACK comments in submitted code (use issues instead)

### Documentation Quality

- All environment variables documented with type, default, and description
- All ports documented with purpose
- Architecture diagram for complex stacks
- Changelog entry for updates to existing stacks

### Commit Standards

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(stack): add Next.js + tRPC stack
fix(django): correct CSP header for admin panel
docs(readme): update prerequisites section
security(express): patch CVE-2024-XXXXX in dependency
```

### Versioning

Stacks follow [Semantic Versioning](https://semver.org/):

- **MAJOR** — Breaking changes to the stack (framework major version upgrade)
- **MINOR** — New features or components added
- **PATCH** — Dependency updates, bug fixes, documentation improvements

---

## Development Setup

### Prerequisites

- Docker Engine 24+ and Docker Compose v2
- Python 3.10+ (for validation scripts)
- Git 2.30+

### Local Development

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/secure-stacks.git
cd secure-stacks

# Install validation tools
pip install -r scripts/requirements.txt

# Validate a stack
python scripts/validate-stack.py stacks/your-stack/stack.yml

# Run a stack locally
cd stacks/your-stack
cp .env.example .env
docker compose up -d

# Run smoke tests
./tests/smoke-test.sh
```

### Useful Tools

| Tool | Purpose | Install |
|------|---------|---------|
| Trivy | Container vulnerability scanning | `apt install trivy` |
| Hadolint | Dockerfile linting | Docker image available |
| gitleaks | Secret scanning | `brew install gitleaks` |
| docker-bench | Docker security benchmarking | GitHub clone |
| Grype | SBOM vulnerability matching | `curl -sSfL install.sh` |

---

## Questions?

- **General questions** — Open a [Discussion](https://github.com/lxl141421/awesome-secure-stacks/discussions)
- **Bug reports** — Open an [Issue](https://github.com/lxl141421/awesome-secure-stacks/issues/new?template=bug_report.md)
- **Security concerns** — Email **security@secure-stacks.dev** (do NOT open a
  public issue for security vulnerabilities)

Thank you for helping make the web more secure! 🔒
