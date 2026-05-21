---
kind: ideas
granularity: day
period_start: '2026-05-17T00:00:00'
period_end: '2026-05-18T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software engineering benchmarks
- vulnerability repair
- tool calling
- code review
- legacy modernization
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/vulnerability-repair
- topic/tool-calling
- topic/code-review
- topic/legacy-modernization
language_code: zh-CN
---

# 面向编码智能体的运行时验证循环

## Summary
测试编码智能体的团队应加入能够运行交付系统的验收闸门，在修复过程中保留运行时证据，并用已经执行过的 API 调用训练工具调用智能体。有价值的工作在智能体外围的验证循环中：浏览器、Docker 运行时、测试、崩溃输入、安全输入和缓存工具输出都成为工作产物的一部分。

## 面向智能体构建应用的依赖感知运行时验收闸门
编码智能体试点需要一个发布闸门：启动生成的应用、驱动 UI，并在人类审查代码前记录哪些需求检查失败。SaaSBench 说明了这个闸门为什么要覆盖搭建和集成：其报告的最佳结果是 20.68% Pass@1，超过 95% 的失败发生在进入深层业务逻辑之前，常见位置是系统搭建、配置、集成、过早停止或反复调试循环。WebGameBench 给出了一个更小的用户可见行为模式：浏览器评估器通过 Playwright 控制 Chrome，检查交付的游戏是否真的处理了输入、规则、计分、重启流程以及胜负条件。

可落地的做法是在现有智能体运行外加一层测试 harness：规范化 Docker 启动，把产品需求编码成按依赖顺序执行的检查，用 Playwright 测 UI 行为，并把被阻塞的检查和直接失败分开标注。团队可以在最近十个由智能体生成的原型或内部工具上试运行。如果失败检查集中在搭建、集成、状态处理和可见行为上，这个 harness 能在智能体输出进入常规代码审查前，给工程经理一个具体的验收信号。

### Evidence
- [SaaSBench: Exploring the Boundaries of Coding Agents in Long-Horizon Enterprise SaaS Engineering](../Inbox/2026-05-17--saasbench-exploring-the-boundaries-of-coding-agents-in-long-horizon-enterprise-saas-engineering.md): SaaSBench 报告了较低的 Pass@1，并指出搭建、配置、集成、过早停止和调试循环是主要失败点。
- [WebGameBench: Requirement-to-Application Evaluation for Coding Agents via Browser-Native Games](../Inbox/2026-05-17--webgamebench-requirement-to-application-evaluation-for-coding-agents-via-browser-native-games.md): WebGameBench 用 Playwright 驱动的运行时检查评估交付的浏览器应用，并报告可用交付和优秀交付之间存在较大差距。

## 面向漏洞修复智能体的崩溃与安全执行循环
安全团队可以把漏洞修复智能体包在一个循环里：比较会崩溃的 Proof-of-Concept 输入和相近的安全输入，在故障附近插入探针，并要求模型先写出修复规格，再编辑源码。ContraFix 报告在 200 个 C/C++ SEC-Bench CVE 实例上达到 84.0% 的解决率，消融实验把 27 个百分点的增益归因于对比式运行时分析。机制很具体：变异 PoC，把执行分成崩溃组和非崩溃组，比较故障附近记录的状态，再按安全条件打补丁。

MemRepair 指出了这个循环在真实代码仓库中需要的支撑层：存储既往修复、安全模式、以及从失败补丁到成功补丁的轨迹，然后用漏洞测试和回归测试验证每个候选补丁。产品安全团队可以从最近已修复的 CVE 开始，存储 sanitizer 报告、堆栈跟踪、探针日志、已接受补丁摘要、失败补丁摘要、CWE、语言和项目标识符。验证器只应接受能够编译，并同时通过原始崩溃用例和回归测试套件的补丁。

### Evidence
- [ContraFix: Agentic Vulnerability Repair via Differential Runtime Evidence and Skill Reuse](../Inbox/2026-05-17--contrafix-agentic-vulnerability-repair-via-differential-runtime-evidence-and-skill-reuse.md): ContraFix 使用成对的崩溃执行和安全执行、运行时探针、修复规格和验证过的补丁；其消融实验把较大增益归因于对比式运行时分析。
- [MemRepair: Hierarchical Memory for Agentic Repository-Level Vulnerability Repair](../Inbox/2026-05-17--memrepair-hierarchical-memory-for-agentic-repository-level-vulnerability-repair.md): MemRepair 描述了持久化修复记忆，以及运行漏洞测试和回归测试后才接受编辑的 Locator、Patcher、Verifier 循环。

## 面向内部 MCP 工具调用智能体的已执行输出数据集
训练智能体使用内部 MCP 服务器的团队，可以在成功 API 探索产出具体结果后再生成任务。FireFly 筛选真实 MCP 工具，构建有向工具图，运行 API，缓存观察到的调用，然后写出与这些观察结果绑定的自然语言任务和答案 schema。这个顺序减少了不可行的工具轨迹和过期标签，因为预期答案已经存在于记录的执行数据中。

内部版本可以从无状态的预发工具开始，这些工具应有清晰的 JSON schema，并且不需要用户特定认证。每条成功轨迹都应存储工具名称、参数、输出和数据流边。缓存响应可以支持离线评估和强化学习，避免反复实时调用会变化的服务。一个小检查就能测试是否适用：选择二十个内部工具，探索多步调用，并衡量缓存输出有多大比例能支撑带精确字段级答案的可检查任务。

### Evidence
- [Firefly: Illuminating Large-Scale Verified Tool-Call Data Generation from Real APIs](../Inbox/2026-05-17--firefly-illuminating-large-scale-verified-tool-call-data-generation-from-real-apis.md): FireFly 先执行真实 MCP API，缓存输出，再从观察到的结果反向生成任务，以此构建已验证的工具调用数据。
- [Firefly: Illuminating Large-Scale Verified Tool-Call Data Generation from Real APIs](../Inbox/2026-05-17--firefly-illuminating-large-scale-verified-tool-call-data-generation-from-real-apis.md): 论文称 FireFly 基于 240 台服务器和 993 个工具生成了 5,144 个已验证任务，并使用缓存执行来进行可复现的离线训练。
