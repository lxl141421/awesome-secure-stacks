# Database Stacks — Secure Stacks

> Last updated: 2026-05-31
> Review cadence: Monthly

---

## 1. PostgreSQL 16.x ⭐ Primary Recommendation

**Security Grade: A+**

| Attribute | Value |
|-----------|-------|
| Version | 16.4 |
| License | PostgreSQL License (permissive) |
| CVEs (2024-2026) | 0 critical, 2 low (patched) |

**Security Features:**
- Row-Level Security (RLS) with policy engine
- Column-level permissions
- SSL/TLS with certificate-based auth (mutual TLS)
- SCRAM-SHA-256 password authentication (default since PG 14)
- `pg_audit` extension for audit logging
- Encryption at rest via `pgcrypto` or filesystem (LUKS)

**Encryption at Rest:**
- Native: Transparent Data Encryption (TDE) not yet upstream — use LUKS/dm-crypt
- Cloud: AWS RDS, GCP Cloud SQL, Azure Database all support encryption at rest
- Extension: `pgcrypto` for column-level encryption

**Authentication:**
```sql
-- pg_hba.conf
hostssl  all  all  10.0.0.0/8  scram-sha-256
```

**Known CVEs:**
- CVE-2024-10978: pg_dump privilege escalation (patched in 16.4+)
- CVE-2024-10979: PL/pgSQL injection (patched in 16.4+)

**Recommended Drivers:**
| Language | Driver | Version | Notes |
|----------|--------|---------|-------|
| Node.js | pg (node-postgres) | 8.13.1 | Use `pg-pool` for connections |
| Python | psycopg | 3.2.3 | Async support, binary protocol |
| Go | pgx | 5.7.1 | Native protocol, fastest |
| Rust | tokio-postgres | 0.7.12 | Async, TLS support |
| Java | PostgreSQL JDBC | 42.7.4 | Battle-tested |
| .NET | Npgsql | 8.0.5 | EF Core integration |

---

## 2. MySQL 8.0.x LTS

**Security Grade: B+**

| Attribute | Value |
|-----------|-------|
| Version | 8.0.40 LTS |
| License | GPL-2.0 (caution for SaaS) |
| CVEs (2024-2026) | 3 moderate (patched) |

**Security Features:**
- Caching SHA-2 password authentication (default)
- TLS/SSL connections with X.509 cert auth
- Enterprise: Transparent Data Encryption (TDE)
- Audit plugin (Enterprise or Percona fork)

**Encryption at Rest:**
- InnoDB tablespace encryption (Enterprise or Percona 8.0+)
- Keyring plugin for key management

**Known CVEs:**
- CVE-2024-21096: mysqldump privilege escalation (patched in 8.0.37+)
- Multiple Oracle CPU patches — track quarterly

**Recommended Drivers:**
| Language | Driver | Version |
|----------|--------|---------|
| Node.js | mysql2 | 3.11.4 |
| Python | PyMySQL | 1.1.1 |
| Go | go-sql-driver/mysql | 1.8.1 |

**Compatibility Notes:**
- GPL license may require open-sourcing application code — prefer PostgreSQL for proprietary SaaS
- `sql_mode=STRICT_TRANS_TABLES` must be enabled

---

## 3. MongoDB 7.x

**Security Grade: B**

| Attribute | Value |
|-----------|-------|
| Version | 7.0.15 |
| License | SSPL (not OSI-approved — caution) |
| CVEs (2024-2026) | 2 moderate |

**Security Features:**
- SCRAM-SHA-256 authentication
- x.509 certificate authentication
- Field-level encryption (Client-Side FLE)
- Auditing enabled by default in Enterprise
- Network encryption via TLS

**Encryption at Rest:**
- Enterprise: Native encryption at rest
- Community: Encrypted storage engine (encrypted collections with FLE2)

**Known Issues:**
- SSPL license may not be suitable for all organizations
- Historical injection vulnerabilities in query parser (mostly resolved)

**Recommended Drivers:**
| Language | Driver | Version |
|----------|--------|---------|
| Node.js | mongodb | 6.10.0 |
| Python | pymongo | 4.10.1 |
| Go | go.mongodb.org/mongo-driver | 1.17.1 |

---

## 4. Redis 7.x

**Security Grade: B**

| Attribute | Value |
|-----------|-------|
| Version | 7.4.2 |
| License | BSD-3-Clause (last OSS-friendly release) |
| CVEs (2024-2026) | 1 critical (patched) |

**Security Features:**
- ACL (Access Control Lists) since Redis 6
- TLS support
- Command renaming/disabling for dangerous commands
- `protected-mode` enabled by default

**Encryption at Rest:**
- No native encryption at rest
- Use: dm-crypt, AWS ElastiCache encryption, or Valkey fork

**Known CVEs:**
- CVE-2024-31449: Lua scripting heap overflow (patched in 7.2.6+ / 7.4.1+)

**Recommended Drivers:**
| Language | Driver | Version |
|----------|--------|---------|
| Node.js | ioredis | 5.4.1 |
| Python | redis-py | 5.2.0 |
| Go | go-redis/v9 | 9.7.0 |

**Alternative:** Consider **Valkey 8.x** (open-source Redis fork, BSD-3 license)

---

## 5. SQLite 3.45.x

**Security Grade: A**

| Attribute | Value |
|-----------|-------|
| Version | 3.45.3 |
| License | Public Domain |
| CVEs (2024-2026) | 0 critical |

**Security Features:**
- File-level encryption via SEE or SQLCipher extension
- No network attack surface (embedded)
- WAL mode for concurrent reads

**Encryption at Rest:**
- SQLCipher 4.6.1 (AES-256-CBC, open source)
- SQLite Encryption Extension (SEE, commercial)

**Use Cases:** Local app storage, edge computing, testing

**Recommended Drivers:** Built into most language runtimes

---

## 6. ClickHouse 24.x

**Security Grade: B+**

| Attribute | Value |
|-----------|-------|
| Version | 24.8.5 LTS |
| License | Apache-2.0 |
| CVEs (2024-2026) | 1 low |

**Security Features:**
- Role-based access control
- TLS for native and HTTP protocols
- LDAP/ Kerberos integration
- Row-level security policies

**Encryption at Rest:**
- Encrypted disk configuration (AES-256-GCM)
- Cloud: ClickHouse Cloud native encryption

**Recommended Drivers:**
| Language | Driver | Version |
|----------|--------|---------|
| Python | clickhouse-connect | 0.8.0 |
| Go | clickhouse-go/v2 | 2.29.0 |
| Node.js | @clickhouse/client | 1.8.0 |

---

## 7. ScyllaDB 5.x

**Security Grade: B+**

| Attribute | Value |
|-----------|-------|
| Version | 5.4.6 |
| License | AGPL-3.0 (Enterprise: proprietary) |
| CVEs | Inherited from Cassandra protocol compat |

**Security Features:**
- Role-based access control
- TLS client-to-node and node-to-node
- LDAP authentication (Enterprise)
- Encryption at rest (Enterprise)

**Recommended Drivers:** Use Cassandra drivers (ScyllaDB is CQL-compatible)
| Language | Driver | Version |
|----------|--------|---------|
| Python | scylla-driver | 3.28.0 |
| Go | gocql | 1.7.0 |

---

## Security Comparison Matrix

| Feature | PostgreSQL | MySQL | MongoDB | Redis | SQLite | ClickHouse | ScyllaDB |
|---------|-----------|-------|---------|-------|--------|------------|----------|
| TLS | ✅ | ✅ | ✅ | ✅ | N/A | ✅ | ✅ |
| RBAC | ✅ | ✅ | ✅ | ✅ | N/A | ✅ | ✅ |
| Encryption at Rest | ⚠️ | ⚠️ | ✅ | ❌ | ⚠️ | ✅ | ⚠️ |
| Row-Level Security | ✅ | ❌ | ✅ | N/A | ❌ | ✅ | ❌ |
| Audit Logging | ✅ | ⚠️ | ✅ | ❌ | ❌ | ✅ | ⚠️ |
| Open License | ✅ | ⚠️ | ❌ | ✅ | ✅ | ✅ | ⚠️ |
| **Security Grade** | **A+** | **B+** | **B** | **B** | **A** | **B+** | **B+** |

✅ = Native support | ⚠️ = Partial/Extension | ❌ = Not available
