---
source: arxiv
url: https://arxiv.org/abs/2604.24678v1
published_at: '2026-04-27T16:38:01'
authors:
- Sivajeet Chand
- Kevin Nguyen
- Peter Kuntz
- Alexander Pretschner
topics:
- code-generation
- domain-specific-languages
- multi-file-editing
- qlora-fine-tuning
- software-engineering
- industrial-case-study
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Leveraging LLMs for Multi-File DSL Code Generation: An Industrial Case Study

## Summary
BMW tested whether 7B code LLMs can turn one natural-language request into a complete multi-file Xtext DSL project update. The paper’s main claim is that QLoRA fine-tuning makes repository-scale DSL generation usable enough for developer review and generator checks.

## Problem
- Enterprise DSL changes often touch several files, folders, imports, and dependent declarations, so single-file code generation does not match the real workflow.
- In this BMW setting, the DSL is the source for Java and TypeScript generation; small DSL mistakes can break the downstream generator or produce wrong market configurations.
- Developers still author these DSL artifacts by hand, which requires domain knowledge and creates delay when creating or changing market-specific configurations.

## Approach
- The method serializes the whole DSL folder tree into path-preserving JSON: folders and files become keys, and file contents become strings.
- Each task uses an instruction, a current project snapshot, and a target project snapshot, so the model learns to output the full updated repository state in one response.
- The dataset contains 774 training examples and 105 held-out evaluation examples, with create, add, and delete operations for markets, attributes, and finance products.
- The study compares Qwen2.5-Coder-7B-Instruct and DeepSeek-Coder-6.7B/7B-Instruct under zero-shot prompting, one-shot prompting, and QLoRA fine-tuning.
- Evaluation combines exact match, BLEU, valid JSON, a change-only similarity metric, structural fidelity over folder/file keys, developer review, and execution through the existing DSL-to-code generator.

## Results
- Fine-tuning is reported as the strongest setting across the tested models and metrics, with structural fidelity of 1.00 on the 105-example held-out set for multi-file outputs.
- Raw models often kept the JSON wrapper valid before task adaptation: Qwen-Raw reached 0.895 valid JSON and DeepSeek-Raw reached 0.848 valid JSON.
- One-shot prompting improved over zero-shot prompting, but the paper states that its gains were smaller than QLoRA fine-tuning.
- The human review used 4 DSL-proficient developers, 20 generated outputs, and 5 operation types with 4 samples per type.
- Reviewer agreement was exact on 2 of 8 rated quality dimensions, or 25%, and within ±1 point on 7 of 8 dimensions, or 87.5%.
- The provided excerpt does not include the full results table, so exact fine-tuned exact-match, BLEU, and change-similarity scores are not available here.

## Link
- [https://arxiv.org/abs/2604.24678v1](https://arxiv.org/abs/2604.24678v1)
