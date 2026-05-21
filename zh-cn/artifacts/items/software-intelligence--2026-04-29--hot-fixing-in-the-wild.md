---
source: arxiv
url: https://arxiv.org/abs/2604.26892v1
published_at: '2026-04-29T17:01:01'
authors:
- Carol Hanna
- Karine Even-Mendoza
- W. B. Langdon
- "Mar Zamorano L\xF3pez"
- Justyna Petke
- Federica Sarro
topics:
- hot-fixing
- autonomous-coding-agents
- software-maintenance
- code-intelligence
- human-ai-collaboration
- empirical-software-engineering
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Hot Fixing in the Wild

## Summary
## 摘要
本文衡量 GitHub 热修复与常规错误修复的差异，以及自主编码代理在紧急修复中的行为。研究对象是 Hao-Li/AIDev 数据集中 61,000 多个仓库里与 issue 关联的 PR。

## 问题
- 热修复很重要，因为它们在时间压力下处理生产故障。团队可能会减少评审、测试和协作，以更快恢复服务。
- GitHub issue 标签给出的紧急程度和严重程度信号不一致，因此大规模热修复研究需要其他线索。
- 编码代理现在会在真实项目中提交 PR，但它们在紧急生产修复中的行为缺少直接测量。

## 方法
- 作者用三个本地 LLM 的单次提示来分类 GitHub issue 的严重程度：Llama 3.2、Qwen2.5-3B-Instruct 和 Phi-4-mini。
- 他们加入两个时间过滤条件：PR 必须在 issue 创建后 12 小时内打开，并且 PR 必须在 PR 创建后 24 小时内关闭。
- 四名评审者人工检查 20% 被 LLM 标记的热修复，必要时使用 issue 文本、PR 文本和仓库上下文。
- 研究在 AIDev 中关联 issue 和 PR，并比较热修复与常规错误修复的贡献者、提交、评审者、变更文件、变更行数、测试文件编辑和合并率。
- 作者按作者类型将热修复 PR 分为人类和 bot，并用词袋词云比较 PR 文本。

## 结果
- 时间过滤将 Llama3.2 的严重 issue 从 1,348 个减少到 269 个，Phi-4-mini 从 425 个减少到 105 个，Qwen 从 148 个减少到 33 个；仅凭紧急措辞会产生许多无法通过行动时间检查的候选项。
- 人工验证发现，LLM 与人工的总体一致度为 0.37；在抽样案例中，Qwen 与评审者完全一致，Phi-4-mini 的一致率约为 50%，Llama3.2 的不一致率为 49%。
- 热修复比常规修复更小。使用 Qwen 标签时，热修复 PR 平均有 2.7 次提交、3.9 个文件、25.7 行新增和 9.3 行删除；常规 PR 的平均值为 4.9 次提交、27.7 个文件、90 行新增和 54.4 行删除。
- 热修复涉及的人更少：热修复的贡献者为 1 到 5 人，常规修复为 1 到 13 人；热修复的评审者最多 5 人，常规修复最多 16 人。
- 热修复触及测试的频率低于常规修复：Qwen 标记的热修复中，29.73% 的 PR 包含测试；常规 PR 为 54.42%，差距为 24.69 个百分点。
- 热修复的合并率更高：Qwen 标记的热修复合并率为 70.27%，常规 PR 为 45.30%；bot 热修复合并率接近人类，例如在 Qwen 下为 66.67% 对 70.97%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26892v1](https://arxiv.org/abs/2604.26892v1)
