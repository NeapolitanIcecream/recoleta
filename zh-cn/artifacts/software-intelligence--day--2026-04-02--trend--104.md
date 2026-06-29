---
kind: trend
trend_doc_id: 104
granularity: day
period_start: '2026-04-02T00:00:00'
period_end: '2026-04-03T00:00:00'
topics:
- coding-agents
- benchmarks
- tool-use
- software-testing
- api-testing
run_id: materialize-outputs
aliases:
- recoleta-trend-104
tags:
- recoleta/trend
- topic/coding-agents
- topic/benchmarks
- topic/tool-use
- topic/software-testing
- topic/api-testing
language_code: zh-CN
---

# 软件代理研究正变得更可执行、可回放，也更贴近生产

## Overview
今天的研究最强的地方，是软件工作可以通过执行来检查。重点是更严格地评估编码代理，以及为代码和 API 生成更好的测试。ProdCodeBench 和 ToolMisuseBench 都缩小了基准分数与部署条件之间的差距。结果是，我们更清楚地看到代理在哪些地方还能用，在哪些地方仍然会失效。

## Clusters

### Production evaluation for coding agents
当下最强的工作，是尝试用能经受真实工程条件的信号来评价编码代理。ProdCodeBench 从工业单体仓库里的真实开发者-助手会话构造任务，保留原始提示，回推出已落地的 diff，并用稳定的 fail-to-pass 和 pass-to-pass 测试给代理评分。这让离线评估更接近团队在实践中面对的约束。ClickHouse 从部署侧补了一份现场报告：当代理能读代码、运行工具，并留在评审和测试循环里时，它们就有用。那里的数字是运行层面的，不是基准层面的，但它们说明了为什么生产团队会在意扎实的评估。

#### Evidence
- [ProdCodeBench: A Production-Derived Benchmark for Evaluating AI Coding Agents](../Inbox/2026-04-02--prodcodebench-a-production-derived-benchmark-for-evaluating-ai-coding-agents.md): Production-derived benchmark design and core results.
- [Agentic Coding at ClickHouse](../Inbox/2026-04-02--agentic-coding-at-clickhouse.md): Concrete deployment report with review-and-testing workflow and operational outcomes.

### Reliability is about behavior under constraints
几篇论文关注的是模型做出一个看起来合理的第一步之后会发生什么。Beyond Resolution Rates 发现，很多失败并不是狭义上的搜索失败。代理常常找到了正确文件，却因为架构判断错误而仍然没能修对。ToolMisuseBench 看的是另一层可靠性：在 schema 漂移、超时、速率限制和授权错误下的工具调用。它的基线在部分超时和 schema 故障上能恢复，但总体成功率仍停在 0.250，预算化成功率也没有变化。共同的信息是，代理质量现在取决于验证行为、恢复策略和动作纪律，而不只是回答质量。

#### Evidence
- [Beyond Resolution Rates: Behavioral Drivers of Coding Agent Success and Failure](../Inbox/2026-04-02--beyond-resolution-rates-behavioral-drivers-of-coding-agent-success-and-failure.md): Trajectory analysis of coding-agent failures and the role of architectural judgment.
- [ToolMisuseBench: An Offline Deterministic Benchmark for Tool Misuse and Recovery in Agentic Systems](../Inbox/2026-04-02--toolmisusebench-an-offline-deterministic-benchmark-for-tool-misuse-and-recovery-in-agentic-systems.md): Deterministic benchmark for tool misuse, recovery, and budgeted reliability.

### LLMs are being pushed into executable testing work
测试正在变成一个一等的生成目标，而不只是事后的检查。TestDecision 把测试套件构建看作一个序贯优化问题，并报告说，相比基础开源模型，它在分支覆盖率、执行通过率和漏洞发现上都有很大提升。APITestGenie 把同样的执行导向态度用到 API 上：它从业务需求加 OpenAPI 规格出发，生成可运行的 Jest 和 Axios 测试，并且在 25 个需求里有 22 个至少生成出一个有效脚本。合在一起，这些论文让测试更可执行、更贴近需求，也更适合作为模型流水线的直接产物。

#### Evidence
- [TestDecision: Sequential Test Suite Generation via Greedy Optimization and Reinforcement Learning](../Inbox/2026-04-02--testdecision-sequential-test-suite-generation-via-greedy-optimization-and-reinforcement-learning.md): Sequential test-suite generation with reported coverage and bug-finding gains.
- [APITestGenie: Generating Web API Tests from Requirements and API Specifications with LLMs](../Inbox/2026-04-02--apitestgenie-generating-web-api-tests-from-requirements-and-api-specifications-with-llms.md): Requirement-driven API test generation with executable validation rates.
