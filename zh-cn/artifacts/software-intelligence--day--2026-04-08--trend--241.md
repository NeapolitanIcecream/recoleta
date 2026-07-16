---
kind: trend
trend_doc_id: 241
granularity: day
period_start: '2026-04-08T00:00:00'
period_end: '2026-04-09T00:00:00'
topics:
- software-agents
- repository-engineering
- evaluation
- code-generation
- agent-infrastructure
run_id: materialize-outputs
aliases:
- recoleta-trend-241
tags:
- recoleta/trend
- topic/software-agents
- topic/repository-engineering
- topic/evaluation
- topic/code-generation
- topic/agent-infrastructure
language_code: zh-CN
---

# 软件代理工作正在更明确地强调规格、检查和整仓库任务

## 概览
当天最强的证据支持这样一种软件代理：它先写下任务，在仓库尺度上行动，并通过具体检查。ReCodeAgent 和 REAgent 在生成前加入规划或需求后，拿到了可测的提升。CLI-Tool-Bench 和 SWD-Bench 则把评测收紧到端到端行为、仓库理解和下游可用性上。

## 研究发现

### Specification and verification sit inside the agent loop
当系统自己带着计划并检查自己的输出时，仓库规模的编码工作证据更强。ReCodeAgent 把翻译拆成分析、规划、翻译和验证，然后报告在 118 个项目和四种语言对上的 99.4% 编译成功率和 86.5% 测试通过率。REAgent 在修复问题时用的是同样的大体模式：先生成结构化需求，用生成的测试给它打分，再反复修改，直到需求足以驱动补丁。报告的改进幅度是在基线之上将已解决问题提高 9.17% 到 24.83%。核心很直接：仓库代理在规格和验证是循环中的一级步骤时表现更好，而不是把清理工作放到最后。

#### 资料来源
- [ReCodeAgent: A Multi-Agent Workflow for Language-agnostic Translation and Validation of Large-scale Repositories](../Inbox/2026-04-08--recodeagent-a-multi-agent-workflow-for-language-agnostic-translation-and-validation-of-large-scale-repositories.md): Multi-agent planning and validation deliver strong repository-level translation results.
- [REAgent: Requirement-Driven LLM Agents for Software Issue Resolution](../Inbox/2026-04-08--reagent-requirement-driven-llm-agents-for-software-issue-resolution.md): Requirement generation and assessment improve issue-resolution outcomes.

### Benchmarks are testing full repository tasks, not just code fragments
基准设计正在更接近开发者真正让代理做的事。CLI-Tool-Bench 从空工作区开始，按命令行为、输出和文件系统影响来评分完整的 CLI 工具。即使是最好的模型，总体成功率也低于 43%。SWD-Bench 按文档是否能帮助回答开发问题、定位功能文件、并在整个仓库中找回实现细节来给文档打分。它还报告，在使用更好的文档时，SWE-Agent 的问题解决率会额外提高 20%。这一时期的评测工作更关注代理能否完成另一个系统可以验证的仓库任务，而不是本地输出是否漂亮。

#### 资料来源
- [Evaluating LLM-Based 0-to-1 Software Generation in End-to-End CLI Tool Scenarios](../Inbox/2026-04-08--evaluating-llm-based-0-to-1-software-generation-in-end-to-end-cli-tool-scenarios.md): 0-to-1 CLI benchmark measures end-to-end repository construction and finds low success rates.
- [Evaluating Repository-level Software Documentation via Question Answering and Feature-Driven Development](../Inbox/2026-04-08--evaluating-repository-level-software-documentation-via-question-answering-and-feature-driven-development.md): Documentation benchmark ties quality to repository QA tasks and downstream agent performance.

### Agent infrastructure is becoming a product surface
产品工作把代理运行时本身打包成交付物。Claude Managed Agents 提供了一个托管循环，包含工具、代码执行、网页访问、持久会话和服务端事件历史。这把运行时控制、引导和环境设置放到平台侧，而不是应用团队侧。这里的证据来自产品文档，不是基准数据，所以结论比研究论文更窄。不过它仍然符合当天的主题：团队想要的是代理行为连同执行、状态和控制面一起到位。

#### 资料来源
- [Claude Managed Agents Overview](../Inbox/2026-04-08--claude-managed-agents-overview.md): Managed runtime product bundles execution, tools, state, and steering for autonomous agents.
