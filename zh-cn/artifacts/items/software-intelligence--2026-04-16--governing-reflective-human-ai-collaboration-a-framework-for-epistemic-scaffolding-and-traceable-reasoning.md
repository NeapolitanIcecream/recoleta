---
source: arxiv
url: http://arxiv.org/abs/2604.14898v1
published_at: '2026-04-16T11:42:36'
authors:
- Rikard Rosenbacke
- Carl Rosenbacke
- Victor Rosenbacke
- Martin McKee
topics:
- human-ai-collaboration
- traceable-reasoning
- epistemic-scaffolding
- ai-governance
- llm-evaluation
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Governing Reflective Human-AI Collaboration: A Framework for Epistemic Scaffolding and Traceable Reasoning

## Summary
## 摘要
本文认为，可靠的人机协作推理应由交互层来治理，而不应被视为模型本身的属性。文中提出 **The Architect’s Pen**，一种结构化对话方法，用来让反思、证伪和修订过程变得可见且可审计。

## 问题
- 当前大语言模型可以生成流畅语言，但没有具身理解、因果锚定或稳定的反思性推理，所以用户可能把看似合理的文本误当成有依据的结论。
- 现有安全工作主要关注模型内部，而许多失败发生在人机循环中：错误确认、幻觉持续、对不确定性的处理薄弱，以及责任分散。
- 这在医学、法律、教育和研究等受监管领域尤其重要，因为这些场景中的决策需要可追踪的推理和可审计性，并要满足欧盟 AI 法案、OECD 原则、NIST AI RMF 和 ISO/IEC 42001 等标准。

## 方法
- 论文把推理定义为人机交互中的可观察过程：主张被外化、受到挑战、被修订，并与证据或领域约束相连。
- 其核心机制是 **The Architect’s Pen**：一个反思循环，包含 **人类抽象 → 模型表述 → 人类反思**。模型负责起草和扩展想法；人类负责检验、证伪和修订。
- 接口增加了 **认识论支架** 和 **认识论摩擦**，例如不确定性标记、反例、比较提示和修订步骤，用来降低对流畅输出的盲目接受。
- 该方法不需要重新训练或新的模型架构。论文把它描述为一种可应用于当前 LLM 系统的交互和治理协议。
- 论文还提出了可测量的评估目标，包括错误确认率、置信度-准确性校准、幻觉持续性、假设多样性、纵向一致性，以及一个拟议的 **System-2 Engagement Score**。

## 结果
- 这段摘录**没有**报告实证基准结果、数据集分数或正面对比的定量比较。
- 它声称该框架可以在现有 LLM 上**无需重新训练**或新的技术突破就实现，因为干预发生在界面层。
- 文中提出了 **6 个可检验假设**，并给出预期方向：错误确认**下降**、置信度-准确性校准**上升**、纵向推理一致性**上升**、幻觉持续性**下降**、假设多样性**上升**，以及 System-2 Engagement Score 与专家评分的决策质量之间的相关性**上升**。
- 这段摘录中最具体的贡献，是一个面向治理的评估设计：将标准聊天会话与使用 The Architect’s Pen 的处理组会话进行比较，并测量对看似合理但错误输出的接受度、重复错误主张、推理分支数量，以及置信度与准确性的一致性。
- 论文主张的进展是概念和流程层面的，而不是实证层面的：它把“推理”从模型内部移到一个可追踪的人机协议中，目的是支持可审计性和合规性。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.14898v1](http://arxiv.org/abs/2604.14898v1)
