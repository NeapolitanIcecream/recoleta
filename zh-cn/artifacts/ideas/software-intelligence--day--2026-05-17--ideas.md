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

# 编码代理的运行时验证循环

## 摘要
测试编码代理的团队应该增加验收门，运行交付出来的系统，在修复过程中保留运行时证据，并用已经执行过的 API 调用来训练工具调用器。真正有用的工作在代理周围的验证循环里：浏览器、Docker 运行时、测试、崩溃输入、安全输入和缓存的工具输出都会成为工作产物。

## 面向代理构建应用的依赖感知运行时验收门
编码代理试点需要一个发布门，先启动生成的应用，驱动界面，并在人工审查代码前记录哪些需求检查失败。SaaSBench 说明这个门必须覆盖设置和集成：它报告的最佳结果是 20.68% Pass@1，而且超过 95% 的失败发生在深层业务逻辑之前，主要出现在系统设置、配置、集成、过早停止或反复调试循环中。WebGameBench 给出一个面向用户行为的较小样本：浏览器评估器通过 Playwright 控制 Chrome，检查交付的游戏是否真正处理输入、规则、计分、重启流程以及胜负条件。

一个可行的实现是在现有代理运行外面加一层 harness：标准化 Docker 启动，把产品需求编码成按依赖顺序执行的检查，用 Playwright 检查界面行为，并把被阻塞的检查和直接失败分开标记。团队可以先在最近的十个代理生成原型或内部工具上试运行。如果失败检查集中在设置、集成、状态处理和可见行为上，这个 harness 就能在代理输出进入常规代码审查前，给工程管理者一个明确的验收信号。

### 资料来源
- [SaaSBench: Exploring the Boundaries of Coding Agents in Long-Horizon Enterprise SaaS Engineering](../Inbox/2026-05-17--saasbench-exploring-the-boundaries-of-coding-agents-in-long-horizon-enterprise-saas-engineering.md): SaaSBench reports low Pass@1 and identifies setup, configuration, integration, premature stopping, and debugging loops as the dominant failure points.
- [WebGameBench: Requirement-to-Application Evaluation for Coding Agents via Browser-Native Games](../Inbox/2026-05-17--webgamebench-requirement-to-application-evaluation-for-coding-agents-via-browser-native-games.md): WebGameBench evaluates delivered browser apps with Playwright-driven runtime checks and reports a large gap between usable and excellent delivery.

## 漏洞修复代理的崩溃与安全执行循环
安全团队可以把漏洞修复代理放进一个循环里：比较会崩溃的 PoC 输入和附近的安全输入，在故障附近插入探针，并让模型在改源代码前先写出修复规格。ContraFix 在 200 个 C/C++ SEC-Bench CVE 实例上报告了 84.0% 的解决率，消融实验中有 27 个百分点的提升归因于对比式运行时分析。这个机制很直接：变异 PoC，把执行分成崩溃组和非崩溃组，比较故障附近记录下来的状态，然后按安全条件打补丁。

MemRepair 指出这个循环在真实仓库里需要的支撑层：保存之前的修复、安全模式和从失败补丁到成功补丁的轨迹，然后用漏洞测试和回归测试验证每个候选补丁。产品安全团队可以从最近修复的 CVE 入手，保存 sanitizer 报告、堆栈跟踪、探针日志、已接受补丁摘要、失败补丁摘要、CWE、语言和项目标识符。验证器应只接受能编译并通过原始崩溃案例和回归套件的补丁。

### 资料来源
- [ContraFix: Agentic Vulnerability Repair via Differential Runtime Evidence and Skill Reuse](../Inbox/2026-05-17--contrafix-agentic-vulnerability-repair-via-differential-runtime-evidence-and-skill-reuse.md): ContraFix uses paired crashing and safe executions, runtime probes, repair specifications, and verified patching; its ablation credits contrastive runtime analysis with a large gain.
- [MemRepair: Hierarchical Memory for Agentic Repository-Level Vulnerability Repair](../Inbox/2026-05-17--memrepair-hierarchical-memory-for-agentic-repository-level-vulnerability-repair.md): MemRepair describes persistent repair memory and a Locator, Patcher, Verifier loop that runs vulnerability and regression tests before accepting edits.

## 面向内部 MCP 工具调用者的已执行输出数据集
训练代理使用内部 MCP 服务器的团队，可以在成功的 API 探索已经产出具体结果之后再生成任务。FireFly 先筛选真实的 MCP 工具，构建有向工具图，运行 API，缓存观察到的调用，然后再写自然语言任务，并把答案模式和这些观察结果绑定起来。这个顺序减少了不可执行的工具轨迹和过期标签，因为预期答案已经存在于记录下来的执行数据里。

内部版本可以从无状态的预发工具开始，这些工具要有清晰的 JSON schema，并且不需要用户特定认证。每条成功轨迹都应保存工具名、参数、输出和数据流边。缓存响应可以支持离线评估和强化学习，而不用反复对变化中的服务发起实时调用。一个小检查就足够测试适配性：选二十个内部工具，探索多步调用，测量缓存输出有多大比例能支持带有精确字段答案的可验证任务。

### 资料来源
- [Firefly: Illuminating Large-Scale Verified Tool-Call Data Generation from Real APIs](../Inbox/2026-05-17--firefly-illuminating-large-scale-verified-tool-call-data-generation-from-real-apis.md): FireFly builds verified tool-call data by executing real MCP APIs first, caching outputs, and generating tasks backward from observed results.
- [Firefly: Illuminating Large-Scale Verified Tool-Call Data Generation from Real APIs](../Inbox/2026-05-17--firefly-illuminating-large-scale-verified-tool-call-data-generation-from-real-apis.md): The paper states that FireFly produced 5,144 verified tasks across 240 servers and 993 tools and used cached execution for reproducible offline training.
