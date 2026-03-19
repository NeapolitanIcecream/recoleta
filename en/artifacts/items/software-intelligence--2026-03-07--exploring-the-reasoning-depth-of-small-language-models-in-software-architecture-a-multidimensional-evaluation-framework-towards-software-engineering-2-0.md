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
language_code: en
---

# Exploring the Reasoning Depth of Small Language Models in Software Architecture: A Multidimensional Evaluation Framework Towards Software Engineering 2.0

## Summary
This paper studies the "reasoning depth" of small language models (SLMs) in generating software architecture decision records (ADRs), and proposes an evaluation framework that simultaneously measures semantic quality, architectural compliance, and diversity. The core conclusion is: smaller SLMs are not necessarily more usable; models with around 3B parameters and above show more robust zero-shot architectural reasoning ability, while high diversity often indicates hallucination rather than effective exploration.

## Problem
- Existing software engineering benchmarks mostly evaluate code implementation or textual similarity, making it difficult to determine whether a model truly understands trade-offs, constraints, and design principles in software architecture.
- Although large models are powerful, they are unsuitable for many enterprise architecture scenarios due to cost, latency, privacy, and local deployment concerns, so it is necessary to determine whether small models are capable enough for ADR generation.
- Relying only on metrics such as ROUGE/BLEU may mistake "writing something that looks right" for "being architecturally correct," which could mislead real-world deployment of software architecture assistants.

## Approach
- The paper proposes **SLM-ArchBench**, evaluating 10 open-source, instruction-tuned SLMs (about 1B to 7B) on ADR generation, using a dataset of 95 expert-written Context-Decision samples.
- It systematically compares three settings: **Zero-shot**, **Few-shot (k=2)**, and **LoRA PEFT fine-tuning**; the LoRA setup includes r=16, alpha=32, dropout=0.5, training for 10 epochs, with 76 training samples and 19 validation samples.
- The evaluation goes beyond textual similarity by adding **Architectural Compliance Score** (with Gemini-2.5-Flash as judge, scored 0-100) to assess technical soundness and alignment with architectural best practices.
- It further uses the average cosine distance among candidates from 3 sampling runs to measure **Semantic Diversity**, distinguishing "valuable solution exploration" from "random hallucinatory divergence."
- The paper aims to answer three simple questions: how strong the native capabilities of small models are, whether few-shot or fine-tuning is more effective, and whether diversity is actually creativity or a signal of error.

## Results
- **Zero-shot performance**: Mistral-7B-v0.3 achieves the highest **BERTScore F1=0.827**; Qwen2.5-3B achieves the highest **Compliance=71.737/100**. The paper concludes that **most models above 3B score over 65 in zero-shot compliance**, indicating a more robust threshold for architectural reasoning.
- **A clear semantic-compliance decoupling appears in small models**: although Gemma-3-1B has **BERTScore F1=0.805**, its **Compliance is only 45.421**; SmolLM2-1.7B has **F1=0.815** and **Compliance=51.053**, showing that "being semantically similar to the answer" does not mean "being architecturally correct."
- **Diversity is not necessarily a good thing**: under zero-shot, SmolLM2-1.7B has relatively high **Diversity=0.541** and Phi-3-mini has **0.499**, but their compliance does not lead accordingly; by contrast, Mistral-7B has **Diversity=0.280** yet stronger semantic and compliance performance. Based on this, the paper argues that high diversity in small models is often associated with hallucination.
- **Few-shot can serve as a calibration mechanism**: for example, Mistral-7B improves from zero-shot **F1=0.827** to few-shot **0.835**, and ROUGE-1 rises from **0.202** to **0.224**; however, its **Compliance drops from 66.947 to 62.0**, indicating that few-shot can improve semantic expression but does not necessarily stably improve architectural correctness.
- **Few-shot is effective for some mid-sized models with short context windows**: Llama-3.2-3B increases **F1 from 0.826 to 0.830**; OLMo-2-1B increases **F1 from 0.825 to 0.826**. The paper uses this to challenge the simplistic assumption that "adding context just causes saturation," arguing that for some models, few-shot functions more like calibration than burden.
- **Quantitative conclusions on fine-tuning are given in the abstract, but the excerpt does not fully show the tables**: the authors claim that **sub-2B models show the most obvious BERTScore gains after Fine-Tuning**, but **improvements in compliance are not guaranteed**. Therefore, the strongest concrete claim is that fine-tuning is better at repairing semantic matching in small models, but does not necessarily truly close the architectural reasoning gap.

## Link
- [http://arxiv.org/abs/2603.07091v1](http://arxiv.org/abs/2603.07091v1)
