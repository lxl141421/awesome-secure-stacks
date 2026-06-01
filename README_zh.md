<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/English-blue?style=flat-square" alt="English"></a>
  <a href="README_zh.md"><img src="https://img.shields.io/badge/中文-grey?style=flat-square" alt="中文"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/🛡️-Awesome_Secure_Stacks-blue?style=for-the-badge&logo=shield&logoColor=white" alt="Awesome Secure Stacks" width="400">
</p>

<h1 align="center">🛡️ 精选安全技术栈 (Awesome Secure Stacks)</h1>

<p align="center">
  <b>社区策展、安全审计的技术栈，版本兼容性经过验证。</b><br>
  <i>构建安全、生产就绪软件栈的权威参考。</i><br>
  <sub>Community-curated, security-audited technology stacks with verified version compatibility.</sub>
</p>

<p align="center">
  <a href="https://github.com/lxl141421/awesome-secure-stacks/stargazers"><img src="https://img.shields.io/github/stars/lxl141421/awesome-secure-stacks?style=social" alt="Stars"></a>
  &nbsp;
  <a href="https://github.com/lxl141421/awesome-secure-stacks/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square" alt="PRs Welcome"></a>
  &nbsp;
  <img src="https://img.shields.io/badge/last%20updated-2026--06-blue?style=flat-square" alt="Last Updated">
  &nbsp;
  <img src="https://img.shields.io/badge/security--audited-✓-brightgreen?style=flat-square&logo=checkmarx&logoColor=white" alt="Security Audited">
  &nbsp;
  <a href="https://github.com/lxl141421/awesome-secure-stacks/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT License"></a>
  &nbsp;
  <img src="https://img.shields.io/badge/stacks-60+-purple?style=flat-square" alt="60+ Stacks">
</p>

---

> **别再猜哪些依赖是安全的。每个技术栈 — 经过审核、评分和生产验证。**
> 我们不追最新版本。我们推荐每个组件**最安全、最稳定、Bug 最少**的版本。
>
> 🤖 **用 AI 写代码？** AI 能生成代码 — 但分不清依赖包有没有后门。
> 这个项目就是 AI 开发的**供应链安全层**。
>
> 💀 **本项目能防住的真实威胁：**
> - 窃取**钱包私钥**、助记词（`~/.ssh`、MetaMask 等）
> - 外泄 **`.env` 文件**中的数据库密码、API Token、云服务密钥
> - 盗取 **SSH 密钥**、GPG 密钥、CI/CD 流水线中的 Secret
> - 静默安装**挖矿程序**（通过 `postinstall` 脚本）
> - 传递依赖中隐藏**勒索软件**
>
> 不追最新，只推最稳。不给攻击者任何机会。

---

## 📖 目录

- [🚀 快速推荐](#-快速推荐)
- [👤 你是谁？](#-你是谁)
- [🚨 问题背景](#-问题背景)
- [💡 我们的解决方案](#-我们的解决方案)
- [📊 安全评分体系](#-安全评分体系)
- [🎯 版本选择哲学](#-版本选择哲学)
- [⭐ 推荐技术栈](#-推荐技术栈)
- [📚 技术栈分类](#-技术栈分类)
- [🕘 供应链攻击时间线](#-供应链攻击时间线)
- [🔒 安全公告](#-安全公告)
- [🤝 社区贡献指南](#-社区贡献指南)
- [🗺️ 路线图](#️-路线图)
- [📜 许可证](#-许可证)
- [🙏 致谢](#-致谢)

---

## 🚀 快速推荐

**不知道从哪里开始？选择你的情况：**

---

> ### 🛡️ "我要最安全的方案"
>
> **Go 1.22 + Chi 5.2 + PostgreSQL 16.4**
>
> 📊 **评分: 96/100 (A+)** — 安全后端开发的黄金标准。
>
> - ✅ Go 的静态编译消除了运行时依赖攻击
> - ✅ Chi **零外部依赖** — 最小攻击面
> - ✅ PostgreSQL 16.4 拥有 30+ 年的安全加固经验
> - ✅ Go 模块默认通过 sum.golang.org 提供加密验证
>
> 👉 **开始使用：** [`stacks/backend.md`](stacks/backend.md) + [`stacks/database.md`](stacks/database.md)

---

> ### ⚡ "我要快速出活"
>
> **React 18.3 + Next.js 14.2.21 + T3 Stack**
>
> 📊 **评分: 95/100 (A+)** — 最久经考验的前端全栈方案。
>
> - ✅ React 18.3 已部署在**数百万**生产应用中
> - ✅ TypeScript 5.6 三年来**零 Critical CVE**
> - ✅ pnpm 严格依赖解析消除幽灵依赖
> - ✅ T3 Stack 提供从数据库到前端的完整类型安全
>
> 👉 **开始使用：** [`stacks/fullstack.md`](stacks/fullstack.md) + [`stacks/frontend.md`](stacks/frontend.md)

---

> ### 🤖 "我在用 AI 写代码"
>
> **AI 能生成代码 — 但分不清依赖包有没有后门。**
>
> 📊 你需要本项目提供的 **AI 安全层**。
>
> - ⚠️ AI 助手可能推荐**幻觉包名** — 攻击者会注册这些包
> - ⚠️ AI 生成的代码经常引入**过时或不安全**的依赖版本
> - ⚠️ 云端 AI 推理可能**泄露你的代码上下文**给第三方
>
> 👉 **先看这里：** [`stacks/ai-development.md`](stacks/ai-development.md) + [`stacks/ai-apps.md`](stacks/ai-apps.md)

---

## 👤 你是谁？

**找到你的入口。** 不同角色，不同需求。

---

| 🎯 你的角色 | 👉 从这里开始 | 📋 你会找到什么 |
|--------------|---------------|---------------------|
| 🧑‍💻 **独立开发者** | [`stacks/fullstack.md`](stacks/fullstack.md) | T3 Stack、Django、Rails — 完整应用蓝图与安全评分 |
| 🤖 **AI 辅助开发** | [`stacks/ai-development.md`](stacks/ai-development.md) | 验证 AI 生成的依赖、避免幻觉包、安全使用 Copilot/Cursor |
| 🌐 **Web 团队** | [`stacks/frontend.md`](stacks/frontend.md) + [`stacks/backend.md`](stacks/backend.md) | React、Vue、Svelte、Angular + Node.js、Go、Rust、Python、Java、.NET |
| 📱 **移动端团队** | [`stacks/mobile.md`](stacks/mobile.md) + [`stacks/mobile-native.md`](stacks/mobile-native.md) | React Native、Flutter、uni-app + Kotlin、Swift、鸿蒙原生深度解析 |
| 🏢 **企业/技术升级** | [`stacks/evolution.md`](stacks/evolution.md) | 框架代际迁移路径，每个阶段保持安全性 |
| 🔄 **单体→微服务** | [`stacks/distributed.md`](stacks/distributed.md) + [`stacks/evolution.md`](stacks/evolution.md) | 服务网格、API 网关、Saga 编排 — 每个迁移阶段的安全保障 |

---

**不确定？** 从上面的[快速推荐](#-快速推荐)开始，或浏览下方的[技术栈分类](#-技术栈分类)。

---

## 🚨 问题背景

> **软件供应链攻击从 2019 到 2022 年增长了 742%。** 它们没有放缓的迹象。
> — _Sonatype 软件供应链状况报告_

现代软件生态建立在**信任**之上 — 信任你从未审计过的包，由你从未见过的人维护，引入你从未选择的数百个传递依赖。**这种信任正在被利用。**

每一次 `npm install`、`pip install`、`go mod download` 都是一次信仰之跃。攻击者正将这种信仰变成武器 — 以越来越复杂的方式瞄准依赖链中最薄弱的环节。

### 重大供应链事件

| 年份 | 事件 | 影响 | 严重性 |
|------|----------|--------|----------|
| 🔴 2024 | **XZ Utils 后门** (`xz` 5.6.x) | 通过多年社会工程几乎攻陷所有主流 Linux 发行版 | 🔴 严重 |
| 🔴 2018 | **`event-stream` / `flatmap-stream`** | 通过入侵流行 npm 包的依赖窃取加密货币 | 🔴 严重 |
| 🔴 2021 | **`ua-parser-js`**（每周 7000 万+ 下载） | 劫持版本注入挖矿程序和密码窃取器 | 🔴 严重 |
| 🔴 2020 | **SolarWinds Orion** | 国家级攻击，影响 18,000+ 组织包括美国政府机构 | 🔴 严重 |
| 🟡 2022 | **`colors.js` / `faker.js` 抗议** | 维护者蓄意破坏导致数千 CI/CD 流水线中断 | 🟡 高危 |
| 🔴 2022 | **`node-ipc`**（抗议软件） | 故意擦除针对俄罗斯和白俄罗斯 IP 地址的数据 | 🔴 严重 |
| 🟡 2021 | **Codecov Bash Uploader** | 被入侵的 CI 工具泄露环境变量（密钥） | 🟡 高危 |
| 🟡 2023 | **PyTorch `torchtriton`** | PyPI 上同名恶意包冒充 nightly 依赖 | 🟡 高危 |

**模式很明确：** 我们的依赖链就是攻击面，而大多数团队没有系统的方法来评估哪些工具组合是安全的。

---

## 💡 我们的解决方案

**Awesome Secure Stacks** 是一个**社区策展、严格评估的完整技术栈集合** — 不是单个包，而是**经过测试的工具、框架、库和基础设施组合**，确保它们能安全地协同工作。

我们替你完成审计整个依赖图的繁重工作。

### 每个技术栈提供什么

对于本仓库中的每个技术栈条目，你将获得：

- ✅ **锁定的、经验证的版本** — **最安全、最稳定**的版本，不一定是最新的
- ✅ **安全评分 (0–100)** — 从 5 个维度计算（参见 [SCORING.md](SCORING.md)）
- ✅ **CVE 分析** — 已知漏洞、传递依赖风险、补丁速度
- ✅ **锁文件模板** — 可重现的依赖文件，冻结你的供应链
- ✅ **Docker 配置** — 加固的容器镜像，锁定基础层
- ✅ **替代方案与权衡** — 当技术栈存在安全顾虑时，我们推荐更安全的选择
- ✅ **兼容性矩阵** — 每个组件的哪些版本可以协同工作
- ✅ **月度重新评估** — 评分定期更新

> **把它想象成"推荐的硬件兼容性列表" — 但用于软件安全。**

---

## 📊 安全评分体系

每个技术栈按五个维度评分 **0–100**：

| 维度 | 权重 | 衡量内容 |
|-----------|--------|------------------|
| 🛡️ **漏洞态势** | 30 分 | 已知 CVE、补丁速度、审计历史 |
| 🔗 **供应链完整性** | 25 分 | 签名、溯源、SBOM、仿冒包防护 |
| 🔧 **维护健康度** | 20 分 | 发布节奏、LTS 政策、Issue 分拣 |
| 👥 **社区信任度** | 15 分 | 治理、审计、采用规模 |
| 📦 **可重现性** | 10 分 | 锁文件、确定性构建、校验和 |

### 等级标准

| 等级 | 分数 | 含义 |
|-------|-------|---------|
| 🟢 **A+** | 95–100 | 卓越 — 金标准，示范性安全实践 |
| 🟢 **A** | 85–94 | 优秀 — 强烈推荐用于生产 |
| 🔵 **B+** | 75–84 | 良好 — 可靠选择，有小幅改进空间 |
| 🔵 **B** | 65–74 | 合格 — 入选本列表的最低门槛 |
| 🟡 **C** | 50–64 | 警告 — 未收录（存在显著安全顾虑） |
| 🔴 **D** | 0–49 | 不推荐 — 存在严重安全缺口 |

> 📋 **完整方法论：** 参见 [SCORING.md](SCORING.md)

**收录最低要求：**

- 总分 ≥ **65 (B 级)**
- 任何维度不低于其满分的 **40%**
- 零未修复的 Critical CVE
- 至少有一次独立安全审计记录

---

## 🎯 版本选择哲学：稳定性优先于新奇

> **"最新"不等于"最安全"。上周发布的版本没有任何生产记录。**

我们的版本选择遵循严格的**稳定性优先**原则：

### 选择规则

| 规则 | 理由 |
|------|-----------|
| 🏆 **优先 LTS 而非 Current** | LTS 版本获得多年安全修复回移 |
| ⏳ **优先 .2+ 而非 .0** | 第一个补丁版本证明主版本稳定 |
| 🔍 **6+ 个月生产记录** | 足够的时间让社区发现真实问题 |
| 🚫 **避免已知回退** | 我们跟踪 Issue 追踪器 — 有确认回退的版本会被标记 |
| 🛡️ **优先有安全审计的版本** | 经独立审计的版本评分更高 |
| 📦 **最小化传递依赖** | 更少依赖 = 更小攻击面 |

### 实际含义

| ❌ 我们不会做 | ✅ 我们会做 |
|---------------------|---------------|
| 推荐 Node.js 24（几周前发布） | 推荐 **Node.js 22 LTS**（久经考验，2 年支持） |
| 推荐 React 19（新主版本，破坏性变更） | 推荐 **React 18.3**（数百万应用验证） |
| 推荐 PostgreSQL 17（新主版本） | 推荐 **PostgreSQL 16.x**（多年生产加固） |
| 推荐 Svelte 5（完全重写） | 推荐 **Svelte 4.x**（稳定，充分理解） |
| 推荐 Redis 8.0（许可证争议） | 推荐 **Redis 7.4**（OSS 许可，经验证） |
| 推荐 Angular 19（刚发布） | 推荐 **Angular 18 LTS**（官方长期支持） |

> **我们的座右铭：宁可无聊但安全，也不要炫酷但有漏洞。**

---

## ⭐ 推荐技术栈

精选技术栈 — 每个类别中最佳的代表。

---

### 🥇 全栈 Web：React 18.3 + Next.js 14.2.21 + TypeScript 5.6

> **评分: 95/100 (A+)** · 分类：[Web 前端](stacks/frontend.md) | [全栈组合](stacks/fullstack.md)

最久经考验的前端技术栈。React 18.3 已部署在数百万生产应用中。Next.js 14.2.21 经过大量安全补丁（包括 CVE-2024-56332 DoS 修复），是推荐的生产版本。TypeScript 5.6 零 Critical CVE，多年稳定验证。

**组件与版本：**

| 组件 | 版本 | 评分 | 备注 |
|-----------|---------|------------------|-------|
| React | 18.3 | A+ | Meta 支持，签名发布，SBOM，数百万生产应用 |
| Next.js | 14.2 | A | Vercel 维护，14.x 是经验证的生产版本 |
| TypeScript | 5.6 | A+ | 3+ 年零 Critical CVE |
| Vite | 5.6 | A | 稳定 5.x 线，广泛生产使用 |
| Node.js | 22 LTS | A+ | 长期支持至 2027，定期安全补丁 |
| pnpm | 9.12 | A | 内容寻址存储，严格解析 |

---

### 🥇 后端 API：Go 1.22 + Chi 5.2 + PostgreSQL 16.4

> **评分: 96/100 (A+)** · 分类：[后端 API](stacks/backend.md) | [数据库](stacks/database.md)

安全后端开发的黄金标准。Go 的静态编译消除了运行时依赖攻击，Chi 是零依赖的极简路由器，PostgreSQL 16.4 拥有多年生产加固经验。

**组件与版本：**

| 组件 | 版本 | 评分 | 备注 |
|-----------|---------|------------------|-------|
| Go | 1.22 | A+ | Google 支持，默认校验和数据库，经验证稳定 |
| Chi | 5.2 | A+ | 零外部依赖，最小攻击面 |
| PostgreSQL | 16.4 | A+ | 30+ 年安全加固，16.x 是经验证的生产版本 |
| sqlc | 1.28 | A | 编译期 SQL 代码生成，消除注入 |

---

### 🥇 系统后端：Rust 1.80 + Axum 0.7

> **评分: 95/100 (A+)** · 分类：[后端 API](stacks/backend.md)

默认内存安全。Rust 在编译期消除了整类漏洞（缓冲区溢出、释放后使用、数据竞争）。Axum 0.7 基于 Tokio 和 Hyper — 处理数百万生产请求的久经考验的基础。

**组件与版本：**

| 组件 | 版本 | 评分 | 备注 |
|-----------|---------|------------------|-------|
| Rust | 1.80 | A+ | 无 GC 内存安全，消除约 70% CVE 类别 |
| Axum | 0.7 | A | Tokio 支持，Tower 中间件生态 |
| Actix-web | 4.8 | A | 替代框架，同等安全水平 |
| Cargo | （内置） | A | 内置审计，安全公告数据库集成 |

---

### 🥇 DevOps 与基础设施：Terraform 1.7 + Kubernetes 1.30.7

> **评分: 91/100 (A)** · 分类：[DevOps 与基础设施](stacks/devops.md)

基础设施即代码与容器编排。每个基础设施变更都经过版本控制、审查和审计。Docker 25.0 提供加固的容器运行时，Kubernetes 1.30.7 增强了 Pod 安全标准（包含 CVE-2024-10220 gitRepo 卷命令执行修复）。

**组件与版本：**

| 组件 | 版本 | 评分 | 备注 |
|-----------|---------|------------------|-------|
| Terraform | 1.7 | A | HashiCorp 签名的 Provider，状态加密 |
| Kubernetes | 1.30 | A | 增强 Pod 安全，签名发布 |
| Docker | 25.0 | A | 内容信任，默认镜像签名 |
| ArgoCD | 2.12 | A | GitOps，声明式可审计部署 |

---

## 📚 技术栈分类

### A 组：按框架生态

按日常使用的技术分类。

---

#### 🖥️ Web 前端

**文件：** [`stacks/frontend.md`](stacks/frontend.md)

框架、打包工具、CSS 方案和客户端安全工具。涵盖 React、Vue、Svelte、Angular 及新兴框架及其推荐配套工具。每个条目包含 CSP 配置、依赖审计结果和 XSS 缓解策略。

> **精选：** React 18.3 + Next.js 14.2.21、Vue 3.5 + Nuxt 3、SvelteKit 2、Angular 18 LTS

---

#### ⚙️ 后端 API

**文件：** [`stacks/backend.md`](stacks/backend.md)

服务端运行时、Web 框架、ORM、认证库和 API 安全工具。涵盖 Node.js、Go、Rust、Python、Java 和 .NET 生态，详细分析中间件安全、输入验证和认证模式。

> **精选：** Go 1.22 + Chi 5.2 + sqlc、Rust 1.80 + Axum 0.7、Node.js 22.22 + Fastify 5、Python 3.12 + FastAPI 0.115、Java 21 + Spring Boot 3.4、.NET 8 + ASP.NET Core 8.0

---

#### 🏗️ 全栈组合

**文件：** [`stacks/fullstack.md`](stacks/fullstack.md)

经验证的端到端组合，涵盖前端、后端、数据库和部署。完整的应用蓝图，包含从浏览器到数据库的全依赖图安全评分。

> **精选：** T3 Stack (Next.js + tRPC + Prisma)、Rails 8 全栈、Django 5.2 + htmx + Alpine.js、Laravel 11

---

### B 组：按领域

按应用类型分类。

---

#### 📱 移动端

**文件：** [`stacks/mobile.md`](stacks/mobile.md)

跨平台和原生移动开发框架、状态管理、导航和移动端专用安全工具。包含应用签名、依赖管理和运行时完整性验证分析。

> **精选：** React Native 0.76 + Expo、Flutter 3.24、uni-app、Kotlin Multiplatform

---

#### 🖥️ 桌面端

**文件：** [`stacks/desktop.md`](stacks/desktop.md)

安全优先的桌面应用框架沙箱。涵盖 Tauri 基于 Rust 的进程隔离、Electron 的 CSP 加固、Qt 原生模块和 .NET MAUI 跨平台部署。评估自动更新安全、原生模块审计流水线和 IPC 边界保护。

> **精选：** Tauri 2.x (Rust 沙箱)、Electron 33 + 安全默认配置、Qt 6.8、.NET MAUI 9.0

---

#### 🎮 游戏

**文件：** [`stacks/gaming.md`](stacks/gaming.md)

游戏引擎和多人游戏基础设施，重点关注供应链安全。涵盖 Unity、Godot、Unreal Engine 和 Bevy (Rust)。评估资产流水线安全、多人网络协议、Mod/UGC 沙箱和反作弊集成。

> **精选：** Unity 2022 LTS、Godot 4.2、Unreal Engine 5.4、Bevy 0.14

---

#### 🤖 AI 开发

**文件：** [`stacks/ai-development.md`](stacks/ai-development.md)

AI 编程助手及其独特的供应链风险。涵盖 GitHub Copilot、Cursor、Aider 及相关工具。AI 生成的代码引入新型攻击向量：幻觉包名、训练数据中的不安全模式、云端推理的上下文泄露。

> **精选：** GitHub Copilot Enterprise、Cursor + 本地模型、Aider + 离线 LLM

---

#### 🧠 AI/LLM 应用

**文件：** [`stacks/ai-apps.md`](stacks/ai-apps.md)

LLM 编排框架、向量数据库和 AI Agent 基础设施。涵盖 LangChain、vLLM、LlamaIndex 和 Agent 框架。重点关注提示注入防御、模型供应链验证、RAG 流水线安全和推理端点加固。

> **精选：** LangChain 0.3 + guardrails、vLLM + 模型溯源、向量数据库安全 (Qdrant, Weaviate)

---

### C 组：基础设施与架构

按基础设施和架构分类。

---

#### 🗄️ 数据库

**文件：** [`stacks/database.md`](stacks/database.md)

关系型、文档型、键值和时序数据库及其客户端库、迁移工具和连接池方案。包含认证机制、静态加密和网络安全配置分析。

> **精选：** PostgreSQL 16.4、MySQL 8.0 LTS、MongoDB 7.0、Redis 7.4

---

#### 🔧 DevOps

**文件：** [`stacks/devops.md`](stacks/devops.md)

基础设施即代码、CI/CD、容器编排、密钥管理、可观测性和云服务商工具。评估整个部署流水线的供应链完整性。

> **精选：** Terraform 1.7 + ArgoCD、Kubernetes 1.30.7 + Docker 25.0、GitHub Actions、Dagger

---

#### ⚡ 实时通信

**文件：** [`stacks/realtime.md`](stacks/realtime.md)

WebSocket、SSE、发布/订阅、消息队列和实时协作工具，关注持久连接的安全考量。评估认证、消息完整性和拒绝服务韧性。

> **精选：** Kafka 3.7、RabbitMQ 3.13.8、NATS 2.10、Socket.IO 4.x、Redis Streams

---

#### 🔗 分布式

**文件：** [`stacks/distributed.md`](stacks/distributed.md)

服务网格、API 网关、分布式追踪和微服务通信模式。涵盖 Istio、Linkerd、Kong 和 Saga 编排。评估零信任网络（全链路 mTLS）、熔断器和服务间认证。

> **精选：** Istio 1.22 + Envoy、Kong Gateway 3.x、Saga 编排模式

---

#### 🔄 架构演进

**文件：** [`stacks/evolution.md`](stacks/evolution.md)

从单体到分布式架构的迁移路径，每个阶段保持安全性。涵盖模块化单体、服务提取模式、绞杀者无花果和事件驱动分解。评估每个转换点的安全回退风险。

> **精选：** 单体 → 模块化单体、绞杀者无花果提取、事件驱动分解

---

## 🕘 供应链攻击时间线

按时间顺序回顾重大供应链攻击事件，这些事件正是本项目存在的原因。了解过去，才能守护未来。

```
2017 ───────────────────────────────────────────────────────────────────────── 2025
│                                                                               │
│  2017-11  ┌─ event-stream / flatmap-stream                                   │
│           │  通过受信 npm 依赖窃取加密货币钱包                                  │
│           │  影响: 数百万用户 | 攻击向量: npm 依赖劫持                           │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2020-03  ┌─ eslint-scope                                                    │
│           │  被盗 npm 凭据导致环境变量泄露                                      │
│           │  影响: CI/CD 流水线 | 攻击向量: 凭据盗窃                            │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2020-12  ┌─ SolarWinds Orion (SUNBURST)                                     │
│           │  国家级攻击，18,000+ 组织受影响                                     │
│           │  影响: 美国政府机构、财富 500 强 | 攻击向量: 构建系统                 │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2021-01  ┌─ ua-parser-js (每周 7000 万+ 下载)                               │
│           │  劫持版本注入挖矿程序和密码窃取器                                   │
│           │  影响: 数百万安装 | 攻击向量: 维护者账户被盗                         │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2021-04  ┌─ Codecov Bash Uploader                                           │
│           │  被篡改的 CI 工具泄露环境变量（密钥）                               │
│           │  影响: 29,000+ 项目 | 攻击向量: CI 工具篡改                         │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2022-01  ┌─ colors.js / faker.js (抗议软件)                                  │
│           │  故意死循环导致数千 CI 流水线中断                                   │
│           │  影响: 全行业 | 攻击向量: 维护者蓄意破坏                             │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2022-03  ┌─ node-ipc (抗议软件)                                              │
│           │  按 IP 地理位置定向擦除数据                                         │
│           │  影响: vue-cli 用户 | 攻击向量: 意识形态破坏                         │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2022-12  ┌─ PyTorch torchtriton (依赖混淆)                                   │
│           │  PyPI 上同名恶意包冒充 nightly 依赖                                │
│           │  影响: ML 研究者 | 攻击向量: 依赖混淆                               │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2023-03  ┌─ 3CX 桌面应用                                                     │
│           │  首个公开记录的级联供应链攻击                                       │
│           │  影响: 600,000+ 企业 | 攻击向量: 级联入侵                           │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2024-03  ┌─ XZ Utils (CVE-2024-3094)                                        │
│           │  多年社会工程 → sshd 后门                                          │
│           │  影响: 几乎所有 Linux 发行版 | 攻击向量: 维护者渗透                  │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2025-01  ┌─ tj-actions/changed-files (GitHub Actions)                       │
│           │  被入侵的 CI Action 泄露数千仓库的密钥                              │
│           │  影响: 23,000+ 仓库 | 攻击向量: GitHub Actions 入侵                 │
│           └──────────────────────────────────────────────────────             │
│                                                                               │
│  2025-??  下一个攻击正在策划中。                                                │
│           这个项目正是为了应对下一个攻击而存在。                                  │
│           保持警惕。使用经验证的技术栈。🔒                                      │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔒 安全公告

### 报告技术栈漏洞

如果你在推荐的技术栈中发现安全问题：

1. **不要**为敏感漏洞创建公开 GitHub Issue
2. 📧 邮箱：**security@awesome-secure-stacks.dev**
3. ⏱️ 我们承诺 **48 小时**内响应，**7 天**内发布公告

### 公告格式

每份公告遵循 [OpenSSF OpenVEX](https://openvex.dev/) 格式：

```
公告: ASSA-2025-001
严重性: 高 (CVSS 8.1)
受影响技术栈: backend-go-chi, fullstack-t3
组件: golang.org/x/crypto v0.21.0
修复版本: v0.22.0
状态: 已解决
发布日期: 2025-05-15
```

### 订阅公告

- 🔔 **GitHub Watch** → 选择本仓库的 "Releases only"
- 📡 **Atom 订阅：** [`/releases.atom`](https://github.com/lxl141421/awesome-secure-stacks/releases.atom)
- 📢 关注 [Releases](https://github.com/lxl141421/awesome-secure-stacks/releases) 页面获取安全公告

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

## 🤝 社区贡献指南

我们欢迎贡献！但安全策展需要严谨。质量优先于数量。

### 如何贡献

| 类型 | 方式 | 难度 |
|------|-----|------|
| 🐛 报告评分错误 | [创建 Issue](https://github.com/lxl141421/awesome-secure-stacks/issues/new) | 简单 |
| 📦 提议新技术栈 | [创建 Issue](https://github.com/lxl141421/awesome-secure-stacks/issues/new) 并附上详情 | 中等 |
| 📊 更新评分 | [提交 PR](https://github.com/lxl141421/awesome-secure-stacks/compare) 并附上证据 | 中等 |
| 🔍 审计技术栈 | [按照审计指南](CONTRIBUTING.md) | 困难 |
| 📝 改进文档 | [提交 PR](https://github.com/lxl141421/awesome-secure-stacks/compare) | 简单 |

### 贡献指南

1. 阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 获取完整指南和模板
2. 所有新技术栈必须包含**复现模板**（锁文件或 Docker Compose）
3. 评分变更需要**证据**（CVE 链接、审计报告、工具输出）
4. 在所有交互中保持尊重和建设性

### 添加新技术栈

```bash
# 1. Fork 并克隆
git clone https://github.com/YOUR_USERNAME/awesome-secure-stacks.git
cd awesome-secure-stacks

# 2. 创建分支
git checkout -b add/my-awesome-stack

# 3. 在对应分类文件中添加技术栈条目
#    按照 CONTRIBUTING.md 中的模板格式
#    包含: 版本矩阵、安全评分、CVE 分析、替代方案

# 4. 提交 PR 并附上证据
git push origin add/my-awesome-stack
```

---

## 🗺️ 路线图

完整项目路线图请参阅 [ROADMAP.md](ROADMAP.md)。关键里程碑包括自动化评分流水线、扩展技术栈覆盖范围，以及与 Sigstore 和 OpenSSF Scorecard 数据的集成。

**即将推出：**

- 🤖 CI/CD 集成的自动化月度评分
- 📊 交互式技术栈对比面板
- 🔗 Sigstore 和 SLSA 溯源验证集成
- 📦 扩展技术栈覆盖：嵌入式系统、游戏引擎、数据工程
- 🌐 多语言文档（中文、日本語、한국어）

---

## 📜 许可证

本项目采用 **MIT 许可证** — 详见 [LICENSE](LICENSE) 文件。

> **为什么选择 MIT？** 安全知识应该自由获取。我们选择 MIT 以最大化采用和贡献。

---

## 🙏 致谢

本项目离不开以下支持：

### 这个项目适合谁？

- 🧑‍💻 **独立开发者** — 没有安全团队，需要经过审核的技术栈
- 🤖 **AI 辅助开发者** — 使用 Copilot/Cursor/Aider，需要验证 AI 生成的依赖选择
- 🌐 **Web 团队** — 构建 React/Vue/Angular 应用，需要生产级安全
- 📱 **移动端团队** — 构建 iOS/Android/跨平台应用，需要加固的原生桥接
- ⚙️ **后端团队** — 运行 Go/Rust/Python/Java 服务，在 API 网关之后
- 🎮 **游戏工作室** — 保护多人游戏基础设施和 Mod 生态
- 🏢 **企业技术升级** — 在框架代际间安全迁移
- 🔄 **单体→微服务团队** — 需要每个迁移阶段的安全保障

### 特别致谢

- 🏛️ **[OpenSSF](https://openssf.org/)** — Scorecard、SLSA 和 Sigstore 基础
- 🔍 **[Sonatype](https://www.sonatype.com/)** — 软件供应链状况报告
- 🛡️ **[Snyk](https://snyk.io/)** — 漏洞数据库和研究
- 📦 **[npm](https://www.npmjs.com/)、[PyPI](https://pypi.org/)、[crates.io](https://crates.io/)** — 包管理生态
- 🐙 **[GitHub Security](https://github.com/security)** — 安全公告数据库和 Dependabot
- 🌐 **[CISA](https://www.cisa.gov/)** — SBOM 指南和供应链安全倡导
- 💜 **所有贡献者** — 审计、测试和维护技术栈条目
- 🦀 **Rust 社区** — 证明内存安全可以成为默认
- 🐧 **Linux 内核社区** — 从 XZ 事件中汲取的深刻教训
- **XZ Utils 事件响应者** — 他们的工作凸显了供应链安全的紧迫性
- **`event-stream` 事件报告者** — 首次揭示了 npm 生态的脆弱性
- **每一位维护者** — 签名发布、发布 SBOM、负责任地响应 CVE

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
