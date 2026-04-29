---
kind: trend
trend_doc_id: 611
granularity: day
period_start: '2026-04-22T00:00:00'
period_end: '2026-04-23T00:00:00'
topics:
- coding-agents
- real-world-evaluation
- agent-harness
- developer-docs
- execution-based-validation
- security-testing
run_id: materialize-outputs
aliases:
- recoleta-trend-611
tags:
- recoleta/trend
- topic/coding-agents
- topic/real-world-evaluation
- topic/agent-harness
- topic/developer-docs
- topic/execution-based-validation
- topic/security-testing
language_code: zh-CN
---

# 编码代理研究正按被保留的代码、控制面和可执行证据来接受评判

## Overview
4月22日的研究，最有力的部分出现在编码工作与真实使用、项目脚手架和直接执行的具体检查相交的地方。SWE-chat用被保留的代码和用户反对行为为编码代理相关说法提供了依据。HARBOR和AGENTS.md表明，harness和文档选择对结果的影响，可能和模型选择一样大。WebGen-R1与LLMVD.

## Clusters

### 真实工作流证据现在已成为编码代理的一类核心输入
真实使用证据越来越难以忽视。SWE-chat 记录了 200 多个代码仓库中的约 6,000 次会话，显示编码代理被用于代码理解、git 操作、调试和完整代码编写，而不只是基准测试式的补丁生成。一个有用的修正是，输出量并不是价值的可靠代理。代理编写的代码整体保留率为 50.3%，协作会话中则降到 44.1%。同一篇论文还显示出明确的成本和风险差异：vibe coding 工作每 100 行已提交代码要用 204K tokens，并且每 1,000 行已提交代码引入 0.76 个漏洞；协作会话中这一数字是 0.14。这与近期一批加入执行检查和行为检查的论文一致，但这篇论文补上了现实使用场景这一层：开发者保留了什么、拒绝了什么，以及他们多久会提出反对。

#### Evidence
- [SWE-chat: Coding Agent Interactions From Real Users in the Wild](../Inbox/2026-04-22--swe-chat-coding-agent-interactions-from-real-users-in-the-wild.md): 关于会话构成、代码保留率、成本和漏洞率的汇总指标。

### 文档、harness 和测试工件现在都是模型行为的一部分
围绕编码代理的控制面正在变得更明确。一条研究路线把项目文档视为直接影响性能的输入。AGENTS.md 研究报告称，简短、任务明确的文件可带来 10% 到 15% 的提升，六步工作流将缺失接线文件的情况从 40% 降到 10%，而文档过于臃肿或充满警告时会导致明显失败。另一条路线则把 harness 本身当作优化目标。HARBOR 表明，手动叠加标志位可能适得其反：15/89 任务的基线，在启用一组原生标志后提升到 17/89，加入自我评估后又降到 13/89，再加入更多已发表技术后降到 12/89。Shift-Up 在同一主题中属于流程侧方法。它用需求、架构记录和可执行测试来约束代理工作，但证据仍以定性为主。共同的重点很明确：团队调优的，不只是模型输出，还有模型外面那一层包装。

#### Evidence
- [A good AGENTS.md is a model upgrade. A bad one is worse than no docs at all](../Inbox/2026-04-22--a-good-agents-md-is-a-model-upgrade-a-bad-one-is-worse-than-no-docs-at-all.md): AGENTS.md 结构对真实软件任务的具体影响。
- [HARBOR: Automated Harness Optimization](../Inbox/2026-04-22--harbor-automated-harness-optimization.md): 手动调优 harness 的结果和对配置的敏感性。
- [Shift-Up: A Framework for Software Engineering Guardrails in AI-native Software Development -- Initial Findings](../Inbox/2026-04-22--shift-up-a-framework-for-software-engineering-guardrails-in-ai-native-software-development-initial-findings.md): 通过需求和可执行测试设置流程护栏，同时指出了证据局限。

### 运行它、渲染它，或利用它：验证正越来越贴近任务本身
以执行为依据的评估正在扩展到相邻的编码任务。WebGen-R1 用强化学习生成多页面网站，但关键细节在于它的奖励设计：网站必须先通过结构检查、构建、启动服务并成功渲染，视觉评分才有意义。在其报告的基准上，有效渲染率从 30.56% 提升到 95.89%，功能质量从 1.59% 提升到 29.21%。安全研究也在采用同样的具体验证模式。LLMVD.js 不只停留在 Node.js 包中的可疑流上；它会生成并运行概念验证利用代码，确认了基准中 84% 的漏洞，并为 260 个近期包中的 36 个生成了已验证的利用代码。另一篇基于 OSV 的评估论文提出了一个更窄但同样重要的观点：即使是扫描器对比，也需要版本级的 ground truth，数字才可信。贯穿其中的是实际验证。系统正按照在直接检查下能否运行、渲染或被利用来接受评判。

#### Evidence
- [WebGen-R1: Incentivizing Large Language Models to Generate Functional and Aesthetic Websites with Reinforcement Learning](../Inbox/2026-04-22--webgen-r1-incentivizing-large-language-models-to-generate-functional-and-aesthetic-websites-with-reinforcement-learning.md): 以执行为基础的奖励设计和网站生成结果。
- [Taint-Style Vulnerability Detection and Confirmation for Node.js Packages Using LLM Agent Reasoning](../Inbox/2026-04-22--taint-style-vulnerability-detection-and-confirmation-for-node-js-packages-using-llm-agent-reasoning.md): 利用确认流程以及基准和软件包上的发现。
- [A Ground-Truth-Based Evaluation of Vulnerability Detection Across Multiple Ecosystems](../Inbox/2026-04-22--a-ground-truth-based-evaluation-of-vulnerability-detection-across-multiple-ecosystems.md): 漏洞评估中需要明确的版本级 ground truth。
