---
kind: ideas
granularity: day
period_start: '2026-04-02T00:00:00'
period_end: '2026-04-03T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- benchmarks
- tool-use
- software-testing
- api-testing
tags:
- recoleta/ideas
- topic/coding-agents
- topic/benchmarks
- topic/tool-use
- topic/software-testing
- topic/api-testing
language_code: zh-CN
---

# Operational Agent Validation

## Summary
面向生产的软件代理工作，正在三个地方变得更具体：用于编码代理的私有回放基准、用于工具调用失败与恢复的确定性测试，以及生成可运行脚本的、由需求驱动的 API 测试生成。每一项都能落到团队自己的仓库、工具契约或基于 OpenAPI 的服务上做试点。

## Private replay benchmark for agent-assisted code changes
已经在使用编码代理的团队，可以先做一个内部基准，来源是真实的已接受代理会话，保留原始提示词，把已落地的 diff 从仓库中回退，并用稳定测试集按 fail-to-pass 和 pass-to-pass 评分。ProdCodeBench 说明，这种方法可以在变化中的 monorepo 里运行，并且在模型和执行框架变化时仍然给出可重复的离线评估。对要在代理配置、工具接线和模型升级之间做选择的团队来说，这很有用，因为线上 A/B 测试要花几周，还会把真实开发者暴露在糟糕运行结果里。

真正有用的不是公开排行榜，而是绑定到你自己的仓库和提示分布的滚动私有评估流水线。先从某个团队已经合并的代理辅助改动开始，去掉无法通过执行检查的请求，再加入变更前和变更后重复跑测试，用来筛掉不稳定测试。把它用于代理更新的发布门禁，以及提示词、检索或工具改动后的回归检查。一个便宜的验证方法，是回放最近几十个已接受会话，看看分数变化是否比你现在的基准组合更贴近审阅者偏好和 CI 结果。

### Evidence
- [ProdCodeBench: A Production-Derived Benchmark for Evaluating AI Coding Agents](../Inbox/2026-04-02--prodcodebench-a-production-derived-benchmark-for-evaluating-ai-coding-agents.md): ProdCodeBench describes a production-derived benchmark that preserves verbatim prompts, backs out landed diffs, and grades agents with stable F2P and P2P tests in a monorepo.
- [ProdCodeBench: A Production-Derived Benchmark for Evaluating AI Coding Agents](../Inbox/2026-04-02--prodcodebench-a-production-derived-benchmark-for-evaluating-ai-coding-agents.md): The paper states that organizations need fast offline signals for model and harness changes because online A/B testing is slow and costly.

## Replay harness for tool-call failure and recovery policy
部署使用工具的代理之前，团队需要一个回放环境，用来覆盖 schema 漂移、超时、速率限制和授权失败。ToolMisuseBench 清楚地说明，通用能力测试看不到这一层。在它的发布设定里，三个基线的总体成功率都只有 0.250，授权和限流子集的成功率都为 0.000。恢复逻辑在超时和 schema 漂移上有帮助，但按预算计算的成功曲线仍然是平的。

这指向一个具体的支撑层：给每个代理工具契约都建一个内部故障注入测试床。记录有代表性的任务，冻结工具 schema 和成功检查，然后在注入故障、严格限制重试次数、调用次数和步骤数的情况下回放同一批任务。把无效调用、策略违规、恢复成功和预算内完成情况都记下来。最先会用到它的是负责代理运行时安全的平台团队，以及看到看似合理的工具计划在常见生产错误下崩掉的 API 负责人。一个便宜的检查方法，是拿最常见的十个代理动作，模拟授权过期、一次 schema 改名和 429 策略。如果成功率断崖式下降，卡点就是运行时恢复策略，不是提示词质量。

### Evidence
- [ToolMisuseBench: An Offline Deterministic Benchmark for Tool Misuse and Recovery in Agentic Systems](../Inbox/2026-04-02--toolmisusebench-an-offline-deterministic-benchmark-for-tool-misuse-and-recovery-in-agentic-systems.md): ToolMisuseBench isolates tool misuse and recovery with deterministic fault injection and explicit step, call, and retry budgets.

## Requirement-to-Jest API acceptance test generation
已经维护 OpenAPI 规范、并且手写验收测试的团队，可以先试点基于需求的 API 测试生成。APITestGenie 接收业务需求和 OpenAPI 文档，输出可运行的 Jest 和 Axios 测试。它在 25 个需求上，三次尝试内为 22 个需求生成了至少一个有效脚本，包括大型工业 API。部分生成的测试暴露了 API 缺陷，包括跨端点问题。报告的平均成本是每次生成 €0.37，平均生成时间是 126 秒。

工作流改动很直接：让产品、QA 或集成工程师在工单或用户故事层提交需求文本，检索相关的 OpenAPI 片段，生成两到三个候选测试，在 CI 中运行，只保留能执行且符合预期行为的脚本。这适合测试覆盖在端点正确性和业务流程正确性之间断开的场景。一个便宜的试点，是选一个 OpenAPI 规范比较完整、而且有一批手写验收测试积压的服务。衡量有效脚本率、审阅者修改时间，以及多端点场景中的缺陷产出。

### Evidence
- [APITestGenie: Generating Web API Tests from Requirements and API Specifications with LLMs](../Inbox/2026-04-02--apitestgenie-generating-web-api-tests-from-requirements-and-api-specifications-with-llms.md): APITestGenie generates executable API tests from business requirements plus OpenAPI specs and reports high requirement-level success on real-world APIs.
