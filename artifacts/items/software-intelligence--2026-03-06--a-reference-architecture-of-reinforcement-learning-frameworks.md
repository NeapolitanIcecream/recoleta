---
source: arxiv
url: http://arxiv.org/abs/2603.06413v1
published_at: '2026-03-06T15:51:34'
authors:
- Xiaoran Liu
- Istvan David
topics:
- reinforcement-learning
- reference-architecture
- software-architecture
- rl-frameworks
- grounded-theory
relevance_score: 0.4
run_id: materialize-outputs
---

# A Reference Architecture of Reinforcement Learning Frameworks

## Summary
本文提出了一个强化学习（RL）框架的参考架构，用来统一描述当前分散且命名混乱的RL基础设施。作者基于18个开源RL框架的归纳分析，抽取出共性的架构组件、关系和典型模式。

## Problem
- RL框架快速增多，但不同实现的架构模式、组件边界和术语使用不一致，导致比较、复用、集成和学习都很困难。
- 业界常把 environment、simulator、framework、algorithm 混用，削弱了工程上的清晰性，也增加了质量评估、依赖管理、认证和交付难度。
- 过去工作多关注局部问题或单一工具，缺少一个能跨多种RL框架通用的参考架构。

## Approach
- 作者采用 grounded-theory 方法，对 **18** 个常用开源RL系统进行迭代式开放编码、主轴编码和选择编码，从源码、配置和文档中归纳架构要素。
- 采样覆盖 environment 和 framework 两类系统；文中称在 **5** 个环境后、**6** 个框架后达到理论饱和，后续样本主要用于验证已有类别。
- 最终提出一个高层RA，包含 **6** 个顶层组件、归入 **4** 个组件组：Framework、Framework Core、Environment、Utilities。
- RA进一步细化出关键部件，如 Experiment Orchestrator、Framework Orchestrator、Agent、Environment，以及其子组件，如 Lifecycle Manager、Configuration Manager、Distributed Execution Coordinator、Multi-Agent Coordinator、Learner、Buffer、Function Approximator 等。
- 作者还用该RA去重建典型RL架构模式，并总结哪些组件在现有框架中更常见、哪些能力通常依赖第三方库实现。

## Results
- 主要产出是一个参考架构，而不是新的RL算法；论文**没有报告传统意义上的任务性能指标**（如奖励、成功率、SOTA提升）。
- 经验基础：分析了 **18** 个开源RL框架；作者称环境侧在 **5** 个样本后达到饱和、框架侧在 **6** 个样本后达到饱和。
- 架构结果：提出 **6** 个顶层组件 / **4** 个组件组的RA，并明确区分 Framework、Framework Core、Environment、Utilities 之间的职责边界。
- 覆盖性主张：论文用表格统计组件在不同框架中的出现情况，例如 Lifecycle Manager 出现在 **10** 个所列框架中，Distributed Execution Coordinator 出现在 **4** 个框架中，Multi-Agent Coordinator 出现在 **7** 个框架中。
- Agent内部三类核心组件——Buffer、Function Approximator、Learner——在所列 **10** 个训练型框架中均可观察到，支持其“这些是RL框架共性核心”的结论。
- 论文还发布了可复核的数据包（Zenodo），强化了其可验证性；但从给定摘录看，**没有与现有架构方法做定量对比实验**。

## Link
- [http://arxiv.org/abs/2603.06413v1](http://arxiv.org/abs/2603.06413v1)
