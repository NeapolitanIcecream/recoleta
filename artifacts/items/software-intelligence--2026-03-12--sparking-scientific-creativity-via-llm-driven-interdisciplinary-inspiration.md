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
- llm-scientific-discovery
- interdisciplinary-ideation
- creativity-support
- retrieval-augmented-generation
- human-ai-collaboration
relevance_score: 0.72
run_id: materialize-outputs
---

# Sparking Scientific Creativity via LLM-Driven Interdisciplinary Inspiration

## Summary
这篇论文提出 **Idea-Catalyst**，一个用大语言模型辅助跨学科科研头脑风暴的框架，目标是在过早收敛到具体方案之前，系统性地引入外部学科的可迁移洞见。它强调增强人类和LLM的创造性推理过程，而不是直接自动化整条科学发现流水线。

## Problem
- 论文要解决的是：科研创新常被困在单一学科“信息孤岛”中，而真正高影响力的突破往往来自跨学科综合。
- 现有AI科研系统多数偏向“快速出方案+做实验”，容易过早锚定、压缩探索空间，削弱创意形成阶段的跨域发散能力。
- 这很重要，因为跨学科研究通常有更高长期影响，但真正深入、远距离学科间的高参与协作仅占约 **5%**，说明研究者很难系统找到“哪个外部领域的什么思想”值得借用。

## Approach
- **核心机制**：先把一个抽象研究目标拆成若干核心研究问题，再分析目标领域文献，找出哪些问题已解决、部分解决或仍开放。
- 对尚未解决的难点，系统把它们改写成**领域无关的概念问题**，例如把具体AI问题抽象成“何时应行使控制，何时应克制控制”。
- 然后到较远的外部学科中检索与这些抽象问题相似的机制、理论或经验规律，提取文献支持的概念性洞见。
- 最后把这些外部洞见重新翻译回目标领域语境，生成候选“idea fragments”，并按其跨学科潜力、相关性与影响力进行排序。
- 实现上，它基于 Semantic Scholar Snippets 做文献片段检索，并以“元认知”原则组织流程：自我认知、情境认知、策略选择、目标管理和评估。

## Results
- 论文声称，Idea-Catalyst 在实验中使生成想法的平均**新颖性提升 21%**。
- 同时，平均**insightfulness（洞察性）提升 16%**，且仍保持与原始研究问题的紧密关联。
- 在贡献列表中，作者给出更精确的数字：通过 **LLM 评估与人工评估**，系统产生的想法**新颖性提高 21.38%**、**洞察性提高 16.22%**。
- 文中还引用背景统计：每增加一个学科，引用影响大约提升 **20%**；但深度跨域合作在跨学科研究中仅约 **5%**，用于说明问题的重要性，而非该方法本身的性能指标。
- 摘要与节选中未提供更细的评测设置细节，如具体数据集规模、对比基线名称、方差/显著性等。

## Link
- [http://arxiv.org/abs/2603.12226v1](http://arxiv.org/abs/2603.12226v1)
