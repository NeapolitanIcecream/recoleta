---
source: arxiv
url: http://arxiv.org/abs/2603.03959v2
published_at: '2026-03-04T11:36:32'
authors:
- Md Akib Haider
- Ahsan Bulbul
- Nafis Fuad Shahid
- Aimaan Ahmed
- Mohammad Ishrak Abedin
topics:
- code-comment-classification
- lora
- model-ensemble
- code-language-models
- parameter-efficient-fine-tuning
relevance_score: 0.81
run_id: materialize-outputs
language_code: zh-CN
---

# LoRA-MME: Multi-Model Ensemble of LoRA-Tuned Encoders for Code Comment Classification

## Summary
LoRA-MME 是一个面向代码注释多标签分类的集成方法，把多个代码专用 Transformer 用 LoRA 低成本微调后再做加权融合。它主要追求更高语义分类准确率，但也明确暴露了集成带来的推理效率代价。

## Problem
- 解决代码注释分类问题：将 Java、Python、Pharo 中的注释句子自动归到语义类别，如 summary、usage、parameters、deprecation 等。
- 这件事很重要，因为注释类型识别能支持自动化文档生成、代码搜索、维护分析和开发者辅助工具。
- 难点在于这是**多语言、多标签、类别不平衡**任务，而且既要利用代码语义，又要控制微调和推理成本。

## Approach
- 使用 4 个代码专用编码器：UniXcoder、CodeBERT、GraphCodeBERT、CodeBERTa，各自独立训练，而不是只依赖单一模型。
- 对每个模型使用 LoRA 做参数高效微调：只在 attention 的 query/key/value/dense 层插入低秩适配器，冻结原始大部分参数；每个模型仅训练约 **4.5% 参数（约 5.9M）**，可在 **RTX 3090** 上训练。
- 将 4 个模型的输出做**按类别学习的加权集成**：不同注释类别可偏向不同模型，而不是简单平均概率。
- 对每个“语言-类别”单独搜索分类阈值，而不是统一用 0.5；阈值在验证集上从 **0.1 到 0.9** 网格搜索，最终范围约 **0.28–0.85**，均值 **0.65**。
- 训练时使用 **focal loss（γ=2.0）** 和正类加权，以缓解类别不平衡。

## Results
- 在测试集上，LoRA-MME 达到 **Weighted F1 = 0.7906**、**Macro F1 = 0.6867**。
- 相比论文给出的 baseline，整体 **Macro F1 从 0.6508 提升到 0.6867（+0.0359）**；分语言提升分别为：**Java 0.7306→0.7445（+0.0139）**、**Python 0.5820→0.6296（+0.0476）**、**Pharo 0.6152→0.6668（+0.0516）**。
- 阈值优化带来明确增益：**Macro F1 0.6512→0.6867（+0.0355）**，**Weighted F1 0.7654→0.7906（+0.0252）**，相对固定阈值 0.5 更好。
- 若看单类别，较强结果包括：**Java/Ownership F1 = 0.9333**、**Pharo/Example F1 = 0.8889**、**Java/Summary F1 = 0.8848**、**Java/Usage F1 = 0.8793**、**Pharo/Intent F1 = 0.8511**。
- 但效率较差：平均推理时间 **45.13 ms/sample**，总计算量约 **235,759.28 GFLOPS**，导致竞赛综合提交分数只有 **41.20%**。
- 论文声称的核心突破不是单模型架构创新，而是把 **LoRA + 多模型代码编码器集成 + 按类别阈值优化** 组合起来，在保持参数高效微调的同时取得更强分类表现，代价是推理开销显著上升。

## Link
- [http://arxiv.org/abs/2603.03959v2](http://arxiv.org/abs/2603.03959v2)
