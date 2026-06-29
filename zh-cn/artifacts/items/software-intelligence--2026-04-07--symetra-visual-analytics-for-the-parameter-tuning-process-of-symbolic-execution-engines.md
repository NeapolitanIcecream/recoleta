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
Symetra 是一个视觉分析系统，用于在人工指导下调优像 KLEE 这样的符号执行引擎。它帮助用户查看哪些参数设置会影响分支覆盖率，找出互补的配置，并为后续调优运行收窄搜索空间。

## 问题
- 符号执行引擎暴露了许多可调参数，它们之间的交互很难理解，所以用户常常退回到默认设置，错过覆盖率。
- 自动调参器可以提升分支覆盖率，但它们很少说明为什么某个配置有效、哪些配置是冗余的，或者哪些设置会导致失败。
- 用户往往需要几个互补的配置来覆盖不同分支，而不只是一个得分最高的运行结果。

## 方法
- Symetra 在调参运行之上增加了一个人机协同的可视化界面。它把调参器当作黑盒，并可视化参数配置与分支覆盖率之间的关系。
- 系统提供两个主要概览：Parameter View 用于查看参数对覆盖率数值的影响，Coverage View 用于查看不同试验之间覆盖模式的相似性。
- 在参数影响上，它拟合了一个 XGBoost 代理模型，并使用 SHAP 值估计每个参数和参数取值对分支覆盖率的贡献，包括与默认值的比较。
- 在覆盖模式上，它使用 Jaccard 相似度结合 UMAP 对分支覆盖向量做嵌入，这样用户可以发现聚类、冗余和互补的试验组。
- 用户可以创建并比较试验组，查看合并后的覆盖增益，然后在下一轮实验前通过移除弱配置或容易失败的设置来收窄参数空间。

## 结果
- 论文声称，使用 Symetra 的专家在分支覆盖率和调优效率上都优于全自动调优。
- 文中报告了三种评估方式：案例研究、专家访谈，以及一个定量的人机协同调优过程。
- 摘要给出了调优设置的具体规模：在 148 个参数中纳入了 61 个 KLEE 参数，实验使用了几百到几千次试验，每次试验上限为 2 分钟。
- 摘要中提到的基准程序是 gawk，10,720 个分支；gcal，15,799 个分支；以及 grep，8,225 个分支。
- 一个界面状态示例显示 gcal 有 2,200 次试验和 15,799 个分支；另一个示例显示 grep 有 2,200 次试验和 8,225 个分支。
- 摘要没有给出相对于自动化基线的具体定量提升数字，因此无法根据所提供文本报告准确的覆盖率或效率增益。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05349v1](http://arxiv.org/abs/2604.05349v1)
