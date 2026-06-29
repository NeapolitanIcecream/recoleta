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

# 编码代理研究正在按保留代码、控制面和可执行证明来评判

## Overview
4 月 22 日的研究，最有力的部分出现在编码工作与真实使用、项目脚手架和直接执行检查相交的地方。SWE-chat 用保留代码和用户反对来支撑编码代理的说法。HARBOR 和 AGENTS.md 显示，harness 和文档选择能像模型选择一样改变结果。WebGen-R1 和 LLMVD.js 把同样的压力推进到网站生成和安全领域，在那里，输出是按运行中的系统来打分，而不是按润色过的文本来打分。

## Clusters

### 真实工作流证据现在是编码代理的一类核心输入
真实使用证据越来越难以忽视。SWE-chat 记录了跨 200 多个仓库的约 6,000 个会话，显示编码代理被用于代码理解、git 操作、调试和完整代码编写，而不只是类似基准测试的打补丁。一个有用的修正是，输出量对价值来说是个很弱的代理指标。代理写出的代码总体保留率是 50.3%，协作会话降到 44.1%。同一篇论文还显示出明确的成本和风险差异：vibe coding 的工作每 100 行已提交代码使用 204K token，每 1,000 行已提交代码引入 0.76 个漏洞；协作会话分别是 0.14 个。这个结果符合近期一批加入执行和行为检查的论文，但这篇补上了缺失的实地层面：开发者保留了什么、拒绝了什么，以及他们多频繁地提出反对。

#### Evidence
- [SWE-chat: Coding Agent Interactions From Real Users in the Wild](../Inbox/2026-04-22--swe-chat-coding-agent-interactions-from-real-users-in-the-wild.md): 关于会话构成、代码保留率、成本和漏洞率的汇总指标。

### 文档、harness 和测试制品现在也是模型行为的一部分
编码代理周围的控制面正在变得更明确。一类工作把项目文档当作直接的性能输入。AGENTS.md 研究报告，简短、面向任务的文件带来 10% 到 15% 的提升；使用六步工作流后，缺失接线文件的比例从 40% 降到 10%；文档过于臃肿或充满警告时，失败会明显增多。另一类工作把 harness 本身当作优化目标。HARBOR 表明，手动叠加标志位会适得其反：基线在 15/89 个任务上通过，加入一组原生标志位后升到 17/89，但再加入自评估后降到 13/89，再加更多已发表技术后降到 12/89。Shift-Up 处在同一主题的流程侧。它用需求、架构记录和可执行测试来约束代理工作，但证据仍然是定性的。共同重点很清楚：团队在调整模型外层的包装，也在调整模型输出本身。

#### Evidence
- [A good AGENTS.md is a model upgrade. A bad one is worse than no docs at all](../Inbox/2026-04-22--a-good-agents-md-is-a-model-upgrade-a-bad-one-is-worse-than-no-docs-at-all.md): AGENTS.md 结构对真实软件任务的具体影响。
- [HARBOR: Automated Harness Optimization](../Inbox/2026-04-22--harbor-automated-harness-optimization.md): 手动 harness 调优结果和配置敏感性。
- [Shift-Up: A Framework for Software Engineering Guardrails in AI-native Software Development -- Initial Findings](../Inbox/2026-04-22--shift-up-a-framework-for-software-engineering-guardrails-in-ai-native-software-development-initial-findings.md): 通过需求和可执行测试设置流程护栏，并注明证据限制。

### 先运行、再渲染、再利用：验证离任务越来越近
带执行结果的评估正在扩展到相邻的编码任务。WebGen-R1 用强化学习做多页网站生成，但关键细节在于它的奖励设计：网站必须先通过结构检查、构建、启动和渲染，视觉评分才开始起作用。在论文报告的基准上，valid render ratio 从 30.56% 升到 95.89%，functional quality 从 1.59% 升到 29.21%。安全研究也在用同样的具体确认方式。LLMVD.js 不停留在 Node.js 包里的可疑流转；它会生成并运行概念验证漏洞利用，确认了基准中 84% 的漏洞，并为最近 260 个包中的 36 个生成了已验证的漏洞利用。另一篇基于 OSV 的评估论文给出一个更窄的判断：即使是扫描器比较，也需要版本级真值，数字才可信。主线是实用验证。系统现在按直接检查下能运行、能渲染，还是能被利用来评判。

#### Evidence
- [WebGen-R1: Incentivizing Large Language Models to Generate Functional and Aesthetic Websites with Reinforcement Learning](../Inbox/2026-04-22--webgen-r1-incentivizing-large-language-models-to-generate-functional-and-aesthetic-websites-with-reinforcement-learning.md): 以执行为基础的奖励设计和网站生成结果。
- [Taint-Style Vulnerability Detection and Confirmation for Node.js Packages Using LLM Agent Reasoning](../Inbox/2026-04-22--taint-style-vulnerability-detection-and-confirmation-for-node-js-packages-using-llm-agent-reasoning.md): 漏洞利用确认流程和基准/包级结果。
- [A Ground-Truth-Based Evaluation of Vulnerability Detection Across Multiple Ecosystems](../Inbox/2026-04-22--a-ground-truth-based-evaluation-of-vulnerability-detection-across-multiple-ecosystems.md): 漏洞评估中需要明确的版本级真值。
