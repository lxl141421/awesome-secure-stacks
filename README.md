<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/English-blue?style=flat-square" alt="English"></a>
  <a href="README_zh.md"><img src="https://img.shields.io/badge/中文-grey?style=flat-square" alt="中文"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/🛡️-Awesome_Secure_Stacks-blue?style=for-the-badge&logo=shield&logoColor=white" alt="Awesome Secure Stacks" width="400">
</p>

<h1 align="center">🛡️ Awesome Secure Stacks</h1>

<p align="center">
  <b>Community-curated, security-audited technology stacks with verified version compatibility.</b><br>
  <i>The definitive reference for building secure, production-ready software stacks.</i><br>
  <sub>社区策展、安全审计的技术栈，版本兼容性经过验证 — 构建安全软件栈的权威参考。</sub>
</p>

<p align="center">
  <a href="https://github.com/lxl141421/awesome-secure-stacks/stargazers"><img src="https://img.shields.io/github/stars/lxl141421/awesome-secure-stacks?style=social" alt="Stars"></a>
  &nbsp;
  <a href="https://github.com/lxl141421/awesome-secure-stacks/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square" alt="PRs Welcome"></a>
  &nbsp;
  <img src="https://img.shields.io/badge/last%20updated-2025--05-blue?style=flat-square" alt="Last Updated">
  &nbsp;
  <img src="https://img.shields.io/badge/security--audited-✓-brightgreen?style=flat-square&logo=checkmarx&logoColor=white" alt="Security Audited">
  &nbsp;
  <a href="https://github.com/lxl141421/awesome-secure-stacks/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT License"></a>
  &nbsp;
  <img src="https://img.shields.io/badge/stacks-60+-purple?style=flat-square" alt="60+ Stacks">
</p>

---

> **Stop guessing which dependencies are safe. Every stack — vetted, scored, and proven in production.**
> We don't chase the latest version. We recommend the **safest, most stable, fewest-bug** version of every component.
> 不追最新，只推最稳。每个技术栈——经过审核、评分，生产环境验证。

---

## 📖 Table of Contents

- [🚨 The Problem](#-the-problem)
- [💡 Our Solution](#-our-solution)
- [⚔️ How We're Different](#️-how-were-different)
- [🚀 Quick Start](#-quick-start)
- [📊 Scoring System](#-scoring-system)
- [⭐ Featured Stacks](#-featured-stacks)
  - [🥇 Full-stack Web: React 18.3 + Next.js 14.2 + TypeScript 5.6](#-full-stack-web-react-183--nextjs-142--typescript-56)
  - [🥇 Backend API: Go 1.22 + Chi 5.2 + PostgreSQL 16.4](#-backend-api-go-122--chi-52--postgresql-164)
  - [🥇 Systems Backend: Rust 1.80 + Axum 0.7](#-systems-backend-rust-180--axum-07)
  - [🥇 DevOps & Infrastructure: Terraform 1.12 + Kubernetes 1.33](#-devops--infrastructure-terraform-112--kubernetes-133)
- [📚 Stack Categories](#-stack-categories)
  - [🖥️ Web Frontend](#️-web-frontend)
  - [⚙️ Backend API](#️-backend-api)
  - [🗄️ Database](#️-database)
  - [🔧 DevOps & Infrastructure](#-devops--infrastructure)
  - [📱 Mobile](#-mobile)
  - [🤖 Machine Learning & AI](#-machine-learning--ai)
  - [⚡ Real-time & Messaging](#-real-time--messaging)
  - [🏗️ Full-stack Combos](#️-full-stack-combos)
  - [🖥️ Desktop Applications](#️-desktop-applications)
  - [🌐 Hybrid & WebView](#-hybrid--webview)
  - [🎮 Game Development](#-game-development)
  - [🤖 AI-Assisted Development](#-ai-assisted-development)
  - [🧠 AI/LLM Applications](#-aillm-applications)
  - [📱 Native Mobile & Cross-Platform Deep Dive](#-native-mobile--cross-platform-deep-dive)
  - [🔄 Architecture Evolution](#-architecture-evolution)
  - [🔗 Distributed Systems & Microservices](#-distributed-systems--microservices)
- [🕘 Supply Chain Attack Timeline](#-supply-chain-attack-timeline)
- [🔒 Security Advisories](#-security-advisories)
- [🤝 Contributing](#-contributing)
- [🗺️ Roadmap](#️-roadmap)
- [📜 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

---

## 🚨 The Problem

> **Software supply chain attacks increased 742% from 2019 to 2022.** They're not slowing down.
> — _Sonatype State of the Software Supply Chain Report_

The modern software ecosystem is built on **trust** — trust in packages you've never audited, maintained by people you've never met, pulling in hundreds of transitive dependencies you didn't choose. **This trust is being exploited.**

Every `npm install`, every `pip install`, every `go mod download` is an act of faith. And attackers are turning that faith into a weapon — targeting the weakest links in our dependency chains with increasing sophistication.

### Notable Supply Chain Incidents

| Year | Incident | Impact | Severity |
|------|----------|--------|----------|
| 🔴 2024 | **XZ Utils Backdoor** (`xz` 5.6.x) | Nearly compromised all major Linux distros via a years-long social engineering campaign | 🔴 Critical |
| 🔴 2018 | **`event-stream` / `flatmap-stream`** | Targeted cryptocurrency theft via compromised dependency of a popular npm package | 🔴 Critical |
| 🔴 2021 | **`ua-parser-js`** (70M+ weekly downloads) | Crypto miners and password stealers injected into hijacked versions | 🔴 Critical |
| 🔴 2020 | **SolarWinds Orion** | Nation-state attack affecting 18,000+ organizations including US government agencies | 🔴 Critical |
| 🟡 2022 | **`colors.js` / `faker.js` protest** | Intentional sabotage by maintainer broke thousands of CI/CD pipelines | 🟡 High |
| 🔴 2022 | **`node-ipc`** (protestware) | Deliberate data-wiping code targeting Russian and Belarusian IP addresses | 🔴 Critical |
| 🟡 2021 | **Codecov Bash Uploader** | Compromised CI tool exfiltrated environment variables (secrets) from CI pipelines | 🟡 High |
| 🟡 2023 | **PyTorch `torchtriton`** | Malicious package on PyPI with the same name as a nightly dependency | 🟡 High |

**The pattern is clear:** our dependency chains are attack surfaces, and most teams have no systematic way to evaluate which combinations of tools are safe. 我们的依赖链就是攻击面，而大多数团队没有系统的方法来评估哪些工具组合是安全的。

---

## 💡 Our Solution

**Awesome Secure Stacks** is a **community-curated, rigorously evaluated collection of complete technology stacks** — not individual packages, but **tested combinations** of tools, frameworks, libraries, and infrastructure that work together securely.

We do the hard work of auditing entire dependency graphs so you don't have to.

### What We Provide for Every Stack

For every stack entry in this repository, you get:

- ✅ **Pinned, verified versions** — the **safest, most stable** versions, not necessarily the latest
- ✅ **Security Score (0–100)** — computed from 5 dimensions (see [SCORING.md](SCORING.md))
- ✅ **CVE analysis** — known vulnerabilities, transitive dependency risk, patch velocity
- ✅ **Lockfile templates** — reproducible dependency files to freeze your supply chain
- ✅ **Docker configurations** — hardened container images with pinned base layers
- ✅ **Alternatives & trade-offs** — when a stack has security concerns, we suggest safer options
- ✅ **Compatibility matrix** — which versions of each component work together
- ✅ **Monthly re-evaluation** — scores are updated on a regular cadence

> **Think of it as a "recommended hardware compatibility list" — but for software security.**
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

CVE databases tell you **what's broken**. We tell you **what works together safely**. CVE databases are reactive; we are proactive. We consume CVE data as input, not as output. Our scoring incorporates CVE data, maintenance history, signing practices, and more into a single actionable number.

### vs. Sigstore / SLSA / in-toto

These are **build-time attestation tools** — they verify *how* software was built. We verify *what combinations* of software are secure to use together. **They are complementary to our mission**, and we incorporate their data into our scoring. Sigstore/SLSA 是构建时的证明工具——它们验证软件是如何构建的。我们验证哪些软件组合可以安全地一起使用。

### vs. OpenSSF Scorecard

OpenSSF Scorecard evaluates **individual projects**. We evaluate **stack combinations** — how frameworks, databases, runtimes, and tooling interact. A project with a great Scorecard might still be part of a vulnerable stack if it pulls in risky transitive dependencies. Our stack-level analysis catches what project-level analysis cannot.

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/lxl141421/awesome-secure-stacks.git
cd awesome-secure-stacks
```

### 2. Browse Stacks

```bash
# List all available stack categories
ls stacks/

# Search for stacks by technology
grep -r "react" stacks/ --include="*.md" -l
grep -r "postgresql" stacks/ --include="*.md" -l

# View a specific category
cat stacks/frontend.md
```

### 3. Understand the Score

Every stack entry follows this format:

```
### 🏷️ React 19.1 + Next.js 15.3 + TypeScript 5.8

| Component | Version | Score |
|-----------|---------|-------|
| React     | 19.1    | A+    |
| Next.js   | 15.3    | A     |
| TypeScript| 5.8     | A+    |
| pnpm      | 9.12    | A     |

**Stack Security Score: 93/100 (A)**
```

See [SCORING.md](SCORING.md) for the complete methodology.

### 4. Use a Stack Template

Each stack category includes **reproduction templates** — lockfiles, Docker Compose files, and setup scripts to get started with the exact verified versions.

```bash
# Example: bootstrap a verified Django stack
cd templates/
cat docker-compose-django.yml
# Review and customize, then:
docker compose -f docker-compose-django.yml up -d
# ✅ Running verified stack with pinned dependencies
```

Available templates:

```bash
ls templates/
# docker-compose-django.yml
# docker-compose-fastapi.yml
# docker-compose-t3-stack.yml
# lockfile-verification.md
# README.md
```

### 5. Stay Updated

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
| 🟢 **A+** | 95–100 | Exceptional — Gold standard, exemplary security practices |
| 🟢 **A** | 85–94 | Excellent — Highly recommended for production use |
| 🔵 **B+** | 75–84 | Good — Solid choice with minor areas for improvement |
| 🔵 **B** | 65–74 | Acceptable — Minimum threshold for inclusion in this list |
| 🟡 **C** | 50–64 | Caution — Not listed (significant security concerns) |
| 🔴 **D** | 0–49 | Avoid — Critical security gaps, not recommended |

> 📋 **Full methodology:** See [SCORING.md](SCORING.md)

**Minimum requirements for listing:**

- Overall score ≥ **65 (Grade B)**
- No dimension below **40%** of its maximum
- Zero open Critical CVEs
- At least one independent security audit on record

---

## 🎯 Version Philosophy: Stability Over Novelty

> **"Latest" does not mean "safest." A version released last week has zero production track record.**

Our version selection follows a strict **stability-first** principle:

### Selection Rules

| Rule | Rationale |
|------|-----------|
| 🏆 **Prefer LTS over Current** | LTS releases receive backported security fixes for years |
| ⏳ **Prefer .2+ over .0** | First patch release proves the major version is stable |
| 🔍 **6+ months production track record** | Enough time for community to surface real-world bugs |
| 🚫 **Avoid known regressions** | We track issue trackers — versions with confirmed regressions are flagged |
| 🛡️ **Prefer versions with security audits** | Independently audited versions score higher |
| 📦 **Minimize transitive dependencies** | Fewer dependencies = smaller attack surface |

### What This Means in Practice

| ❌ What We DON'T Do | ✅ What We DO |
|---------------------|---------------|
| Recommend Node.js 24 (released weeks ago) | Recommend **Node.js 22 LTS** (battle-tested, 2yr support) |
| Recommend React 19 (new major, breaking changes) | Recommend **React 18.3** (proven in millions of apps) |
| Recommend PostgreSQL 17 (new major) | Recommend **PostgreSQL 16.x** (years of production hardening) |
| Recommend Svelte 5 (complete rewrite) | Recommend **Svelte 4.x** (stable, well-understood) |
| Recommend Redis 8.0 (new license controversy) | Recommend **Redis 7.4** (OSS license, proven track record) |
| Recommend Angular 19 (just released) | Recommend **Angular 18 LTS** (official long-term support) |

> **Our motto: We'd rather be boring and secure than exciting and vulnerable.**
> 我们宁可无聊但安全，也不要炫酷但有漏洞。

---

## ⭐ Featured Stacks

Hand-picked stacks that represent the best of each category. 推荐技术栈 — 每个类别中最佳的代表。

---

### 🥇 Full-stack Web: React 18.3 + Next.js 14.2 + TypeScript 5.6

> **Score: 95/100 (A+)** · Category: [Web Frontend](stacks/frontend.md) | [Full-stack Combos](stacks/fullstack.md)

The most battle-tested frontend stack available. React 18.3 is deployed in millions of production applications worldwide. Next.js 14.2 has received extensive security patching and is the recommended production release. TypeScript 5.6 has zero Critical CVEs and years of proven stability.

**Components & Versions:**

| Component | Version | Individual Score | Notes |
|-----------|---------|------------------|-------|
| React | 18.3 | A+ | Meta-backed, signed releases, SBOM, millions of production apps |
| Next.js | 14.2 | A | Vercel-maintained, 14.x is the proven production release |
| TypeScript | 5.6 | A+ | Zero Critical CVEs in 3+ years |
| Vite | 5.6 | A | Stable 5.x line, extensive production use |
| Node.js | 22 LTS | A+ | Long-term support until 2027, regular security patches |
| pnpm | 9.12 | A | Content-addressable storage, strict resolution |

**Why it's featured:**

- 🏆 **Stability choice**: React 18.3 over 19.x — 18.x is proven in millions of production apps; 19.x is too new
- 🔒 TypeScript 5.6 has had zero Critical CVEs in 3+ years — a remarkable security record
- 📦 pnpm's strict dependency resolution eliminates phantom dependencies and supply chain confusion attacks
- 🏛️ Next.js 14.2 is the stable production release — 15.x introduces breaking changes and is less battle-tested
- ✅ All components sign their releases and publish provenance attestations

---

### 🥇 Backend API: Go 1.22 + Chi 5.2 + PostgreSQL 16.4

> **Score: 96/100 (A+)** · Category: [Backend API](stacks/backend.md) | [Database](stacks/database.md)

The gold standard for secure backend development. Go's static compilation eliminates runtime dependency attacks, Chi is a minimal and well-audited router with zero dependencies, and PostgreSQL 16.4 has years of production hardening with zero critical vulnerabilities.

**Components & Versions:**

| Component | Version | Individual Score | Notes |
|-----------|---------|------------------|-------|
| Go | 1.22 | A+ | Google-backed, checksum database by default, proven stable |
| Chi | 5.2 | A+ | Zero external dependencies, minimal attack surface |
| PostgreSQL | 16.4 | A+ | 30+ years of security hardening, 16.x is the proven production release |
| sqlc | 1.28 | A | Compile-time SQL codegen, eliminates injection |

**Why it's featured:**

- 🏆 **Stability choice**: Go 1.22 over 1.24 — 1.22 is the proven previous stable with extensive production use
- 🏆 **Stability choice**: PostgreSQL 16.4 over 17.x — 16.x has years of production hardening; 17.x is a new major
- 🛡️ Go's `govulncheck` provides first-class vulnerability scanning built into the toolchain
- 📦 Go modules have cryptographic verification by default via the checksum database (sum.golang.org)
- 🔒 sqlc eliminates SQL injection by design — queries are validated at compile time, not runtime

---

### 🥇 Systems Backend: Rust 1.80 + Axum 0.7

> **Score: 95/100 (A+)** · Category: [Backend API](stacks/backend.md)

Memory-safe by default. Rust eliminates entire vulnerability classes (buffer overflows, use-after-free, data races) at compile time. Axum 0.7 is built on Tokio and Hyper — battle-tested foundations handling millions of production requests. Actix-web 4.8 is available as an alternative with similar security posture.

**Components & Versions:**

| Component | Version | Individual Score | Notes |
|-----------|---------|------------------|-------|
| Rust | 1.87 | A+ | Memory safety without GC, ~70% of CVE classes eliminated |
| Axum | 0.8 | A | Tokio-backed, Tower middleware ecosystem |
| Actix-web | 4.11 | A | Alternative framework, equally well-audited |
| Cargo | (bundled) | A | Built-in audit, advisory database integration |

**Why it's featured:**

- 🦀 Memory safety without garbage collection — eliminates ~70% of CVEs by category at compile time
- 📦 Cargo has built-in audit (`cargo audit`) with RustSec advisory database integration
- 🔒 `unsafe` usage is explicit, auditable, and flagged in code review
- 🏛️ Rust Foundation (Mozilla, AWS, Google, Microsoft, Meta) ensures long-term governance
- 🛡️ Rust 1.87 includes enhanced `unsafe` diagnostics and improved supply chain tooling

---

### 🥇 DevOps & Infrastructure: Terraform 1.12 + Kubernetes 1.33

> **Score: 91/100 (A)** · Category: [DevOps & Infrastructure](stacks/devops.md)

Infrastructure-as-code with container orchestration. Every infrastructure change is version-controlled, reviewed, and auditable. Docker 28.1 provides hardened container runtimes, Kubernetes 1.33 brings enhanced pod security standards, and Terraform 1.12's provider ecosystem is HashiCorp-signed with SLSA provenance.

**Components & Versions:**

| Component | Version | Individual Score | Notes |
|-----------|---------|------------------|-------|
| Terraform | 1.12 | A | HashiCorp-signed providers, state encryption |
| Kubernetes | 1.33 | A | Enhanced pod security, signed releases |
| Docker | 28.1 | A | Content trust, image signing by default |
| ArgoCD | 2.13 | A | GitOps, declarative auditable deployments |

**Why it's featured:**

- 🔐 All Terraform providers are signed by HashiCorp — tamper detection at init time
- 🔄 ArgoCD provides declarative, auditable deployments with drift detection
- 📦 Kubernetes 1.33 includes enhanced Pod Security Admission and signed container images
- 📋 Infrastructure state is fully reproducible from version-controlled configuration
- 🛡️ Docker 28.1 content trust ensures image integrity from build to runtime

---

## 📚 Stack Categories

### 🖥️ Web Frontend

**File:** [`stacks/frontend.md`](stacks/frontend.md)

Frameworks, bundlers, CSS solutions, and client-side security tools. Covers React, Vue, Svelte, Angular, and emerging frameworks with their recommended companion tools. Each entry includes CSP configurations, dependency audit results, and XSS mitigation strategies.

> **Featured:** React 19.1 + Next.js 15.3, Vue 3 + Nuxt 3, SvelteKit 2, Angular 19

---

### ⚙️ Backend API

**File:** [`stacks/backend.md`](stacks/backend.md)

Server-side runtimes, web frameworks, ORMs, authentication libraries, and API security tools. Covers Node.js, Go, Rust, Python, Java, and .NET ecosystems with detailed analysis of middleware security, input validation, and authentication patterns.

> **Featured:** Go 1.24 + Chi 5.2 + sqlc, Rust 1.87 + Axum 0.8, Node.js 22 + Fastify 5.3, Python 3.13 + FastAPI 0.115, Java 21 + Spring Boot 3.4, .NET 8 + ASP.NET Core 8.0

---

### 🗄️ Database

**File:** [`stacks/database.md`](stacks/database.md)

Relational, document, key-value, and time-series databases with their client libraries, migration tools, and connection pooling solutions. Includes analysis of authentication mechanisms, encryption at rest, and network security configurations.

> **Featured:** PostgreSQL 17.5, MySQL 8.4 LTS, MongoDB 8.0, Redis 8.0

---

### 🔧 DevOps & Infrastructure

**File:** [`stacks/devops.md`](stacks/devops.md)

Infrastructure-as-code, CI/CD, container orchestration, secret management, observability, and cloud provider tools. Each stack is evaluated for supply chain integrity of the entire deployment pipeline.

> **Featured:** Terraform 1.12 + ArgoCD, Kubernetes 1.33 + Docker 28.1, GitHub Actions, Dagger

---

### 📱 Mobile

**File:** [`stacks/mobile.md`](stacks/mobile.md)

Cross-platform and native mobile development frameworks, state management, navigation, and mobile-specific security tooling. Includes analysis of app signing, dependency management, and runtime integrity verification.

> **Featured:** React Native 0.79 + Expo, Flutter 3.32, Kotlin Multiplatform

---

### 🤖 Machine Learning & AI

**File:** [`stacks/ml-ai.md`](stacks/ml-ai.md)

ML frameworks, model serving, vector databases, LLM tooling, and data pipeline security. Special focus on model supply chain — provenance verification, adversarial robustness, and training data integrity.

> **Featured:** PyTorch 2.7 + vLLM, LangChain 0.3 + vector stores, JAX + Flax, scikit-learn + ONNX Runtime

---

### ⚡ Real-time & Messaging

**File:** [`stacks/realtime.md`](stacks/realtime.md)

WebSockets, SSE, pub/sub, message queues, and real-time collaboration tools with security considerations for persistent connections. Evaluates authentication, message integrity, and denial-of-service resilience.

> **Featured:** Kafka 4.0, RabbitMQ 4.1, NATS 2.11, Socket.IO 4.x, Redis Streams

---

### 🏗️ Full-stack Combos

**File:** [`stacks/fullstack.md`](stacks/fullstack.md)

Pre-verified end-to-end combinations spanning frontend, backend, database, and deployment. Complete application blueprints with security scores for the full dependency graph — from browser to database.

> **Featured:** T3 Stack (Next.js + tRPC + Prisma), Rails 8 Full Stack, Django 5.2 + htmx + Alpine.js

---

### 🖥️ Desktop Applications

**File:** [`stacks/desktop.md`](stacks/desktop.md)

Desktop app frameworks with security-first sandboxing. Covers Tauri's Rust-based process isolation, Electron's CSP hardening, Qt native modules, and .NET MAUI cross-platform deployment. Auto-update security, native module audit pipelines, and IPC boundary protection are evaluated for each.

> **Featured:** Tauri 2.x (Rust sandbox), Electron 33 + secure defaults, Qt 6.8, .NET MAUI 9.0

---

### 🌐 Hybrid & WebView

**File:** [`stacks/hybrid.md`](stacks/hybrid.md)

Capacitor, Ionic, and WebView-based apps with JavaScript bridge security hardening. Covers PWA alternatives, hybrid navigation patterns, and the critical attack surface of JS-to-native bridges. Each stack is evaluated for bridge injection resistance and offline integrity.

> **Featured:** Capacitor 6 + Ionic 8, WebView hardening patterns, PWA-first alternatives

---

### 🎮 Game Development

**File:** [`stacks/gaming.md`](stacks/gaming.md)

Game engines and multiplayer infrastructure with supply chain security focus. Covers Unity, Godot, Unreal Engine, and Bevy (Rust). Asset pipeline security, multiplayer networking protocols, mod/UGC sandboxing, and anti-cheat integration are evaluated for each.

> **Featured:** Unity 2022 LTS, Godot 4.2, Unreal Engine 5.4, Bevy 0.14

---

### 🤖 AI-Assisted Development

**File:** [`stacks/ai-development.md`](stacks/ai-development.md)

AI coding assistants and their unique supply chain risks. Covers GitHub Copilot, Cursor, Aider, and related tools. AI-generated code introduces novel attack vectors: hallucinated package names, insecure patterns from training data, and context leakage through cloud inference.

> **Featured:** GitHub Copilot Enterprise, Cursor + local models, Aider + offline LLMs

---

### 🧠 AI/LLM Applications

**File:** [`stacks/ai-apps.md`](stacks/ai-apps.md)

LLM orchestration frameworks, vector databases, and AI agent infrastructure. Covers LangChain, vLLM, LlamaIndex, and agent frameworks. Special focus on prompt injection defense, model supply chain verification, RAG pipeline security, and inference endpoint hardening.

> **Featured:** LangChain 0.3 + guardrails, vLLM + model provenance, Vector DB security (Qdrant, Weaviate)

---

### 📱 Native Mobile & Cross-Platform Deep Dive

**File:** [`stacks/mobile-native.md`](stacks/mobile-native.md)

Native Android (Kotlin), iOS (Swift), HarmonyOS, and advanced cross-platform frameworks (uni-app, KMP). Covers certificate pinning, secure enclave usage, on-device AI model security, and platform-specific hardening beyond what cross-platform wrappers provide.

> **Featured:** Android 15 (Kotlin), iOS 18 (Swift), HarmonyOS NEXT, Kotlin Multiplatform 2.0

---

### 🔄 Architecture Evolution

**File:** [`stacks/evolution.md`](stacks/evolution.md)

Migration paths from monolith to distributed architectures with security preserved at each stage. Covers Modular Monolith, Service Extraction patterns, Strangler Fig, and event-driven decomposition. Each transition point is evaluated for security regression risk.

> **Featured:** Monolith → Modular Monolith, Strangler Fig extraction, Event-driven decomposition

---

### 🔗 Distributed Systems & Microservices

**File:** [`stacks/distributed.md`](stacks/distributed.md)

Service mesh, API gateways, distributed tracing, and microservice communication patterns. Covers Istio, Linkerd, Kong, and Saga orchestration. Zero-trust networking with mTLS everywhere, circuit breakers, and inter-service authentication are evaluated for each stack.

> **Featured:** Istio 1.22 + Envoy, Kong Gateway 3.x, Saga orchestration patterns

---

## 🕘 Supply Chain Attack Timeline

A chronological history of major supply chain attacks that motivate this project. Understanding the past is essential to securing the future.

```
2017 ───────────────────────────────────────────────────────────────────────── 2025
│                                                                               │
│  2017-11  ┌─ event-stream / flatmap-stream                                   │
│           │  Cryptocurrency wallet theft via trusted npm dependency           │
│           │  Impact: Millions of users | Vector: npm dependency hijack        │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2020-03  ┌─ eslint-scope                                                    │
│           │  Stolen npm credentials exfiltrated environment variables         │
│           │  Impact: CI/CD pipelines | Vector: credential theft               │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2020-12  ┌─ SolarWinds Orion (SUNBURST)                                     │
│           │  Nation-state attack, 18,000+ organizations compromised           │
│           │  Impact: US gov agencies, Fortune 500 | Vector: build system      │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2021-01  ┌─ ua-parser-js (70M+ weekly downloads)                            │
│           │  Crypto miners + password stealers injected into hijacked pkg     │
│           │  Impact: Millions of installs | Vector: maintainer account theft  │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2021-04  ┌─ Codecov Bash Uploader                                           │
│           │  CI secrets exfiltrated via compromised upload tool               │
│           │  Impact: 29,000+ projects | Vector: CI tool tampering             │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2022-01  ┌─ colors.js / faker.js (protestware)                              │
│           │  Intentional infinite loop broke thousands of CI pipelines        │
│           │  Impact: Industry-wide | Vector: maintainer sabotage              │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2022-03  ┌─ node-ipc (protestware)                                          │
│           │  Data-wiping code targeted by IP geolocation                      │
│           │  Impact: vue-cli users | Vector: ideological sabotage             │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2022-12  ┌─ PyTorch torchtriton (dependency confusion)                      │
│           │  Malicious PyPI package with identical name to nightly dep        │
│           │  Impact: ML researchers | Vector: dependency confusion            │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2023-03  ┌─ 3CX Desktop App                                                 │
│           │  First publicly documented cascading supply chain attack          │
│           │  Impact: 600,000+ businesses | Vector: cascading compromise       │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2024-03  ┌─ XZ Utils (CVE-2024-3094)                                        │
│           │  Multi-year social engineering campaign → sshd backdoor           │
│           │  Impact: Nearly all Linux distros | Vector: maintainer infiltration│
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2025-01  ┌─ tj-actions/changed-files (GitHub Actions)                       │
│           │  Compromised CI action leaked secrets from thousands of repos     │
│           │  Impact: 23,000+ repos | Vector: GitHub Actions compromise        │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2025-??  The next one is being planned right now.                            │
│           这个项目正是为了应对下一个攻击而存在。                                    │
│           Stay vigilant. Use verified stacks. 🔒                              │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔒 Security Advisories

### Reporting a Stack Vulnerability

If you discover a security issue in any recommended stack:

1. **DO NOT** open a public GitHub issue for sensitive vulnerabilities
2. 📧 Email: **security@awesome-secure-stacks.dev**
3. ⏱️ We aim to respond within **48 hours** and publish advisories within **7 days**

### Advisory Format

Each advisory follows the [OpenSSF OpenVEX](https://openvex.dev/) format:

```
Advisory: ASSA-2025-001
Severity: High (CVSS 8.1)
Affected Stacks: backend-go-chi, fullstack-t3
Component: golang.org/x/crypto v0.21.0
Fixed In: v0.22.0
Status: Resolved
Published: 2025-05-15
```

### Subscribe to Advisories

- 🔔 **GitHub Watch** → "Releases only" on this repository
- 📡 **Atom feed:** [`/releases.atom`](https://github.com/lxl141421/awesome-secure-stacks/releases.atom)
- 📢 Watch the [Releases](https://github.com/lxl141421/awesome-secure-stacks/releases) page for security advisories

---

## 🤝 Contributing

We welcome contributions! But security curation requires rigor. 贡献安全策展需要严谨性 — quality over quantity.

### How to Contribute

| Type | How | Difficulty |
|------|-----|------------|
| 🐛 Report a scoring error | [Open an issue](https://github.com/lxl141421/awesome-secure-stacks/issues/new) | Easy |
| 📦 Propose a new stack | [Open an issue](https://github.com/lxl141421/awesome-secure-stacks/issues/new) with stack details | Medium |
| 📊 Update a score | [Submit a PR](https://github.com/lxl141421/awesome-secure-stacks/compare) with evidence | Medium |
| 🔍 Audit a stack | [Follow the audit guide](CONTRIBUTING.md) | Hard |
| 📝 Improve docs | [Submit a PR](https://github.com/lxl141421/awesome-secure-stacks/compare) | Easy |

### Contribution Guidelines

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines and templates
2. All new stacks must include a **reproduction template** (lockfile or Docker Compose)
3. Score changes require **evidence** (CVE links, audit reports, tool output)
4. Be respectful and constructive in all interactions

### Adding a New Stack

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/awesome-secure-stacks.git
cd awesome-secure-stacks

# 2. Create a branch
git checkout -b add/my-awesome-stack

# 3. Add your stack entry to the appropriate category file
#    Follow the template format in CONTRIBUTING.md
#    Include: version matrix, security score, CVE analysis, alternatives

# 4. Submit PR with evidence
git push origin add/my-awesome-stack
```

---

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md) for the full project roadmap. Key milestones include automated scoring pipelines, expanded stack coverage, and integration with Sigstore and OpenSSF Scorecard data.

**Upcoming highlights:**

- 🤖 Automated monthly scoring with CI/CD integration
- 📊 Interactive stack comparison dashboard
- 🔗 Sigstore and SLSA provenance verification integration
- 📦 Expanded stack coverage: embedded systems, game engines, data engineering
- 🌐 Multi-language documentation (中文, 日本語, 한국어)

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

> **Why MIT?** Security knowledge should be freely accessible. We chose MIT to maximize adoption and contribution. 安全知识应该自由获取。

---

## 🙏 Acknowledgments

This project would not be possible without:

### Who Is This For?

- 🧑‍💻 **Independent developers** building solo projects who need vetted stacks without a security team
- 🤖 **AI-assisted developers** using Copilot/Cursor/Aider who want to verify generated dependency choices
- 🌐 **Web teams** shipping React/Vue/Angular apps with production-grade security
- 📱 **Mobile teams** building iOS/Android/cross-platform apps with hardened native bridges
- ⚙️ **Backend teams** running Go/Rust/Python/Java services behind API gateways
- 🎮 **Game studios** securing multiplayer infrastructure and mod ecosystems
- 🏢 **Enterprises doing tech upgrades** migrating between framework generations safely
- 🔄 **Teams evolving from monolith to microservices** who need security at every migration stage

---

### Special Thanks

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
  <b>⭐ If this project helps you ship more secure software, give it a star! ⭐</b><br>
  <sub>如果这个项目帮助你构建更安全的软件，请给我们一个 Star！</sub><br><br>
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
    <a href="https://github.com/lxl141421/awesome-secure-stacks/pulls">Pull Requests</a> ·
    <a href="https://github.com/lxl141421/awesome-secure-stacks/discussions">Discussions</a>
  </sub>
</p>
