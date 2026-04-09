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

# 代理运行验证

## Summary
面向生产的 software-agent 工作正在三个方向上变得更具体：面向编码代理的私有回放基准、面向工具调用失败与恢复的确定性测试，以及按需求生成可运行脚本的 API 测试。每一项都对应一种团队可以用自己的代码仓库、工具契约或基于 OpenAPI 的服务来试点的构建。

## 面向代理辅助代码变更的私有回放基准
对已经在使用编码代理的团队，一个实际的下一步是建立内部基准：样本来自真实且已被接受的代理会话，保留原始提示词，把已落地的 diff 从仓库状态中回退出来，并用稳定测试集按 fail-to-pass 和 pass-to-pass 计分。ProdCodeBench 表明，这件事可以在持续变化的 monorepo 中完成，同时仍然对模型和 harness 变化给出可重复的离线评估。这对要在代理配置、工具接线方式和模型升级之间做选择的团队很重要，因为线上 A/B 测试往往要花几周时间，还会让真实开发者遭遇表现差的运行结果。

这里值得做的不是公开排行榜，而是一个绑定你自己代码仓库和提示词分布的滚动式私有评估流水线。可以先从一个团队已合并的代理辅助改动开始，排除那些无法通过执行来检查的请求，再加入改动前和改动后的重复测试运行，用来筛掉不稳定的测试。它可以用于代理更新的发布闸门，也可以用于提示词、检索或工具变更后的回归检查。一个低成本的验证办法是回放最近几十个已接受的会话，看看分数变化是否比你当前的基准组合更能贴合 reviewer 偏好和 CI 结果。

### Evidence
- [ProdCodeBench: A Production-Derived Benchmark for Evaluating AI Coding Agents](../Inbox/2026-04-02--prodcodebench-a-production-derived-benchmark-for-evaluating-ai-coding-agents.md): ProdCodeBench 描述了一个源自生产环境的基准：它保留逐字提示词，回退已落地的 diff，并在 monorepo 中用稳定的 F2P 和 P2P 测试为代理打分。
- [ProdCodeBench: A Production-Derived Benchmark for Evaluating AI Coding Agents](../Inbox/2026-04-02--prodcodebench-a-production-derived-benchmark-for-evaluating-ai-coding-agents.md): 论文指出，组织需要针对模型和 harness 变化获得快速的离线信号，因为线上 A/B 测试速度慢、成本高。

## 面向工具调用失败与恢复策略的回放 harness
在扩大生产访问范围之前，部署工具使用型代理的团队需要一个回放 harness，用来覆盖 schema drift、超时、限流和授权失败。ToolMisuseBench 清楚地说明，通用能力测试会漏掉这一层。在其发布设置中，三个基线的总体成功率都停在 0.250，而授权和限流子集的成功率仍是 0.000。恢复逻辑对超时和 schema drift 有帮助，但预算约束下的成功率曲线依然是平的。

这指向一个明确的支撑层：针对每个代理工具契约建立内部故障注入测试床。记录有代表性的任务，冻结工具 schema 和成功判定，然后在注入故障和严格限制重试次数、调用次数、步骤数的条件下回放同一批 episode。对无效调用、策略违规、恢复成功率和预算内完成情况计分。第一批用户会是负责代理运行时安全的平台团队，以及那些发现看起来合理的工具计划会在正常生产错误下失败的 API owner。一个低成本检查办法是挑出你最常见的十个代理动作，模拟一次过期授权、一次 schema 重命名和一条 429 策略。如果成功率明显下滑，卡点在运行时恢复策略，不在提示词质量。

### Evidence
- [ToolMisuseBench: An Offline Deterministic Benchmark for Tool Misuse and Recovery in Agentic Systems](../Inbox/2026-04-02--toolmisusebench-an-offline-deterministic-benchmark-for-tool-misuse-and-recovery-in-agentic-systems.md): ToolMisuseBench 通过确定性的故障注入以及明确的步骤、调用和重试预算，单独评估工具误用和恢复。

## 从需求到 Jest 的 API 验收测试生成
对于已经维护 OpenAPI 规格并且仍在手写验收测试的团队，按需求生成 API 测试已经可以做试点。APITestGenie 接收业务需求和 OpenAPI 文档，输出可运行的 Jest 与 Axios 测试。在 25 条需求上，它在三次尝试内为其中 22 条生成了至少一个有效脚本，其中包括大型工业 API。一些生成的测试还暴露了 API 缺陷，包括跨端点问题。论文报告的平均成本是每次生成 €0.37，平均生成时间是 126 秒。

这个流程改动很直接：让产品、QA 或集成工程师在工单或 story 层面提交需求文本，检索相关的 OpenAPI 片段，生成两到三个候选测试，在 CI 中运行，并只保留那些能执行且符合预期行为的脚本。这适用于测试覆盖在端点正确性与业务流程正确性的边界处断开的场景。一个低成本试点可以从一个 OpenAPI 规格还不错、同时积压了不少手写验收测试的服务开始。重点衡量有效脚本率、reviewer 编辑时间，以及多端点场景下的缺陷发现率。

### Evidence
- [APITestGenie: Generating Web API Tests from Requirements and API Specifications with LLMs](../Inbox/2026-04-02--apitestgenie-generating-web-api-tests-from-requirements-and-api-specifications-with-llms.md): APITestGenie 能根据业务需求和 OpenAPI 规格生成可执行的 API 测试，并在真实 API 上报告了较高的需求级成功率。
