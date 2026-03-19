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
- peft
- transformer-ensemble
- software-engineering
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# LoRA-MME: Multi-Model Ensemble of LoRA-Tuned Encoders for Code Comment Classification

## Summary
本文提出 LoRA-MME，用多个经过 LoRA 参数高效微调的代码编码器做加权集成，用于多语言代码注释多标签分类。它的主要价值是在不做全量微调的情况下提升分类精度，但代价是推理成本较高。

## Problem
- 解决的是**代码注释分类**问题：将 Java、Python、Pharo 中的注释自动分到语义类别，如 summary、usage、parameters、deprecation 等。
- 这件事重要，因为高质量的注释分类能支持自动文档生成、代码检索、程序理解和开发者辅助工具。
- 难点在于这是**多语言、多标签、类别不平衡**任务，而且既需要理解自然语言，又要理解代码相关术语与结构，同时还要兼顾精度与计算效率。

## Approach
- 核心方法很简单：分别对 4 个代码专用 Transformer 编码器（UniXcoder、CodeBERT、GraphCodeBERT、CodeBERTa）加上 **LoRA 适配器**单独微调，再把它们的预测结果做**学习式加权集成**。
- LoRA 只在注意力层的 query/key/value/dense 中加入低秩可训练矩阵，冻结原始大部分参数，使每个模型只训练约 **4.5% 参数（约 5.9M）**，可在 **RTX 3090** 上完成训练。
- 集成不是简单平均，而是为每个类别学习单独权重，让不同模型在擅长的类别上贡献更大；例如带结构信息的 GraphCodeBERT 可对某些代码结构相关类别更重要。
- 为了处理类别不平衡，训练时使用 **Focal Loss（γ=2.0）** 和正类加权；并对每个**语言-类别**单独搜索分类阈值，而不是统一用 0.5。
- 数据侧还做了语言感知预处理，包括修复符号损坏、保留 JavaDoc/Sphinx/Pharo 特定语法，以及对 Pharo 注释做启发式切分。

## Results
- 在测试集上，LoRA-MME 达到 **Weighted F1 = 0.7906**、**Macro F1 = 0.6867**。
- 相比官方/文中 baseline，整体 **Macro F1 从 0.6508 提升到 0.6867（+0.0359）**；分语言提升分别为：**Java 0.7306→0.7445（+0.0139）**、**Python 0.5820→0.6296（+0.0476）**、**Pharo 0.6152→0.6668（+0.0516）**。
- 阈值优化带来明确收益：**固定阈值 0.5** 时 **Macro F1 = 0.6512、Weighted F1 = 0.7654**；改为**按类别优化阈值**后提升到 **0.6867 / 0.7906**，即 **+0.0355 Macro F1、+0.0252 Weighted F1**。
- 若看具体类别，较强结果包括 **Java/Ownership F1 = 0.9333**、**Pharo/Example F1 = 0.8889**、**Java/Summary F1 = 0.8848**、**Java/Usage F1 = 0.8793**、**Pharo/Intent F1 = 0.8511**；较弱类别如 **Java/Rational F1 = 0.3696**、**Python/DevelopmentNotes F1 = 0.3929**。
- 论文也明确指出效率代价：平均推理时间 **45.13 ms/sample**，总计算量约 **235,759.28 GFLOPS**，因此竞赛综合提交分只有 **41.20%**，说明精度提升伴随着明显的推理开销。

## Link
- [http://arxiv.org/abs/2603.03959v2](http://arxiv.org/abs/2603.03959v2)
