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
- llm-evaluation
- prompt-engineering
- software-engineering
relevance_score: 0.79
run_id: materialize-outputs
language_code: zh-CN
---

# Can ChatGPT Generate Realistic Synthetic System Requirement Specifications? Results of a Case Study

## Summary
本文研究在没有真实系统需求规格说明书（SyRS）和领域专家参与生成阶段的前提下，ChatGPT 能否生成“看起来真实”的合成 SyRS。结论是：可以在一定程度上做到，但仅靠 LLM 自评并不可靠，仍需要专家复核。

## Problem
- 真实 SyRS 对需求工程研究、测试生成和工具评测很重要，但常因保密、专有性和不可获得性而难以获取。
- 用黑盒 LLM 直接生成合成 SyRS 很有吸引力，因为不需要真实数据或额外训练，但会面临幻觉和过度自信，尤其是在专业领域文本中更危险。
- 核心问题是：在**没有真实样本、没有 RAG、没有领域专家参与生成**的条件下，ChatGPT 生成的合成需求文档是否足够真实，能否替代真实 SyRS 用于研究。

## Approach
- 作者设计了一个**迭代式生成-评估流程**：用 ChatGPT-4o 按模板生成文档，再用提示词评估“完整性”和“真实度（DoR）”，同时用 SBERT 衡量同一领域文档间的语义相似度，避免完全重复。
- 生成覆盖 **10 个行业领域**，经过 **10 轮迭代**，总共生成 **300 份 SSyRS**；每轮每个领域生成 3 份，最终选第十轮结果做重点分析和专家评估。
- 提示工程采用了简单但系统的方法：**zero-shot、template pattern、persona pattern、chain-of-thought**；并故意使用“scenario”而非“SyRS”来降低术语诱发的幻觉风险。
- 真实度评估不仅做了 ChatGPT 自评，还加入**跨模型检查**，比较 GPT-4o、GPT-5.2（instant / thinking）与 Sonnet 4.5，以测试上下文偏差和模型偏差。

## Results
- 最终数据集包含 **300 份**合成 SyRS；第十轮子集共 **30 份**，总计 **21,478 词**，单文档平均 **716 词**，范围 **644–811 词**。
- **完整性（Completeness）**：作者称所有 SSyRS 都通过模板完整性检查，即最终数据集的完整性结果为**全部有效**。
- **多样性/相似度**：SBERT 语义相似度总体均值 **0.66**、中位数 **0.67**、范围 **0.50–0.82**；最低领域均值为政府 **0.59**，最高为医疗 **0.73**。作者据此认为数据“相似但不冗余”。
- **专家评估**：基于 **33% 样本**开展问卷，收到 **n=87** 份提交（文中另处提到 **n=83 experts**）；其中 **62%** 的专家认为这些合成 SyRS 是现实可信的。
- **LLM 真实度评分差异很大**：按模型平均 DoR，GPT-4o（同上下文）**0.90**，GPT-4o（新上下文）**0.86**，GPT-5.2 instant **0.85**，GPT-5.2 thinking **0.73**，Sonnet 4.5 **0.64**。这说明**模型选择对评分影响远大于上下文影响**。
- **评分不稳定性明显**：同一份医疗 SSyRS 用 Sonnet 4.5 重复评估 **10 次**，DoR 从 **0.48 到 0.73**，跨度 **0.25**，均值 **0.59**，标准差 **0.08**。论文据此明确指出，**定量 DoR 评估高度不可靠**；深入检查还发现文本中存在**矛盾陈述和缺陷**。

## Link
- [http://arxiv.org/abs/2603.09335v1](http://arxiv.org/abs/2603.09335v1)
