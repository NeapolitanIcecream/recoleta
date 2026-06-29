---
source: arxiv
url: https://arxiv.org/abs/2606.25257v1
published_at: '2026-06-24T00:32:18'
authors:
- Gianmario Voria
- Alfonso Cannavale
- Andrea De Lucia
- Yutaro Kashiwa
- Gemma Catolino
- Fabio Palomba
topics:
- agent-context-files
- coding-agents
- code-quality
- software-maintenance
- empirical-software-engineering
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# How Do Developers Maintain and Evolve Their Agents' Instructions? An Empirical Study

## Summary
## 摘要
本文提出一项实证研究，考察开发者如何修改使用编码代理的代码库中的 Agent Context Files，例如 CLAUDE.md、AGENTS.md 和 copilot-instructions.md。研究把指令文件变更与后续代理生成代码的质量，以及代码库历史中的时间模式联系起来。

## 问题
- 自主编码代理需要项目特定指令，但开发者缺少证据来了解这些指令文件如何随时间变化。
- 维护不佳的 Agent Context Files 可能削弱对代理行为的控制，使意图更难追溯，并影响代码质量。
- 对于把代理指令当作有版本管理的工程制品，而不是一次性提示词的软件团队，这项研究有实际意义。

## 方法
- 研究挖掘两个数据集：AIDev，其中包含 116,211 个代码库和 932,791 个涉及代理生成代码的拉取请求；以及一个 ACF 数据集，其中包含来自 1,925 个代码库的 2,303 个上下文文件。
- 研究通过比较 CLAUDE.md、AGENTS.md 和 copilot-instructions.md 等文件的变更前后版本，在提交级别重建 Agent Context File 历史。
- 研究通过定性编码构建 ACF 变更分类法，然后把各类别映射到软件维护类型，例如纠正性、预防性、适应性、完善性和新增性变更。
- 研究定义相邻 ACF 修改提交之间的开发窗口，并在每个窗口中使用圈复杂度、代码行数、耦合度和 Corrective Commit Probability 衡量后续代理生成代码。
- 研究计划使用卡方检验分析类别分布，使用 Kruskal-Wallis 和 Wilcoxon 检验分析质量差异，使用 Cohen’s kappa 衡量标注一致性，并使用 Cliff’s Delta 衡量效应量。

## 结果
- 摘录报告的是研究设计，因此还没有关于 ACF 变更分布、代码质量影响或生命周期时间模式的完整实证结果。
- 可行性证据包括源 ACF 数据集中超过 10,000 个修改 ACF 的提交，可用于分类法工作。
- 初步流水线生成了 10,763 个包含上下文文件的提交快照、18,213 个带文件元数据的提交，以及 8,600 个同时包含 ACF 和代理代码信息的提交。
- 定性分类法的大规模标注前，计划采用的一致性阈值是 Cohen’s kappa ≥ 0.70。
- 论文引用的既有输入数据包括覆盖 1,925 个代码库的 2,303 个 ACF，以及 AIDev 的 116,211 个代码库和 932,791 个拉取请求，但论文尚未声称已测得 ACF 变更带来的代码质量提升或下降。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.25257v1](https://arxiv.org/abs/2606.25257v1)
