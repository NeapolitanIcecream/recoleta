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

# 带执行检查的代理工作流

## Summary
这里最值得直接动手测试的工作，是把软件代理放进带有硬执行检查的循环中。近期最清晰的三个构建方向是：一个会同时修改测试和代码的仓库修复 worker、一个面向高吞吐审计型业务的编译式工作流工具，以及一个用于微服务集成测试的在线依赖模拟器。每个方向都有明确用户、有边界清楚的试点方式，也都有足够具体的结果，适合放进现有工程流程里验证。

## 将代码补丁与测试补丁生成联动的仓库修复
仓库级修复代理可以开始把测试当作可编辑的证据，而不是固定不变的把关者。Agent-CoEvo 清楚地展示了一种可落地的做法：同时运行代码补丁和测试补丁，在同一个执行矩阵里给两者打分，并且只保留那些既能解释 issue 报告、又会在有缺陷的仓库上失败、并在修复后的仓库上通过的候选。这里的实际痛点很常见：团队遇到的缺陷报告里，现有测试经常不完整、过时，或不足以准确约束行为变化，因此只改代码的修复循环要么对糟糕测试过拟合，要么直接卡住。

一个实际的产品形态，是面向大型 Python 或 Java 仓库维护者的 CI 侧修复 worker。它会提交一个草稿 PR，其中包含两个关联的 diff：实现补丁，以及为该补丁提供依据的测试改动。前期验证可以做得很窄也很直接：抽样那些维护者在修复时必须修改测试的 issue，再比较纯代码代理和协同进化循环在合并率与审查拒绝率上的差异。论文在 SWE-bench Lite 上报告了 41.33% 的 resolved，在 SWT-bench Lite 上报告了 46.4%，测试质量也高于列出的基线，这已经足以支持在那些缺陷积压稳定、且已有 CI 覆盖的仓库中测试这一工作流。

### Evidence
- [Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints](../Inbox/2026-04-06--beyond-fixed-tests-repository-level-issue-resolution-as-coevolution-of-code-and-behavioral-constraints.md): 报告了代码补丁与测试补丁的联合搜索，以及在 SWE-bench Lite 和 SWT-bench Lite 上的基准提升。
- [Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints](../Inbox/2026-04-06--beyond-fixed-tests-repository-level-issue-resolution-as-coevolution-of-code-and-behavioral-constraints.md): 解释了协同进化机制，以及为什么固定测试会让仓库级修复的约束不足。

## 面向高吞吐审计型业务的编译式工作流部署
高吞吐的文档和交易工作流可以把模型调用前移到构建阶段，并在生产环境里运行经过验证的代码。Compiled AI 给出了一个具体模式：先在固定模板中一次性生成一个小型业务逻辑函数，再执行安全扫描、类型和语法检查、沙箱测试，以及基于黄金集的准确率检查，然后在主路径中运行这个已批准的产物，不再进行运行时模型调用。用户侧的压力很直接：计费、预授权、理赔录入和文档处理团队需要可重复的输出、较短的延迟，以及能够经受审查的审计记录。

这现在就可以做成一个内部工具，给已经在维护基于提示词自动化的工作流工程师使用。先从一个模式稳定、数据量足够大的窄流程开始，例如发票字段抽取或基于规则的录入分流。第一步验证看成本和波动：把当前的提示词工作流编译成代码，回放一周的生产输入，再比较单笔交易延迟、输出漂移和人工异常处理率。论文报告 BFCL 上的盈亏平衡点约为 17 笔交易，中位延迟为 4.5 ms，可复现性为 100%，而且在规模化后成本差距很大。DocILE 的结果也说明，当脏乱文档仍然需要受约束的模型调用时，受限的混合模式是可行的。

### Evidence
- [Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation](../Inbox/2026-04-06--compiled-ai-deterministic-code-generation-for-llm-based-workflow-automation.md): 概述了编译式工作流模式、验证关卡，以及它与企业工作流的契合点。
- [Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation](../Inbox/2026-04-06--compiled-ai-deterministic-code-generation-for-llm-based-workflow-automation.md): 提供了函数调用类工作负载的盈亏平衡、token 和延迟结果。

## 用于微服务集成测试的在线依赖模拟
做微服务测试的团队可以用在线依赖模拟器替换脆弱的录制式 mock；这种模拟器会在测试运行期间响应请求，并在整个场景里保留状态。Mirage 说明了原因：保留出来的测试场景会击穿静态替代物，因为后者必须在测试开始前就猜到所有相关行为，而运行时模拟器可以对新参数、错误路径和多步流程即时作出反应。这正对应了服务团队里的常见阻碍：下游系统部署成本高、在 CI 中不可用，或者太不稳定，无法支撑可重复的集成测试。

一个具体的构建方式，是做一个测试 harness，拉起一个与 FastAPI 兼容的 mock 端点，底层由 LLM 驱动；有依赖源码时用源码做输入，没有时就用 traces。最早的用户会是平台和后端团队，他们通常有 service mesh、大量内部 API，并且经常遇到契约漂移。第一项检查很直接：选一个当前依赖 record-replay fixture 的下游依赖，让同一套集成测试分别跑在真实依赖、现有 mock 和在线模拟器上，然后比较通过/失败结果的一致性和 payload 形状保真度。Mirage 报告称，在 110 个场景上的白盒模式下，status-code fidelity 为 99%，response-shape fidelity 也为 99%；而 record-replay 在同一基准上分别只有 62% 和 16%。这个差距已经足以支持围绕最容易出问题的依赖做一次小范围试点。

### Evidence
- [MIRAGE: Online LLM Simulation for Microservice Dependency Testing](../Inbox/2026-04-06--mirage-online-llm-simulation-for-microservice-dependency-testing.md): 概述了在线模拟方法，以及它相对静态替代物的保真度提升。
- [MIRAGE: Online LLM Simulation for Microservice Dependency Testing](../Inbox/2026-04-06--mirage-online-llm-simulation-for-microservice-dependency-testing.md): 说明了为什么保留场景会让 record-replay 和其他预生成 mock 失效。
