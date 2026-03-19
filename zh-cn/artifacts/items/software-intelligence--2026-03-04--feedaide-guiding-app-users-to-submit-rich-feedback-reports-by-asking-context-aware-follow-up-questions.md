---
source: arxiv
url: http://arxiv.org/abs/2603.04244v1
published_at: '2026-03-04T16:31:55'
authors:
- Ali Ebrahimi Pourasad
- Meyssam Saghiri
- Walid Maalej
topics:
- user-feedback
- multimodal-llm
- mobile-apps
- requirements-engineering
- human-ai-interaction
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# FeedAIde: Guiding App Users to Submit Rich Feedback Reports by Asking Context-Aware Follow-Up Questions

## Summary
FeedAIde 是一个面向移动应用反馈收集的上下文感知交互式框架，用多模态大模型在用户提交反馈时主动追问关键信息。它试图同时降低用户表达门槛，并让开发者拿到更完整、更可执行的缺陷与需求报告。

## Problem
- 移动应用用户常提交**含糊、缺少上下文**的反馈，而开发者需要的是可复现、可判断优先级的详细信息。
- 这种信息落差会导致开发者反复追问；文中指出约 **45%** 的开发者回复是在索要更多细节，而很多用户**不会再回复**或需要**数小时到数天**才补充。
- 现有用户侧反馈方式多是简单文本框，缺少对**截图、设备信息、交互日志**等上下文的即时利用，因而反馈质量低、处理成本高。

## Approach
- 提出 **FeedAIde**：当用户触发反馈时，系统自动收集上下文，包括**截图、设备信息、应用版本、近期交互日志**等。
- 使用 **多模态大语言模型（MLLM）**先根据上下文生成最多 **3 个**用户可能想表达的反馈选项，用户可直接选择或自行输入。
- 在用户选择后，模型再提出**固定 2 个**简短、上下文相关的追问，补齐开发者最需要的信息，同时避免技术性过强或问题过长。
- 最终将用户回答与上下文整合成结构化 JSON 报告，包含**userIntentSummary**、**developerSummary**、问答历史和上下文数据，便于开发者消费。
- 作者实现了一个可集成到 iOS 应用中的 **Swift Package**，支持 shake-to-report，并通过提示工程控制语言、问题形式、隐私与上下文裁剪。

## Results
- 在一个真实健身房内部 iOS 应用上进行了评估：**7 名**真实用户、**4 个**反馈场景（**2 个 bug + 2 个 feature request**）、被收集并评审的报告共 **54 份**。
- 与原有简单文本表单相比，参与者主观上认为 **FeedAIde 更容易使用、也更有帮助**；摘要未给出具体 Likert 均值或显著性检验数值。
- 由 **2 名行业专家**对 **54 份**报告进行质量评估，结论是 FeedAIde 提升了**bug report**和**feature request**两类报告的质量，尤其是**完整性（completeness）**。
- 论文未在给定摘录中报告更细的量化指标（如平均分、效应量、p 值）；最强的具体结论是：相较传统文本框，FeedAIde 产出的报告被专家认为**更高质量、更完整**。
- 作者也指出局限：系统仍可改进，例如让追问更多挖掘**根因**，而不是过度围绕用户提出的表面解决方案展开。

## Link
- [http://arxiv.org/abs/2603.04244v1](http://arxiv.org/abs/2603.04244v1)
