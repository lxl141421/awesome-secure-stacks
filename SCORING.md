# 📊 Secure Stacks Scoring Methodology

> **Version:** 1.0.0 | **Last Updated:** 2026-05-31

Every stack listed in **awesome-secure-stacks** is evaluated using a rigorous, transparent scoring system. This document details how scores are calculated and what they mean.

---

## 🎯 Overview

Each technology stack receives a **Security Score** from **0 to 100**, derived from five weighted dimensions. A stack must score **≥ 65 (Grade B)** to be included in this list. Scores are re-evaluated **monthly** or upon any security event.

```
Security Score = Vulnerability Posture + Supply Chain Integrity
              + Maintenance Health + Community Trust + Reproducibility
```

| Dimension | Weight | Description |
|---|---|---|
| 🛡️ Vulnerability Posture | **30 pts** | Known CVEs, patch velocity, severity distribution |
| 🔗 Supply Chain Integrity | **25 pts** | Dependency trust, provenance, signing, SBOM |
| 🔧 Maintenance Health | **20 pts** | Update frequency, LTS status, EOL timelines |
| 👥 Community Trust | **15 pts** | Adoption, governance, audit history |
| 📦 Reproducibility | **10 pts** | Lockfiles, deterministic builds, container pinning |

---

## 🛡️ Dimension 1: Vulnerability Posture (30 points)

Assesses the current security state of the stack and its components.

### Sub-criteria

| Sub-criterion | Max Points | Description |
|---|---|---|
| Open Critical/High CVEs | 10 | Deductions per open CVE: Critical -5, High -3, Medium -1 |
| Patch Velocity | 8 | Time from CVE disclosure to fix: <48h = 8, <7d = 6, <30d = 4, >30d = 1 |
| Historical CVE Density | 7 | CVEs per year over last 3 years (lower is better) |
| Security Audit Recency | 5 | Last independent audit: <6mo = 5, <1yr = 3, >1yr = 1, never = 0 |

### Scoring Example: Node.js 22 LTS

```
Open Critical/High CVEs:   0 open  → 10/10
Patch Velocity:            avg 3d  →  6/8
Historical CVE Density:    4/yr    →  4/7
Security Audit Recency:    8mo ago →  3/5
                                    ───────
Subtotal:                         23/30
```

---

## 🔗 Dimension 2: Supply Chain Integrity (25 points)

Evaluates the trustworthiness of the package supply chain.

### Sub-criteria

| Sub-criterion | Max Points | Description |
|---|---|---|
| Package Signing | 6 | Components sign releases: all = 6, partial = 3, none = 0 |
| Provenance / SLSA Level | 6 | SLSA 4 = 6, SLSA 3 = 5, SLSA 2 = 3, SLSA 1 = 1, none = 0 |
| Dependency Audit Tooling | 4 | Has native audit (npm audit, pip-audit, etc.) = 4, manual = 1 |
| SBOM Availability | 4 | Official SBOM (CycloneDX/SPDX) = 4, partial = 2, none = 0 |
| Typosquatting Protections | 3 | Scoped packages, namespace controls, verified publishers |
| Reproducible CI/CD | 2 | CI pipeline is reproducible and auditable |

### Scoring Example: Go Standard Library

```
Package Signing:           Go checksums + sig   →  6/6
Provenance / SLSA:        SLSA 3               →  5/6
Dependency Audit:          govulncheck          →  4/4
SBOM:                      Partial              →  2/4
Typosquatting:             Module path verified →  3/3
Reproducible CI:           Yes                  →  2/2
                                                    ────
Subtotal:                                            22/25
```

---

## 🔧 Dimension 3: Maintenance Health (20 points)

Measures ongoing maintenance and long-term viability.

### Sub-criteria

| Sub-criterion | Max Points | Description |
|---|---|---|
| Release Cadence | 5 | Regular releases: monthly+ = 5, quarterly = 4, biannual = 2, irregular = 1 |
| LTS / Support Policy | 5 | Clear LTS policy = 5, informal = 3, none = 0 |
| Open Issue Triage | 4 | Issues triaged <7d = 4, <30d = 2, >30d = 1, unmanaged = 0 |
| Breaking Change Management | 3 | Deprecation policy, migration guides = 3, partial = 1 |
| Documentation Quality | 3 | Comprehensive + security docs = 3, basic = 1, minimal = 0 |

### Scoring Example: PostgreSQL 16

```
Release Cadence:     Quarterly minor, annual major →  4/5
LTS / Support:       5yr support per major          →  5/5
Issue Triage:        <7d average                    →  4/4
Breaking Changes:    Strict backward compat         →  3/3
Documentation:       Excellent security docs        →  3/3
                                                      ────
Subtotal:                                              19/20
```

---

## 👥 Dimension 4: Community Trust (15 points)

Assesses the broader ecosystem trust and adoption signals.

### Sub-criteria

| Sub-criterion | Max Points | Description |
|---|---|---|
| Governance Model | 4 | Foundation-backed = 4, corporate-backed = 3, BDFL = 2, solo = 1 |
| Independent Audits | 4 | Multiple audits = 4, one audit = 2, none = 0 |
| Adoption Scale | 3 | npm/PyPI downloads, Docker pulls (relative category) |
| Corporate Contributors | 2 | >10 companies = 2, 3-10 = 1, <3 = 0 |
| CVE Response Transparency | 2 | Published security advisories, CVE process = 2, informal = 1 |

### Scoring Example: React

```
Governance:          Meta-backed + open governance →  3/4
Independent Audits:  None publicly known            →  0/4
Adoption:            Top 1 in frontend              →  3/3
Corporate Contributors: 50+ companies              →  2/2
CVE Transparency:    GitHub advisories              →  2/2
                                                    ────
Subtotal:                                            10/15
```

---

## 📦 Dimension 5: Reproducibility (10 points)

Ensures builds and deployments are deterministic and verifiable.

### Sub-criteria

| Sub-criterion | Max Points | Description |
|---|---|---|
| Lockfile Support | 3 | Native lockfile = 3, third-party = 1, none = 0 |
| Deterministic Builds | 3 | Bit-for-bit reproducible = 3, mostly = 1, no = 0 |
| Container Image Pinning | 2 | Digest-pinned images = 2, tag-only = 1, none = 0 |
| Checksum Verification | 2 | All artifacts checksummed = 2, partial = 1, none = 0 |

### Scoring Example: Deno

```
Lockfile:         deno.lock native           →  3/3
Deterministic:    Mostly reproducible        →  1/3
Container:        Digest-pinned official img  →  2/2
Checksums:        All releases checksummed   →  2/2
                                              ────
Subtotal:                                      8/10
```

---

## 🏆 Grade System

| Grade | Score Range | Meaning | Badge Color |
|---|---|---|---|
| **A+** | 95 – 100 | 🟢 Exceptional — Gold standard, recommended for high-security contexts | ![#00c853](https://via.placeholder.com/12/00c853/00c853.png) Green |
| **A** | 85 – 94 | 🟢 Excellent — Production-ready with strong security posture | ![#4caf50](https://via.placeholder.com/12/4caf50/4caf50.png) Green |
| **B+** | 75 – 84 | 🔵 Good — Solid choice, minor areas for improvement | ![#2196f3](https://via.placeholder.com/12/2196f3/2196f3.png) Blue |
| **B** | 65 – 74 | 🔵 Acceptable — Minimum tier for inclusion in this list | ![#64b5f6](https://via.placeholder.com/12/64b5f6/64b5f6.png) Light Blue |
| **C** | 50 – 64 | 🟡 Caution — Not listed; significant security concerns | ![#ffc107](https://via.placeholder.com/12/ffc107/ffc107.png) Yellow |
| **D** | 0 – 49 | 🔴 Avoid — Critical security gaps; actively discouraged | ![#f44336](https://via.placeholder.com/12/f44336/f44336.png) Red |

### Minimum Requirements for Inclusion

To be listed in **awesome-secure-stacks**, a stack must:

1. **Score ≥ 65 (Grade B)** overall
2. **No dimension below 40%** of its maximum (i.e., Vulnerability Posture ≥ 12/30, Supply Chain ≥ 10/25, etc.)
3. **Zero open Critical CVEs** at time of listing
4. **At least one component** must have an independent security audit on record

---

## 📋 Score Report Template

Each stack entry includes a score breakdown:

```
┌─────────────────────────────────────────────┐
│  📦 Stack: Node.js 22 + Express 5 + pnpm    │
│  🏅 Grade: A   |   Score: 87/100            │
├─────────────────────────────────────────────┤
│  🛡️ Vulnerability Posture    ████░░  23/30  │
│  🔗 Supply Chain Integrity   ██████░ 22/25  │
│  🔧 Maintenance Health       █████   19/20  │
│  👥 Community Trust          ███░    10/15  │
│  📦 Reproducibility          ████    8/10   │
├─────────────────────────────────────────────┤
│  ⏱️ Evaluated: 2026-05-31                    │
│  📝 Evaluator: @contributor                  │
│  📄 Full Report: stacks/backend.md#nodejs    │
└─────────────────────────────────────────────┘
```

---

## 🔄 Re-evaluation Triggers

A stack's score is re-evaluated:

| Trigger | Timeline |
|---|---|
| 📅 Scheduled review | Monthly (1st of each month) |
| 🚨 New Critical CVE | Within 24 hours |
| 🔗 Supply chain incident | Within 48 hours |
| 📦 Major version release | Within 1 week |
| 🗳️ Community report | Within 72 hours |

---

## 🤖 Automation

Scores are partially automated:

- **Automated data collection:** CVE feeds (NVD, GitHub Advisories, OSV), download stats, commit frequency
- **Human evaluation:** Audit quality, governance assessment, documentation review
- **CI pipeline:** `scripts/score.sh` pulls automated metrics; maintainers fill in human-scored fields

---

## 📚 References

- [NVD - National Vulnerability Database](https://nvd.nist.gov/)
- [OSV - Open Source Vulnerabilities](https://osv.dev/)
- [SLSA Framework](https://slsa.dev/)
- [Sigstore](https://www.sigstore.dev/)
- [OpenSSF Scorecard](https://securityscorecards.dev/)
- [CycloneDX SBOM Standard](https://cyclonedx.org/)
- [SPDX](https://spdx.dev/)

---

<p align="center">
  <i>This scoring methodology is versioned and open for community feedback.<br>
  Propose changes via <a href="https://github.com/awesome-secure-stacks/awesome-secure-stacks/issues">GitHub Issues</a>.</i>
</p>
