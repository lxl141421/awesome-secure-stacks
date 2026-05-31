# ML & AI Stacks — Secure Stacks

> Last updated: 2026-05-31
> Review cadence: Bi-weekly (rapid ecosystem changes)
> ⚠️ ML/AI supply chain is a high-risk area — see supply chain section at bottom

---

## 1. Training Stack ⭐

**Security Grade: B+**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| PyTorch | 2.2.2 | BSD-3 | 0 critical |
| Python | 3.11.10 | PSF | 0 critical |
| CUDA | 12.4.1 | NVIDIA EULA | N/A |
| cuDNN | 8.9.7 | NVIDIA EULA | N/A |
| NumPy | 1.26.4 | BSD-3 | 0 |
| Pandas | 2.2.3 | BSD-3 | 0 |
| Transformers | 4.44.3 | Apache-2.0 | 0 |

**Lockfile (pip):**
```
# requirements-lock.txt (generate with pip-compile or uv)
torch==2.2.2+cu124
numpy==1.26.4
pandas==2.2.3
transformers==4.44.3
datasets==2.21.0
accelerate==0.34.2
safetensors==0.4.5
```

**Reproducible Build:**
```bash
pip install uv
uv pip compile requirements.in --hash --universal -o requirements-lock.txt
pip install --require-hashes -r requirements-lock.txt
```

**Security Notes:**
- Use `safetensors` format exclusively (not pickle/pth — arbitrary code execution risk)
- Validate dataset integrity with checksums before training
- Run training in isolated containers (no network access)

---

## 2. Model Serving

**Security Grade: B**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| vLLM | 0.4.3 | Apache-2.0 | 0 |
| TGI (Text Generation Inference) | 2.2.0 | Apache-2.0 (HF) | 0 |
| Triton Inference Server | 24.08 | BSD-3 | 0 |
| ONNX Runtime | 1.19.2 | MIT | 0 |

**vLLM Deployment:**
```bash
pip install vllm==0.4.3
vllm serve meta-llama/Llama-3-8B-Instruct \
  --dtype auto \
  --api-key sk-secret-here \
  --disable-log-requests \
  --max-model-len 8192
```

**Triton Deployment:**
```bash
docker run --gpus all -p 8000:8000 -p 8001:8001 -p 8002:8002 \
  nvcr.io/nvidia/tritonserver:24.08-py3 \
  tritonserver --model-repository=/models
```

**Security Best Practices:**
- API key authentication on all inference endpoints
- Rate limiting per client
- Input sanitization (prompt injection defense)
- Model integrity verification (SHA-256 of model weights)
- Network isolation (inference should not have outbound internet access)

---

## 3. MLOps & Experiment Tracking

**Security Grade: B+**

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| MLflow | 2.11.3 | Apache-2.0 | 0 critical |
| Weights & Biases (wandb) | 0.18.5 | MIT | 0 |
| DVC | 3.55.2 | Apache-2.0 | 0 |
| Ray | 2.10.0 | Apache-2.0 | 0 |

**MLflow Security Configuration:**
```bash
# Secure MLflow tracking server
mlflow server \
  --backend-store-uri postgresql://user:pass@db:5432/mlflow \
  --default-artifact-root s3://mlflow-artifacts/ \
  --host 0.0.0.0 \
  --port 5000 \
  --gunicorn-opts "--timeout 120"
```

**Security Checklist for MLflow:**
- [ ] Enable authentication (proxy via OAuth2/OIDC)
- [ ] Use S3 with SSE-KMS for artifact encryption
- [ ] Restrict artifact download to authorized users
- [ ] Enable HTTPS (reverse proxy with TLS)
- [ ] Sanitize logged parameters (prevent SSRF via artifact URIs)

**W&B Security:**
- Self-hosted option available for air-gapped environments
- SOC 2 Type II certified (cloud)
- RBAC for team-based access control

---

## 4. LLM Frameworks

**Security Grade: B-** (rapidly evolving, higher risk)

| Component | Pinned Version | License | CVEs |
|-----------|---------------|---------|------|
| LangChain | 0.1.20 | MIT | 0 |
| LlamaIndex | 0.10.68 | MIT | 0 |
| OpenAI SDK | 1.51.0 | Apache-2.0 | 0 |
| Ollama | 0.3.14 | MIT | 0 |
| LiteLLM | 1.50.4 | MIT | 0 |

**LangChain Security Notes:**
- ⚠️ LangChain had known code execution vulnerabilities in `PALChain` and `LLMMathChain` (deprecated in 0.1.x)
- Avoid `allow_dangerous_code_execution=True` in any chain
- Use LCEL (LangChain Expression Language) instead of legacy chains

```python
# Safer pattern with LangChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Pinned versions
# langchain==0.1.20, langchain-openai==0.1.25, openai==1.51.0
llm = ChatOpenAI(model="gpt-4o", temperature=0)
# Never enable: llm_math PALChain, shell tools, arbitrary Python execution
```

**LlamaIndex Security Notes:**
- `load_data` from URLs can be an SSRF vector — validate sources
- Use `SubQuestionQueryEngine` with caution (generates sub-queries)
- Pin all LlamaIndex integration packages separately

---

## 5. ⚠️ ML Supply Chain Risks

### Critical Threats

**Model Poisoning:**
- Downloaded models (HuggingFace, Torch Hub) may contain backdoors
- **Mitigation:** Verify model SHA-256 checksums against official sources
- **Mitigation:** Use `safetensors` format exclusively (no arbitrary code execution)
- **Mitigation:** Scan models with `picklescan` before loading

**Malicious Packages:**
- Typosquatting on `torch`, `transformers`, `tensorflow` ecosystem
- Example: `torch-vision` (malicious) vs `torchvision` (legitimate)
- **Mitigation:** Use `pip-audit` and `safety check` in CI
- **Mitigation:** Pin all dependencies with hashes

**Data Poisoning:**
- Public datasets may contain adversarial examples
- **Mitigation:** Validate dataset checksums
- **Mitigation:** Use `datasets` library with integrity verification

### Recommended Security Tools

```bash
# Scan for malicious pickle files
pip install picklescan
picklescan-scan /path/to/models/

# Audit Python dependencies
pip install pip-audit
pip-audit --strict --desc

# Check for known vulnerabilities
pip install safety
safety check --full-report

# Verify model format
python -c "from safetensors import safe_open; safe_open('model.safetensors', framework='pt')"
```

### Supply Chain Checklist

- [ ] Never load `.pkl` or `.pth` files from untrusted sources
- [ ] Prefer `safetensors` format for all model weights
- [ ] Pin all Python dependencies with hashes
- [ ] Run `pip-audit` in CI pipeline
- [ ] Verify model checksums against official release page
- [ ] Isolate training environments (no internet access)
- [ ] Use private package registries (Artifactory, AWS CodeArtifact)
- [ ] Scan Docker images for ML-specific vulnerabilities
- [ ] Monitor for typosquatting on PyPI (use `supply-chain` monitoring)
- [ ] Enable 2FA on all PyPI accounts publishing ML packages

---

## Security Comparison Matrix

| Feature | PyTorch | vLLM | MLflow | LangChain | LlamaIndex |
|---------|---------|------|--------|-----------|------------|
| Maturity | High | Moderate | High | Moderate | Moderate |
| Safe Formats | safetensors | safetensors | N/A | N/A | N/A |
| Auth Built-in | N/A | API key | Proxy | N/A | N/A |
| Audit History | ✅ | ⚠️ | ✅ | ⚠️ | ⚠️ |
| **Grade** | **B+** | **B** | **B+** | **B-** | **B-** |
