---
source: arxiv
url: http://arxiv.org/abs/2603.12226v1
published_at: '2026-03-12T17:48:34'
authors:
- Priyanka Kargupta
- Shuhaib Mehri
- Dilek Hakkani-Tur
- Jiawei Han
topics:
- scientific-discovery
- llm-ideation
- interdisciplinary-research
- retrieval-augmented-generation
- human-ai-collaboration
relevance_score: 0.08
run_id: materialize-outputs
---

# Sparking Scientific Creativity via LLM-Driven Interdisciplinary Inspiration

## Summary
Idea-Catalyst 是一个面向科研头脑风暴阶段的 LLM 驱动框架，用于系统性挖掘跨学科灵感，而不是直接自动化实验或快速收敛到单一方案。它通过分解目标问题、定位目标领域未解挑战、再从外部学科检索类比性见解，来生成更有新颖性且仍与原问题紧密相关的研究想法。

## Problem
- 论文解决的是：如何帮助研究者和 LLM 在科研早期产生**有根据的跨学科创意**，突破单一学科信息茧房。
- 这很重要，因为跨学科研究通常带来更高长期影响；文中称每增加一个学科，引用影响约提升 **20%**，但真正高投入的远距离跨学科合作仅约 **5%**。
- 现有 AI 科学发现方法常过早转向实验执行与可行性筛选，导致想法更偏增量、单领域，削弱创造性探索。

## Approach
- 输入只需要一个简短研究目标；系统先把它拆成若干**核心研究问题**，并分别用目标领域文献分析这些问题已经解决到什么程度。
- 对尚未解决的难点，系统把它们从“领域术语”改写成**领域无关的概念问题**，例如把特定 AI 协作问题抽象成“何时应控制、何时应让渡控制”。
- 然后它去较远的外部学科中检索是否存在处理相似概念问题的机制、理论或经验规律，并提取文献支持的关键洞见。
- 最后把这些外部洞见**重新语境化**回目标领域，形成候选 idea fragments，并按“跨学科潜力”排序，平衡新颖性与相关性。
- 核心机制可用最简单的话概括为：**先找清楚本领域卡在哪里，再去别的学科找“同类问题的解法”，最后翻译回来形成新想法。**

## Results
- 文中声称，Idea-Catalyst 在实证评估中将平均**novelty 提升 21%**。
- 同时将平均**insightfulness 提升 16%**。
- 在贡献总结中给出更精确数字：比对基线/对照后，生成的想法平均**新颖性提高 21.38%**、**洞察性提高 16.22%**。
- 论文还强调这些提升是在“**仍然 grounded in the original research problem**”的前提下获得的，即没有为了跨学科而偏离原始任务。
- 摘要与节选中未提供更细的量化细节，如具体数据集规模、评测样本数、所用基线名称或显著性检验结果。

## Link
- [http://arxiv.org/abs/2603.12226v1](http://arxiv.org/abs/2603.12226v1)
