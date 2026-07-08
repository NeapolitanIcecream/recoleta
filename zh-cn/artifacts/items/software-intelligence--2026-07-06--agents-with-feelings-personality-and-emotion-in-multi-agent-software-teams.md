---
source: arxiv
url: https://arxiv.org/abs/2607.05659v1
published_at: '2026-07-06T22:00:27'
authors:
- Yunyan Ding
- Thomas Zimmermann
- Iftekhar Ahmed
topics:
- multi-agent-systems
- llm-agents
- software-engineering
- code-generation
- code-review
- persona-prompting
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Agents with Feelings? Personality and Emotion in Multi-Agent Software Teams

## Summary
## 摘要
本文测试人格和情绪提示是否会改变软件工程 LLM 智能体团队的性能和行为。

## 问题
- 多智能体软件工程系统通常改变智能体角色和工作流，对行为画像的测试不足。
- 这个问题很重要，因为画像提示会改变智能体编码系统中的通过率、评审输出、修订循环和 token 成本。

## 方法
- 用大五人格特质、六种情绪、O*NET 工作风格和任务角色构建智能体人格设定。
- 测试共享画像团队和混合画像团队：共享画像团队中所有智能体获得相同画像，混合画像团队中不同角色获得不同画像。
- 代码生成使用 Planner、Implementer 和 Reviewer；代码评审使用两个 Writer 和一个 Supervisor。
- 评估 78 种团队画像配置：54 种共享画像配置和 24 种混合画像配置。
- 在 659 个任务实例上运行四个指令微调 LLM：282 个 LiveCodeBench v6 lite 代码生成问题和 377 个 Hydra-Reviewer 代码评审实例。

## 结果
- 研究覆盖 4 个 LLM、2 项任务、每个模型-任务组合 78 种画像配置，以及 659 个抽样任务实例。
- 在代码生成中，各模型的最佳和最差共享画像配置在 pass@1 上相差 7.1 到 11.3 个百分点。
- 最佳混合画像配置在 8 个模型-任务设置中的 6 个超过最佳共享画像配置。
- 恐惧画像和高尽责性画像会带来更多修订活动、更多过度修订和更高 token 用量，但没有稳定的性能提升。
- 摘录没有给出代码评审的详细 BLEU-4 数值；其最具体的强主张是，画像选择会改变参考对齐和协作行为。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.05659v1](https://arxiv.org/abs/2607.05659v1)
