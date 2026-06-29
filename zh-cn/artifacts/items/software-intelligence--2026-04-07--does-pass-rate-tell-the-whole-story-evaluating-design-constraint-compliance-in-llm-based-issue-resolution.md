---
source: arxiv
url: http://arxiv.org/abs/2604.05955v1
published_at: '2026-04-07T14:47:27'
authors:
- Kai Yu
- Zhenhao Zhou
- Junhao Zeng
- Ying Wang
- Xueying Du
- Zhiqiang Yuan
- Junwei Liu
- Ziyu Zhou
- Yujia Wang
- Chong Wang
- Xin Peng
topics:
- llm-agents
- issue-resolution
- benchmarking
- design-constraints
- code-review-mining
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Does Pass Rate Tell the Whole Story? Evaluating Design Constraint Compliance in LLM-based Issue Resolution

## Summary
## 摘要
这篇论文认为，在基于 LLM 的问题修复任务中，测试通过率遗漏了补丁质量的很大一部分。它提出了 SWE-Shield，这是一个基准，用来衡量生成的补丁是否遵守从真实 pull request 中挖掘出的项目特定设计约束。

## 问题
- 现有的问题修复基准主要按测试通过率给补丁评分，但被接受的补丁还需要遵守项目设计约束，例如架构选择、错误处理、API 一致性和可维护性规则。
- 这些约束很多没有写进测试里，只是在 pull request 评审讨论中被暗示出来，所以一个通过测试的补丁在真实开发中仍可能不可接受。
- 如果没有办法提取、关联和验证这些约束，当前基准分数就会高估 LLM 代理在真实代码仓库工作中的实用性。

## 方法
- 论文构建了 **SWE-Shield**，这是一个面向设计的基准，与 SWE-bench-Verified 和 SWE-bench-Pro 对齐，覆盖 **495 个 issues**、**1,787 条已验证约束**、**6 个仓库**，以及在验证前提取出的 **10,885 条约束**。
- 它提出了 **DesignHunter**，一个两阶段的 LLM 流程：先从代码审查线程中提取原子级设计建议，再把这些建议分组并综合成结构化设计约束，包含问题、选项、条件和参考代码。
- 为了把约束和 issues 关联起来，这个流程使用显式追踪和语义匹配，然后再进行人工验证。
- 在评估时，它增加了一个 **基于 LLM 的验证器**，检查生成的补丁是否满足关联的设计约束，因为这些约束不能直接执行，而且通常依赖上下文。

## 结果
- 在 **SWE-Shield-verified** 上，代理的 **通过率** 达到 **70.25%–75.95%**，但 **设计满足率（DSR）** 只有 **32.64%–50.20%**。
- 在 **SWE-Shield-pro** 上，**通过率** 达到 **42.69%**，但设计违规仍然很高，**设计违规率（DVR）** 最高达到 **45.85%**。
- 在大多数设置中，功能正确性和设计符合性之间几乎没有统计关系：**Cramér’s V ≤ 0.11**，论文还报告了大多数卡方检验没有显著关联。
- 在 **swe-agent** 的相同设置下，基础模型在 **SWE-Shield-pro** 上的 DSR 只变化了 **12 个百分点**，即使通过率差异更大，这说明很多设计失败是各模型共有的。
- 加入针对单个 issue 的设计指导会减少违规，**DVR 最多下降 6.35 个百分点**，但剩余违规率仍然保持在 **30% 以上**。
- 主要结论是，基于测试的评估明显高估了补丁质量，因为在很多设置里，完全满足设计要求的已解决 issues 不到一半。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05955v1](http://arxiv.org/abs/2604.05955v1)
