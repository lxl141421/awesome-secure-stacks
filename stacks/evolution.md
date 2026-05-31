# Architecture Evolution Paths

> **Philosophy**: Evolution, not revolution. Every phase builds on the last. Security increases at every stage. Never skip phases — each one teaches lessons needed for the next.

---

## Table of Contents

1. [Phase 1: Monolith](#phase-1-monolith)
2. [Phase 2: Modular Monolith](#phase-2-modular-monolith)
3. [Phase 3: Service Extraction](#phase-3-service-extraction)
4. [Phase 4: Full Microservices](#phase-4-full-microservices)
5. [Phase 5: Distributed Systems](#phase-5-distributed-systems)
6. [Technology Upgrade Paths](#technology-upgrade-paths)
7. [Database Evolution](#database-evolution)
8. [Security Evolution](#security-evolution)
9. [Migration Checklists](#migration-checklists)
10. [Rollback Strategies](#rollback-strategies)

---

## Phase 1: Monolith

### Description
Single deployable unit. One codebase, one database, one process. This is where 90% of projects should start and where many should stay.

### Recommended Stacks

**Java/Kotlin:**
- Spring Boot 3.2 + Java 17 LTS
- PostgreSQL 16 + Flyway migrations
- Gradle 8.5 or Maven 3.9
- Deployed as single JAR/WAR

**Python:**
- Django 5.0 + Python 3.12 LTS
- PostgreSQL 16 + Django ORM
- Gunicorn + Nginx
- Docker container

**Ruby:**
- Rails 7.1 + Ruby 3.3
- PostgreSQL 16
- Puma + Nginx
- Docker or traditional deploy

**Node.js:**
- NestJS 10 + TypeScript 5.3
- PostgreSQL 16 + TypeORM/Prisma
- PM2 process manager
- Docker container

### Security Considerations
```
┌─────────────────────────────────────┐
│              NGINX                  │
│    (TLS termination, rate limit)    │
├─────────────────────────────────────┤
│         MONOLITH APP                │
│  ┌───────────┬───────────┬────────┐ │
│  │  Auth     │  Business  │  API   │ │
│  │  Module   │  Logic     │  Layer │ │
│  └───────────┴───────────┴────────┘ │
├─────────────────────────────────────┤
│         PostgreSQL 16               │
│    (single DB, all tables)          │
└─────────────────────────────────────┘
```

- **Auth**: Session-based or simple JWT
- **TLS**: Terminate at reverse proxy (Nginx/Caddy)
- **Secrets**: Environment variables + `.env` files (never committed)
- **DB access**: Single connection pool, parameterized queries only
- **Dependencies**: `npm audit` / `pip audit` / `bundler-audit` in CI

### What Stays the Same (in later phases)
- Unit tests
- Database migrations strategy
- Code quality standards
- Logging framework

### What Changes (in later phases)
- Deployment model
- Communication patterns
- Database access patterns
- Monitoring and observability

---

## Phase 2: Modular Monolith

### Description
Single deployable, but with clear internal module boundaries. Each module has its own API, data access, and business logic. Modules communicate through well-defined interfaces, not direct database queries.

### Recommended Stacks

**Java/Kotlin:**
- Spring Boot 3.2 + Spring Modulith 1.2
- ArchUnit for architecture testing
- Module structure:
  ```
  app/
  ├── user-module/
  │   ├── api/          (public interfaces)
  │   ├── domain/       (business logic)
  │   └── persistence/  (data access)
  ├── order-module/
  │   ├── api/
  │   ├── domain/
  │   └── persistence/
  └── shared/
      ├── events/
      └── security/
  ```

**Python:**
- Django 5.0 with domain-driven structure
- django-modular or custom app boundaries
- Module structure:
  ```
  apps/
  ├── users/
  │   ├── models.py      (internal)
  │   ├── services.py    (business logic)
  │   └── api.py         (public interface)
  ├── orders/
  │   ├── models.py
  │   ├── services.py
  │   └── api.py
  └── shared/
      ├── events.py
      └── security.py
  ```

### Security Considerations
- **Module boundaries enforced by architecture tests**
  ```kotlin
  // ArchUnit test
  @ArchTest
  val moduleRule = classes()
      .that().resideInAPackage("..user..")
      .should().onlyDependOnClassesThat()
      .resideInAnyPackage("..user..", "..shared..", "java..", "javax..")
  ```
- **No cross-module database queries** — modules own their tables
- **Internal event bus** for module communication
- **Shared security module** for auth, encryption, audit logging

### What Stays the Same
- Single deployment pipeline
- Single database (but tables partitioned by module)
- Single monitoring stack
- Existing test suite

### What Changes
- Code organization (module boundaries)
- Inter-module communication (events vs direct calls)
- Data access patterns (no cross-module joins)
- Build can fail on architecture violations

---

## Phase 3: Service Extraction

### Description
Extract modules from the monolith into independent services using the Strangler Fig pattern. The monolith shrinks over time as services grow. API Gateway routes traffic.

### Recommended Stacks

**Infrastructure:**
- Docker + Docker Compose (dev) / Kubernetes (prod)
- API Gateway: Kong 3.5, Traefik 3.0, or AWS API Gateway
- Service Discovery: Consul 1.18 or Kubernetes DNS
- Message Queue: RabbitMQ 3.13 or AWS SQS

**Service Stacks (per extracted service):**
- Any of the Phase 1 stacks, but smaller and focused
- Each service owns its database
- gRPC or REST for inter-service communication

### Strangler Fig Pattern
```
Phase A: Route new features to new service
┌──────────────┐     ┌──────────────┐
│  API Gateway  │────▶│   Monolith   │ (existing features)
│               │────▶│   Service A  │ (new features)
└──────────────┘     └──────────────┘

Phase B: Migrate existing features one by one
┌──────────────┐     ┌──────────────┐
│  API Gateway  │────▶│   Monolith   │ (shrinking)
│               │────▶│   Service A  │
│               │────▶│   Service B  │
└──────────────┘     └──────────────┘

Phase C: Monolith becomes just another service (or disappears)
┌──────────────┐     ┌──────────────┐
│  API Gateway  │────▶│   Service A  │
│               │────▶│   Service B  │
│               │────▶│   Service C  │
└──────────────┘     └──────────────┘
```

### Security Considerations
- **API Gateway** handles auth, rate limiting, TLS termination
- **Service-to-service auth**: mTLS or JWT tokens
- **Data isolation**: Each service has its own database credentials
- **Network policies**: Services can only talk to services they need
  ```yaml
  # Kubernetes NetworkPolicy
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
    name: order-service-policy
  spec:
    podSelector:
      matchLabels:
        app: order-service
    ingress:
      - from:
          - podSelector:
              matchLabels:
                app: api-gateway
        ports:
          - port: 8080
    egress:
      - to:
          - podSelector:
              matchLabels:
                app: payment-service
        ports:
          - port: 8080
      - to:
          - podSelector:
              matchLabels:
                app: order-db
        ports:
          - port: 5432
  ```

### What Stays the Same
- Core business logic (just moved to services)
- Database schema (split across service databases)
- Test strategy (add integration/e2e tests)

### What Changes
- Deployment (multiple pipelines)
- Data consistency (no more ACID across services)
- Debugging (distributed tracing required)
- Monitoring (per-service metrics)

---

## Phase 4: Full Microservices

### Description
Complete microservice architecture. Service mesh for communication. Event-driven architecture. CQRS for complex read/write patterns.

### Recommended Stacks

**Infrastructure:**
- Kubernetes 1.29 + Helm 3
- Service Mesh: Istio 1.21 or Linkerd 2.15
- Event Bus: Apache Kafka 3.7 or NATS 2.10
- Observability: OpenTelemetry + Grafana/Loki/Tempo
- Secrets: HashiCorp Vault 1.15

**Service Mesh Security:**
```yaml
# Istio PeerAuthentication — enforce mTLS everywhere
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT

# Istio AuthorizationPolicy — zero-trust
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: order-service-policy
  namespace: production
spec:
  selector:
    matchLabels:
      app: order-service
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/production/sa/api-gateway"]
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/api/orders*"]
```

### CQRS Pattern
```
                    ┌──────────────┐
                    │  Command Bus │
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
  ┌──────────┐      ┌──────────┐      ┌──────────┐
  │  Order   │      │  User    │      │  Payment │
  │  Service │      │  Service │      │  Service │
  └────┬─────┘      └────┬─────┘      └────┬─────┘
       │                 │                  │
       ▼                 ▼                  ▼
  ┌──────────┐      ┌──────────┐      ┌──────────┐
  │ Order DB │      │ User DB  │      │Payment DB│
  └────┬─────┘      └────┬─────┘      └────┬─────┘
       │                 │                  │
       └─────────────────┼──────────────────┘
                         │ Event Store (Kafka)
                         ▼
              ┌─────────────────────┐
              │  Read Model / Query │
              │  (Elasticsearch /   │
              │   Read Replicas)    │
              └─────────────────────┘
```

### Security Considerations
- **Zero-trust networking**: mTLS everywhere, no implicit trust
- **Service identity**: SPIFFE/SPIRE for workload identity
- **Secrets management**: Vault with short-lived credentials
  ```bash
  # Vault dynamic database credentials
  vault read database/creds/order-service
  # Returns temporary username/password with TTL
  ```
- **Event security**: Signed events, encrypted payloads
- **API versioning**: Contract testing prevents breaking changes

### What Stays the Same
- Business logic (refactored into bounded contexts)
- Team structure (should mirror service boundaries)

### What Changes
- Consistency model (eventual consistency)
- Deployment (independent per service)
- Testing (contract tests, chaos engineering)
- On-call (per-service ownership)

---

## Phase 5: Distributed Systems

### Description
Multi-region, globally distributed. Eventual consistency as a feature, not a bug. Edge computing. Chaos engineering as practice.

### Recommended Stacks

**Infrastructure:**
- Multi-region Kubernetes (GKE Autopilot / EKS / AKS)
- Global load balancing: Cloudflare / AWS Global Accelerator
- Data: CockroachDB 23.2 (multi-region SQL) or YugabyteDB
- Cache: Redis Cluster 7.2 with geo-replication
- CDN: Cloudflare / Fastly with edge compute

**Architecture:**
```
┌─ US-EAST ──────────────────────────────────┐
│  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │ K8s     │  │ K8s     │  │ Cockroach│    │
│  │ Cluster │  │ Cluster │  │ DB Node  │    │
│  └────┬────┘  └────┬────┘  └────┬─────┘    │
│       └─────────────┼────────────┘          │
│                     │                       │
│              ┌──────┴──────┐                │
│              │ Global LB   │                │
│              └──────┬──────┘                │
└─────────────────────┼───────────────────────┘
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
┌─ EU-WEST ────┐ ┌─ APAC ────┐ ┌─ US-WEST ────┐
│ K8s + DB Node│ │ K8s + DB  │ │ K8s + DB Node│
│              │ │ Node      │ │              │
└──────────────┘ └───────────┘ └──────────────┘
```

### Security Considerations
- **Data residency**: EU data stays in EU (GDPR), China data stays in China
- **Global secrets**: Vault with regional seal/unseal
- **Cross-region auth**: Federated identity with regional IdPs
- **DDoS protection**: Edge-level mitigation
- **Compliance**: Per-region audit trails
- **Chaos engineering**: Regular failure injection to verify security under stress

---

## Technology Upgrade Paths

### Node.js 18 → 22
```
Phase 1: Node 18 LTS (Hydrogen) — Active LTS until 2025-04
Phase 2: Node 20 LTS (Iron)    — Active LTS until 2026-04
Phase 3: Node 22 LTS (Jod)     — Active LTS until 2027-04
```

**Migration Checklist:**
- [ ] Run `npm outdated` and update dependencies
- [ ] Enable `--experimental-vm-modules` flag if using ESM
- [ ] Test with `NODE_OPTIONS=--throw-deprecation` to catch issues
- [ ] Verify native addon compatibility (node-gyp rebuild)
- [ ] Update CI/CD pipelines for new Node version
- [ ] Run full test suite with Node 22
- [ ] Deploy to staging, run smoke tests for 24h
- [ ] Update `.nvmrc` and `engines` in package.json
- [ ] Security audit: `npm audit --audit-level=high`

**Rollback:** Keep Node 18 container image tagged. Blue-green deploy with instant rollback.

### Python 3.10 → 3.12
```
Phase 1: Python 3.10 — EOL 2026-10
Phase 2: Python 3.11 — EOL 2027-10
Phase 3: Python 3.12 — EOL 2028-10
```

**Migration Checklist:**
- [ ] Update `pyproject.toml` / `setup.cfg` python_requires
- [ ] Fix deprecation warnings (Python 3.12 removed many deprecated features)
- [ ] `python -W error::DeprecationWarning -m pytest` — all warnings are errors
- [ ] Verify C extensions compatibility (numpy, pillow, etc.)
- [ ] Update type hints (Python 3.12 has improved generics)
- [ ] Test performance (Python 3.12 is 5% faster on average)
- [ ] Update Docker base image: `python:3.12-slim`
- [ ] Security: `pip audit` and `safety check`

**Rollback:** Pin previous Python Docker tag. `pip freeze > requirements-lock.txt` before upgrade.

### Java 17 → 21
```
Phase 1: Java 17 LTS — Active support until 2026-09
Phase 2: Java 21 LTS — Active support until 2028-09
```

**Migration Checklist:**
- [ ] Update `sourceCompatibility` and `targetCompatibility` in build
- [ ] Enable preview features if needed (`--enable-preview`)
- [ ] Test with `-XX:+EnableValhalla` if using value types
- [ ] Verify all dependencies support Java 21 bytecode
- [ ] Update Spring Boot to 3.2+ (requires Java 17+, supports 21)
- [ ] Test virtual threads: `Executors.newVirtualThreadPerTaskExecutor()`
- [ ] Run JMH benchmarks to verify performance
- [ ] Security: Update `java.security` policy if customized
- [ ] Update CI/CD: `setup-java@v4` with `java-version: '21'`

**Rollback:** Keep Java 17 in parallel. Switch `JAVA_HOME` and redeploy.

### .NET 6 → 8
```
Phase 1: .NET 6 LTS — EOL 2024-11 ⚠️ (upgrade immediately if still on 6)
Phase 2: .NET 8 LTS — Supported until 2026-11
```

**Migration Checklist:**
- [ ] Update `global.json` to SDK 8.0.x
- [ ] Update `TargetFramework` to `net8.0` in all .csproj files
- [ ] Replace deprecated APIs (check `SYSLIB` warnings)
- [ ] Update NuGet packages to .NET 8 compatible versions
- [ ] Test AOT compilation (`PublishAot=true`) if applicable
- [ ] Verify gRPC, SignalR, and EF Core compatibility
- [ ] Update Docker base: `mcr.microsoft.com/dotnet/aspnet:8.0`
- [ ] Security: `dotnet list package --vulnerable`

**Rollback:** Keep .NET 6 deployment slots. Instant rollback via slot swap.

---

## Database Evolution

### Stage 1: Single Database
```
┌──────────────┐
│  PostgreSQL   │
│  16 (single)  │
│  All tables   │
│  Full ACID    │
└──────────────┘
```
- **When**: Phase 1-2 (Monolith)
- **Security**: Row-level security, encrypted at rest, parameterized queries

### Stage 2: Read Replicas
```
       ┌──────────────┐
       │   Primary     │ ← writes
       │   PostgreSQL  │
       └──────┬───────┘
              │ WAL streaming
    ┌─────────┼─────────┐
    ▼         ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐
│Replica 1│ │Replica 2│ │Replica 3│ ← reads
└────────┘ └────────┘ └────────┘
```
- **When**: Phase 2-3 (read-heavy workloads)
- **Security**: Replication over TLS, separate credentials per replica
- **Consistency**: Eventual (replication lag: typically <1s)

### Stage 3: Sharding
```
┌──────────────┐
│  Citus /     │
│  Vitess      │ ← query router
└──────┬───────┘
       │
  ┌────┼────┬────┐
  ▼    ▼    ▼    ▼
┌───┐┌───┐┌───┐┌───┐
│Sh1││Sh2││Sh3││Sh4│  ← each shard is a full DB
└───┘└───┘└───┘└───┘
```
- **When**: Phase 3-4 (single DB can't handle write volume)
- **Security**: Per-shard encryption, cross-shard query audit
- **Considerations**: Shard key choice is permanent (choose wisely)

### Stage 4: CQRS + Event Sourcing
```
Commands → Event Store → Events → Projections → Read Models
                                              ↓
                                         Query Models
                                         (optimized for reads)
```
- **When**: Phase 4-5 (complex read/write patterns)
- **Security**: Signed events, immutable audit log, encryption per stream
- **Stack**: Kafka + Debezium (CDC) + Elasticsearch (read model)

---

## Security Evolution

### Level 1: Basic Auth
```
Client ──▶ Server ──▶ Session Store
  │                    (Redis/Memory)
  └── session cookie ◀──┘
```
- Session-based authentication
- CSRF tokens for form submissions
- HTTPS everywhere
- **When**: Phase 1

### Level 2: OAuth2 + OIDC
```
Client ──▶ Authorization Server ──▶ Resource Server
  │              │                       │
  │         ┌────┴────┐                  │
  │         │ IdP     │                  │
  │         │ (Keycloak│                  │
  │         │  Auth0)  │                  │
  │         └─────────┘                  │
  └──────── access token ───────────────┘
```
- OAuth2 authorization code flow + PKCE
- Short-lived access tokens (15min)
- Refresh token rotation
- **When**: Phase 2-3

### Level 3: Zero-Trust
```
Every request is authenticated and authorized,
regardless of network location.

User ──▶ Proxy ──▶ Policy Engine ──▶ Service
  │                  (OPA/Cedar)        │
  │                                     │
  └──── mTLS + JWT + Policy Check ─────┘
```
- No implicit trust based on network location
- Every service-to-service call authenticated (mTLS)
- Policy-as-code (OPA, Cedar, Casbin)
- Device posture checks
- **When**: Phase 3-4

### Level 4: mTLS Everywhere
```
All traffic encrypted and mutually authenticated.

Service A ◀──mTLS──▶ Service B
    │                    │
    ▼                    ▼
  SPIFFE ID          SPIFFE ID
  (workload           (workload
   identity)           identity)

Managed by service mesh (Istio/Linkerd)
```
- SPIFFE/SPIRE for workload identity
- Automatic certificate rotation (every 1h)
- Short-lived credentials everywhere
- **When**: Phase 4-5

---

## Migration Checklists

### Monolith → Modular Monolith
- [ ] Map bounded contexts
- [ ] Define module APIs (public interfaces)
- [ ] Add architecture tests (ArchUnit / custom)
- [ ] Refactor database: partition tables by module
- [ ] Remove cross-module direct DB queries
- [ ] Add internal event bus for module communication
- [ ] Verify all tests pass
- [ ] Security: audit module boundary enforcement

### Modular Monolith → Services
- [ ] Choose first extraction candidate (least coupled, most changed)
- [ ] Set up container orchestration (Docker + K8s)
- [ ] Deploy API gateway
- [ ] Implement Strangler Fig routing
- [ ] Extract service with its own database
- [ ] Implement event-driven sync between monolith and service
- [ ] Add distributed tracing (OpenTelemetry)
- [ ] Update CI/CD for multi-service deployment
- [ ] Security: implement service-to-service auth (mTLS/JWT)
- [ ] Security: network policies between services
- [ ] Monitor for 2 weeks before next extraction

### Services → Full Microservices
- [ ] Implement service mesh (Istio/Linkerd)
- [ ] Add centralized secret management (Vault)
- [ ] Implement circuit breakers (Resilience4j)
- [ ] Add contract testing (Pact)
- [ ] Implement saga pattern for distributed transactions
- [ ] Add chaos engineering (Chaos Monkey / Litmus)
- [ ] Security: zero-trust policies
- [ ] Security: signed events in event bus
- [ ] Performance: load testing per service

---

## Rollback Strategies

### Database Rollback
```sql
-- Always have a down migration
-- V001__create_users.sql
CREATE TABLE users (id BIGSERIAL PRIMARY KEY, email VARCHAR(255));

-- V001__create_users_DOWN.sql (manual rollback script)
DROP TABLE IF EXISTS users;
```

### Application Rollback
```
Blue-Green Deployment:
┌─────────┐         ┌─────────┐
│  Blue   │ ◀─────  │  Green  │
│ (v1.2)  │  traffic │ (v1.3)  │
└─────────┘         └─────────┘

If v1.3 fails health checks:
  → Switch traffic back to v1.2
  → Investigate v1.3 issues
  → Fix and redeploy
```

### Service Rollback (Kubernetes)
```bash
# Instant rollback
kubectl rollout undo deployment/order-service

# Rollback to specific revision
kubectl rollout undo deployment/order-service --to-revision=3

# Check rollout status
kubectl rollout status deployment/order-service
```

### Circuit Breaker for Gradual Rollback
```java
// Resilience4j — degrade gracefully before full rollback
CircuitBreakerConfig config = CircuitBreakerConfig.custom()
    .failureRateThreshold(50)
    .waitDurationInOpenState(Duration.ofSeconds(30))
    .slidingWindowSize(10)
    .build();
```

---

## Security Audit Points (Per Phase)

### Phase 1: Monolith
- [ ] OWASP Top 10 scan (ZAP / Burp Suite)
- [ ] Dependency vulnerability scan
- [ ] SQL injection testing
- [ ] XSS testing
- [ ] Secret scan (truffleHog / gitleaks)

### Phase 2: Modular Monolith
- [ ] Architecture boundary enforcement
- [ ] Cross-module data access audit
- [ ] Internal API security review
- [ ] Event bus security (no sensitive data in events)

### Phase 3: Service Extraction
- [ ] API gateway security configuration
- [ ] Service-to-service authentication
- [ ] Network policy audit
- [ ] Secret rotation procedures
- [ ] Distributed tracing data sensitivity

### Phase 4: Full Microservices
- [ ] mTLS certificate rotation
- [ ] Service mesh policy audit
- [ ] Event encryption verification
- [ ] Chaos engineering security scenarios
- [ ] Supply chain security (container scanning)

### Phase 5: Distributed Systems
- [ ] Cross-region data compliance (GDPR, CCPA, PIPL)
- [ ] Global secret management audit
- [ ] DDoS mitigation testing
- [ ] Regional failover security verification
- [ ] Multi-tenant isolation testing

---

## Decision Matrix: When to Evolve

| Signal | Current Phase | Action |
|--------|--------------|--------|
| Team growing past 8 people | Monolith | → Modular Monolith |
| Deployment conflicts (stepping on each other) | Modular | → Service Extraction |
| Need independent scaling per feature | Services | → Full Microservices |
| Users in multiple continents | Microservices | → Distributed Systems |
| Single DB can't handle write load | Any | → Database evolution stage |
| Auth is becoming complex | Basic Auth | → OAuth2/OIDC |
| Security incidents from internal threats | OAuth2 | → Zero-Trust |

### The Anti-Pattern: Premature Distribution
```
❌ "We need microservices" (team of 3, no users yet)
✅ "We need modular boundaries" (team of 8, deployment conflicts)

❌ "We need Kubernetes" (1000 requests/day)
✅ "We need containers" (consistent dev/prod parity)

❌ "We need Kafka" (simple request/response)
✅ "We need Kafka" (event sourcing, high throughput, replay needed)
```

---

## Quick Reference: Phase-by-Phase Stack Summary

| Component | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 |
|-----------|---------|---------|---------|---------|---------|
| Deploy | Single binary | Single binary | K8s pods | K8s + mesh | Multi-region K8s |
| DB | Single PostgreSQL | Single PG (partitioned) | DB per service | CQRS + event store | CockroachDB |
| Auth | Sessions | Sessions + internal | OAuth2 at gateway | mTLS + JWT | SPIFFE + zero-trust |
| Network | Nginx | Nginx | API Gateway | Service mesh | Global LB + edge |
| Events | N/A | Internal bus | RabbitMQ/SQS | Kafka | Kafka + CDC |
| Secrets | .env files | .env files | K8s secrets | Vault | Vault (regional) |
| Observability | Logs | Logs + metrics | Distributed tracing | Full OTel stack | OTel + edge |
| Testing | Unit + integration | + Architecture tests | + Contract tests | + Chaos engineering | + Failure injection |

---

*Last updated: 2026-05-31*
*Principle: Evolution, not revolution. Every phase earns the next.*
