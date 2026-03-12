---
source: hn
url: https://www.nih.gov/news-events/news-releases/automated-ct-scan-analysis-could-fast-track-clinical-assessments
published_at: '2026-03-05T23:54:26'
authors:
- hhs
topics:
- medical-imaging
- ct-foundation-model
- vision-language
- multitask-learning
- clinical-ai
relevance_score: 0.08
run_id: materialize-outputs
---

# Automated CT scan analysis could fast-track clinical assessments

## Summary
这篇工作提出了 **Merlin**，一个面向3D腹部CT的视觉-语言基础模型，目标是把单一医学影像模型扩展为可泛化的多任务临床分析系统。它在诊断、预后、质控等超过750项任务上展现出强通用性，并在多项任务中超过专用模型。

## Problem
- 现有CT分析通常依赖放射科医生逐项解读，并常需额外检查，流程耗时，且医生短缺使临床负担加重。
- 以往自动化模型多为单任务专用工具，难以同时处理诊断、分割、报告生成、风险预测等广泛任务。
- 如果能直接从CT中提取更丰富、甚至早于人工可见征象的疾病信号，就可能加速诊疗并发现慢性病早期生物标志物，这很重要。

## Approach
- 核心方法是训练一个 **CT vision-language foundation model**：把 **15,000+** 个3D腹部CT、对应放射报告以及 **近100万** 个诊断代码联合起来，让模型学习“影像内容”和“文字/诊断标签”之间的对应关系。
- 简单说，Merlin先在大规模临床数据上学会“CT里什么样的视觉模式通常对应哪些医学描述和疾病代码”，再把这种通用表示迁移到不同下游任务。
- 研究中将Merlin评测在 **6大类、750+** 个任务上，覆盖诊断、预后和质量评估；其中有些任务可直接零样本/少量适配完成，复杂任务如报告生成和3D器官勾画则再做额外训练。
- 评测使用了 **50,000+** 个来自 **4家医院** 的未见过的腹部CT，并与多个针对单任务设计的SOTA专用模型比较。
- 还测试了跨解剖部位泛化：虽然训练数据不含胸部CT，Merlin仍被拿去解释胸部CT，以检验其是否学到可泛化疾病特征。

## Results
- 在 **692** 个诊断代码的平均表现上，Merlin预测“两张扫描中哪一张更可能对应某个诊断代码”的正确率超过 **81%**，优于两类其他模型的多个变体。
- 在一个 **102** 个诊断代码的子集上，Merlin的表现提升到 **90%**。
- 在基于CT预测未来 **5年** 慢性病风险的任务中，Merlin识别“哪位健康受试者更可能在未来患病”的正确率为 **75%**，对比模型为 **68%**；文中举例疾病包括糖尿病、骨质疏松和心脏病。
- 在胸部CT这一**训练时未出现的解剖部位**上，Merlin表现达到或超过仅用胸部扫描训练的模型，说明其具备跨部位泛化能力；但摘录未提供该项具体数值。
- 作者声称，作为通用模型，Merlin在全部评测任务上都**匹配或超过**专用模型，关键原因在于其3D架构以及影像-文本联合训练数据；不过摘录未给出每个任务的完整量化表。

## Link
- [https://www.nih.gov/news-events/news-releases/automated-ct-scan-analysis-could-fast-track-clinical-assessments](https://www.nih.gov/news-events/news-releases/automated-ct-scan-analysis-could-fast-track-clinical-assessments)
