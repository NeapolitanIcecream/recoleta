---
source: arxiv
url: https://arxiv.org/abs/2607.18886v1
published_at: '2026-07-21T09:14:59'
authors:
- Mingyu Chen
- Yakun Zhang
- Zihao Xie
- Yixing Luo
- Jinrui Xu
- Cuiyun Gao
- Kaiqi Zhao
- Yunming Ye
topics:
- software-foundation-model
- code-intelligence
- automated-software-production
- multi-agent-software-engineering
- requirements-traceability
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# TraceDev: A Traceability-Driven Multi-agent Framework for Requirement-to-Code Development

## Summary
## 摘要
TraceDev 是一个由五个智能体组成的框架，可根据复杂的多步骤用例生成仓库级代码。其核心机制是一个连接需求、设计模型和代码的异构可追溯图，使智能体能够发现遗漏并完善各类制品。

## 问题
- 现有的需求到代码系统通常采用简化的单句任务，无法表示包含多个功能点和语义约束的用例。
- 这类系统通常缺乏需求、设计与实现之间的显式可追溯性，因此难以发现遗漏以及跨阶段的语义错误。
- 这一点很重要，因为不完整或不正确的仓库级实现会降低自动化软件生产的功能正确性、可维护性和可信度。

## 方法
- TraceDev 使用五个具有特定角色的 LLM 智能体：需求细化器（Requirement Refiner）、设计器（Designer）、开发者（Developer）、测试器（Tester）和验证器（Validator）。
- 需求细化器统一用例术语，推断缺失的主语，重写有歧义的步骤，并执行迭代式语法验证。
- 设计器创建 PlantUML 类图和时序图；开发者根据这些设计生成代码；测试器生成并执行测试，并将失败结果反馈以进行有界自我修正。
- 验证器构建一个包含需求实体、设计元素和代码文件的异构有向图。LLM 语义匹配将需求连接到设计，而基于 AST 的匹配则将设计连接到代码，并揭示缺失的实现。

## 结果
- 在 ETOUR 和 SMOS 数据集上，评估涵盖 125 个用例，并将 TraceDev 与 ChatDev 和 MetaGPT 进行比较。
- 在 ETOUR 上，TraceDev 的语义覆盖率为 71.72%，比 ChatDev 高 51.66%，比 MetaGPT 高 75.14%。
- 在 ETOUR 上，TraceDev 的成功率为 53.63%，比 ChatDev 高 129.19%，比 MetaGPT 高 186.64%。
- 在 SMOS 上，TraceDev 的成功率为 56.82%，最高超过基线方法 340.80%。
- 摘录未提供消融实验结果、统计显著性、执行成本或完整的分数据集指标，因此这些证据支持其基准测试性能有所提升，但不足以单独测量可追溯图的因果贡献。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.18886v1](https://arxiv.org/abs/2607.18886v1)
