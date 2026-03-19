---
source: arxiv
url: http://arxiv.org/abs/2603.02944v1
published_at: '2026-03-03T12:51:54'
authors:
- Edi Sutoyo
- Paris Avgeriou
- Andrea Capiluppi
topics:
- architecture-technical-debt
- active-learning
- explainable-ai
- issue-tracking
- satd-detection
relevance_score: 0.76
run_id: materialize-outputs
language_code: zh-CN
---

# Reducing Labeling Effort in Architecture Technical Debt Detection through Active Learning and Explainable AI

## Summary
该论文研究如何以更少的人工标注成本检测 Jira issue 中的架构技术债（ATD），并同时让模型预测更可解释。核心是把关键词过滤、主动学习和可解释 AI 结合起来，面向大规模开源项目构建 ATD 检测流程。

## Problem
- ATD 是技术债中最难检测、影响又最广的一类，因为它涉及抽象的架构决策与上下文，而不是简单的代码坏味道。
- 现有 SATD/TD 研究多关注通用技术债，针对 issue tracker 中 ATD 的高质量标注数据很少；专家标注又昂贵、耗时且难扩展。
- 即使模型能分类，缺少可解释性也会削弱工程人员对结果的信任和采纳，因此需要可追溯、可理解的 ATD 识别方法。

## Approach
- 先将已有 116 条与 ATD 相关的 Jira issue 数据进一步精炼，得到 57 条经专家验证的样本，并从中提取有代表性的 ATD 关键词。
- 用这些关键词在 10 个大型开源项目中做初筛，找到超过 103,000 条候选 issue，以缩小人工检查范围并评估关键词在跨项目上的可复用性。
- 在过滤后的数据上应用池式主动学习，比较多种查询策略（如 Breaking Ties、Prediction Entropy、Least Confidence、Embedding K-Means、Contrastive Active Learning、Random），优先挑选“最值得标”的样本。
- 用分类模型自动识别 ATD，并借助 LIME 与 SHAP 给出局部解释，标出哪些词语/特征推动了模型判断；再让专家从多项标准上评价解释质量。

## Results
- 数据构建方面：从已有 **116** 条 ATD 相关 issue 中精炼出 **57** 条专家验证样本，并据此在 **10** 个开源项目中筛出 **103,000+** 条候选 issue。
- 主动学习方面：**Breaking Ties** 策略表现最稳定，取得最高 **F1 = 0.72**，同时将人工标注工作量降低 **49%**。
- 可解释性方面：专家评估认为 **LIME** 和 **SHAP** 都能提供“合理”的分类解释；解释是否有用很大程度取决于被高亮特征是否与架构债语义相关。
- 偏好方面：专家总体上更偏好 **LIME**，理由是其解释更清晰、更加易用。
- 论文还声称这是首批将领域专家系统性纳入 SATD/ATD 检测解释评估的工作之一；但给定摘录中未提供更细的数值结果（如各策略完整 precision/recall、关键词过滤误报漏报、专家评分均值）。

## Link
- [http://arxiv.org/abs/2603.02944v1](http://arxiv.org/abs/2603.02944v1)
