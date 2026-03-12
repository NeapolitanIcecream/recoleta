---
source: arxiv
url: http://arxiv.org/abs/2603.07091v1
published_at: '2026-03-07T08:00:48'
authors:
- Ha Vo
- Nhut Tran
- Khang Vo
- Phat T. Tran-Truong
- Son Ha
topics:
- small-language-models
- software-architecture
- architectural-decision-records
- benchmarking
- reasoning-evaluation
relevance_score: 0.03
run_id: materialize-outputs
---

# Exploring the Reasoning Depth of Small Language Models in Software Architecture: A Multidimensional Evaluation Framework Towards Software Engineering 2.0

## Summary
本文研究小语言模型在软件架构决策记录（ADR）生成中的“推理深度”，并提出一个同时看语义质量、架构合规性和多样性的评测框架。结论是：小模型并非只看文本相似度就够，约 3B 参数附近出现明显能力分水岭，而高多样性常常意味着幻觉而非更好的架构探索。

## Problem
- 论文要解决的是：**小语言模型（SLM, <7B）能否可靠地支持软件架构决策**，尤其是在 ADR 生成这类需要权衡、约束理解和技术合规性的任务上。
- 这很重要，因为大模型虽然强，但**成本高、隐私风险高、难以本地部署**；而企业的软件架构文档常含敏感信息，更适合用可本地托管的小模型。
- 现有评测大多依赖 **ROUGE/BLEU** 等文本相似度，无法识别“写得像但架构上是错的”答案，因此缺少对**真正架构推理能力**的系统性评估。

## Approach
- 作者提出 **SLM-ArchBench**，用 ADR 生成为核心任务，评测 10 个开源指令微调 SLM（约 1B 到 7B），数据来自 **95 条**专家撰写的 GitHub ADR，上下文-决策配对，按 **80/20** 划分训练/验证。
- 评估分三种设置：**Zero-shot**、**Few-shot（k=2）**、以及 **LoRA 微调**；LoRA 使用 **r=16、alpha=32、dropout=0.5、10 epochs、learning rate=2e-4**，在 **76** 条训练样本上训练。
- 指标不是只看文本匹配，还同时看：**BERTScore**（语义准确性）、**ROUGE/BLEU/METEOR**（文本相似）、**Architectural Compliance**（由 Gemini-2.5-Flash 作为裁判，0–100 分评估技术正确性/最佳实践一致性）、以及 **Semantic Diversity**（每个输入采样 **3** 个答案，计算平均成对余弦距离）。
- 核心机制可简单理解为：**让模型写 ADR，再从“像不像参考答案”“技术上对不对”“是不是只是胡乱发散”三个维度一起打分**，从而区分表面流畅和真正的架构推理。

## Results
- 在 **Zero-shot** 下，**Mistral-7B-v0.3** 的语义相似度最好，**BERTScore F1 = 0.827**；而 **Qwen2.5-3B** 的架构合规性最高，**Compliance = 71.737/100**。这说明“最像参考答案”和“最符合架构原则”并不总是同一模型。
- 作者声称存在明显的**参数阈值效应**：多数 **>3B** 模型的合规分数超过 **65**，如 **Llama-3.2-3B = 65.421**、**Phi-3-mini (3.8B) = 66.421**、**Mistral-7B = 66.947**、**Qwen2.5-3B = 71.737**；而部分 **<2B** 模型明显较弱，如 **Gemma-3-1B = 45.421**、**SmolLM2-1.7B = 51.053**。
- 文本相似度与架构正确性会明显背离：例如 **Gemma-3-1B** 虽有 **BERTScore F1 = 0.805**，但合规仅 **45.421**；**SmolLM2-1.7B** 的 **BERTScore F1 = 0.815**，合规也只有 **51.053**。论文据此强调仅靠 ROUGE/BLEU/BERTScore 会高估小模型的架构能力。
- 在 **Few-shot（k=2）** 下，部分中等规模模型得到有效“校准”：**Mistral-7B** 的 **BERTScore F1 从 0.827 提升到 0.835**；**Llama-3.2-3B** 从 **0.826 提升到 0.830**；**OLMo-2-1B** 从 **0.825 提升到 0.826**。但合规提升并不稳定，**Llama-3.2-3B** 的合规反而从 **65.421 降到 57.105**，**Mistral-7B** 从 **66.947 降到 62.0**。
- 论文摘要还明确声称：**子 2B 模型在 Fine-Tuning 后获得最强的 BERTScore 增益，但合规性提升并无保证**；同时，**高语义多样性**在现成小模型中往往更接近**幻觉**而非有效架构探索。当前摘录未提供完整微调结果表，因此无法逐一列出所有微调数值。

## Link
- [http://arxiv.org/abs/2603.07091v1](http://arxiv.org/abs/2603.07091v1)
