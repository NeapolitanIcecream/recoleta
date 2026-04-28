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
本文认为，可靠的人机推理应在交互层治理，而不应只被看作模型本身的属性。文章提出 **The Architect’s Pen**，一种结构化对话方法，使反思、证伪和修订变得可见且可审计。

## 问题
- 当前的 LLM 能生成流畅语言，但没有具身理解、因果锚定或稳定的反思性推理，因此用户可能把看似合理的文本误当成有根据的结论。
- 现有安全工作主要关注模型内部，而许多失败发生在人机回路中：错误确认、幻觉持续、对不确定性的处理薄弱，以及责任归属失效。
- 这在医疗、法律、教育和研究等受监管领域尤为重要，因为这些场景中的决策需要可追溯的推理和可审计性，以满足 EU AI Act、OECD principles、NIST AI RMF 和 ISO/IEC 42001 等标准。

## 方法
- 论文将推理定义为发生在人机交互中的可观察过程：主张被外化、被质疑、被修订，并与证据或领域约束相连接。
- 其核心机制是 **The Architect’s Pen**：一个由 **human abstraction → model articulation → human reflection** 组成的反思循环。模型负责起草并展开想法；人类负责检验、证伪并修订这些想法。
- 界面加入了 **epistemic scaffolding** 和 **epistemic friction**，例如不确定性标注、反例、对比提示和修订步骤，以减缓用户对流畅输出的盲目接受。
- 该方法不需要重新训练，也不需要新的模型架构。论文将其表述为一种可应用于当前 LLM 系统的交互与治理协议。
- 论文还提出了可测量的评估目标，包括错误确认率、置信度-准确率校准、幻觉持续性、假设多样性、长期一致性，以及一个提出中的 **System-2 Engagement Score**。

## 结果
- 这段摘录**没有**报告经验基准结果、数据集分数或面对面的量化比较。
- 文中称，该框架可以在现有 LLM 上实现，**无需重新训练**，也不需要新的技术突破，因为干预发生在界面层。
- 文中提出了 **6 个可检验假设** 及其预期方向性效果：错误确认**下降**、置信度-准确率校准**上升**、长期推理一致性**上升**、幻觉持续性**下降**、假设多样性**上升**，以及 System-2 Engagement Score 与专家评分的决策质量之间的相关性**上升**。
- 这段摘录中最具体的贡献是一个面向治理的评估设计：将标准聊天会话与使用 The Architect’s Pen 的处理组会话进行比较，并测量用户对“看似合理但实际错误”的输出的接受率、重复错误主张的情况、推理分支数量，以及置信度与准确率的一致程度。
- 论文声称的进展主要是概念和流程层面的，而非经验层面的：它将“推理”从模型内部转移到一个可追溯的人机协议上，目标是支持可审计性和合规。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.14898v1](http://arxiv.org/abs/2604.14898v1)
