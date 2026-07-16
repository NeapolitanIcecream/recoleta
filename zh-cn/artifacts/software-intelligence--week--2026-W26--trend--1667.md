---
kind: trend
trend_doc_id: 1667
granularity: week
period_start: '2026-06-22T00:00:00'
period_end: '2026-06-29T00:00:00'
topics:
- coding agents
- agent evaluation
- software engineering
- security
- cost control
- repository context
run_id: materialize-outputs
aliases:
- recoleta-trend-1667
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-evaluation
- topic/software-engineering
- topic/security
- topic/cost-control
- topic/repository-context
language_code: zh-CN
---

# 编码智能体正被作为受控生产软件来评判

## 概览
本周的研究把大型语言模型（LLM）智能体视为生产软件。最有力的工作把任务成功与上下文恢复、产物交付、成本核算、权限边界和凭据安全联系起来。DeepDiscovery、EnterpriseClawBench 和 Rel(AI)Build 提供了最清晰的证据。

## 研究发现

### 仓库上下文与工作场景交付
智能体评估正在转向决定工作能否交付的条件：正确文件、可用产物、保留的状态和可度量成本。DeepDiscovery 显示，仓库任务需要贯通代码、配置、测试和组织结构的上下文。其报告的 SWE-bench Verified 解题率达到 78.6%，比基线高 8.2 个百分点。

EnterpriseClawBench 补充了工作场景证据。它把真实企业会话转成 852 个可复现任务，包含夹具、交付物、硬性规则、轨迹、运行时间、token 使用量和成本。经过审计的 Lite 集最佳结果为 0.663，产物质量和交付仍有很大提升空间。开源普查提供了规模证据：超过 1.8 亿个仓库中的智能体轨迹需要多种检测信号，因为拉取请求、提交、作者模式和配置文件覆盖的是不同群体。

#### 资料来源
- [From Fragments to Paths: Task-Level Context Recovery for Large Industrial Codebases](../Inbox/2026-06-22--from-fragments-to-paths-task-level-context-recovery-for-large-industrial-codebases.md): DeepDiscovery 摘要，包含仓库上下文方法和 SWE-bench Verified 结果。
- [EnterpriseClawBench: Benchmarking Agents from Real Workplace Sessions](../Inbox/2026-06-22--enterpriseclawbench-benchmarking-agents-from-real-workplace-sessions.md): EnterpriseClawBench 摘要，包含工作场景任务构建、评分维度和结果。
- [Detecting AI Coding Agents in Open Source: A Validated Multi-Method Census of 180 Million Repositories](../Inbox/2026-06-23--detecting-ai-coding-agents-in-open-source-a-validated-multi-method-census-of-180-million-repositories.md): 经过验证的编码智能体轨迹普查，覆盖超过 1.8 亿个仓库。

### 成本感知编排与恢复测试
本周的基准研究关注智能体能否在执行过程中管理不确定性。贝叶斯控制把编码智能体编排视为围绕候选程序正确性的决策问题。它保留后验信念，并在评估器、重新生成、验证和停止之间选择。最明确的收益出现在低先验、高验证器成本的设置中，此时低成本评估器能提供有用信号。

ToolBench-X 和 CodeChat-Eval 暴露了两类常见失败模式。ToolBench-X 在 1,106 个可执行任务和 4,956 个工具中注入可恢复的工具风险；没有被评估的模型达到 0.60 的总体准确率。CodeChat-Eval 测试十轮代码细化，并发现后续编辑后功能正确性下降 19.2% 到 69.2%，具体取决于模型。这些结果把回归保持和恢复选择变成核心评估目标。

#### 资料来源
- [Bayesian control for coding agents](../Inbox/2026-06-23--bayesian-control-for-coding-agents.md): 贝叶斯控制摘要，包含信念状态编排和成本区间。
- [Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability](../Inbox/2026-06-24--beyond-function-calling-benchmarking-tool-using-agents-under-tool-environment-unreliability.md): ToolBench-X 摘要，包含可恢复的工具风险和准确率结果。
- [CodeChat-Eval: Evaluating Large Language Models in Multi-Turn Code Refinement Dialogues](../Inbox/2026-06-24--codechat-eval-evaluating-large-language-models-in-multi-turn-code-refinement-dialogues.md): CodeChat-Eval 摘要，包含多轮细化设置和正确性下降。

### 安全、权限和凭据边界
安全证据已经扩展到生成片段之外。VibeApps 研究收集了 10,517 个主要由 AI 构建的应用，并在 200 个已部署 Web 应用的随机样本中验证了 1,471 个可利用漏洞。反复出现的问题包括访问控制失效、密码学失败、注入、密钥暴露、占位逻辑和未过滤输入。

Rel(AI)Build 把智能体提示词、权限和工作流状态作为受管理的产物。在 10,008 个公开仓库中，它发现了 6,145 个智能体配置文件；经过 fork 调整后，10.1% 的被跟踪配置路径是完全重复项，声明权限边界的不到 1%。DevFortress 提供了围绕凭据的事件级证据：引用数字包括 2025 年公共 GitHub 上暴露的 2,860 万个新密钥，以及 MCP 配置文件中发现的 24,008 个唯一密钥。产品声明的测试少于事件证据，但风险模式很具体。

#### 资料来源
- [Understanding the (In)Security of Vibe-Coded Applications](../Inbox/2026-06-22--understanding-the-in-security-of-vibe-coded-applications.md): Vibe-coded 应用安全研究，包含语料库和经过验证的漏洞数量。
- [A Deterministic Control Plane for LLM Coding Agents](../Inbox/2026-06-25--a-deterministic-control-plane-for-llm-coding-agents.md): Rel(AI)Build 摘要，包含智能体配置普及度、权限边界发现和控制机制。
- [AI Agent Credential Crisis: Six Months of Incidents](../Inbox/2026-06-28--ai-agent-credential-crisis-six-months-of-incidents.md): 凭据事件摘要，包含密钥暴露和 MCP 配置指标。
