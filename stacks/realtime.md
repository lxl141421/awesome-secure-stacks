# Real-time & Messaging — Secure Stacks

> Last updated: 2026-05-31
> Review cadence: Monthly

---

## 1. WebSocket Libraries

### Socket.IO 4.7.x ⭐

**Security Grade: A**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Socket.IO Server | 4.7.5 | MIT | 0 |
| Socket.IO Client | 4.7.5 | MIT | 0 |
| Engine.IO | 6.5.5 | MIT | 0 |

**Security Configuration:**
```javascript
import { Server } from "socket.io";

const io = new Server(3000, {
  cors: {
    origin: ["https://app.example.com"],
    credentials: true,
    methods: ["GET", "POST"],
  },
  maxHttpBufferSize: 1e6, // 1MB max payload
  pingTimeout: 20000,
  pingInterval: 25000,
  connectTimeout: 10000,
  // Require authentication on connection
});

io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  if (!verifyToken(token)) {
    return next(new Error("Authentication failed"));
  }
  next();
});
```

**Security Best Practices:**
- Authenticate on connection (JWT or session token)
- Validate all event payloads with Zod/Joi schema
- Rate-limit events per socket
- Set `maxHttpBufferSize` to prevent memory exhaustion
- Use namespaced rooms for authorization boundaries
- Enable CORS with explicit origins (never `*`)

### ws 8.x (Raw WebSocket)

**Security Grade: A**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| ws | 8.18.0 | MIT | 0 |

**Security Configuration:**
```javascript
import { WebSocketServer } from "ws";

const wss = new WebSocketServer({
  port: 8080,
  maxPayload: 1024 * 1024, // 1MB
  perMessageDeflate: false, // Prevent compression-based attacks
  verifyClient: (info, callback) => {
    const token = new URL(info.req.url, "http://localhost")
      .searchParams.get("token");
    callback(verifyToken(token));
  },
});
```

**When to Use:**
- Socket.IO: feature-rich apps (auto-reconnect, rooms, namespaces)
- ws: raw performance, simple use cases, custom protocols

---

## 2. Message Queues

### RabbitMQ 3.13.x ⭐

**Security Grade: A**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| RabbitMQ | 3.13.7 | MPL-2.0 | 0 critical |
| Erlang/OTP | 26.2.5 | Apache-2.0 | 0 |

**Security Configuration:**
```erlang
%% rabbitmq.conf
listeners.tcp.local_only = false
listeners.ssl.default = 5671
ssl_options.cacertfile = /etc/rabbitmq/ca_certificate.pem
ssl_options.certfile   = /etc/rabbitmq/server_certificate.pem
ssl_options.keyfile    = /etc/rabbitmq/server_key.pem
ssl_options.verify     = verify_peer
ssl_options.fail_if_no_peer_cert = true

# Disable default guest user
loopback_users.guest = false
```

**Security Features:**
- TLS client certificate authentication
- Virtual hosts for tenant isolation
- Fine-grained permissions (configure/write/read per vhost)
- OAuth 2.0 plugin for modern auth
- Audit logging via firehose plugin

**Recommended Clients:**
| Language | Client | Version |
|----------|--------|---------|
| Node.js | amqplib | 0.10.4 |
| Python | pika | 1.3.2 |
| Go | amqp091-go | 2.1.0 |
| Java | amqp-client | 5.22.0 |

### Apache Kafka 3.7.x

**Security Grade: A**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| Kafka | 3.7.2 | Apache-2.0 | 0 critical |
| KRaft (no ZooKeeper) | 3.7.2 | Apache-2.0 | 0 |

**Security Configuration:**
```properties
# server.properties
security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-512
ssl.truststore.location=/etc/kafka/truststore.jks
ssl.keystore.location=/etc/kafka/keystore.jks
authorizer.class.name=org.apache.kafka.metadata.authorizer.StandardAuthorizer
allow.everyone.if.no.acl.found=false
```

**Security Features:**
- SASL/SCRAM-SHA-512 authentication
- ACL-based authorization
- TLS encryption in transit
- KRaft mode (no ZooKeeper dependency — reduced attack surface)

**Known Issues:**
- KRaft mode only (ZooKeeper fully removed in 4.0; using KRaft since 3.3+)
- Prefer KRaft mode for reduced attack surface

---

## 3. Pub/Sub Systems

### Redis Pub/Sub

**Security Grade: B+**

| Component | Pinned Version | License | Notes |
|-----------|---------------|---------|-------|
| Redis | 7.4.1 | RASL/SSPL | See database.md |

```javascript
// Node.js with ioredis
import Redis from "ioredis";

const pub = new Redis({
  host: "redis.internal",
  port: 6379,
  password: process.env.REDIS_PASSWORD,
  tls: { ca: fs.readFileSync("/certs/ca.pem") },
  maxRetriesPerRequest: 3,
});
```

**Limitations:**
- No message persistence (fire-and-forget)
- No consumer groups (use Redis Streams for these)
- No delivery guarantees

**Recommendation:** Use Redis Streams (XREAD/XADD) for production pub/sub needs.

### NATS 2.10.x ⭐

**Security Grade: A**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
|| NATS Server | 2.10.22 | Apache-2.0 | 0 |
| JetStream | (built-in) | Apache-2.0 | 0 |
| nats.go | 1.37.0 | Apache-2.0 | 0 |
| nats.ws | 1.28.0 | Apache-2.0 | 0 |

**Security Configuration:**
```hcl
# nats-server.conf
authorization {
  users: [
    { user: "app", password: "$2a$11$...", permissions: {
      publish: ["orders.>", "events.>"],
      subscribe: ["orders.>", "notifications.>"]
    }},
  ]
}
tls {
  cert_file: "/certs/server.pem"
  key_file: "/certs/server-key.pem"
  ca_file: "/certs/ca.pem"
  verify: true
}
jetstream {
  store_dir: "/data/jetstream"
  max_mem: 1G
  max_file: 10G
}
```

**Security Features:**
- JWT/NKey-based decentralized auth
- TLS with mutual authentication
- Fine-grained publish/subscribe permissions
- JetStream for durable, at-least-once delivery
- Account isolation (multi-tenancy)

**Why NATS over Redis Pub/Sub:**
- Built-in persistence (JetStream)
- Proper auth model
- Better for microservices patterns

---

## 4. gRPC

### grpc-go (Go) 1.72.x

**Security Grade: A**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| grpc-go | 1.72.1 | Apache-2.0 | 0 |
| protobuf-go | 1.36.6 | BSD-3 | 0 |

```go
// Server with TLS
creds, err := credentials.NewServerTLSFromFile("server.pem", "server-key.pem")
s := grpc.NewServer(grpc.Creds(creds))
```

### @grpc/grpc-js (Node.js) 1.13.x

**Security Grade: A**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| @grpc/grpc-js | 1.13.0 | Apache-2.0 | 0 |
| @grpc/proto-loader | 0.7.15 | Apache-2.0 | 0 |
| protobufjs | 7.4.0 | BSD-3 | 0 |

```typescript
import * as grpc from "@grpc/grpc-js";
import * as fs from "fs";

const creds = grpc.ServerCredentials.createSsl(
  fs.readFileSync("ca.pem"),
  [{
    cert_chain: fs.readFileSync("server.pem"),
    private_key: fs.readFileSync("server-key.pem"),
  }],
  false // checkClientCertificate
);
```

**gRPC Security Best Practices:**
- Always use TLS (plaintext gRPC is insecure)
- Implement interceptors for authentication (JWT validation)
- Set max message sizes to prevent memory exhaustion
- Use deadline/timeouts on all calls
- Enable health checking for load balancer integration

---

## Security Comparison Matrix

| Feature | Socket.IO | ws | RabbitMQ | Kafka | NATS | gRPC |
|---------|-----------|-----|----------|-------|------|------|
| TLS | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Auth | JWT/Custom | Custom | SASL/SCRAM | SASL/OAuth | NKey/JWT | mTLS |
| Persistence | ❌ | ❌ | ✅ | ✅ | ✅ (JS) | ❌ |
| Replay | ❌ | ❌ | ❌ | ✅ | ✅ (JS) | ❌ |
| Max Payload | Configurable | Configurable | Configurable | 1MB default | 1MB default | 4MB default |
|| **Grade** | **A** | **A** | **A** | **A** | **A** | **A** |
