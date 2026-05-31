# Distributed Systems & Microservices — Security Guide

> Last updated: 2026-05-31 | Stability-first: LTS and battle-tested releases only

---

## 1. Service Mesh

### Istio 1.21.x

**Security Score: A+**
**Stability: ★★★★★**

| Component       | Version  | EOL       | Notes                           |
|-----------------|----------|-----------|---------------------------------|
| Istio           | 1.21.x   | 2024-12   | Envoy-based, mature mTLS       |
| Envoy Proxy     | 1.29.x   | Tied      | Data plane                      |

#### mTLS Configuration (Strict Mode)

```yaml
# PeerAuthentication — enforce mTLS cluster-wide
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system  # Mesh-wide
spec:
  mtls:
    mode: STRICT
```

```yaml
# AuthorizationPolicy — zero-trust service-to-service
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
        methods: ["POST"]
        paths: ["/api/orders"]
```

#### Security Checklist — Istio

- [ ] Enable `STRICT` mTLS mesh-wide — no `PERMISSIVE` mode in production
- [ ] Use `AuthorizationPolicy` for service-to-service access control
- [ ] Enable **Envoy access logging** for audit trails
- [ ] Rotate root CA certificates annually (Istio Citadel or external CA)
- [ ] Use `PeerAuthentication` per namespace for gradual mTLS rollout
- [ ] Enable **Envoy rate limiting** at sidecar level
- [ ] Monitor `istio_requests_total` for anomalous traffic patterns
- [ ] Disable `ALLOW_ANY` for external traffic — use `REGISTRY_ONLY`

---

### Linkerd 2.14.x

**Security Score: A+**
**Stability: ★★★★★**

| Component       | Version  | EOL       | Notes                           |
|-----------------|----------|-----------|---------------------------------|
| Linkerd         | 2.14.x   | Active    | Lightweight, Rust data plane    |
| linkerd2-proxy  | Current  | Tied      | Rust-based, memory-safe         |

#### mTLS Configuration

```yaml
# Linkerd enables mTLS automatically — verify it's active
# Check: linkerd diagnostics authz -n production deploy/order-service

# ServiceProfile for fine-grained routing
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: order-service.production.svc.cluster.local
  namespace: production
spec:
  routes:
  - name: POST /api/orders
    condition:
      method: POST
      pathRegex: /api/orders
```

```bash
# Verify mTLS is active
linkerd viz edges deploy -n production
# All edges should show "mTLS: true"
```

#### Security Checklist — Linkerd

- [ ] Verify mTLS is active on all edges: `linkerd viz edges deploy`
- [ ] Use `ServerAuthorization` for access control
- [ ] Enable **tap** for traffic inspection (disable in production after debugging)
- [ ] Monitor certificate rotation: `linkerd check --proxy`
- [ ] Use `linkerd viz stat` for anomaly detection
- [ ] Restrict Linkerd dashboard access to admin network only

---

### Cilium 1.15.x

**Security Score: A+**
**Stability: ★★★★☆**

| Component       | Version  | EOL       | Notes                           |
|-----------------|----------|-----------|---------------------------------|
| Cilium          | 1.15.x   | Active    | eBPF-based, L3/L4/L7 policies  |
| Hubble          | 1.15.x   | Tied      | Network observability           |

#### Network Policy (L3/L4/L7)

```yaml
# CiliumNetworkPolicy — L7-aware
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: order-service-policy
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: order-service
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: api-gateway
    toPorts:
    - ports:
      - port: "8080"
        protocol: TCP
      rules:
        http:
        - method: POST
          path: "/api/orders"
        - method: GET
          path: "/api/orders/.*"
          headers:
          - 'Authorization: Bearer .*'
```

#### Security Checklist — Cilium

- [ ] Enable **eBPF-based encryption** (WireGuard) for pod-to-pod traffic
- [ ] Use `CiliumNetworkPolicy` with L7 rules — not just `NetworkPolicy`
- [ ] Enable Hubble for flow visibility and anomaly detection
- [ ] Use **Cilium Tetragon** for runtime security (process, file, network)
- [ ] Enable DNS-aware policies to prevent DNS exfiltration
- [ ] Audit `CiliumEnvoyConfig` for custom Envoy filters

### Service Mesh Comparison

| Feature              | Istio 1.21      | Linkerd 2.14     | Cilium 1.15      |
|----------------------|-----------------|------------------|-------------------|
| Data plane           | Envoy (C++)     | linkerd-proxy (Rust)| eBPF (kernel)  |
| mTLS                 | Built-in        | Automatic        | WireGuard         |
| L7 policies          | AuthorizationPolicy | ServerAuth    | CiliumNetworkPolicy|
| Resource overhead    | High            | Low              | Very Low          |
| Complexity           | High            | Low              | Medium            |
| Best for             | Enterprise      | Simplicity       | Performance       |

---

## 2. API Gateway

### Kong 3.6.x

**Security Score: A**
**Stability: ★★★★★**

```yaml
# Kong declarative config — security plugins
services:
- name: order-service
  url: http://order-service.production:8080
  routes:
  - name: orders-api
    paths: ["/api/orders"]
    strip_path: true
    protocols: [https]

  plugins:
  - name: rate-limiting
    config:
      minute: 100
      policy: redis
      redis_host: redis.production
  - name: jwt
    config:
      claims_to_verify: [exp]
      key_claim_name: kid
  - name: cors
    config:
      origins: ["https://app.example.com"]
      methods: [GET, POST, PUT, DELETE]
      headers: [Authorization, Content-Type]
      max_age: 3600
  - name: ip-restriction
    config:
      deny: ["10.0.0.0/8"]  # Block internal ranges from external
```

### APISIX 3.9.x

**Security Score: A**
**Stability: ★★★★☆**

```yaml
# APISIX route with security plugins
routes:
  - uri: /api/orders*
    upstream:
      type: roundrobin
      nodes:
        "order-service:8080": 1
    plugins:
      jwt-auth: {}
      rate-limit:
        count: 100
        time_window: 60
        rejected_code: 429
      cors:
        allow_origins: "https://app.example.com"
        allow_methods: "GET,POST,PUT,DELETE"
      prometheus: {}
```

### API Gateway Security Checklist

- [ ] Enforce HTTPS termination at gateway — no cleartext to backends
- [ ] Implement **JWT validation** at gateway level (not per-service)
- [ ] Rate limit per API key AND per IP
- [ ] Use **request size limits** to prevent payload attacks
- [ ] Enable **WAF plugins** (ModSecurity / Coraza integration)
- [ ] Strip `Server`, `X-Powered-By` headers from responses
- [ ] Implement **circuit breaker** at gateway level
- [ ] Log all requests with correlation IDs for audit

---

## 3. Distributed Tracing

### OpenTelemetry + Jaeger 1.54

```yaml
# OpenTelemetry Collector configuration
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
        tls:
          cert_file: /etc/otel/collector.crt
          key_file: /etc/otel/collector.key
          client_ca_file: /etc/otel/ca.crt
          client_auth_type: require_and_verify_client_cert

processors:
  batch:
    timeout: 5s
  # Scrub sensitive data from spans
  attributes:
    actions:
    - key: db.statement
      action: hash  # Hash SQL queries, don't store plaintext
    - key: http.request.header.authorization
      action: delete  # Never export auth tokens
    - key: user.email
      action: hash

exporters:
  jaeger:
    endpoint: jaeger-collector.observability:14250
    tls:
      cert_file: /etc/otel/collector.crt
      key_file: /etc/otel/collector.key

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, attributes]
      exporters: [jaeger]
```

### Grafana Tempo 2.4

```yaml
# Tempo configuration — trace storage
server:
  http_listen_port: 3200

distributor:
  receivers:
    otlp:
      protocols:
        grpc:
          tls_config:
            cert_file: /etc/tempo/server.crt
            key_file: /etc/tempo/server.key
            client_ca_file: /etc/tempo/ca.crt

storage:
  trace:
    backend: s3
    s3:
      bucket: tempo-traces
      endpoint: minio.internal:9000
      insecure: false
```

### Tracing Security Checklist

- [ ] **Never export PII or secrets** in span attributes
- [ ] Hash or redact sensitive fields (SQL queries, headers, request bodies)
- [ ] Use mTLS for collector → backend communication
- [ ] Restrict Jaeger/Tempo UI access to admin network
- [ ] Set trace retention policies (30 days default, 90 for compliance)
- [ ] Use RBAC for trace query access

---

## 4. Service Discovery

### Consul 1.18.x

```hcl
# Consul server configuration — security hardening
datacenter = "dc1"
encrypt = "<gossip-encryption-key>"
tls {
  defaults {
    ca_file   = "/etc/consul/ca.pem"
    cert_file = "/etc/consul/server.pem"
    key_file  = "/etc/consul/server-key.pem"
    verify_incoming = true
    verify_outgoing = true
  }
}
acl {
  enabled = true
  default_policy = "deny"
  tokens {
    initial_management = "<bootstrap-token>"
  }
}
```

### etcd 3.5.x

```yaml
# etcd security configuration
etcd:
  peer-transport-security:
    cert-file: /etc/etcd/server.crt
    key-file: /etc/etcd/server.key
    client-cert-auth: true
    trusted-ca-file: /etc/etcd/ca.crt
  client-transport-security:
    cert-file: /etc/etcd/server.crt
    key-file: /etc/etcd/server.key
    client-cert-auth: true
    trusted-ca-file: /etc/etcd/ca.crt
```

### Service Discovery Security Checklist

- [ ] Enable **gossip encryption** (Consul) or **peer TLS** (etcd)
- [ ] Use ACLs to restrict which services can discover which
- [ ] Enable **auto-encrypt** for service TLS certificates
- [ ] Rotate encryption keys quarterly
- [ ] Monitor for unauthorized service registrations

---

## 5. Distributed Transactions

### Saga Pattern Implementation

```go
// Go — Choreography-based Saga with compensation
type OrderSaga struct {
    Steps []SagaStep
}

type SagaStep struct {
    Execute    func(ctx context.Context, data *OrderData) error
    Compensate func(ctx context.Context, data *OrderData) error
}

func (s *OrderSaga) Run(ctx context.Context, data *OrderData) error {
    completed := make([]int, 0, len(s.Steps))

    for i, step := range s.Steps {
        if err := step.Execute(ctx, data); err != nil {
            // Compensate in reverse order
            for j := len(completed) - 1; j >= 0; j-- {
                if compErr := s.Steps[completed[j]].Compensate(ctx, data); compErr != nil {
                    // Log — compensation failure requires manual intervention
                    slog.Error("saga compensation failed",
                        "step", completed[j], "error", compErr)
                }
            }
            return fmt.Errorf("saga failed at step %d: %w", i, err)
        }
        completed = append(completed, i)
    }
    return nil
}

// Usage
saga := &OrderSaga{
    Steps: []SagaStep{
        {Execute: reserveInventory, Compensate: releaseInventory},
        {Execute: chargePayment, Compensate: refundPayment},
        {Execute: createShipment, Compensate: cancelShipment},
    },
}
```

### Saga Security Considerations

- [ ] **Idempotency keys** on all saga steps — prevent duplicate execution
- [ ] **Signed saga state** — prevent tampering with saga progress
- [ ] **Timeout + dead-letter** for stuck sagas
- [ ] **Audit log** every step execution and compensation
- [ ] **Encrypt saga state** if stored in external store

---

## 6. Message-Driven: Kafka 3.7 + Schema Registry

**Security Score: A**
**Stability: ★★★★★**

### Security Configuration

```yaml
# Kafka broker security
security.inter.broker.protocol: SASL_SSL
sasl.mechanism.inter.broker.protocol: SCRAM-SHA-512
ssl.keystore.location: /etc/kafka/kafka.server.keystore.jks
ssl.keystore.password: ${KEYSTORE_PASSWORD}
ssl.truststore.location: /etc/kafka/kafka.server.truststore.jks
ssl.truststore.password: ${TRUSTSTORE_PASSWORD}
ssl.client.auth: required

# ACLs
authorizer.class.name=kafka.security.authorizer.AclAuthorizer
super.users=User:admin
allow.everyone.if.no.acl.found=false
```

```bash
# Create ACLs — principle of least privilege
kafka-acls --add --allow-principal User:order-service \
  --operation Write --topic orders \
  --bootstrap-server kafka-0:9093 \
  --command-config admin.properties

kafka-acls --add --allow-principal User:payment-service \
  --operation Read --topic orders --group payment-group \
  --bootstrap-server kafka-0:9093 \
  --command-config admin.properties
```

### Schema Registry Security

```yaml
# Schema Registry with authentication
kafkastore.bootstrap.servers: SASL_SSL://kafka-0:9093
authentication.method: BASIC
authentication.realm: SchemaRegistry-Props
authentication.roles: ["admin", "developer", "reader"]

# Schema compatibility — prevent breaking changes
schema.compatibility.level: BACKWARD
```

### Kafka Security Checklist

- [ ] Enable **SASL_SSL** — never use PLAINTEXT in production
- [ ] Use **ACLs** per topic per service (principle of least privilege)
- [ ] Enable **Schema Registry** with `BACKWARD` compatibility
- [ ] Encrypt data in transit (TLS) and at rest (volume encryption)
- [ ] Use **idempotent producers** (`enable.idempotence=true`)
- [ ] Set **retention policies** — auto-delete sensitive data
- [ ] Monitor consumer lag for stuck consumers
- [ ] Enable **audit logging** for admin operations

---

## 7. Monolith → Microservices: Strangler Fig Pattern

```go
// Go — Strangler Fig proxy with gradual migration
func stranglerProxy(monolith, microservice http.Handler, routes map[string]string) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Route decision: which backend handles this path?
        if backend, ok := routes[r.URL.Path]; ok {
            switch backend {
            case "microservice":
                // New service handles this
                slog.Info("routed to microservice", "path", r.URL.Path)
                microservice.ServeHTTP(w, r)
            case "monolith":
                // Legacy handles this
                slog.Info("routed to monolith", "path", r.URL.Path)
                monolith.ServeHTTP(w, r)
            case "shadow":
                // Shadow mode: send to both, use monolith response
                rec := httptest.NewRecorder()
                go microservice.ServeHTTP(rec, r)
                monolith.ServeHTTP(w, r)
                // Compare responses asynchronously
            default:
                monolith.ServeHTTP(w, r) // Default: monolith
            }
        } else {
            monolith.ServeHTTP(w, r)
        }
    })
}
```

### Migration Security Checklist

- [ ] **Shadow mode** first — route to both, compare responses
- [ ] **Feature flags** for gradual traffic shifting
- [ ] **Consistent authentication** across monolith and microservices
- [ ] **Shared secret management** during migration (Vault, AWS Secrets Manager)
- [ ] **Contract testing** between old and new services
- [ ] **Rollback plan** with < 5 minute RTO
- [ ] **Security review** at each migration stage

---

## Zero-Trust Networking Checklist

- [ ] **mTLS everywhere** — no plaintext service-to-service communication
- [ ] **Identity-based access** — service identity via SPIFFE/SPIRE or mesh
- [ ] **Least privilege** — each service can only reach what it needs
- [ ] **No implicit trust** — even internal traffic is authenticated and authorized
- [ ] **Encryption at rest** — all data stores encrypted (KMS-managed keys)
- [ ] **Secret rotation** — automated rotation of all certificates and keys
- [ ] **Audit logging** — every access logged with correlation ID
- [ ] **Network segmentation** — namespaces, network policies, service mesh

## Secret Rotation Schedule

| Secret Type           | Rotation Period | Method                     |
|-----------------------|-----------------|----------------------------|
| TLS certificates      | 90 days         | cert-manager / SPIRE       |
| Database credentials  | 30 days         | Vault dynamic secrets      |
| API keys              | 90 days         | Automated key rollover     |
| Kafka SASL passwords  | 30 days         | Vault + Kafka integration  |
| Gossip encryption key | 90 days         | Consul key rotation        |
| JWT signing keys      | 24 hours        | JWKS with auto-rotation    |

## Circuit Breaker Patterns

```go
// Go — Circuit breaker with security-aware thresholds
type CircuitBreaker struct {
    failures    int
    threshold   int
    resetAfter  time.Duration
    lastFailure time.Time
    state       string // "closed", "open", "half-open"
    mu          sync.Mutex
}

func (cb *CircuitBreaker) Call(fn func() error) error {
    cb.mu.Lock()
    if cb.state == "open" {
        if time.Since(cb.lastFailure) > cb.resetAfter {
            cb.state = "half-open"
        } else {
            cb.mu.Unlock()
            return errors.New("circuit open — request rejected")
        }
    }
    cb.mu.Unlock()

    err := fn()

    cb.mu.Lock()
    defer cb.mu.Unlock()
    if err != nil {
        cb.failures++
        cb.lastFailure = time.Now()
        if cb.failures >= cb.threshold {
            cb.state = "open"
            slog.Warn("circuit opened", "failures", cb.failures)
        }
        return err
    }

    cb.failures = 0
    cb.state = "closed"
    return nil
}
```

---

## Cross-Component Security Summary

| Component              | Score | mTLS | Zero-Trust | Complexity |
|------------------------|-------|------|------------|------------|
| Istio 1.21             | A+    | ✓    | ✓          | High       |
| Linkerd 2.14           | A+    | ✓    | ✓          | Low        |
| Cilium 1.15            | A+    | ✓    | ✓          | Medium     |
| Kong 3.6               | A     | ✓    | Partial    | Medium     |
| APISIX 3.9             | A     | ✓    | Partial    | Medium     |
| Consul 1.18            | A     | ✓    | ✓          | Medium     |
| etcd 3.5               | A     | ✓    | ✓          | Low        |
| Kafka 3.7              | A     | ✓    | ✓          | Medium     |
| Jaeger 1.54            | A-    | ✓    | Partial    | Low        |
| Tempo 2.4              | A-    | ✓    | Partial    | Low        |
