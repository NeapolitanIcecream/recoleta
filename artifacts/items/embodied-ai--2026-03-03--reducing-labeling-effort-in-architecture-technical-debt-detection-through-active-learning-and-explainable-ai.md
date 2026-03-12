---
source: arxiv
url: http://arxiv.org/abs/2603.02944v1
published_at: '2026-03-03T12:51:54'
authors:
- Edi Sutoyo
- Paris Avgeriou
- Andrea Capiluppi
topics:
- technical-debt-detection
- architecture-technical-debt
- active-learning
- explainable-ai
- issue-tracking
- satd
relevance_score: 0.01
run_id: materialize-outputs
---

# Reducing Labeling Effort in Architecture Technical Debt Detection through Active Learning and Explainable AI

## Summary
本文研究如何在检测 Jira 问题单中的架构技术债（ATD）时，减少昂贵的专家标注工作，并让模型输出更易理解。作者结合关键词过滤、主动学习和可解释 AI，构建了一个更高效且更透明的 ATD 检测流程。

## Problem
- 架构技术债比一般技术债更抽象、更依赖上下文，因此很难从 issue 文本中自动识别。
- 高质量 ATD 标注数据稀缺，且专家人工标注成本高、耗时长，限制了可扩展性。
- 现有 SATD/TD 检测研究多关注分类性能，较少处理 ATD 这一细分类别，也缺乏对模型解释质量的专家验证。

## Approach
- 先从已有 116 条 ATD 相关 Jira issue 中精炼出 57 条专家验证样本，作为更可靠的种子数据。
- 用这些种子样本提取代表性 ATD 关键词，并在 10 个开源项目中筛出超过 103,000 条候选 issue，以缩小需要人工检查的范围。
- 在过滤后的数据上使用主动学习，比较多种查询策略（如 Breaking Ties、Prediction Entropy、Least Confidence、Embedding K-Means、Contrastive Active Learning、Random），优先请求标注“最有信息量”的样本。
- 用 LIME 和 SHAP 对自动分类结果进行解释，突出影响预测的词语/特征，并请专家评估解释的可用性。

## Results
- 数据构建方面：作者将先前的 116 条 ATD issue 精炼为 57 条专家验证实例，并用其扩展到 10 个项目、超过 103,000 条候选 issue。
- 主动学习方面：**Breaking Ties** 策略表现最稳定，取得最高 **F1 = 0.72**，同时将**标注工作量降低 49%**。
- 可解释性方面：专家评估认为 **LIME 和 SHAP 都能提供合理解释**，但解释是否有用取决于高亮特征是否真正相关。
- 偏好方面：专家**总体更偏好 LIME**，理由是其解释更清晰、更易使用。
- 摘要未提供更多完整量化结果（如 precision/recall、各策略逐项对比、关键词过滤的误报/漏报具体数值），因此无法进一步做数字化比较。

## Link
- [http://arxiv.org/abs/2603.02944v1](http://arxiv.org/abs/2603.02944v1)
