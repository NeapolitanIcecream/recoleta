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
- adr-generation
- benchmarking
- architectural-reasoning
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# Exploring the Reasoning Depth of Small Language Models in Software Architecture: A Multidimensional Evaluation Framework Towards Software Engineering 2.0

## Summary
本文研究小语言模型（SLM）在软件架构决策记录（ADR）生成中的“推理深度”，并提出一个同时衡量语义质量、架构合规性与多样性的评测框架。核心结论是：SLM并非越小越好用，约3B参数以上出现更稳健的零样本架构推理能力，而高多样性常常意味着幻觉而非有效探索。

## Problem
- 现有软件工程基准多评测代码实现或文本相似度，难以判断模型是否真的理解软件架构中的权衡、约束与设计原则。
- 大模型虽强，但在成本、延迟、隐私与本地部署上不适合很多企业架构场景，因此需要弄清小模型是否足够胜任ADR生成。
- 仅靠ROUGE/BLEU等指标可能把“写得像”误判为“架构上正确”，这会误导真实的软件架构辅助部署。

## Approach
- 提出 **SLM-ArchBench**，针对ADR生成评估10个开源、指令微调的SLM（约1B到7B），数据集为95个专家编写的Context-Decision样本。
- 用三种设置系统比较：**Zero-shot**、**Few-shot（k=2）**、以及 **LoRA PEFT微调**；LoRA设置包括r=16、alpha=32、dropout=0.5，训练10个epoch，训练集76条、验证集19条。
- 评测不只看文本相似度，还加入 **Architectural Compliance Score**（由Gemini-2.5-Flash作为judge，0-100分）来判断技术合理性与架构最佳实践一致性。
- 进一步用3次采样候选之间的平均余弦距离衡量 **Semantic Diversity**，区分“有价值的方案探索”与“随机幻觉式发散”。
- 论文试图回答三个简单问题：小模型原生能力有多强、few-shot和微调谁更有效、以及多样性究竟是创造力还是错误信号。

## Results
- **零样本表现**：Mistral-7B-v0.3取得最高 **BERTScore F1=0.827**；Qwen2.5-3B取得最高 **Compliance=71.737/100**。论文总结称，**3B以上模型大多零样本合规分超过65**，显示出更稳健的架构推理门槛。
- **小模型的语义-合规脱钩明显**：Gemma-3-1B虽有 **BERTScore F1=0.805**，但 **Compliance仅45.421**；SmolLM2-1.7B **F1=0.815**，**Compliance=51.053**，说明“语义像答案”不代表“架构上正确”。
- **多样性未必是好事**：零样本下 SmolLM2-1.7B 的 **Diversity=0.541**、Phi-3-mini 的 **0.499** 较高，但其合规性并未同步领先；相反 Mistral-7B 的 **Diversity=0.280** 却有更强语义与合规表现。论文据此声称，高多样性在小模型中常与幻觉相关。
- **Few-shot可作为校准机制**：例如 Mistral-7B 从零样本 **F1=0.827** 提升到 few-shot **0.835**，ROUGE-1 从 **0.202** 提升到 **0.224**；但其 **Compliance 从66.947降到62.0**，表明few-shot能改善语义表达，但未必稳定提升架构正确性。
- **Few-shot对部分短上下文中型模型有效**：Llama-3.2-3B 的 **F1从0.826升至0.830**；OLMo-2-1B 的 **F1从0.825升至0.826**。论文据此反驳“上下文一加就饱和”的简单假设，认为few-shot对某些模型更像校准而非负担。
- **微调方面的定量结论在摘要中给出但节选未完整展示表格**：作者声称 **sub-2B模型在Fine-Tuning后BERTScore增益最明显**，但**合规性提升并不保证**。因此最强具体主张是：微调更能修复小模型的语义匹配，而不一定真正补齐架构推理缺口。

## Link
- [http://arxiv.org/abs/2603.07091v1](http://arxiv.org/abs/2603.07091v1)
