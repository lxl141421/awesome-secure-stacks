# AI/LLM Application Development Stacks — Secure Stacks

> Last updated: 2026-05-31
> Review cadence: Bi-weekly (rapid ecosystem changes)
> ⚠️ LLM application stack has unique supply chain risks — see AI特有供应链风险 section

---

## 1. LLM Application Frameworks

**Security Grade: B-** (fast-moving, broad attack surface)

| Component | Pinned Version | License | Security Score |
|-----------|---------------|---------|----------------|
| LangChain | 0.2.17 | MIT | 6/10 |
| LlamaIndex | 0.10.68 | MIT | 7/10 |
| Semantic Kernel | 1.6.0 | MIT | 8/10 |

### LangChain
- **Version:** 0.2.17 (pin to minor, not latest)
- **Security Score:** 6/10
- **Known Risks:**
  - Broad dependency tree — transitive vulnerabilities common
  - `Chain.invoke()` can execute arbitrary code via prompt chains
  - `LLMMathChain` historically used `numexpr` with eval-like behavior
  - Plugin/tool ecosystem has minimal vetting
  - Historically had deserialization vulnerabilities (pickle in `load_chain`)
- **Mitigation:**
  - Use `langchain-core` only if possible (smaller surface)
  - Avoid `pickle`-based serialization — use JSON
  - Pin all transitive dependencies
  - Disable arbitrary tool execution in production
  - Use `langchain-sandbox` for code execution tools
- **Lockfile:**
  ```
  langchain-core==0.2.43
  langchain-community==0.2.17
  langchain-text-splitters==0.2.4
  # Avoid langchain-experimental in production
  ```

### LlamaIndex
- **Version:** 0.10.68
- **Security Score:** 7/10
- **Known Risks:**
  - Document loaders can execute embedded scripts
  - Custom reader plugins may have arbitrary code execution
  - Index serialization uses pickle by default in some formats
- **Mitigation:**
  - Use `Document` objects with sanitized content only
  - Enable `strict` mode for document loading
  - Avoid custom readers from untrusted sources
  - Use JSON-based index persistence, not pickle

### Semantic Kernel
- **Version:** 1.6.0
- **Security Score:** 8/10
- **Known Risks:**
  - Plugin system allows native code execution
  - OpenAPI plugin connector can access arbitrary endpoints
- **Mitigation:**
  - Use plugin sandboxing
  - Restrict OpenAPI plugin to approved endpoints
  - Enable Microsoft Defender for Cloud integration

---

## 2. Vector Databases

**Security Grade: B**

| Component | Pinned Version | License | Security Score |
|-----------|---------------|---------|----------------|
| Qdrant | 1.8.4 | Apache-2.0 | 8/10 |
| Milvus | 2.4.13 | Apache-2.0 | 7/10 |
| Chroma | 0.5.23 | Apache-2.0 | 7/10 |
| Weaviate | 1.25.24 | BSD-3 | 8/10 |

### Qdrant
- **Version:** 1.8.4
- **Security Score:** 8/10
- **Known Risks:**
  - gRPC API — ensure TLS is enabled
  - Snapshot API can leak collection data if exposed
- **Mitigation:**
  - Enable API key authentication
  - Use TLS for all connections
  - Restrict snapshot API to admin-only
  - Run behind reverse proxy with rate limiting

### Milvus
- **Version:** 2.4.13
- **Security Score:** 7/10
- **Known Risks:**
  - Depends on etcd (coordination) — etcd has its own attack surface
  - MinIO/S3 for storage — credentials management critical
  - Large deployment surface (multiple components)
- **Mitigation:**
  - Use Milvus Lite for simpler deployments
  - Enable RBAC with authentication
  - Encrypt data at rest in object storage
  - Network-isolate etcd access

### Chroma
- **Version:** 0.5.23
- **Security Score:** 7/10
- **Known Risks:**
  - Client-server mode has minimal auth by default
  - SQLite backend for local — file permissions matter
  - Relatively young project — security audit history limited
- **Mitigation:**
  - Enable authentication for server mode
  - Use file-system permissions for local SQLite
  - Run in containerized environment

### Weaviate
- **Version:** 1.25.24
- **Security Score:** 8/10
- **Known Risks:**
  - OIDC/OAuth configuration complexity
  - Module system (text2vec-*) processes external data
- **Mitigation:**
  - Enable authentication (OIDC or API key)
  - Restrict module network access
  - Use private-by-default collections

---

## 3. Embedding Models

**Security Grade: B+**

| Component | Pinned Version | License | Security Score |
|-----------|---------------|---------|----------------|
| text-embedding-3-small | API (OpenAI) | Proprietary | 7/10 |
| text-embedding-3-large | API (OpenAI) | Proprietary | 7/10 |
| BGE-large-en-v1.5 | 1.5 | MIT | 9/10 |
| E5-large-v2 | 2.0 | MIT | 9/10 |
| Nomic Embed | 1.5 | Apache-2.0 | 8/10 |

### Cloud Embedding (OpenAI, Cohere, etc.)
- **Security Score:** 7/10
- **Risks:** Data sent to external API, PII leakage in embeddings
- **Mitigation:** Strip PII before embedding, use API data retention policies

### Self-Hosted Embeddings (BGE, E5)
- **Security Score:** 9/10
- **Risks:** Model download integrity, ONNX/safetensors file tampering
- **Mitigation:**
  - Verify model checksums from HuggingFace
  - Use `safetensors` format only
  - Download from official repos only

---

## 4. LLM Serving Infrastructure

**Security Grade: B**

| Component | Pinned Version | License | Security Score |
|-----------|---------------|---------|----------------|
| vLLM | 0.6.3 | Apache-2.0 | 7/10 |
| Ollama | 0.3.14 | MIT | 8/10 |
| TGI (Text Generation Inference) | 2.3.2 | Apache-2.0 | 7/10 |

### vLLM
- **Version:** 0.6.3
- **Security Score:** 7/10
- **Known Risks:**
  - OpenAI-compatible API — no built-in auth by default
  - Model loading uses `torch.load` (pickle risk for untrusted models)
  - High GPU memory usage — denial of service via large requests
- **Mitigation:**
  - Add API authentication via reverse proxy (nginx + auth)
  - Use `safetensors` models only (set `--load-format safetensors`)
  - Set `--max-model-len` and rate limiting
  - Run in isolated container with GPU quota

### Ollama
- **Version:** 0.3.14
- **Security Score:** 8/10
- **Known Risks:**
  - Default API binds to localhost only (good)
  - `ollama pull` downloads models without signature verification
  - Model blobs stored with permissive file permissions
- **Mitigation:**
  - Don't expose Ollama API to network without auth
  - Verify model checksums after download
  - Set restrictive file permissions on `~/.ollama/models`

### TGI (Text Generation Inference)
- **Version:** 2.3.2
- **Security Score:** 7/10
- **Known Risks:**
  - HuggingFace token management required for gated models
  - Token streaming can leak partial responses
- **Mitigation:**
  - Use HuggingFace token with minimal scopes
  - Enable output filtering for sensitive content
  - Set request timeout and token limits

---

## 5. AI Agent Frameworks

**Security Grade: C+** (highest risk category — autonomous code execution)

| Component | Pinned Version | License | Security Score |
|-----------|---------------|---------|----------------|
| AutoGen | 0.4.0 | MIT | 6/10 |
| CrewAI | 0.8.6 | MIT | 6/10 |
| LangGraph | 0.2.53 | MIT | 7/10 |

### AutoGen
- **Version:** 0.4.0
- **Security Score:** 6/10
- **Known Risks:**
  - Multi-agent code execution — agents can run arbitrary code
  - Group chat mode allows agent-to-agent collusion
  - Docker code execution recommended but not enforced
- **Mitigation:**
  - Always use Docker sandboxing for code execution agents
  - Set `human_input_mode="ALWAYS"` for production
  - Restrict agent tool access to approved set
  - Implement conversation timeout and token limits

### CrewAI
- **Version:** 0.8.6
- **Security Score:** 6/10
- **Known Risks:**
  - Tool delegation allows agents to grant tools to other agents
  - Process execution tools can escape sandbox
  - Third-party tool integrations have broad permissions
- **Mitigation:**
  - Audit all tool definitions before deployment
  - Disable tool delegation in production
  - Use environment variable isolation per agent

### LangGraph
- **Version:** 0.2.53
- **Security Score:** 7/10
- **Known Risks:**
  - State persistence can store sensitive data
  - Human-in-the-loop patterns may bypass security checks
  - Checkpoint storage requires secure backend
- **Mitigation:**
  - Encrypt checkpoint storage
  - Sanitize state before persistence
  - Validate all human inputs in HITL patterns

---

## 6. RAG Security Patterns

### Secure Retrieval
```
┌──────────┐    ┌───────────┐    ┌──────────┐    ┌──────────┐
│  Query    │──▶│ Sanitize  │──▶│ Retrieve │──▶│ Filter   │──▶ LLM
│  Input    │   │ Query     │   │ Documents│   │ Results  │
└──────────┘    └───────────┘    └──────────┘    └──────────┘
                     │                                │
                 Remove injection               Remove sensitive
                 patterns                       metadata/PII
```

### Document Sanitization Pipeline
```python
# Sanitize documents before indexing
def sanitize_document(doc: str) -> str:
    # 1. Remove potential prompt injection patterns
    doc = re.sub(r'(ignore|forget|disregard)\s+(previous|above|all)', '[FILTERED]', doc, flags=re.IGNORECASE)
    # 2. Strip HTML/script tags
    doc = bleach.clean(doc, tags=[], strip=True)
    # 3. Remove control characters
    doc = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', doc)
    # 4. Truncate to max length
    return doc[:MAX_DOC_LENGTH]
```

### Prompt Injection Defense for RAG
- **Input filtering:** Detect and block common injection patterns in queries
- **Output filtering:** Validate LLM responses don't contain leaked context
- **Context isolation:** Use system/user message separation strictly
- **Instruction hierarchy:** System prompt > retrieved context > user query
- **Canary tokens:** Insert unique tokens in context to detect leakage

---

## 7. AI Security: Production Checklist

### Prompt Injection Prevention
- [ ] Input validation and sanitization on all user inputs
- [ ] Separate system instructions from user content (use structured prompts)
- [ ] Implement input length limits
- [ ] Detect common injection patterns ("ignore previous instructions", etc.)
- [ ] Use content classifiers to flag adversarial inputs

### Output Sanitization
- [ ] Validate LLM output format before processing
- [ ] Strip or escape HTML/SQL/commands from LLM responses
- [ ] Implement output length limits
- [ ] Monitor for PII leakage in outputs
- [ ] Rate-limit output generation

### Model Access Control
- [ ] API key rotation policy (90-day max)
- [ ] Per-user/per-service rate limits
- [ ] Model access audit logging
- [ ] Separate API keys for dev/staging/prod
- [ ] Monitor token usage for anomalies

### Data Leakage Prevention
- [ ] Strip PII before sending to external LLM APIs
- [ ] Use data loss prevention (DLP) filters on inputs
- [ ] Configure API data retention policies (opt out of training)
- [ ] Encrypt prompts/responses in transit and at rest
- [ ] Audit what data flows to which model provider

---

## 8. Local/Edge AI Deployment

**Security Grade: A-** (no data leaves the device)

| Component | Pinned Version | License | Security Score |
|-----------|---------------|---------|----------------|
| ONNX Runtime | 1.17.5 | MIT | 9/10 |
| llama.cpp | b3700+ | MIT | 9/10 |
| MLX | 0.21.x | MIT | 9/10 |

### ONNX Runtime
- **Version:** 1.17.5
- **Security Score:** 9/10
- **Known Risks:**
  - ONNX model files can contain adversarial inputs
  - Model download integrity verification needed
- **Mitigation:**
  - Verify model file checksums
  - Use models from trusted sources only
  - Run inference in isolated process

### llama.cpp
- **Version:** b3700+
- **Security Score:** 9/10
- **Known Risks:**
  - GGUF model format — ensure files from trusted sources
  - C/C++ codebase — memory safety considerations
  - Network mode (`--server`) has minimal auth by default
- **Mitigation:**
  - Verify GGUF file SHA256 checksums
  - Don't expose server mode to network without reverse proxy auth
  - Keep updated for security patches

### MLX (Apple Silicon)
- **Version:** 0.21.x
- **Security Score:** 9/10
- **Known Risks:**
  - Apple Silicon only — limited ecosystem
  - Model conversion pipeline (HuggingFace → MLX format) can be tampered
- **Mitigation:**
  - Verify model conversion provenance
  - Use official MLX model repositories
  - Standard sandboxing applies

---

## 9. AI特有供应链风险 (AI-Specific Supply Chain Risks)

### 9.1 Model Poisoning
- **Risk:** Adversarial modifications to model weights during training or distribution
- **Attack Vector:** Backdoored models that generate malicious code or leak data on trigger
- **Severity:** Critical
- **Mitigation:**
  - Only use models from verified publishers (HuggingFace verified badges)
  - Verify model file checksums (SHA256) against published values
  - Test models with known-clean benchmark inputs
  - Use model signing when available (SafeTensors + signatures)
  - Prefer models with documented training data provenance

### 9.2 Malicious Python Packages for AI
- **Risk:** Typosquatting on popular AI package names
- **Attack Vector:** `langchain-plus` instead of `langchain`, `openai-utils` (fake)
- **Severity:** High
- **Mitigation:**
  ```bash
  # Verify package author and download count
  pip index versions <package>
  # Use lockfiles with hashes
  pip-compile --generate-hashes requirements.in
  # Audit dependencies
  pip-audit
  ```

### 9.3 HuggingFace Model Hub Risks
- **Risk:** Models with embedded malicious code (pickle deserialization)
- **Attack Vector:** `.pt`/`.bin` model files containing arbitrary Python code
- **Severity:** Critical
- **Mitigation:**
  - Use `safetensors` format exclusively
  - Avoid loading models with `torch.load()` on untrusted files
  - Use `huggingface_hub` with `local_files_only=True` in production
  - Scan model files with `picklescan` before loading
  ```bash
  pip install picklescan
  python -m picklescan --scan model.bin
  ```

### 9.4 Prompt Data Poisoning (RAG-specific)
- **Risk:** Malicious content in document corpus that manipulates LLM behavior
- **Attack Vector:** Injected "ignore instructions" text in crawled documents
- **Severity:** High
- **Mitigation:**
  - Sanitize all documents before indexing (see Section 6)
  - Use content trust scoring for document sources
  - Implement output validation against expected formats
  - Monitor for anomalous model behavior post-indexing

### 9.5 API Key and Token Exposure
- **Risk:** LLM API keys leaked in code, logs, or embeddings
- **Attack Vector:** AI-generated code that hardcodes API keys
- **Severity:** High
- **Mitigation:**
  - Use secret scanning in CI (gitleaks, trufflehog)
  - Rotate API keys on developer departure
  - Use environment variables or secret managers exclusively
  - Scan embeddings for sensitive data patterns

---

## 10. Deployment Security Checklist

### Container Security for AI Services
```dockerfile
# Secure LLM serving container
FROM python:3.12-slim AS base
RUN useradd -m -r -s /bin/bash appuser
WORKDIR /app
COPY --chown=appuser:appuser requirements-lock.txt .
RUN pip install --no-cache-dir --require-hashes -r requirements-lock.txt
COPY --chown=appuser:appuser . .
USER appuser
EXPOSE 8000
# Non-root, read-only filesystem, no shell
```

### Network Security
- [ ] AI serving endpoints behind API gateway
- [ ] Rate limiting per client
- [ ] TLS everywhere (model serving ↔ application ↔ client)
- [ ] No direct internet access from model serving containers
- [ ] WAF rules for prompt injection patterns

### Monitoring
- [ ] Log all LLM API requests (sanitized) for audit
- [ ] Monitor for unusual token consumption patterns
- [ ] Alert on prompt injection detection
- [ ] Track model response quality degradation
- [ ] Monitor for data exfiltration patterns in outputs

---

## 11. Version Pinning & Lockfile Strategy

```txt
# requirements-lock.txt — AI/LLM Application Stack
langchain-core==0.2.43
langchain-community==0.2.17
llama-index-core==0.10.68
qdrant-client==1.8.4
chromadb==0.5.23
onnxruntime==1.17.5
safetensors==0.4.5
transformers==4.44.3
```

```bash
# Generate lockfile with hashes
uv pip compile requirements.in --hash --universal -o requirements-lock.txt

# Install with hash verification
pip install --require-hashes -r requirements-lock.txt
```

### Dependency Update Policy
- **Security patches:** Apply within 48 hours
- **Minor versions:** Review and test bi-weekly
- **Major versions:** Quarterly review with full security audit
- **Never:** Auto-update AI/LLM dependencies in production

---

*This stack covers the rapidly evolving LLM application ecosystem. Security scores reflect current assessment and are reviewed bi-weekly. For the latest, see the project repository.*
