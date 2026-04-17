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
这篇论文认为，在基于 LLM 的问题修复任务中，仅看测试通过率会漏掉补丁质量中的很大一部分。论文提出了 SWE-Shield，这是一个衡量生成补丁是否遵守从真实 pull request 中挖掘出的项目特定设计约束的基准。

## 问题
- 现有的问题修复基准主要用测试通过率给补丁打分，但被接受的补丁还需要遵守项目的设计约束，例如架构选择、错误处理、API 一致性和可维护性规则。
- 这些约束很多都没有编码进测试里，只是在 pull request 的评审讨论中被隐含提到，因此，一个通过测试的补丁在真实开发中仍然可能无法被接受。
- 如果没有办法提取、关联并验证这些约束，当前基准分数就会高估 LLM agent 在真实仓库工作中的实际价值。

## 方法
- 论文构建了 **SWE-Shield**，这是一个与 SWE-bench-Verified 和 SWE-bench-Pro 对齐、具备设计感知能力的基准，覆盖 **495 个问题**、**1,787 条已验证约束**、**6 个仓库**，以及验证前提取出的 **10,885 条约束**。
- 论文提出了 **DesignHunter**，一个两阶段的 LLM 流水线：先从代码评审线程中提取原子化的设计建议，再将它们分组并整合成结构化设计约束，其中包含问题、选项、条件和参考代码。
- 为了把约束关联到具体问题，这个流水线结合了显式可追溯性和语义匹配，并在之后进行人工验证。
- 在评估阶段，论文加入了一个**基于 LLM 的验证器**，用于检查生成补丁是否满足已关联的设计约束，因为这些约束不可执行，而且通常依赖具体上下文。

## 结果
- 在 **SWE-Shield-verified** 上，agent 的 **Pass Rate** 达到 **70.25%–75.95%**，但**设计满足率（DSR）**只有 **32.64%–50.20%**。
- 在 **SWE-Shield-pro** 上，**Pass Rate** 达到 **42.69%**，但设计违规仍然很多，**设计违规率（DVR）**最高达到 **45.85%**。
- 在大多数设置中，功能正确性与设计合规性之间几乎没有统计关系：**Cramér’s V ≤ 0.11**，而且论文报告称，大多数卡方检验都没有发现显著关联。
- 在 **SWE-Shield-pro** 上，使用相同 **swe-agent** 设置比较不同基础模型时，即使 **Pass Rate** 的差异更大，**DSR** 也只变化了 **12 个百分点**，这说明许多设计失败是不同模型共同存在的问题。
- 加入针对具体问题的设计指导后，违规情况有所下降，**DVR** 最多降低 **6.35 个百分点**，但剩余违规率仍然**高于 30%**。
- 论文的核心结论是，基于测试的评估会明显高估补丁质量，因为在很多设置下，得到解决的问题中，完全满足设计要求的还不到一半。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05955v1](http://arxiv.org/abs/2604.05955v1)
