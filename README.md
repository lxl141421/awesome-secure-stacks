<p align="center">
  <img src="https://img.shields.io/badge/🔒-Secure%20Stacks-blue?style=for-the-badge&logo=shield&logoColor=white" alt="Secure Stacks">
</p>

<h1 align="center">🛡️ Awesome Secure Stacks</h1>

<p align="center">
  <b>Community-curated, security-audited technology stacks with verified version compatibility.</b><br>
  <i>No more guessing which dependencies are safe. Every stack — vetted, scored, and battle-tested.</i><br>
  <sub>不再猜测哪些依赖是安全的。每个技术栈——经过审核、评分和实战检验。</sub>
</p>

<p align="center">
  <a href="https://github.com/lxl141421/awesome-secure-stacks/stargazers"><img src="https://img.shields.io/github/stars/lxl141421/awesome-secure-stacks?style=social" alt="Stars"></a>
  &nbsp;
  <a href="https://github.com/lxl141421/awesome-secure-stacks/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square" alt="PRs Welcome"></a>
  &nbsp;
  <img src="https://img.shields.io/badge/last%20updated-2026--05--31-blue?style=flat-square" alt="Last Updated">
  &nbsp;
  <img src="https://img.shields.io/badge/security--audited-✓-brightgreen?style=flat-square&logo=checkmarx&logoColor=white" alt="Security Audited">
  &nbsp;
  <a href="https://github.com/lxl141421/awesome-secure-stacks/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT License"></a>
  &nbsp;
  <img src="https://img.shields.io/badge/stacks-40+-purple?style=flat-square" alt="40+ Stacks">
</p>

---

## 📖 Table of Contents

- [🚨 The Problem](#-the-problem)
- [💡 Our Solution](#-our-solution)
- [⚔️ How We're Different](#️-how-were-different)
- [🚀 Quick Start](#-quick-start)
- [📊 Scoring System](#-scoring-system)
- [⭐ Featured Stacks](#-featured-stacks)
- [📚 Stack Categories](#-stack-categories)
  - [🖥️ Web Frontend](#️-web-frontend)
  - [⚙️ Backend API](#️-backend-api)
  - [🗄️ Database](#️-database)
  - [🔧 DevOps & Infrastructure](#-devops--infrastructure)
  - [📱 Mobile](#-mobile)
  - [🤖 Machine Learning & AI](#-machine-learning--ai)
  - [⚡ Real-time & Messaging](#-real-time--messaging)
  - [🏗️ Full-stack Combos](#️-full-stack-combos)
- [🕘 Supply Chain Attack Timeline](#-supply-chain-attack-timeline)
- [🔒 Security Advisories](#-security-advisories)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

---

## 🚨 The Problem

> **Software supply chain attacks increased 742% from 2019 to 2022.** They're not slowing down.
> — _Sonatype State of the Software Supply Chain Report_

The modern software ecosystem is built on trust — trust in packages you've never audited, maintained by people you've never met, pulling in hundreds of transitive dependencies you didn't choose. **This trust is being exploited.**

### Notable Supply Chain Incidents

| Year | Incident | Impact | Severity |
|------|----------|--------|----------|
| 🔴 2024 | **XZ Utils Backdoor** (`xz` 5.6.x) | Nearly compromised all major Linux distros via a years-long social engineering campaign | 🔴 Critical |
| 🔴 2021 | **`event-stream` / `flatmap-stream`** | Targeted cryptocurrency theft via compromised dependency of a popular npm package | 🔴 Critical |
| 🔴 2021 | **`ua-parser-js`** (70M+ weekly downloads) | Crypto miners and password stealers injected into hijacked versions | 🔴 Critical |
| 🟡 2022 | **`colors.js` / `faker.js` protest** | Intentional sabotage by maintainer broke thousands of CI/CD pipelines | 🟡 High |
| 🔴 2020 | **SolarWinds Orion** | Nation-state attack affecting 18,000+ organizations including US government agencies | 🔴 Critical |
| 🟡 2023 | **PyTorch `torchtriton`** | Malicious package on PyPI with the same name as a nightly dependency | 🟡 High |
| 🔴 2022 | **`node-ipc`** (protestware) | Deliberate data-wiping code targeting Russian and Belarusian IP addresses | 🔴 Critical |
| 🟡 2021 | **Codecov Bash Uploader** | Compromised CI tool exfiltrated environment variables (secrets) from CI pipelines | 🟡 High |

**The pattern is clear:** our dependency chains are attack surfaces, and most teams have no systematic way to evaluate which combinations of tools are safe. 我们的依赖链就是攻击面，而大多数团队没有系统的方法来评估哪些工具组合是安全的。

---

## 💡 Our Solution

**Awesome Secure Stacks** is a **community-curated, rigorously evaluated collection of complete technology stacks** — not individual packages, but **tested combinations** of tools, frameworks, libraries, and infrastructure that work together securely.

### What We Provide

For every stack, you get:

- ✅ **Pinned, verified versions** — exact versions that have been tested together
- ✅ **Security Score (0–100)** — computed from 5 dimensions (see [SCORING.md](SCORING.md))
- ✅ **Dependency audit results** — known CVEs, transitive dependency analysis
- ✅ **Supply chain integrity checks** — signing, provenance, SBOM availability
- ✅ **Compatibility matrix** — which versions of each component work together
- ✅ **Reproduction instructions** — lockfiles, Docker images, setup scripts
- ✅ **Monthly re-evaluation** — scores are updated on a regular cadence

> **Think of it as a "recommended hardware compatibility list" but for software security.**
> 就像硬件兼容性列表，但用于软件安全。

---

## ⚔️ How We're Different

### vs. Awesome-xxx Lists

| Aspect | Typical `awesome-*` Lists | **Awesome Secure Stacks** |
|--------|---------------------------|---------------------------|
| Focus | Popularity, features | **Security, integrity, compatibility** |
| Evaluation | Subjective, opinion-based | **Quantitative scoring (0–100)** |
| Versions | Rarely specified | **Pinned and verified** |
| Dependencies | Ignored | **Full transitive analysis** |
| Updates | Whenever someone bothers | **Monthly automated + event-driven** |
| Scope | Individual packages | **Complete, tested stacks** |

### vs. CVE Databases (NVD, OSV, GitHub Advisories)

CVE databases tell you **what's broken**. We tell you **what works together safely**. CVE databases are reactive; we are proactive. We consume CVE data as input, not as output.

### vs. Sigstore / SLSA / in-toto

These are **build-time attestation tools** — they verify *how* software was built. We verify *what combinations* of software are secure to use together. **They are complementary to our mission**, and we incorporate their data into our scoring. Sigstore/SLSA 是构建时的证明工具——它们验证软件是如何构建的。我们验证哪些软件组合可以安全地一起使用。

### vs. OpenSSF Scorecard

OpenSSF Scorecard evaluates **individual projects**. We evaluate **stack combinations** — how frameworks, databases, runtimes, and tooling interact. A project with a great Scorecard might still be part of a vulnerable stack if it pulls in risky transitive dependencies.

---

## 🚀 Quick Start

### 1. Find a Stack

Browse the [Stack Categories](#-stack-categories) or search directly:

```bash
# Clone the repository
git clone https://github.com/lxl141421/awesome-secure-stacks.git
cd awesome-secure-stacks

# Search for stacks by technology
grep -r "react" stacks/ --include="*.md" -l
grep -r "postgresql" stacks/ --include="*.md" -l

# View a specific stack
cat stacks/frontend.md
```

### 2. Understand the Score

Every stack entry looks like this:

```
### 🏷️ React 18 + Next.js 15 + TypeScript 5.5

| Component | Version | Score |
|-----------|---------|-------|
| React | 18.3.1 | A |
| Next.js | 15.1.0 | A |
| TypeScript | 5.5.4 | A+ |
| pnpm | 9.12.0 | A |

**Stack Security Score: 91/100 (A)**
Full report: stacks/frontend.md#react-nextjs-ts
```

See [SCORING.md](SCORING.md) for the complete methodology.

### 3. Use a Stack

Each stack entry includes a **reproduction template** — a lockfile, Docker Compose, or setup script to get started with the exact verified versions.

```bash
# Example: bootstrap a verified Next.js stack
cd templates/react-nextjs-ts/
cp .env.example .env
docker compose up -d
# ✅ Running verified stack with pinned dependencies
```

### 4. Stay Updated

- ⭐ **Star** this repo to get notified of score changes
- 👀 **Watch** for security advisory releases
- 📡 Subscribe to our [RSS feed](https://github.com/lxl141421/awesome-secure-stacks/releases.atom) for monthly score updates

---

## 📊 Scoring System

Every stack is scored **0–100** across five dimensions:

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| 🛡️ **Vulnerability Posture** | 30 pts | Known CVEs, patch velocity, audit history |
| 🔗 **Supply Chain Integrity** | 25 pts | Signing, provenance, SBOM, typosquatting protection |
| 🔧 **Maintenance Health** | 20 pts | Release cadence, LTS policy, issue triage |
| 👥 **Community Trust** | 15 pts | Governance, audits, adoption scale |
| 📦 **Reproducibility** | 10 pts | Lockfiles, deterministic builds, checksums |

### Grade Scale

| Grade | Score | Meaning |
|-------|-------|---------|
| 🟢 **A+** | 95–100 | Exceptional — Gold standard |
| 🟢 **A** | 85–94 | Excellent — Highly recommended |
| 🔵 **B+** | 75–84 | Good — Solid choice |
| 🔵 **B** | 65–74 | Acceptable — Minimum for inclusion |
| 🟡 **C** | 50–64 | Caution — Not listed (significant concerns) |
| 🔴 **D** | 0–49 | Avoid — Critical security gaps |

> 📋 **Full methodology:** See [SCORING.md](SCORING.md)

**Minimum requirements for listing:**
- Overall score ≥ **65 (Grade B)**
- No dimension below **40%** of its maximum
- Zero open Critical CVEs
- At least one independent security audit on record

---

## ⭐ Featured Stacks

Hand-picked stacks that represent the best of each category. 推荐技术栈。

---

### 🥇 Next.js 15 + React 18 + TypeScript 5.5 + pnpm

> **Score: 93/100 (A)** · Category: [Web Frontend](stacks/frontend.md)

A production-grade frontend stack with excellent supply chain integrity. TypeScript catches type errors early, pnpm's content-addressable storage prevents phantom dependencies, and Next.js's server-side rendering reduces client-side attack surface.

**Why it's featured:**
- 🔒 TypeScript 5.5 has had zero Critical CVEs in 2 years
- 📦 pnpm's strict dependency resolution eliminates phantom dependencies
- 🏛️ Vercel maintains active security response program
- ✅ All components sign releases

---

### 🥇 Go 1.22 + Chi Router + PostgreSQL 16 + sqlc

> **Score: 95/100 (A+)** · Category: [Backend API](stacks/backend.md)

The gold standard for secure backend development. Go's static compilation eliminates runtime dependency attacks, Chi is a minimal and well-audited router, and sqlc generates type-safe SQL from queries — no ORM injection surface.

**Why it's featured:**
- 🛡️ Go's `govulncheck` provides first-class vulnerability scanning
- 📦 Go modules have cryptographic verification by default (checksum database)
- 🔒 sqlc eliminates SQL injection by design (compile-time code generation)
- 🏢 Backed by Google (Go) + PostgreSQL Global Development Group

---

### 🥇 Rust + Axum + SeaORM + SQLite/PostgreSQL

> **Score: 91/100 (A)** · Category: [Backend API](stacks/backend.md)

Memory-safe by default. Rust eliminates entire vulnerability classes (buffer overflows, use-after-free) at compile time. Axum is built on Tokio and Hyper — battle-tested foundations. SeaORM provides safe database access with compile-time query validation.

**Why it's featured:**
- 🦀 Memory safety without garbage collection — eliminates ~70% of CVEs by category
- 📦 Cargo has built-in audit (`cargo audit`) with advisory database
- 🔒 `unsafe` usage is explicit and auditable
- 🏛️ Rust Foundation (Mozilla, AWS, Google, Microsoft, Meta)

---

### 🥇 Terraform 1.9 + AWS (EKS) + ArgoCD + SOPS

> **Score: 89/100 (A)** · Category: [DevOps & Infrastructure](stacks/devops.md)

Infrastructure-as-code with GitOps delivery. Every infrastructure change is version-controlled, reviewed, and auditable. SOPS provides secret encryption at rest, ArgoCD ensures drift detection, and Terraform's provider ecosystem is HashiCorp-signed.

**Why it's featured:**
- 🔐 SOPS encrypts secrets with AWS KMS / GCP KMS / age
- 🔄 ArgoCD provides declarative, auditable deployments
- 📦 Terraform providers are signed by HashiCorp
- 📋 Infrastructure state is fully reproducible

---

## 📚 Stack Categories

### 🖥️ Web Frontend

**File:** [`stacks/frontend.md`](stacks/frontend.md)

Frameworks, bundlers, CSS solutions, and client-side security tools. Covers React, Vue, Svelte, Angular, and emerging frameworks with their recommended companion tools.

> **Featured:** React 18 + Next.js 15, Vue 3 + Nuxt 3, SvelteKit 2, Angular 18

---

### ⚙️ Backend API

**File:** [`stacks/backend.md`](stacks/backend.md)

Server-side runtimes, web frameworks, ORMs, authentication libraries, and API security tools. Covers Node.js, Go, Rust, Python, Java, and .NET ecosystems.

> **Featured:** Go + Chi + sqlc, Rust + Axum, Node.js 22 + Fastify, Python 3.12 + FastAPI

---

### 🗄️ Database

**File:** [`stacks/database.md`](stacks/database.md)

Relational, document, key-value, and time-series databases with their client libraries, migration tools, and connection pooling solutions.

> **Featured:** PostgreSQL 16, SQLite 3.46, Redis 7.4, CockroachDB, ClickHouse

---

### 🔧 DevOps & Infrastructure

**File:** [`stacks/devops.md`](stacks/devops.md)

Infrastructure-as-code, CI/CD, container orchestration, secret management, observability, and cloud provider tools.

> **Featured:** Terraform + ArgoCD, Kubernetes 1.30, GitHub Actions, Dagger

---

### 📱 Mobile

**File:** [`stacks/mobile.md`](stacks/mobile.md)

Cross-platform and native mobile development frameworks, state management, navigation, and mobile-specific security tooling.

> **Featured:** React Native 0.75 + Expo, Flutter 3.24, Kotlin Multiplatform

---

### 🤖 Machine Learning & AI

**File:** [`stacks/ml-ai.md`](stacks/ml-ai.md)

ML frameworks, model serving, vector databases, LLM tooling, and data pipeline security. Special focus on model supply chain (provenance, adversarial robustness).

> **Featured:** PyTorch 2.4 + vLLM, JAX + Flax, scikit-learn + ONNX Runtime

---

### ⚡ Real-time & Messaging

**File:** [`stacks/realtime.md`](stacks/realtime.md)

WebSockets, SSE, pub/sub, message queues, and real-time collaboration tools with security considerations for persistent connections.

> **Featured:** Socket.IO 4.x, Ably/Pusher (managed), NATS, Redis Streams

---

### 🏗️ Full-stack Combos

**File:** [`stacks/fullstack.md`](stacks/fullstack.md)

Pre-verified end-to-end combinations spanning frontend, backend, database, and deployment. Complete application blueprints with security scores for the full dependency graph.

> **Featured:** T3 Stack (Next.js + tRPC + Prisma), Rails 7 Full Stack, Django + htmx + Alpine.js

---

## 🕘 Supply Chain Attack Timeline

A chronological history of major supply chain attacks that motivate this project:

```
2017 ──────────────────────────────────────────────────────────── 2026
  │                                                                │
  ├─ 2017-11  event-stream / flatmap-stream                       │
  │           Cryptocurrency wallet theft via trusted npm dep     │
  │                                                                │
  ├─ 2020-03  eslint-scope                                         │
  │           Stolen npm credentials exfiltrated env variables    │
  │                                                                │
  ├─ 2020-12  SolarWinds Orion (SUNBURST)                          │
  │           Nation-state attack, 18,000+ orgs compromised       │
  │                                                                │
  ├─ 2021-01  ua-parser-js (70M weekly downloads)                  │
  │           Crypto miners + password stealers injected           │
  │                                                                │
  ├─ 2021-10  Codecov Bash Uploader                                │
  │           CI secrets exfiltrated via compromised tool          │
  │                                                                │
  ├─ 2022-01  colors.js / faker.js (protestware)                   │
  │           Intentional infinite loop broke CI pipelines         │
  │                                                                │
  ├─ 2022-03  node-ipc (protestware)                               │
  │           Data-wiping code targeted by IP geolocation          │
  │                                                                │
  ├─ 2022-12  PyTorch torchtriton (dependency confusion)           │
  │           Malicious PyPI package with identical name           │
  │                                                                │
  ├─ 2023-03  3CX Desktop App                                     │
  │           First publicly documented cascading supply chain    │
  │                                                                │
  ├─ 2024-03  XZ Utils (CVE-2024-3094)                             │
  │           Multi-year social engineering → sshd backdoor       │
  │                                                                │
  ├─ 2025-01  tj-actions/changed-files (GitHub Actions)            │
  │           Compromised CI action leaked secrets from repos     │
  │                                                                │
  └─ 2026-??  The next one is being planned right now.            │
              这个项目正是为了应对下一个攻击而存在。
              Stay vigilant. Use verified stacks. 🔒              │
```

---

## 🔒 Security Advisories

### Reporting a Stack Vulnerability

If you discover a security issue in any recommended stack:

1. **DO NOT** open a public GitHub issue
2. 📧 Email: **security@awesome-secure-stacks.dev** (PGP key available at [SECURITY.md](SECURITY.md))
3. 🔐 Use our [security advisory template](.github/SECURITY_ADVISORY_TEMPLATE.md)
4. ⏱️ We aim to respond within **48 hours** and publish advisories within **7 days**

### Advisory Format

Each advisory follows the [OpenSSF OpenVEX](https://openvex.dev/) format:

```
Advisory: ASSA-2026-001
Severity: High (CVSS 8.1)
Affected Stacks: backend-go-chi, fullstack-t3
Component: golang.org/x/crypto v0.21.0
Fixed In: v0.22.0
Status: Resolved
Published: 2026-05-15
```

### Subscribe to Advisories

- 🔔 **GitHub Watch** → "Releases only"
- 📡 **Atom feed:** [`/advisories.atom`](https://github.com/lxl141421/awesome-secure-stacks/releases.atom)
- 🐦 **Twitter/X:** [@secure_stacks](https://twitter.com/secure_stacks)

---

## 🤝 Contributing

We welcome contributions! But security curation requires rigor. 贡献安全策展需要严谨性。

### How to Contribute

| Type | How | Difficulty |
|------|-----|------------|
| 🐛 Report a scoring error | [Open an issue](https://github.com/lxl141421/awesome-secure-stacks/issues/new?template=bug_report.md) | Easy |
| 📦 Propose a new stack | [Stack proposal template](https://github.com/lxl141421/awesome-secure-stacks/issues/new?template=stack_proposal.md) | Medium |
| 📊 Update a score | [Score update PR](https://github.com/lxl141421/awesome-secure-stacks/compare) | Medium |
| 🔍 Audit a stack | [Audit guide](CONTRIBUTING.md#auditing-a-stack) | Hard |
| 📝 Improve docs | [Standard PR](https://github.com/lxl141421/awesome-secure-stacks/compare) | Easy |

### Contribution Guidelines

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines
2. All new stacks must include a **reproduction template** (lockfile or Docker Compose)
3. Score changes require **evidence** (CVE links, audit reports, tool output)
4. Use our [PR template](.github/PULL_REQUEST_TEMPLATE.md) for all submissions
5. Be respectful and follow our [Code of Conduct](CODE_OF_CONDUCT.md)

### Adding a New Stack

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/awesome-secure-stacks.git

# 2. Create a branch
git checkout -b add/my-awesome-stack

# 3. Add your stack entry to the appropriate category file
#    Follow the template in CONTRIBUTING.md

# 4. Run the scoring script
./scripts/score.sh --stack my-awesome-stack

# 5. Submit PR with evidence
git push origin add/my-awesome-stack
```

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Awesome Secure Stacks Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

> **Why MIT?** Security knowledge should be freely accessible. We chose MIT to maximize adoption and contribution.

---

## 🙏 Acknowledgments

This project would not be possible without:

- 🏛️ **[OpenSSF](https://openssf.org/)** — for Scorecard, SLSA, and Sigstore foundations
- 🔍 **[Sonatype](https://www.sonatype.com/)** — for State of the Software Supply Chain reports
- 🛡️ **[Snyk](https://snyk.io/)** — for vulnerability database and research
- 📦 **[npm](https://www.npmjs.com/), [PyPI](https://pypi.org/), [crates.io](https://crates.io/)** — for package ecosystems
- 🐙 **[GitHub Security](https://github.com/security)** — for Advisory Database and Dependabot
- 🌐 **[CISA](https://www.cisa.gov/)** — for SBOM guidance and supply chain security advocacy
- 💜 **All contributors** who audit, test, and maintain the stack entries
- 🦀 **The Rust community** — for proving that memory safety can be the default
- 🐧 **The Linux kernel community** — for the hard lessons learned from XZ

### Special Thanks

- **XZ Utils incident responders** — whose work highlighted the urgency of supply chain security
- **The `event-stream` incident reporters** — who first showed the npm ecosystem's vulnerability
- **Every maintainer** who signs their releases, publishes SBOMs, and responds to CVEs responsibly

---

<p align="center">
  <b>⭐ If this project helps you ship more secure software, give it a star! ⭐</b><br><br>
  <a href="https://github.com/lxl141421/awesome-secure-stacks/stargazers">
    <img src="https://img.shields.io/github/stars/lxl141421/awesome-secure-stacks?style=social" alt="Stars">
  </a>
</p>

---

<p align="center">
  <sub>
    Made with 🔒 by the security community.<br>
    <a href="https://github.com/lxl141421/awesome-secure-stacks">GitHub</a> · 
    <a href="https://github.com/lxl141421/awesome-secure-stacks/issues">Issues</a> · 
    <a href="https://github.com/lxl141421/awesome-secure-stacks/discussions">Discussions</a>
  </sub>
</p>
