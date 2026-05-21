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
这项访谈研究发现，业界在软件工程中使用代理式 AI 仍主要停留在助手或任务代理层面。主要障碍是验证：公司可以做出能力更强的代理原型，但如果没有人工审查，就无法认定其输出可用于实际工作流。

## 问题
- 研究关注公司如何在真实软件开发工作流中采用代理式 AI，而这方面的证据仍有限。
- 这个问题很重要，因为不可靠的 AI 输出、薄弱的可追溯性、数据泄露风险，以及对专有代码的适配不佳，都可能阻碍其在安全监管场景和大型遗留系统中的使用。

## 方法
- 作者对 12 家不同规模公司的 16 名从业者进行了半结构化访谈，覆盖小型、中型和大型组织。
- 他们将每家公司归入一个 6 级代理式 AI 成熟度量表，其中第 0 级是无支持的个人使用，第 5 级是自修复系统。
- 他们按公司规模、监管情况、正在使用的工具、SDLC 任务、报告的限制和实验性部署情况对案例进行了比较。
- 他们使用两个本地 LLM，gpt-oss-20b 和 Qwen3-14B，检查结构化访谈摘要；在人工审查后，62 条建议补充中有 11 条被采纳。

## 结果
- 当前生产成熟度较低：12 家公司中，7 家处于第 1 级 AI 助手，4 家处于第 2 级任务代理，1 家处于第 3 级协作式 AI，第 0、4、5 级均为 0 家。
- 监管并未阻止所有进展：在受监管公司中，5 家为第 1 级，3 家为第 2 级；在不受监管公司中，2 家为第 1 级，1 家为第 2 级，1 家为第 3 级。
- C6、C7、C8 和 C12 四家公司拥有高于其生产成熟度等级的实验性能力，但由于输出验证依赖人工审查，无法将这些能力转入实际工作流。
- 报告中最强的部署障碍包括：大型且碎片化代码库带来的上下文窗口限制、在专有语言和协议上的表现较弱、与资质认定规则冲突的非确定性输出，以及云端 LLM 的数据保密限制。
- C7 报告称，copilot 环境内的多代理工作流将缺陷解决周转时间从数天或数周缩短到数小时，但端到端代理式流水线仍被排除在实际开发工作流之外。
- 研究没有报告基准测试式的模型准确率结果；其定量说法来自访谈计数、成熟度划分，以及 16 次访谈、12 家公司的样本。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14675v1](https://arxiv.org/abs/2605.14675v1)
