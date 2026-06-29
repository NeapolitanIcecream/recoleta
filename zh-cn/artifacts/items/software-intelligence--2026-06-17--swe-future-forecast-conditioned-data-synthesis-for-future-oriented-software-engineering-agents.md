---
source: arxiv
url: https://arxiv.org/abs/2606.18733v1
published_at: '2026-06-17T06:22:28'
authors:
- Qiao Zhao
- JianYing Qu
- Jun Zhang
- Yehua Yang
- Hanwen Du
- Zhongkai Sun
topics:
- software-engineering-agents
- code-agent-benchmarks
- synthetic-data-generation
- benchmark-contamination
- software-evolution
- multi-agent-task-construction
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# SWE-Future: Forecast-Conditioned Data Synthesis for Future-Oriented Software Engineering Agents

## Summary
## 摘要
SWE-Future 先预测代码仓库未来可能出现的工作，再用经过验证的预测任务族合成可执行的编码智能体任务。它保留 GitHub 仓库任务的真实感，同时减少对公开 pull request 的直接重放。

## 问题
- 许多编码智能体基准会重放公开的 GitHub issue 和 pull request；当这些材料进入预训练、微调、合成数据或基准选择流程时，会带来污染风险。
- 完全合成的任务可以避免直接重放，但可能偏离真实仓库需求、项目约定、依赖限制和维护者优先级。
- 论文的目标是为软件工程智能体构建面向未来的真实任务，同时不把后续 pull request 变成任务提示或参考解法。

## 方法
- 对每个仓库，SWE-Future 使用 forecast snapshot T0 之前可见的 issue、pull request、标签、标题和短文本构建证据包。
- 它把 T0 之前反复出现的信号聚类为任务族，覆盖功能实现或增强、bug 修复和重构。每个任务族会给出锚点、预期行为、证据引用、目标提示和验收标准。
- 它先冻结这些预测，再在六个月验证窗口内用后续 pull-request 元数据进行检查。评审者看不到补丁。
- 在 task-generation snapshot Tgen，经过验证的任务族作为条件信号用于任务合成。一个多智能体构建循环会编写公开 issue、设计测试、编写标准补丁，并验证可执行行为。
- 发布的任务会暴露仓库快照和 issue 风格请求。测试、标准补丁、验证标签、来源信息和执行日志保持隐藏。

## 结果
- 在一项覆盖 80 个仓库的回顾性研究中，预测器在 76 个仓库中生成了 260 个任务族：139 个 bug 修复任务族、93 个功能/增强任务族和 28 个重构任务族。
- 主要的未来工作相关性结果为 151/260 个任务族，即 58.1%；这些任务族与 T0 之后的 pull-request 元数据存在强语义匹配或相关语义匹配。
- 更严格的强匹配率为 111/260，即 42.7%。
- bug 修复预测表现最好：139 个 bug 修复任务族中有 89 个被判定为强匹配或相关匹配。功能/增强预测中，93 个任务族有 45 个强匹配或相关匹配。
- 一项独立语义审计在 216/260 个案例中与主要的“相关或拒绝”判定一致，即 83.1%。
- 最终数据集包含 61 个仓库中的 200 个合成可执行任务：120 个 bug 修复任务、60 个功能/增强任务和 20 个重构任务。其中，160 个任务以强预测匹配为条件，40 个任务以相关预测匹配为条件。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.18733v1](https://arxiv.org/abs/2606.18733v1)
