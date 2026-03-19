---
source: hn
url: https://www.nih.gov/news-events/news-releases/automated-ct-scan-analysis-could-fast-track-clinical-assessments
published_at: '2026-03-05T23:54:26'
authors:
- hhs
topics:
- medical-foundation-model
- vision-language-model
- ct-analysis
- clinical-ai
- disease-risk-prediction
relevance_score: 0.23
run_id: materialize-outputs
language_code: zh-CN
---

# Automated CT scan analysis could fast-track clinical assessments

## Summary
Merlin 是一个面向 3D 腹部 CT 的视觉-语言基础模型，目标是把一次通用训练扩展到诊断、预后和质控等大量临床任务。它通过大规模 CT、放射学报告和诊断代码联合训练，在多类任务上超过或追平专用模型。

## Problem
- 传统 CT 影像解读依赖放射科医生逐项分析，流程耗时且在医生短缺背景下更难扩展。
- 现有自动化工具通常只为单一任务设计，难以同时覆盖诊断、预后、器官分割、报告生成等广泛需求。
- 如果不能从常规 CT 中稳定提取更丰富的疾病信号，临床就会错失更早发现慢病风险和潜在生物标志物的机会。

## Approach
- 构建名为 Merlin 的 CT foundation model，用大规模、弱标注/未专门逐任务标注的数据学习通用影像表征。
- 训练数据来自超过 **15,000** 个 3D 腹部 CT，与对应放射学报告和接近 **100 万** 个诊断代码关联；文中称这是迄今最大的腹部 CT 数据集合。
- 核心机制可简单理解为：让模型同时看 **CT 图像** 和 **文字医学结论**，从而学会“影像特征 ↔ 临床含义”的对应关系，再把这种通用能力迁移到很多任务。
- 在评测阶段，研究者用来自 **4 家医院** 的超过 **50,000** 个未见过的腹部 CT，在 **6** 大类、超过 **750** 个任务上测试；其中部分复杂任务再做额外训练/微调，如报告生成和 3D 器官勾画。
- 同时使用各任务的最先进专用模型作为对照，验证通用模型是否能真正替代或超过专家系统。

## Results
- 在 **692** 个诊断代码预测上，Merlin 平均能以超过 **81%** 的准确比较出“两张 CT 中哪一张更可能对应某诊断代码”，优于两个其他模型的多个变体。
- 在一个包含 **102** 个诊断代码的子集上，Merlin 的表现提升到 **90%**。
- 在慢病风险预测中，仅基于 CT，Merlin 对“未来 **5 年** 内更可能患病的患者”进行两两比较时，正确率达到 **75%**，高于对照模型的 **68%**；涉及疾病包括糖尿病、骨质疏松和心脏病。
- 模型在胸部 CT 上也显示出跨解剖部位泛化能力：尽管训练时没有胸部 CT，文中称其表现与仅用胸部 CT 训练的模型 **相当或更好**，但摘录未给出具体数值。
- 整体上，作者声称 Merlin 在所有测试任务中都 **超过或匹配** 专用模型，覆盖诊断、预后和质控等场景。
- 研究还提出一个重要临床意义：模型可能从 CT 中发现肉眼难以察觉的早期疾病特征，为新的疾病生物标志物挖掘提供线索。

## Link
- [https://www.nih.gov/news-events/news-releases/automated-ct-scan-analysis-could-fast-track-clinical-assessments](https://www.nih.gov/news-events/news-releases/automated-ct-scan-analysis-could-fast-track-clinical-assessments)
