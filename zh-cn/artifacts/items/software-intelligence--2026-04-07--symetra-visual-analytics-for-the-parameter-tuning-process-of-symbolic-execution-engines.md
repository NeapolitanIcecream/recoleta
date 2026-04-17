---
source: arxiv
url: http://arxiv.org/abs/2604.05349v1
published_at: '2026-04-07T02:42:28'
authors:
- Donghee Hong
- Minjong Kim
- Sooyoung Cha
- Jaemin Jo
topics:
- visual-analytics
- symbolic-execution
- parameter-tuning
- software-testing
- human-in-the-loop
relevance_score: 0.68
run_id: materialize-outputs
language_code: zh-CN
---

# Symetra: Visual Analytics for the Parameter Tuning Process of Symbolic Execution Engines

## Summary
## 摘要
Symetra 是一个用于调优符号执行引擎（如 KLEE）的可视分析系统，由人参与指导。它帮助用户查看哪些参数设置会影响分支覆盖率，找出互补的配置，并为后续调优运行缩小搜索空间。

## 问题
- 符号执行引擎公开了许多可调参数，这些参数之间的相互作用很难理解，因此用户常常退回到默认设置，导致遗漏覆盖。
- 自动调优器可以提高分支覆盖率，但它们很少解释为什么某个配置有效、哪些配置是冗余的，或哪些设置会导致失败。
- 用户通常需要多个互补的配置来覆盖不同分支，而不只是一次得分高的运行。

## 方法
- Symetra 在调优运行之上加入了一个人机协同的可视界面。它将调优器视为黑箱，并将参数配置与分支覆盖率之间的关系可视化。
- 系统提供两个主要视图：用于展示参数对覆盖率数值影响的 Parameter View，以及用于展示不同试验之间覆盖模式相似性的 Coverage View。
- 在参数影响分析中，系统拟合一个 XGBoost 替代模型，并使用 SHAP 值估计每个参数及其参数取值对分支覆盖率的贡献，其中包括与默认值的比较。
- 在覆盖模式分析中，系统使用基于 Jaccard 相似度的 UMAP 对分支覆盖向量进行嵌入，让用户能够发现聚类、冗余情况和互补的试验组。
- 用户可以创建并比较试验组，查看合并后的覆盖增益，然后在下一轮实验前通过移除效果弱或容易失败的设置来缩小参数空间。

## 结果
- 论文称，使用 Symetra 的专家在分支覆盖率和调优效率上都优于完全自动化的调优方法。
- 文中报告了三种评估方式：案例研究、专家访谈，以及定量的人机协同调优过程。
- 摘录给出了调优设置的一些具体规模数据：在总共 148 个 KLEE 参数中纳入了 61 个，实验使用了几百到几千次试验，并且每次试验的时间上限为 2 分钟。
- 摘录中提到的基准程序包括 gawk（10,720 个分支）、gcal（15,799 个分支）和 grep（8,225 个分支）。
- 一个界面示例状态显示 gcal 有 2,200 次试验和 15,799 个分支；另一个示例显示 grep 有 2,200 次试验和 8,225 个分支。
- 摘录没有提供相对于自动化基线方法的实际定量提升数据，因此无法根据已提供文本报告确切的覆盖率或效率增益。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05349v1](http://arxiv.org/abs/2604.05349v1)
