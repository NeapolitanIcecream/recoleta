---
source: arxiv
url: https://arxiv.org/abs/2605.14675v1
published_at: '2026-05-14T10:34:59'
authors:
- Spyridon Alvanakis Apostolou
- Jan Bosch
- "Helena Holmstr\xF6m Olsson"
topics:
- agentic-ai
- software-engineering
- industrial-adoption
- multi-agent-systems
- human-ai-interaction
- ai-verification
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Agentic AI in Industry: Adoption Level and Deployment Barriers

## Summary
## 摘要
这项访谈研究发现，工业界在软件工程中使用 agentic AI 仍然主要停留在助手或任务代理层面。主要阻碍在于验证：公司可以原型化更强的智能体，但在没有人工审查的情况下，无法把它们的输出纳入正式工作流程。

## 问题
- 该研究考察公司如何在真实软件开发流程中采用 agentic AI，而这方面的证据仍然有限。
- 这个问题很重要，因为不可靠的 AI 输出、弱可追溯性、数据泄露风险，以及与专有代码不匹配，都可能阻止它在安全监管严格和大型遗留系统中使用。

## 方法
- 作者对 12 家公司的 16 名从业者进行了半结构化访谈，这些公司覆盖小型、中型和大型组织。
- 他们把每家公司归入一个 6 级的 agentic AI 成熟度量表，其中 Level 0 表示不受支持的个人使用，Level 5 表示自我修复系统。
- 他们按公司规模、监管情况、在用工具、SDLC 任务、报告的限制和实验性部署对案例进行了比较。
- 他们使用了两个本地 LLM，gpt-oss-20b 和 Qwen3-14B，来检查结构化访谈摘要；在人工复核后，62 条建议补充中的 11 条被采纳。

## 结果
- 当前生产成熟度较低：12 家公司中有 7 家处于 Level 1 AI Assistants，4 家处于 Level 2 Task Agents，1 家处于 Level 3 Collaborative AI，Level 0、4 或 5 都没有公司达到。
- 监管并没有完全阻止进展：在受监管公司中，5 家处于 Level 1，3 家处于 Level 2；在不受监管公司中，2 家处于 Level 1，1 家处于 Level 2，1 家处于 Level 3。
- 有 4 家公司，C6、C7、C8 和 C12，拥有高于其生产成熟度水平的实验能力，但由于输出验证依赖人工审查，无法把这些能力转入正式工作流程。
- 报告中最强的部署障碍包括：用于大型且碎片化代码库的上下文窗口限制、专有语言和协议上的表现较弱、与资格认证规则冲突的非确定性输出，以及云端 LLM 的数据保密限制。
- C7 报告称，copilot 环境中的多智能体工作流把 bug 修复周转时间从数天或数周缩短到数小时，但端到端的 agentic 流水线仍未进入正式开发流程。
- 该研究没有报告基准式的模型准确率结果；其定量结论来自访谈计数、成熟度分配，以及 16 次访谈、12 家公司的样本。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14675v1](https://arxiv.org/abs/2605.14675v1)
