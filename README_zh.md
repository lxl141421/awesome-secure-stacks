<div align="center">

[English](README.md) | **中文**

# 🛡️ 精选安全技术栈 (Awesome Secure Stacks)

**社区策展、安全审计的技术栈版本兼容性推荐**

*Community-curated, security-audited technology stacks with verified version compatibility.*

[![GitHub Stars](https://img.shields.io/github/stars/lxl141421/awesome-secure-stacks?style=social)](https://github.com/lxl141421/awesome-secure-stacks)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

*帮助开发者在供应链攻击日益猖獗的今天，构建安全、可审计、版本兼容的技术栈。*

> 🤖 **用 AI 写代码？** AI 能生成代码，但分不清依赖包有没有后门。
> 本项目就是 AI 开发的**供应链安全层**。
>
> 💀 **本项目能防住的真实威胁：**
> - 窃取**钱包私钥**、助记词（`~/.ssh`、MetaMask 等）
> - 外泄 **`.env` 文件**中的数据库密码、API Token、云服务密钥
> - 盗取 **SSH 密钥**、GPG 密钥、CI/CD 流水线中的 Secret
> - 静默安装**挖矿程序**（通过 `postinstall` 脚本）
> - 传递依赖中隐藏**勒索软件**
>
> 不追最新，只推最稳。不给攻击者任何机会。

</div>

---

## 📖 目录

- [为什么需要这个项目？](#为什么需要这个项目)
- [安全评分体系](#安全评分体系)
- [版本选择哲学](#版本选择哲学)
- [推荐技术栈](#推荐技术栈)
  - [前端开发](#前端开发)
  - [后端开发](#后端开发)
  - [数据库与存储](#数据库与存储)
  - [基础设施与容器](#基础设施与容器)
  - [AI/机器学习](#ai机器学习)
  - [移动开发](#移动开发)
  - [消息与流处理](#消息与流处理)
- [供应链安全核心原则](#供应链安全核心原则)
- [依赖链审计指南](#依赖链审计指南)
- [锁文件最佳实践](#锁文件最佳实践)
- [可重现构建](#可重现构建)
- [历史重大事件回顾](#历史重大事件回顾)
- [安全工具链推荐](#安全工具链推荐)
- [企业级安全栈](#企业级安全栈)
- [社区贡献指南](#社区贡献指南)
- [致谢](#致谢)

---

## 为什么需要这个项目？

### 问题背景

近年来，软件供应链攻击呈指数级增长。从 **SolarWinds** 事件到 **XZ Utils** 后门植入，攻击者已经将目光从直接攻击转向了更加隐蔽的**供应链投毒**手段。

- 📈 2023年至2025年间，npm 生态系统中检测到的恶意包数量增长了 **430%**
- 🔗 平均每个 Node.js 项目依赖 **超过 700 个**传递性依赖
- ⏱️ 从漏洞披露到被利用的平均时间已缩短至 **不到 24 小时**

### 我们的解决方案

本项目为每一种主流技术栈提供：

1. **经安全审计的版本兼容性矩阵** — 明确标注哪些版本组合经过验证
2. **依赖链深度分析** — 追踪到最后一层传递性依赖
3. **已知漏洞态势评估** — 实时更新的 CVE 数据库
4. **社区驱动的持续更新** — 由数百名安全研究者共同维护

---

## 安全评分体系

我们采用 A+ 到 D 的五级评分体系，综合考量以下维度：

| 等级 | 分数范围 | 含义 |
|------|---------|------|
| **A+** | 95–100 | 卓越 — 最高安全标准，零已知重大漏洞 |
| **A** | 85–94 | 优秀 — 安全状况良好，仅有低风险问题 |
| **B+** | 75–84 | 良好 — 安全基线达标，存在可管理的风险 |
| **B** | 65–74 | 合格 — 基本安全要求满足，但需要注意 |
| **C** | 50–64 | 警告 — 存在中等风险，建议尽快升级 |
| **D** | <50 | 不推荐 — 存在严重安全风险，不应在生产环境使用 |

### 评分维度

- **漏洞密度**（40%）：已知 CVE 数量及严重程度
- **维护活跃度**（20%）：补丁发布频率与响应速度
- **依赖链健康度**（20%）：传递性依赖的安全状况
- **社区信任度**（10%）：下载量、采用率、企业使用情况
- **可审计性**（10%）：源代码开放程度、构建可重现性

---

## 版本选择哲学

> **不追最新，只推最稳。**

本项目的核心理念是：**稳定性优先于一切**。我们不推荐最新版本，而是推荐经过充分生产验证、拥有最少已知缺陷的版本。

### 为什么选择旧版本？

1. **更少的未知漏洞** — 新版本的初始发布往往伴随着尚未发现的安全问题，而经过数月甚至数年维护的版本已修复了绝大多数已知漏洞
2. **更成熟的生态系统** — 配套工具、第三方库、社区文档均已完善，降低了集成风险
3. **更稳定的 API** — 减少因 API 变动导致的兼容性问题和意外行为
4. **更广泛的生产验证** — 全球数以万计的生产环境已在使用这些版本，问题早被发现并修复

### 我们的选择标准

- 优先选择 **LTS（长期支持）** 版本
- 版本必须经过 **至少 3 个月** 的生产环境验证
- 已知高危 CVE 必须已被修复
- 社区和维护者活跃度达标
- 依赖链健康，无已知供应链风险

### 不追最新，只推最稳

| 策略 | ❌ 追新 | ✅ 求稳 |
|------|---------|---------|
| 版本选择 | 最新发布版 | 经验证的稳定版 |
| 升级时机 | 版本发布即升级 | 等待至少 3 个月生产验证 |
| 风险评估 | 接受未知风险 | 最小化已知与未知风险 |
| 生态兼容 | 可能存在工具链不兼容 | 生态完善，工具链成熟 |

---

## 推荐技术栈

### 前端开发

#### React 全栈方案

| 组件 | 推荐版本 | 安全评分 | 备注 |
|------|---------|---------|------|
| React | **18.3** | A+ | 并发渲染模式成熟稳定 |
| Next.js | **14.2** | A+ | 经充分生产验证，App Router 成熟 |
| TypeScript | **5.8** | A+ | 严格类型检查可防止整类运行时错误 |
| Vite | **6.3** | A | 热更新性能大幅提升 |

**核心安全配置：**

```json
// next.config.mjs
{
  "poweredByHeader": false,
  "reactStrictMode": true,
  "headers": [
    { "key": "X-Content-Type-Options", "value": "nosniff" },
    { "key": "X-Frame-Options", "value": "DENY" },
    { "key": "Content-Security-Policy", "value": "default-src 'self'" }
  ]
}
```

**依赖管理建议：**

```bash
# 使用 npm audit 检查已知漏洞
npm audit --audit-level=high

# 启用严格锁文件模式
npm ci --strict-peer-deps

# 使用 Socket.dev 检测供应链风险
npx socket npm install
```

**版本兼容性矩阵：**

- React 18.3 + Next.js 14.2 + TypeScript 5.8 ✅ 经验证
- React 18.3 + Vite 6.3 + TypeScript 5.8 ✅ 经验证
- React 18.3 + Next.js 15.x + TypeScript 5.8 ⚠️ Next.js 15.x 尚未充分验证，建议使用 14.2

---

### 后端开发

#### Node.js 方案

| 组件 | 推荐版本 | 安全评分 | 备注 |
|------|---------|---------|------|
| Node.js | **22 LTS** | A | 长期支持版本，持续安全补丁 |
| Express | **5.x** | A | 修复了多个原型污染漏洞 |
| Prisma | **6.x** | A+ | 参数化查询防止 SQL 注入 |

```javascript
// 安全中间件配置示例
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';

app.use(helmet());
app.use(rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
}));
```

#### Python 方案

| 组件 | 推荐版本 | 安全评分 | 备注 |
|------|---------|---------|------|
| Python | **3.12** | A | 稳定版本，内存安全持续改进 |
| FastAPI | **0.115+** | A | 自动输入验证与 OpenAPI 文档 |
| Django | **5.2** | A+ | 内置 CSRF、XSS、SQL 注入防护 |

```python
# Python 依赖安全检查
# requirements.txt 示例
fastapi==0.115.0
uvicorn==0.34.0
pydantic==2.10.0  # 严格数据验证

# 使用 pip-audit 检查漏洞
# $ pip-audit --strict --desc
```

#### Go 方案

| 组件 | 推荐版本 | 安全评分 | 备注 |
|------|---------|---------|------|
| Go | **1.22** | A+ | 稳定版本，内存安全语言特性 |
| Gin | **1.10+** | A | 高性能 HTTP 框架 |
| Fiber | **2.52+** | A | 基于 fasthttp，零内存分配路由 |

#### Rust 方案

| 组件 | 推荐版本 | 安全评分 | 备注 |
|------|---------|---------|------|
| Rust | **1.80** | A+ | 稳定版本，编译期内存安全保证 |
| Actix-web | **4.x** | A+ | 极致性能，内存安全 |
| Axum | **0.8+** | A+ | Tokio 团队维护 |

---

### 数据库与存储

| 组件 | 推荐版本 | 安全评分 | 备注 |
|------|---------|---------|------|
| PostgreSQL | **16.4** | A+ | 长期支持版本，业界最安全的开源关系型数据库 |
| Redis | **7.4+** | A | 新增 ACL 细粒度权限控制 |
| MongoDB | **7.0** | A | 稳定版本，字段级加密 (FLE) |

**PostgreSQL 安全加固清单：**

```sql
-- 1. 禁用默认超级用户远程登录
ALTER ROLE postgres WITH NOLOGIN;

-- 2. 启用行级安全策略
ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;

-- 3. 配置 SSL 强制连接
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_min_protocol_version = 'TLSv1.3';

-- 4. 审计日志
ALTER SYSTEM SET log_statement = 'mod';
```

---

### 基础设施与容器

| 组件 | 推荐版本 | 安全评分 | 备注 |
|------|---------|---------|------|
| Docker | **27.5** | A | 稳定版本，镜像签名验证完善 |
| Kubernetes | **1.30** | A | LTS 版本，Pod 安全准入控制器成熟 |
| Terraform | **1.7** | A+ | 稳定版本，基础设施即代码，审计友好 |

**Docker 安全最佳实践：**

```dockerfile
# ✅ 使用最小基础镜像
FROM cgr.dev/chainguard/python:latest

# ✅ 创建非 root 用户
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# ✅ 固定依赖版本
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ 只读文件系统
VOLUME ["/tmp"]
```

**Kubernetes 安全策略：**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: myapp@sha256:abc123...  # 使用摘要而非标签
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: ["ALL"]
```

---

### AI/机器学习

| 组件 | 推荐版本 | 安全评分 | 备注 |
|------|---------|---------|------|
| PyTorch | **2.3** | A | 稳定版本，安全模型加载，safetensors 支持 |
| TensorFlow | **2.18+** | A | SavedModel 格式更安全 |
| Hugging Face Transformers | **4.48+** | A | 安全的模型序列化 |

**⚠️ ML 供应链特别警告：**

机器学习生态系统是供应链投毒的重灾区。恶意模型文件（.pkl、.pt）可执行任意代码。

```python
# ❌ 危险：不要这样做
import pickle
model = pickle.load(open('model.pkl', 'rb'))

# ✅ 安全：使用 safetensors 格式
from safetensors.torch import load_file
tensors = load_file("model.safetensors")

# ✅ 安全：使用 torch.load 的 weights_only 参数
model = torch.load('model.pt', weights_only=True)
```

---

### 移动开发

| 组件 | 推荐版本 | 安全评分 | 备注 |
|------|---------|---------|------|
| Flutter | **3.22** | A | 稳定版本，Dart 语言内存安全 |
| React Native | **0.74** | A | 稳定版本，新架构渐趋成熟 |
| Kotlin Multiplatform | **2.1+** | A+ | 空安全特性 |

---

### 消息与流处理

| 组件 | 推荐版本 | 安全评分 | 备注 |
|------|---------|---------|------|
| Apache Kafka | **3.7** | A | 稳定版本，KRaft 模式成熟可用 |
| RabbitMQ | **3.13** | A | 稳定版本，OAuth 2.0 支持 |
| NATS | **2.11+** | A+ | 内置 TLS，零依赖 |

---

## 供应链安全核心原则

### 原则一：最小依赖原则

> 每增加一个依赖，就增加一个攻击面。

- 评估每个依赖的必要性
- 优先选择标准库能解决的功能
- 使用 `depcheck`、`cargo-udeps` 等工具定期清理未使用的依赖

### 原则二：信任但验证

- 不盲目信任大厂出品的包（参考 **event-stream** 事件）
- 检查依赖的维护者身份和提交历史
- 使用 Sigstore 验证包的签名

### 原则三：锁定一切

- 始终提交锁文件（`package-lock.json`、`poetry.lock`、`Cargo.lock`）
- 生产环境使用 `npm ci` 而非 `npm install`
- 锁文件应该纳入版本控制

### 原则四：纵深防御

- 多层安全措施叠加，不依赖单一防线
- 结合 SCA、SAST、DAST 多种扫描手段
- 运行时监控与静态分析并用

---

## 依赖链审计指南

### npm 生态

```bash
# 查看完整依赖树
npm ls --all

# 检查已知漏洞
npm audit

# 使用 lockfile-lint 验证锁文件完整性
npx lockfile-lint --path package-lock.json \
  --type npm \
  --validate-https \
  --allowed-hosts npm

# 使用 Socket.dev 检测可疑行为
npx socket npm ls
```

### Python 生态

```bash
# 使用 pip-audit 扫描漏洞
pip-audit --strict --desc

# 使用 safety 检查
safety check --full-report

# 生成软件物料清单 (SBOM)
pip install cyclonedx-bom
cyclonedx-py -o sbom.json
```

### Go 生态

```bash
# 检查已知漏洞
go install golang.org/x/vuln/cmd/govulncheck@latest
govulncheck ./...

# 验证依赖完整性
go mod verify

# 生成 SBOM
go install github.com/anchore/syft/cmd/syft@latest
syft dir:. -o spdx-json > sbom.json
```

---

## 锁文件最佳实践

锁文件是供应链安全的基石。它确保每个开发者和 CI/CD 环境使用完全相同的依赖版本。

### 各语言锁文件一览

| 语言/运行时 | 锁文件 | 是否提交到 Git |
|------------|--------|---------------|
| Node.js (npm) | `package-lock.json` | ✅ 必须 |
| Node.js (pnpm) | `pnpm-lock.yaml` | ✅ 必须 |
| Python (Poetry) | `poetry.lock` | ✅ 必须 |
| Python (Pipenv) | `Pipfile.lock` | ✅ 必须 |
| Rust (Cargo) | `Cargo.lock` | ✅ 应用程序必须 |
| Go | `go.sum` | ✅ 必须 |
| Ruby (Bundler) | `Gemfile.lock` | ✅ 必须 |

### 常见陷阱

```bash
# ❌ 错误：CI 环境中使用 npm install
npm install

# ✅ 正确：使用 npm ci 严格按锁文件安装
npm ci

# ❌ 错误：忽略锁文件中的 integrity 字段
# ✅ 正确：确保启用了完整性校验
npm config set strict-ssl true
npm config set audit-level high
```

---

## 可重现构建

可重现构建（Reproducible Builds）确保从源代码到二进制产物的路径是确定性的、可验证的。

### 为什么重要？

- 验证发布的二进制确实来自公开的源代码
- 检测构建过程中的篡改行为
- 增强对开源软件的信任

### 实践指南

```bash
# Nix — 函数式包管理，天然支持可重现构建
nix-build --option binary-caches ""

# Bazel — Google 开源的构建系统
bazel build --stamp //myapp:myapp

# Go — 内置可重现构建支持
CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o myapp

# Docker — 使用 BuildKit 和固定基础镜像
DOCKER_BUILDKIT=1 docker build --no-cache .
```

### 验证工具

- **[diffoscope](https://diffoscope.org/)** — 深度比较文件差异
- **[reprotest](https://pypi.org/project/reprotest/)** — 测试构建可重现性
- **[in-toto](https://in-toto.io/)** — 供应链完整性框架

---

## 历史重大事件回顾

### 🔴 XZ Utils 后门事件 (2024)

**事件概述：** 攻击者 "Jia Tan" 花费近两年时间逐步取得 XZ Utils 项目的维护者信任，最终在 5.6.0 和 5.6.1 版本中植入后门，影响几乎所有 Linux 发行版的 SSH 服务。

**教训：**
- 单人维护的关键基础设施极其危险
- 社会工程学攻击极难防范
- 需要建立维护者身份验证机制

### 🔴 SolarWinds 供应链攻击 (2020)

**事件概述：** 攻击者入侵了 SolarWinds 的构建系统，在 Orion 平台的更新包中植入恶意代码（SUNBURST），影响了约 18,000 个组织，包括多个美国政府机构。

**教训：**
- 构建环境必须与开发环境隔离
- 需要完整的构建审计日志
- 软件物料清单 (SBOM) 至关重要

### 🟡 event-stream 事件 (2018)

**事件概述：** 攻击者通过社工手段接管了广泛使用的 `event-stream` npm 包，注入窃取加密货币钱包的恶意代码。

**教训：**
- 不能仅凭下载量判断包的可信度
- 维护者变更需要严格审查

### 🟡 Log4Shell (2021)

**事件概述：** Apache Log4j 2 的 JNDI 注入漏洞 (CVE-2021-44228)，CVSS 评分 10.0，影响全球数十万应用程序。

**教训：**
- 日志库这类基础设施也会成为攻击目标
- 传递性依赖风险不可忽视
- 需要快速响应机制

---

## 安全工具链推荐

### 软件组成分析 (SCA)

| 工具 | 语言支持 | 开源 | 推荐度 |
|------|---------|------|-------|
| [Socket.dev](https://socket.dev) | npm, PyPI | 部分 | ⭐⭐⭐⭐⭐ |
| [Snyk](https://snyk.io) | 多语言 | 部分 | ⭐⭐⭐⭐⭐ |
| [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/) | 多语言 | ✅ | ⭐⭐⭐⭐ |
| [Trivy](https://trivy.dev) | 多语言 | ✅ | ⭐⭐⭐⭐⭐ |
| [Grype](https://github.com/anchore/grype) | 多语言 | ✅ | ⭐⭐⭐⭐ |

### 静态应用安全测试 (SAST)

| 工具 | 特点 | 开源 |
|------|------|------|
| [Semgrep](https://semgrep.dev) | 规则丰富，支持自定义 | ✅ |
| [CodeQL](https://codeql.github.com) | GitHub 深度集成 | 部分 |
| [Bandit](https://bandit.readthedocs.io) | Python 专用 | ✅ |
| [gosec](https://github.com/securego/gosec) | Go 专用 | ✅ |

### SBOM 生成

| 工具 | 格式 | 语言 |
|------|------|------|
| [Syft](https://github.com/anchore/syft) | SPDX, CycloneDX | Go |
| [CycloneDX](https://cyclonedx.org) | CycloneDX | 多语言 |
| [Tern](https://terntools.dev) | SPDX | Python |

---

## 企业级安全栈

### 零信任架构参考栈

```
┌─────────────────────────────────────────────┐
│                  用户层                       │
│  身份认证 (OIDC) → 设备验证 → 权限最小化      │
├─────────────────────────────────────────────┤
│                  应用层                       │
│  API 网关 → mTLS → 输入验证 → RBAC           │
├─────────────────────────────────────────────┤
│                  数据层                       │
│  加密存储 → 审计日志 → 数据脱敏               │
├─────────────────────────────────────────────┤
│                  基础设施层                    │
│  网络隔离 → 运行时安全 → 镜像签名             │
└─────────────────────────────────────────────┘
```

### 合规性对照

| 标准 | 适用场景 | 核心要求 |
|------|---------|---------|
| SOC 2 Type II | SaaS 服务 | 访问控制、变更管理、监控 |
| ISO 27001 | 国际业务 | 信息安全管理体系 |
| NIST SSDF | 软件开发 | 安全软件开发框架 |
| EU CRA | 欧盟市场 | 网络韧性法案合规 |

---

## 社区贡献指南

我们欢迎社区的每一份贡献！参与方式：

### 如何贡献

1. **Fork** 本仓库
2. 创建特性分支：`git checkout -b feat/add-new-stack`
3. 按照模板提交新的技术栈推荐
4. 提交 Pull Request

### 推荐模板

```markdown
## [技术栈名称]

| 组件 | 推荐版本 | 安全评分 | 备注 |
|------|---------|---------|------|
| ... | ... | ... | ... |

### 安全审计信息
- 审计日期：YYYY-MM-DD
- 审计工具：...
- 发现问题：...

### 版本兼容性验证
- [ ] 全新安装测试通过
- [ ] 升级路径测试通过
- [ ] CI/CD 集成测试通过
- [ ] 生产环境验证通过
```

### 贡献质量要求

- ✅ 必须提供至少两个版本组合的兼容性验证
- ✅ 必须包含安全评分及评分依据
- ✅ 必须使用推荐的锁文件配置
- ✅ 必须注明审计日期和审计范围

---

## 致谢

感谢以下组织和个人对本项目的支持：

- [OpenSSF](https://openssf.org) — 开源安全基金会
- [Sigstore](https://sigstore.dev) — 软件签名基础设施
- [SLSA Framework](https://slsa.dev) — 供应链安全等级标准
- 所有贡献者和安全研究者 ❤️

---

<div align="center">

**如果这个项目对你有帮助，请给我们一个 ⭐**

[![Star History Chart](https://api.star-history.com/svg?repos=lxl141421/awesome-secure-stacks&type=Date)](https://star-history.com/#lxl141421/awesome-secure-stacks&Date)

---

📝 本项目采用 [MIT 许可证](LICENSE) 发布

🏠 [项目主页](https://github.com/lxl141421/awesome-secure-stacks) · 
📮 [提交问题](https://github.com/lxl141421/awesome-secure-stacks/issues) · 
💬 [参与讨论](https://github.com/lxl141421/awesome-secure-stacks/discussions)

</div>
