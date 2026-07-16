---
kind: trend
trend_doc_id: 1037
granularity: day
period_start: '2026-05-17T00:00:00'
period_end: '2026-05-18T00:00:00'
topics:
- coding agents
- software engineering benchmarks
- vulnerability repair
- tool calling
- code review
- legacy modernization
run_id: materialize-outputs
aliases:
- recoleta-trend-1037
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/vulnerability-repair
- topic/tool-calling
- topic/code-review
- topic/legacy-modernization
language_code: zh-CN
---

# 代码代理正按已交付系统和已验证修复循环接受评判

## 概览
当天最强的信号是具体执行。SaaSBench 和 WebGameBench 评估已交付的软件行为，而 ContraFix 和 MemRepair 通过把运行时证据和历史修复放进循环来改进修复。当前重点是运维层面：环境搭建、集成、验证和审查控制决定代理是否有用。

## 研究发现

### Full-stack delivery benchmarks
SaaSBench 把企业软件交付当作测试对象。它的任务包括冗长的产品需求、Docker 运行时、按依赖顺序执行的验证节点、多种语言、数据库，以及前后端技术栈。已报告的最佳 Pass@1 是 20.68%，超过 95% 的失败发生在深入业务逻辑之前，常见于环境搭建、配置、集成、过早停止或卡住的调试过程。

WebGameBench 把同样的问题放到用户可见的场景里。代理先构建浏览器游戏，然后运行时评估器通过 Playwright 控制 Chrome，并按需求检查行为。最佳配置的可用率达到 76.9%，但优秀率只有 20.2%。页面可以加载，却仍然缺少规则、输入处理、计分、重启行为或胜负条件。

#### 资料来源
- [SaaSBench: Exploring the Boundaries of Coding Agents in Long-Horizon Enterprise SaaS Engineering](../Inbox/2026-05-17--saasbench-exploring-the-boundaries-of-coding-agents-in-long-horizon-enterprise-saas-engineering.md): SaaSBench task design, validation setup, and failure results.
- [WebGameBench: Requirement-to-Application Evaluation for Coding Agents via Browser-Native Games](../Inbox/2026-05-17--webgamebench-requirement-to-application-evaluation-for-coding-agents-via-browser-native-games.md): WebGameBench runtime evaluation and usable versus excellent results.

### Vulnerability repair with runtime evidence and memory
两篇修复论文把漏洞修复变成了反馈问题。ContraFix 对比崩溃执行和安全执行，在故障附近插入探针，并在打补丁前写出修复规范。在 SEC-Bench 上，它修复了 200 个 C/C++ CVE 实例中的 84.0%，消融实验把 27 个百分点的提升归因于对比式运行时分析。

MemRepair 走的是以记忆为中心的路线。它保存过去的修复、可复用的安全模式，以及从失败补丁到成功补丁的轨迹。一个由 Locator、Patcher 和 Verifier 组成的循环会先运行漏洞测试和回归测试，再决定是否接受修改。在 SEC-Bench 上，使用 DeepSeek-v3.2 的 MemRepair 修复了 58.00% 的任务，超过了列出的 OpenHands、SWE-agent 和 Aider 基线。

#### 资料来源
- [ContraFix: Agentic Vulnerability Repair via Differential Runtime Evidence and Skill Reuse](../Inbox/2026-05-17--contrafix-agentic-vulnerability-repair-via-differential-runtime-evidence-and-skill-reuse.md): ContraFix method, SEC-Bench result, and ablation evidence.
- [MemRepair: Hierarchical Memory for Agentic Repository-Level Vulnerability Repair](../Inbox/2026-05-17--memrepair-hierarchical-memory-for-agentic-repository-level-vulnerability-repair.md): MemRepair memory design, verification loop, and benchmark results.

### Verified tool-call data from real APIs
FireFly 先执行真实的 Model Context Protocol（MCP）API，再在观察到输出后编写任务，从而构建工具调用训练数据。这个流程把 Smithery 服务器筛到 240 个服务器和 993 个工具，构建有向工具图，探索在线 API，并缓存已观察到的调用，用于离线强化学习。

最后得到的是一个包含 5,144 个已验证任务和 9,749 条轨迹的数据集。Qwen3-4B 在 FireFly 测试集上训练后，pass@1 从 28.1% 提升到 41.5%，接近 Claude Sonnet 4.6 的 42.2%。论文还报告了在 Tau2-Bench、MCP-Atlas 和 MCPMark 上的提升。

#### 资料来源
- [Firefly: Illuminating Large-Scale Verified Tool-Call Data Generation from Real APIs](../Inbox/2026-05-17--firefly-illuminating-large-scale-verified-tool-call-data-generation-from-real-apis.md): FireFly data-generation pipeline, dataset scale, and model results.

### Human-controlled software workflows
这篇代码审查论文把代理式审查当作一个带有人类决策点的协同 pull request 流程。它的五个阶段覆盖 PR 创建、PR 扩展、审查者选择、AI 辅助审查和复盘。论文是一个愿景性工作：没有报告新的基准、原型评估、用户研究或受控实验。

AgentModernize 把一种更可测试的结构用于遗留系统现代化。它把业务规则提取到 Behavioral Specification Graph 中，生成 Python/FastAPI 代码，并通过反馈验证行为。结果仍然偏低：GPT-5.3-codex 的平均 Behavioral Equivalence Rate 达到 19.4%，而单次提示和思维链基线在测试场景中都得到了 0.0%。

#### 资料来源
- [Rethinking Code Review in the Age of AI: A Vision for Agentic Code Review](../Inbox/2026-05-17--rethinking-code-review-in-the-age-of-ai-a-vision-for-agentic-code-review.md): Agentic code-review workflow and lack of new empirical evaluation.
- [AgentModernize: Preserving Business Logic in Legacy Modernization with Multi-Agent LLMs and Behavioral Specification Graphs](../Inbox/2026-05-17--agentmodernize-preserving-business-logic-in-legacy-modernization-with-multi-agent-llms-and-behavioral-specification-graphs.md): AgentModernize specification graph, validation loop, and behavioral equivalence results.
