---
kind: ideas
granularity: day
period_start: '2026-04-22T00:00:00'
period_end: '2026-04-23T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- real-world-evaluation
- agent-harness
- developer-docs
- execution-based-validation
- security-testing
tags:
- recoleta/ideas
- topic/coding-agents
- topic/real-world-evaluation
- topic/agent-harness
- topic/developer-docs
- topic/execution-based-validation
- topic/security-testing
language_code: zh-CN
---

# 可由代码库验证的代理评测

## Summary
编码代理评测正越来越接近团队可以在自己的代码库和流水线中直接验证的内容。这里最可用的方向是：与提交关联的保留代码和审查摩擦评分卡、与最近 PR 回放评测绑定的狭窄 `AGENTS.md` 生成流程，以及只提升那些已执行概念验证利用案例的 Node.js 安全分诊。

## 与提交关联的编码代理评分卡，用于衡量保留代码和审查摩擦
正在交付编码代理的团队需要一种与提交记录关联的评分卡，用来衡量开发者保留了什么、丢弃了什么，以及代理带来了多少审查摩擦。SWE-chat 为此提供了最直接的依据。在约 6,000 次真实会话中，代理编写代码的总体留存率为 50.3%，协作会话中降至 44.1%。用户在 39% 的轮次中提出了反对，而 vibe coding 相比协作模式有更高的 token 成本、每条已提交代码行更慢的耗时，以及更多新引入的漏洞。这些数字支持一个明确的产品改动：在代理日志中加入会话结束后的归因和提交关联，然后按代码留存、审查返工、中断率以及每条已提交代码行的安全发现，对提示、代码库和工作流进行排序。第一批用户会是那些已经在共享代码库中为编码代理付费，并且正在争论这些输出是否真的有帮助的团队。一个低成本试点可以是 GitHub 应用或 CLI 包装器，把会话轨迹关联到已合并的 diff，并在正常使用一周后展示留存率和拒绝率。

### Evidence
- [SWE-chat: Coding Agent Interactions From Real Users in the Wild](../Inbox/2026-04-22--swe-chat-coding-agent-interactions-from-real-users-in-the-wild.md): 提供了编码代理会话中代码留存、用户反对、成本和漏洞率的真实世界指标。
- [SWE-chat: Coding Agent Interactions From Real Users in the Wild](../Inbox/2026-04-22--swe-chat-coding-agent-interactions-from-real-users-in-the-wild.md): 确认了数据集规模，以及将会话轨迹与开发者实际提交内容关联起来这一重点。

## 面向特定任务的 AGENTS.md 生成，以及前后对比的 PR 回放
对使用仓库代理的团队来说，带评测闭环的短小、任务专用 `AGENTS.md` 生成器现在已经是一个可行产品。现有证据已经足够把文档视为性能输入。在 Augment 的研究中，约 100 到 150 行的高质量文件带来了 10% 到 15% 的提升，而一个用于添加新集成的六步工作流把遗漏连接文件的比例从 40% 降到 10%，同时将正确性提高了 25%，完整性提高了 20%。同一项研究也说明，把事情做糟很容易：偏重架构的文件会拉入约 80K 无关 token，只包含警告规则的文件会让 PR 耗时翻倍。这里有价值的产品不是通用文档写作器，而是一个仓库扫描器：围绕狭窄的任务类型起草 `AGENTS.md`，从本地代码库插入决策表和小型代码示例，并在最近的 PR 上运行前后对比的任务回放评测。第一批买家会是平台团队和开发者效率团队，他们已经维护内部设置文档，但并不知道代理 harness 实际会读取哪些指令。

### Evidence
- [A good AGENTS.md is a model upgrade. A bad one is worse than no docs at all](../Inbox/2026-04-22--a-good-agents-md-is-a-model-upgrade-a-bad-one-is-worse-than-no-docs-at-all.md): 给出了有帮助和有害的 AGENTS.md 模式的主要量化结果，包括工作流和 token 加载影响。
- [A good AGENTS.md is a model upgrade. A bad one is worse than no docs at all](../Inbox/2026-04-22--a-good-agents-md-is-a-model-upgrade-a-bad-one-is-worse-than-no-docs-at-all.md): 详细说明了六步工作流的结果：减少了遗漏连接文件，并提高了正确性和完整性。

## 用于 Node.js 依赖分诊的概念验证利用确认
Node.js 包安全扫描可以通过为疑似污点类漏洞生成并执行概念验证利用代码，更接近可直接用于分诊的输出。LLMVD.js 清楚表明这已经可以构建。该系统确认了 84% 的基准漏洞，远高于摘录中的既有工具，并且在 260 个新近发布的包中为其中 36 个产出了已验证的利用。它的流水线和这个 headline 数字一样重要：它把候选漏洞发现、可利用性判断、约束推断和基于执行的确认拆分开来，并为路径遍历、代码注入、原型污染和命令注入使用按漏洞类别设计的预言机。这支持注册表运营方、供应链安全厂商以及拥有大量 npm 依赖的大型应用团队调整实际工作流。把利用确认放在静态怀疑之后、分析师审查之前，这样分诊就能从那些已经有可复现实物的包开始。一个小规模验证步骤是把它运行在最近的一组内部依赖上，衡量有多少扫描器告警可以收敛为带可运行证明的已确认案例。

### Evidence
- [Taint-Style Vulnerability Detection and Confirmation for Node.js Packages Using LLM Agent Reasoning](../Inbox/2026-04-22--taint-style-vulnerability-detection-and-confirmation-for-node-js-packages-using-llm-agent-reasoning.md): 概述了基于执行的漏洞确认流水线和基准结果。
- [Taint-Style Vulnerability Detection and Confirmation for Node.js Packages Using LLM Agent Reasoning](../Inbox/2026-04-22--taint-style-vulnerability-detection-and-confirmation-for-node-js-packages-using-llm-agent-reasoning.md): 确认了文中报告的 84% 基准确认率，以及在近期软件包上得到的 36 个已验证利用。
