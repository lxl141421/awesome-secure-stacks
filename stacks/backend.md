# Backend API Stacks — Secure Stacks

> Last updated: 2026-05-31
> Review cadence: Monthly

---

## 1. Node.js Stack ⭐

**Security Grade: A**

| Component | Pinned Version | License | CVEs (2024-2026) |
|-----------|---------------|---------|-------------------|
| Node.js | 22.16.0 | MIT | 0 critical (LTS) |
| Express | 4.21.2 | MIT | 0 (4.x mature) |
| Fastify | 4.28.1 | MIT | 0 | *(stability choice)* |
| TypeScript | 5.4.5 | Apache-2.0 | N/A |

**Dependency Tree Analysis:**
- Express: ~30 transitive deps (minimal attack surface)
- Fastify: ~15 transitive deps (smaller, faster)
- Fastify recommended for new projects (schema validation built-in)

**Security Audit Status:**
```bash
npm audit --production
# Expected: 0 critical, 0 high
```

**Lockfile Pinning:**
```json
{
  "node": ">=22.16.0 <23",
  "express": "4.21.2",
  "fastify": "4.28.1",
  "helmet": "8.0.0",
  "express-rate-limit": "7.4.1",
  "typescript": "5.4.5",
  "zod": "3.23.8"
}
```

**Reproducible Build Support:**
- `npm ci` with lockfile integrity check
- Use `--ignore-scripts` to prevent postinstall attacks
- Container: `node:22.16.0-alpine` (SHA256 pinned)

---

## 2. Python Stack

**Security Grade: A**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Python | 3.12.7 | PSF | 0 critical | *(stability choice)* |
| FastAPI | 0.115.12 | MIT | 0 |
| Pydantic | 2.9.2 | MIT | 0 |
| uvicorn | 0.31.0 | BSD-3 | 0 |
| SQLAlchemy | 2.0.35 | MIT | 0 |

**Dependency Tree Analysis:**
- FastAPI + Pydantic: ~12 direct deps, ~40 transitive
- Starlette (ASGI) underpins FastAPI — well-audited

**Security Audit Status:**
```bash
pip-audit --strict --desc
safety check --full-report
```

**Lockfile Pinning:**
```toml
# pyproject.toml (use uv or poetry for locking)
[tool.uv]
resolution = "lowest-direct"

[project.dependencies]
fastapi = "==0.115.12"
pydantic = "==2.9.2"
uvicorn = {extras = ["standard"], version = "==0.31.0"}
sqlalchemy = "==2.0.35"
```

**Reproducible Build Support:**
- Use `uv lock` or `poetry.lock` with hash verification
- `pip install --require-hashes -r requirements.txt`
- Container: `python:3.12.7-slim-bookworm` (SHA256 pinned)

---

## 3. Go Stack

**Security Grade: A+**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Go | 1.22.8 | BSD-3 | 0 critical | *(stability choice)* |
| Gin | 1.10.0 | MIT | 0 |
| Echo | 4.12.0 | MIT | 0 |
| chi | 5.1.0 | MIT | 0 |

**Dependency Tree Analysis:**
- Go stdlib: minimal external deps needed
- Gin: ~5 transitive deps (excellent)
- chi: ~0 transitive deps (stdlib-compatible)

**Security Audit Status:**
```bash
govulncheck ./...
go mod verify
```

**Lockfile Pinning:**
```
go 1.22.8
require (
    github.com/gin-gonic/gin v1.10.0
    github.com/go-playground/validator/v10 v10.22.1
)
```

**Reproducible Build Support:**
- Go modules with `go.sum` hash verification
- `CGO_ENABLED=0` for static binaries
- Container: `golang:1.22.8-alpine` → `scratch` (minimal)

---

## 4. Rust Stack

**Security Grade: A+**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Rust | 1.80.1 | MIT/Apache-2.0 | 0 | *(stability choice)* |
| Actix-web | 4.8.0 | MIT/Apache-2.0 | 0 | *(stability choice)* |
| Axum | 0.7.9 | MIT | 0 | *(stability choice)* |
| Tokio | 1.41.1 | MIT | 0 |
| Serde | 1.0.214 | MIT/Apache-2.0 | 0 |

**Dependency Tree Analysis:**
- Axum: ~8 direct deps (built on hyper/tokio)
- Actix-web: ~10 direct deps
- Memory safety guaranteed by Rust's type system

**Security Audit Status:**
```bash
cargo audit
cargo deny check
```

**Reproducible Build Support:**
- `Cargo.lock` with cryptographic hashes
- `cargo build --release` produces static binaries
- Container: `rust:1.80.1-bookworm` → `scratch`

---

## 5. Java Stack

**Security Grade: A**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Java (Temurin) | 21.0.4 | GPL-2.0 w/ CPE | 0 critical |
| Spring Boot | 3.2.11 | Apache-2.0 | 0 critical | *(stability choice)* |
| Spring Security | 6.2.7 | Apache-2.0 | 0 |
| Hibernate | 6.4.10 | LGPL-2.1 | 0 |

**Known Vulnerabilities:**
- Spring Framework CVE-2024-22234: authorization bypass (patched in 3.2.3)

**Dependency Tree Analysis:**
- Spring Boot starter: ~80 transitive deps (heaviest stack)
- Use `mvn dependency:tree` to audit

**Security Audit Status:**
```bash
mvn org.owasp:dependency-check-maven:check
./gradlew dependencyCheckAnalyze
```

**Reproducible Build Support:**
- Maven/Gradle lockfile plugins
- Container: `eclipse-temurin:21.0.4-jre-alpine`

---

## 6. .NET Stack

**Security Grade: A**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| .NET | 8.0.16 | MIT | 0 critical |
| ASP.NET Core | 8.0.16 | MIT | 0 |
| Entity Framework | 8.0.16 | MIT | 0 |

**Security Audit Status:**
```bash
dotnet list package --vulnerable
```

**Reproducible Build Support:**
- `packages.lock.json` with NuGet restore
- Container: `mcr.microsoft.com/dotnet/aspnet:8.0-alpine`

---

## Cross-Cutting Security Checklist (All Backend Stacks)

- [ ] Input validation on all endpoints (Zod/Pydantic/Struct/etc.)
- [ ] Rate limiting with configurable thresholds
- [ ] CORS restricted to known origins (never `*`)
- [ ] TLS 1.3 enforced, TLS 1.2 minimum
- [ ] SQL injection prevention via parameterized queries/ORM
- [ ] Secrets in environment variables or vault (never in code)
- [ ] Dependency scanning in CI (Snyk, Dependabot, cargo audit)
- [ ] Health check endpoints without sensitive info
- [ ] Request ID middleware for audit logging
- [ ] Graceful shutdown handling

## Comparison Matrix

| Feature | Node.js | Python | Go | Rust | Java | .NET |
|---------|---------|--------|-----|------|------|------|
| Performance | Good | Moderate | Excellent | Best | Good | Good |
| Memory Safety | No | No | Partial | Yes | GC | GC |
| Startup Time | Fast | Moderate | Fast | Fast | Slow | Moderate |
| Dep Count | ~30 | ~40 | ~5 | ~10 | ~80 | ~20 |
| Security Grade | A | A | A+ | A+ | A | A |
