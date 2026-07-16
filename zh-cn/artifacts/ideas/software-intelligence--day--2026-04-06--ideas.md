---
kind: ideas
granularity: day
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-07T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- reinforcement-learning
- software-testing
- program-repair
- verification
- workflow-automation
tags:
- recoleta/ideas
- topic/coding-agents
- topic/reinforcement-learning
- topic/software-testing
- topic/program-repair
- topic/verification
- topic/workflow-automation
language_code: zh-CN
---

# 带执行检查的软件代理工作流

## 摘要
这里最可操作的工作，是把软件代理放进带硬执行检查的循环里。最清楚的近期构建方向有三个：一个会连同代码一起改测试的仓库修复工作器、一个面向高吞吐审计型运营的编译式工作流工具，以及一个用于微服务集成测试的在线依赖模拟器。它们都有明确用户、可控试点，而且报告结果具体到足以放进现有工程流程里验证。

## 带代码和测试补丁联动生成的仓库修复
仓库修复代理可以开始把测试当作可编辑的证据，而不是固定的门槛。Agent-CoEvo 是最清楚的例子：它把代码补丁和测试补丁放在一起运行，在同一个执行矩阵里评分，只保留那些能解释问题报告、并且在有缺陷的仓库上先失败、在修复后的仓库上再通过的候选项。实际中的痛点很常见：团队接到的 bug 报告里，现有测试不完整、过时，或者力度不够，无法锁定行为变化，所以只改代码的修复循环要么对着坏测试过拟合，要么卡住。

一个可落地的产品形态，是给大型 Python 或 Java 仓库维护者用的 CI 修复工作器。它会打开一个草稿 PR，里面有两份关联的 diff：一份是实现补丁，一份是用来说明补丁的测试改动。便宜而明确的检查方式是：抽取那些维护者在修复时确实改过测试的问题，然后把只改代码的代理和共演化循环在合并率、审阅者拒绝率上做对比。论文报告在 SWE-bench Lite 上解决率为 41.33%，在 SWT-bench Lite 上为 46.4%，而且测试质量高于列出的基线，这足以支持在有稳定 bug 积压和现有 CI 覆盖的仓库上试这个流程。

### 资料来源
- [Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints](../Inbox/2026-04-06--beyond-fixed-tests-repository-level-issue-resolution-as-coevolution-of-code-and-behavioral-constraints.md): Reports joint search over code and test patches, plus benchmark gains on SWE-bench Lite and SWT-bench Lite.
- [Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints](../Inbox/2026-04-06--beyond-fixed-tests-repository-level-issue-resolution-as-coevolution-of-code-and-behavioral-constraints.md): Explains the coevolution mechanism and why fixed tests under-constrain repository repair.

## 面向高吞吐审计型运营的编译式工作流部署
高吞吐的文档和事务工作流，可以把模型使用移到构建时，在生产中运行已验证的代码。Compiled AI 给出了一种具体做法：先在固定模板里生成一次小的业务逻辑函数，再做安全扫描、语法和类型检查、沙箱测试，以及对照金标数据的准确性检查，最后让通过审批的产物在主路径上执行，运行时不再调用模型。用户侧的压力很直接：账单、事前授权、理赔录入和文档处理团队需要可重复的输出、较短的延迟，以及经得起审查的审计轨迹。

这已经可以作为内部工具交给维护提示词自动化的工作流工程师来做。先选一个边界清楚、模式稳定、流量也足够的流程，比如发票字段提取或基于规则的录入路由。第一步验证的是成本和波动：把当前的提示词工作流编译成代码，回放一周的生产输入，比较每笔交易的延迟、输出漂移和人工例外率。论文报告在 BFCL 上的打平点大约是 17 笔交易，中位延迟 4.5 ms，可复现性 100%，在规模上也有很大的成本差异。DocILE 的结果还说明，当脏文档仍然需要受限的模型调用时，受控的混合模式是可行的。

### 资料来源
- [Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation](../Inbox/2026-04-06--compiled-ai-deterministic-code-generation-for-llm-based-workflow-automation.md): Summarizes the compiled workflow pattern, validation gates, and enterprise workflow fit.
- [Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation](../Inbox/2026-04-06--compiled-ai-deterministic-code-generation-for-llm-based-workflow-automation.md): Provides break-even, token, and latency results for function-calling workloads.

## 微服务集成测试中的在线依赖模拟
测试微服务的团队，可以用在线依赖模拟器替代脆弱的录制 mock，让它在测试运行期间回答请求，并在整个场景里保留状态。Mirage 说明了这件事为什么重要：被留出的场景会让静态替代物失效，因为它必须提前猜出所有相关行为；而运行时模拟器可以对新参数、错误路径和多步流程作出反应。这对应服务团队里一个常见阻碍：下游系统部署成本高、在 CI 里拿不到，或者太不稳定，没法做可重复的集成测试。

具体的构建方式，是搭一个测试夹具，用 LLM 提供一个兼容 FastAPI 的 mock 端点；如果能拿到依赖方源码，就用源码做种子，否则就用 traces。早期用户是平台和后端团队，他们有服务网格、很多内部 API，而且契约漂移频繁。第一步检查很直接：挑一个现在依赖 record-replay fixtures 的依赖项，把同一套集成测试分别跑在真实依赖、现有 mock 和在线模拟器上，再比较通过/失败是否一致，以及负载形状是否一致。Mirage 在 white-box 模式下、覆盖 110 个场景时，状态码一致性和响应形状一致性都达到 99%；而 record-replay 在同一基准上只有 62% 和 16%。这个差距已经足够支持围绕最容易失败的依赖项做一个聚焦试点。

### 资料来源
- [MIRAGE: Online LLM Simulation for Microservice Dependency Testing](../Inbox/2026-04-06--mirage-online-llm-simulation-for-microservice-dependency-testing.md): Summarizes the online simulation approach and fidelity gains over static substitutes.
- [MIRAGE: Online LLM Simulation for Microservice Dependency Testing](../Inbox/2026-04-06--mirage-online-llm-simulation-for-microservice-dependency-testing.md): Details why held-out scenarios break record-replay and other pre-generated mocks.
