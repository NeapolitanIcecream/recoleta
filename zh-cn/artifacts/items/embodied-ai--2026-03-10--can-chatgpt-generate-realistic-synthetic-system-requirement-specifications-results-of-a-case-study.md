---
source: arxiv
url: http://arxiv.org/abs/2603.09335v1
published_at: '2026-03-10T08:10:56'
authors:
- Alex R. Mattukat
- Florian M. Braun
- Horst Lichter
topics:
- requirements-engineering
- synthetic-data
- large-language-models
- prompt-engineering
- quality-evaluation
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# Can ChatGPT Generate Realistic Synthetic System Requirement Specifications? Results of a Case Study

## Summary
这篇论文研究在**没有真实系统需求规格说明书（SyRS）和不依赖领域专家参与生成过程**的条件下，是否能用 ChatGPT 生成“看起来真实”的合成需求文档。结论是：**可以在一定程度上做到**，但基于 LLM 的自动质量评估明显不稳定，**仍不能替代专家审查**。

## Problem
- 论文要解决的问题是：真实 **SyRS** 对软件工程研究很有价值，但往往因**保密、专有性和获取困难**而无法公开，导致数据稀缺。
- 如果能生成足够真实的**合成 SyRS（SSyRS）**，就能支持需求工程中的方法开发、工具评测、测试生成和基准构建。
- 难点在于黑盒 LLM（如 ChatGPT）容易**幻觉**和**过度自信**，尤其在专业领域文本生成中，可能写出貌似合理但实际矛盾或错误的需求。

## Approach
- 作者设计了一个**迭代式生成—评估—改写提示词**流程，用 ChatGPT-4o 在 **10 个行业**中生成 SSyRS，并经过 **10 轮迭代**最终得到 **300 份**文档。
- 生成时使用了简化的 **ISO/IEC/IEEE 29148** 风格模板，并结合 **zero-shot、template、persona、chain-of-thought** 等提示模式，让模型按统一结构写需求文档。
- 他们定义了三个质量属性：**Completeness**（模板是否完整）、**Degree of Realism / DoR**（与真实 SyRS 的相似真实性）、**Semantic Similarity**（同一领域内不同文档的语义重合度，避免完全重复）。
- Completeness 和 DoR 主要由 LLM 提示评估；Semantic Similarity 则用 **SBERT all-mpnet-base-v2** 计算，以降低幻觉影响。
- 为检验自动评分可靠性，作者还做了**跨模型验证**，比较 **GPT-4o、GPT-5.2（instant / thinking）和 Sonnet 4.5** 对 DoR 的打分差异，并辅以专家问卷研究。

## Results
- 最终数据集包含 **300 份 SSyRS**，覆盖 **10 个行业**；第 10 轮数据集共有 **21,478 词**，单篇平均 **716 词**，中位数 **719 词**，最短 **644**、最长 **811**。
- **Completeness** 结果最强：作者称**所有 SSyRS 都通过了完整性检查**，即模板要求的元素都被包含。
- **Semantic Similarity** 整体均值为 **0.66**、中位数 **0.67**、范围 **0.50–0.82**；按领域均值从 **0.59（government）** 到 **0.73（healthcare）**，说明文档彼此相关但不完全冗余。
- 专家研究共收到 **n=87** 份提交（文中也提到 **n=83 experts**），其中 **62% 的专家**认为这些合成需求文档是**现实可信的**。
- 但 **DoR 自动评分非常不稳定且模型相关性强**：按模型平均值，**GPT-4o same-context = 0.90**，**GPT-4o new-context = 0.86**，**GPT-5.2 instant = 0.85**，**GPT-5.2 thinking = 0.73**，**Sonnet 4.5 = 0.64**。这表明模型选择对“真实性评分”的影响远大于上下文差异。
- 在 Sonnet 4.5 的重复测试中，同一份 healthcare 文档的 DoR 从 **0.48 到 0.73**，跨度 **0.25**，平均 **0.59**、标准差 **0.08**；作者据此明确指出**定量 DoR 评估高度不可靠**。此外，深入检查还发现文档存在**自相矛盾和内容缺陷**，因此论文的核心结论不是“LLM 已能可靠替代真实需求文档”，而是“**能部分生成逼真的合成需求，但自动评估不足以替代专家评审**”。

## Link
- [http://arxiv.org/abs/2603.09335v1](http://arxiv.org/abs/2603.09335v1)
