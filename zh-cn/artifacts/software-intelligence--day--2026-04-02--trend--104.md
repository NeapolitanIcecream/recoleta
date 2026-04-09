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

# 软件代理研究正变得更可执行、更可重放，也更贴近生产环境

## Overview
今天的研究在软件工作可以通过执行来检验的地方最有说服力。重点有两个：更严格的编码代理评估，以及更好的代码和 API 测试生成。ProdCodeBench 和 ToolMisuseBench 都在缩小基准分数与部署条件之间的差距。这让人们能更实际地看到代理在哪些地方扛得住，哪些地方还会失效。

## Clusters

### 编码代理的生产环境评估
今天最强的一批工作，正在尝试用能经受真实工程环境的信号来评估编码代理。ProdCodeBench 从工业 monorepo 中真实的开发者-助手会话构建任务，保留原始提示词，回退已落地的 diff，并用稳定的 fail-to-pass 和 pass-to-pass 测试给代理打分。这让离线评估更接近团队在实际工作中面对的约束。ClickHouse 则从部署一侧给出了一份现场报告：当代理能读代码、运行工具，并保持在审查和测试循环内时，它们就有用。那里的数字是运营数据，不是严格基准测试结果，但它们说明了生产团队为什么在意贴近实际的评估。

#### Evidence
- [ProdCodeBench: A Production-Derived Benchmark for Evaluating AI Coding Agents](../Inbox/2026-04-02--prodcodebench-a-production-derived-benchmark-for-evaluating-ai-coding-agents.md): 源自生产环境的基准设计与核心结果。
- [Agentic Coding at ClickHouse](../Inbox/2026-04-02--agentic-coding-at-clickhouse.md): 包含审查与测试工作流及运营结果的具体部署报告。

### 可靠性取决于约束下的行为
有几篇论文关注的是，模型走出看似合理的第一步之后会发生什么。Beyond Resolution Rates 发现，很多失败并不是狭义上的搜索失败。代理经常能找到正确的文件，却还是修不好，因为架构判断出了错。ToolMisuseBench 看的是另一层可靠性：在 schema 漂移、超时、速率限制和授权错误下的工具调用。它的基线方法能从部分超时和 schema 故障中恢复，但总体成功率仍停在 0.250，预算约束下的成功率曲线也没有改善。共同的信息是，代理质量现在取决于验证行为、恢复策略和动作纪律，而不只是答案质量。

#### Evidence
- [Beyond Resolution Rates: Behavioral Drivers of Coding Agent Success and Failure](../Inbox/2026-04-02--beyond-resolution-rates-behavioral-drivers-of-coding-agent-success-and-failure.md): 对编码代理失败轨迹的分析，以及架构判断的作用。
- [ToolMisuseBench: An Offline Deterministic Benchmark for Tool Misuse and Recovery in Agentic Systems](../Inbox/2026-04-02--toolmisusebench-an-offline-deterministic-benchmark-for-tool-misuse-and-recovery-in-agentic-systems.md): 用于衡量工具误用、恢复能力和预算约束可靠性的确定性基准。

### LLM 正在被推向可执行测试工作
测试正在变成生成流程中的一级目标，不再只是事后检查。TestDecision 把测试套件构建视为一个序列优化问题，并报告了相对基础开源模型在分支覆盖率、执行通过率和缺陷发现上的大幅提升。APITestGenie 把同样重视执行的思路用在 API 上：它从业务需求和 OpenAPI 规范出发，生成可运行的 Jest 与 Axios 测试，并在 25 条需求中为 22 条至少生成了一份有效脚本。这两篇论文让测试更可执行、更贴近需求，也更像模型流水线的直接产物。

#### Evidence
- [TestDecision: Sequential Test Suite Generation via Greedy Optimization and Reinforcement Learning](../Inbox/2026-04-02--testdecision-sequential-test-suite-generation-via-greedy-optimization-and-reinforcement-learning.md): 序列化测试套件生成，以及文中报告的覆盖率和缺陷发现提升。
- [APITestGenie: Generating Web API Tests from Requirements and API Specifications with LLMs](../Inbox/2026-04-02--apitestgenie-generating-web-api-tests-from-requirements-and-api-specifications-with-llms.md): 由需求驱动的 API 测试生成，以及可执行验证成功率。
