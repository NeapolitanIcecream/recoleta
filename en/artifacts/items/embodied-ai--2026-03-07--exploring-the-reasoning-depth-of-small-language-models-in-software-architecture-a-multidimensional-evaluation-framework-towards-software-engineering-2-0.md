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
language_code: en
---

# Exploring the Reasoning Depth of Small Language Models in Software Architecture: A Multidimensional Evaluation Framework Towards Software Engineering 2.0

## Summary
This paper studies the “reasoning depth” of small language models in generating Software Architecture Decision Records (ADRs), and proposes an evaluation framework that jointly examines semantic quality, architectural compliance, and diversity. The conclusion is: for small models, text similarity alone is not enough; a clear capability watershed appears around 3B parameters, and high diversity often indicates hallucination rather than better architectural exploration.

## Problem
- The paper aims to answer: **can small language models (SLMs, <7B) reliably support software architecture decisions**, especially on tasks like ADR generation that require trade-off analysis, constraint understanding, and technical compliance?
- This matters because, although large models are powerful, they are **costly, pose greater privacy risks, and are difficult to deploy locally**; meanwhile, enterprise software architecture documents often contain sensitive information, making locally hosted small models more suitable.
- Existing evaluations mostly rely on text similarity metrics such as **ROUGE/BLEU**, which cannot identify answers that “read like the reference but are architecturally wrong,” so there is a lack of systematic evaluation of **true architectural reasoning ability**.

## Approach
- The authors propose **SLM-ArchBench**, using ADR generation as the core task to evaluate 10 open-source instruction-tuned SLMs (roughly 1B to 7B parameters). The data come from **95** expert-written GitHub ADRs, paired as context-decision examples, and split into train/validation with an **80/20** ratio.
- Evaluation is conducted under three settings: **Zero-shot**, **Few-shot (k=2)**, and **LoRA fine-tuning**; LoRA uses **r=16, alpha=32, dropout=0.5, 10 epochs, learning rate=2e-4**, trained on **76** training samples.
- The metrics go beyond text matching and jointly measure: **BERTScore** (semantic accuracy), **ROUGE/BLEU/METEOR** (text similarity), **Architectural Compliance** (Gemini-2.5-Flash as judge, scoring 0–100 for technical correctness / alignment with best practices), and **Semantic Diversity** (sampling **3** outputs per input and computing the average pairwise cosine distance).
- The core mechanism can be understood simply as: **have the model write an ADR, then score it jointly from three dimensions—“does it resemble the reference answer,” “is it technically correct,” and “is it merely diverging randomly”**—thereby distinguishing surface fluency from genuine architectural reasoning.

## Results
- Under **Zero-shot**, **Mistral-7B-v0.3** achieves the best semantic similarity, with **BERTScore F1 = 0.827**; meanwhile, **Qwen2.5-3B** has the highest architectural compliance, at **Compliance = 71.737/100**. This shows that “most similar to the reference answer” and “most consistent with architectural principles” are not always the same model.
- The authors argue that there is a clear **parameter-threshold effect**: most models **>3B** score above **65** in compliance, such as **Llama-3.2-3B = 65.421**, **Phi-3-mini (3.8B) = 66.421**, **Mistral-7B = 66.947**, and **Qwen2.5-3B = 71.737**; by contrast, some models **<2B** are noticeably weaker, such as **Gemma-3-1B = 45.421** and **SmolLM2-1.7B = 51.053**.
- Text similarity and architectural correctness can diverge substantially: for example, **Gemma-3-1B** has **BERTScore F1 = 0.805** but only **45.421** compliance; **SmolLM2-1.7B** has **BERTScore F1 = 0.815** but compliance of only **51.053**. Based on this, the paper emphasizes that relying only on ROUGE/BLEU/BERTScore would overestimate the architectural ability of small models.
- Under **Few-shot (k=2)**, some mid-sized models are effectively “calibrated”: **Mistral-7B** improves its **BERTScore F1 from 0.827 to 0.835**; **Llama-3.2-3B** improves from **0.826 to 0.830**; **OLMo-2-1B** improves from **0.825 to 0.826**. However, compliance gains are not stable: **Llama-3.2-3B** actually drops in compliance from **65.421 to 57.105**, and **Mistral-7B** drops from **66.947 to 62.0**.
- The abstract also explicitly states that **sub-2B models achieve the strongest BERTScore gains after Fine-Tuning, but improvements in compliance are not guaranteed**; at the same time, **high semantic diversity** in off-the-shelf small models often aligns more with **hallucination** than effective architectural exploration. The current excerpt does not provide the full fine-tuning results table, so it is not possible to list all fine-tuning values one by one.

## Link
- [http://arxiv.org/abs/2603.07091v1](http://arxiv.org/abs/2603.07091v1)
