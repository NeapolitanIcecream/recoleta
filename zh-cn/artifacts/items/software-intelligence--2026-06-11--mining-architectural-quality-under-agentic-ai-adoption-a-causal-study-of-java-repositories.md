---
source: arxiv
url: https://arxiv.org/abs/2606.13298v1
published_at: '2026-06-11T12:50:36'
authors:
- Oliver Aleksander Larsen
- Mahyar T. Moghaddam
topics:
- architectural-smells
- difference-in-differences
- ai-code-adoption
- software-maintainability
- java-repositories
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Mining Architectural Quality Under Agentic AI Adoption: A Causal Study of Java Repositories

## Summary
## 摘要
这篇论文检验了 agentic AI 编码采用是否会改变 Java 仓库的架构质量。结果显示，采用与更低的架构异味密度相关，但下降来自代码增长更快，而不是异味数量减少。

## 问题
- 以往关于 AI 编码工具的因果研究测量的是代码层面的结果，而不是架构层面的影响。
- 架构异味很重要，因为它们会反映依赖图的退化，并损害可维护性和演化能力。
- 论文要回答的是，agentic AI 使用是否会改变架构异味密度，哪些异味类型会变化，以及这种变化是来自异味数量还是代码规模。

## 方法
- 研究跟踪了 151 个开源 Java 仓库，观察窗口为 13 个月，其中 74 个为处理组，77 个为倾向得分匹配的对照组。
- 它通过仓库工件识别 agentic AI 采用情况，例如工具配置文件和 Co-Authored-By 提交尾注。
- 主要设计是分期差分中的差分，使用 Borusyak 插补估计量，并加入仓库和时间固定效应。
- 结果变量是架构异味密度，定义为每千行代码的总异味数；同时对原始异味计数和 KLOC 建模，以拆分分子和分母效应。
- 论文还做了事件研究、按异味类型建模，以及稳健性检验，包括 wild cluster bootstrap 和 Lee bounds。

## 结果
- 架构异味密度的主效应为 -6.7%，采用 Borusyak 插补估计（β = -0.0698，SE 0.0239，95% CI [-0.117, -0.023]，p = 0.004），基于 1,811 个按月观测值。
- TWFE-Sun-Abraham 结果一致，为 -6.6%（p = 0.005）。
- 预趋势平坦：Wald 检验 p = 0.896。
- 原始异味计数没有变化：+1.1%（p = 0.82）。
- 代码规模增加：log KLOC 上升 +12.8%（p = 0.0027），这说明 ASD 下降是分母效应。
- 按异味类型看，hub-like dependency 下降 5.0%（Holm 校正后 p = 0.003）；cyclic dependency 也为 -5.0%，但未通过 Holm 校正；unstable dependency 和 god component 的密度变化都不显著。
- 按工具分层的估计为负：Claude Code 为 -5.1%（p = 0.039），Copilot 为 -4.0%（p = 0.005），Cursor 为 -13.5%（p < 0.001）。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.13298v1](https://arxiv.org/abs/2606.13298v1)
