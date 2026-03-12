---
source: hn
url: https://news.ycombinator.com/item?id=47311657
published_at: '2026-03-09T16:53:52'
authors: []
topics:
- agent-platform
- filesystem-agents
- sandbox-deployment
- code-agents
- developer-infrastructure
relevance_score: 0.94
run_id: fa4f5d9d-bee2-47ee-b80f-c690622f57d0
---

# Launch HN: Terminal Use (YC W26) – Vercel for filesystem-based agents

## Summary
- TL;DR: Terminal Use 是一个面向“需要沙箱+文件系统”的智能体部署平台，把代码打包、沙箱运行、消息流式传输、任务状态持久化和文件读写统一成类似“Vercel for agents”的工作流，重点创新在于把文件系统做成独立于任务生命周期的一等公民。
- Problem:
  - 部署文件系统型智能体（如编码、研究、文档处理、内部工具）通常要手工拼装多个组件：打包、沙箱、消息流、状态持久化、文件上传下载，工程复杂且脆弱。
  - 传统托管方式往往把沙箱生命周期与工作区文件强绑定，导致跨轮次持续工作、多人/多智能体共享文件、版本迁移与回滚都很麻烦。
  - 这很重要，因为很多真实软件生产与代码智能体任务都依赖可持久化工作区，而不只是无状态聊天接口。
- Approach:
  - 用 `config.yaml` + `Dockerfile` 从代码仓库打包智能体，并通过 CLI 一键部署到沙箱环境，提供统一 API/SDK。
  - 定义 `on_create`、`on_event`、`on_cancel` 三个生命周期端点来驱动任务/会话执行，但不强绑定具体 agent harness。
  - 提供对 Claude Agent SDK、Codex SDK 的适配，也允许自定义 harness 接入其消息协议（兼容 Vercel AI SDK v6 类型）。
  - 核心机制是将文件系统与任务生命周期解耦：工作区可跨轮次持久化、被多个智能体共享、独立上传/下载，并可通过预签名 URL 直接传输文件而无需后端代理。
  - 在部署层支持现代开发平台能力，如 preview/production 环境、git 驱动环境切换、日志、回滚，以及任务迁移/版本固定策略。
- Results:
  - 文本未提供基准测试、实验数据或量化指标，因此没有可核验的性能/准确率提升数字。
  - 声称可将原本需要拼接的多项基础设施（打包、沙箱、流式消息、状态持久化、文件传输）收敛到单一部署流程中。
  - 声称其主要差异化在存储：文件系统被作为一等公民，可跨轮次持久化、跨智能体共享，并支持独立于沙箱活跃状态的文件上传/下载。
  - 声称支持部署后自动迁移现有任务到新版本；如遇破坏性变更，也可让旧任务继续停留在旧版本，仅新任务使用新部署。
  - 已支持 Claude Agent SDK 与 Codex SDK，并计划补齐更通用沙箱能力，如 preview URLs 与更底层的 `sandbox.exec(...)` API。

## Links
- Canonical: https://news.ycombinator.com/item?id=47311657
