---
source: arxiv
url: https://arxiv.org/abs/2607.13285v1
published_at: '2026-07-14T21:39:55'
authors:
- Ruhan Wang
- Yucheng Shi
- Zongxia Li
- Zhongzhi Li
- Yue Yu
- Junyao Yang
- Kishan Panaganti
- Haitao Mi
- Dongruo Zhou
- Leoweiliang
topics:
- code-intelligence
- automated-software-production
- agent-harness
- behavior-localization
- repository-understanding
- coding-agents
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Harness Handbook: Making Evolving Agent Harnesses Readable,Navigable, and Editable

## Summary
## 摘要
Harness Handbook 按运行时行为表示智能体 harness，并将每种行为关联到源代码位置。在 Codex 和 Terminus-2 上的评估中，借助手册进行规划提高了规划质量和定位准确性，同时减少了规划器使用的 token 数量。

## 问题
- 修改请求描述的是期望行为，而生产环境中的 harness 将这些行为分散实现于多个文件、执行阶段、函数和共享状态中。
- 在规划安全修改之前，人类和编程智能体必须定位所有受影响的实现位置；但现有的代码仓库映射、搜索、索引和长上下文方法仍围绕代码结构组织，而不是围绕行为组织。
- 定位缺失或不完整可能导致智能体遗漏分散在多个模块中、跨模块或很少执行的路径，从而生成不完整或范围过大的修改计划。

## 方法
- Harness Handbook 构建以行为为中心的表示，并采用 L1–L3 层级：系统概览、组件或阶段概览，以及关联源代码的实现细节。配套的状态寄存器视图记录跨阶段依赖关系。
- 构建流程结合确定性的静态事实提取、调用图分析、LLM 辅助的行为组织和分层综合，并支持以函数或文件作为叶节点的表示方式。
- Behavior-Guided Progressive Disclosure（BGPD）从相关阶段导航至与状态关联的组件和源代码位置，通过调用关系扩展候选位置，并根据当前代码仓库验证每个定位结果。
- 修改完成后，非空差异会触发重新同步，使变更后的函数或文件、程序图和手册条目与代码仓库保持一致；对于不确定的内容，系统会将其冻结或记录，而不是进行猜测。

## 结果
- 在两个开源 harness 上分别提出 30 个请求的评估中，Handbook-Assisted 规划的总体评审胜率高于 Baseline：Codex 上为 38.3%，对比 28.3%；Terminus-2 上为 45.6%，对比 26.7%。
- Codex 请求的平均规划器使用量从 0.102M token 降至 0.089M，减少 12.7%；Terminus-2 请求则从 0.058M token 降至 0.053M，减少 8.6%。
- 以三位评审的结果取平均后，Codex 上 Localization、Scope Control 和 Reasoning 的胜率分别提高 2.2、1.1 和 3.3 个百分点；Terminus-2 上分别提高 12.2、6.7 和 4.5 个百分点。
- 在 Codex 上与 Opus 4.8 参考计划对比时，手册指导使文件级 F1 从 46.6 提高到 61.8，使符号级 F1 从 38.3 提高到 57.1；相应的 Wrong 率分别从 37.0% 降至 14.8%，以及从 44.4% 降至 18.5%。
- 在 Codex 上与 GPT-5.5 参考计划对比时，手册指导使文件级 F1 从 47.3 提高到 52.3，使符号级 F1 从 43.8 提高到 51.2；符号级 Wrong 率从 28.6% 降至 21.4%。
- 所提供的摘录截断了 Terminus-2 定位表的剩余部分，因此这里无法获得论文报告的完整比较数值。论文称，在 Query、Cross-file 和 Search-Hostile 请求以及不同的定位难度等级下，改进仍然存在。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.13285v1](https://arxiv.org/abs/2607.13285v1)
