---
source: arxiv
url: https://arxiv.org/abs/2606.30610v1
published_at: '2026-06-29T17:45:36'
authors:
- Chuyue Li
- Ziqi Tang
- Jingyi Wang
- Yu Wu
- Kazuma Hashimoto
- Lingyu Gao
topics:
- code-intelligence
- software-foundation-models
- code-error-classification
- programming-education
- llm-benchmarking
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# PyMETA: A Benchmark Dataset for Hierarchical Student Code Error Classification with Python-Interpreter-Based Labels

## Summary
PyMETA is a Python student-code error classification benchmark with 48,646 submissions and interpreter-derived labels. It tests finetuned code models and prompted LLMs on a three-level error taxonomy, plus a small expert-labeled multi-error subset.

## Problem
- Educational debugging tools need error labels that match Python execution behavior, but public datasets are often small, narrow, and use inconsistent taxonomies.
- Single runtime labels can hide multiple coexisting errors, which weakens feedback quality and model evaluation.
- Prompted LLMs need a shared benchmark for student-code diagnosis under low-resource or training-free settings.

## Approach
- The authors collect 48,646 Python submissions from 579 users across 155 problems on the Circle Cat platform using Moodle CodeRunner outputs.
- They derive single-error labels from online judge execution results and Python exception types, with Logic Error assigned to code that runs but fails tests.
- They organize labels into three tasks: binary Error/No Error, three-class No Error/Explicit Error/Logic Error, and a 14-class fine-grained taxonomy.
- They expert-annotate 97 likely multi-error samples, selected from CodeBERT misclassifications and high-entropy predictions, with an average of 1.91 error types per sample.
- They evaluate finetuned CodeBERT and CodeLlama-7B, plus prompted GPT-3.5, GPT-4o, Gemini 2.5 Pro, and DeepSeek-V3.

## Results
- PyMETA contains 48,646 submissions: 23,207 No Error, 11,387 Logic Error, 5,618 Syntax Error, 2,565 Name Error, 2,074 Type Error, and smaller counts for 9 other classes after merging rare labels.
- Under the problem-level test split, CodeLlama-7B reaches 96.3% macro F1 on binary classification, 93.5% macro F1 on three-class classification, and 80.6% macro F1 on 14-class classification.
- CodeBERT is much weaker on the fine-grained task, with 45.2% macro F1 and 71.0% weighted F1 on Task C.
- In single-error prompting, Gemini 2.5 Pro is the best prompted model with 85.9% accuracy and 71.9% macro F1; GPT-4o gets 28.0% macro F1, DeepSeek-V3 gets 29.1%, and GPT-3.5 gets 8.8%.
- Prompted LLMs over-predict Logic Error: the reported Logic Error Overprediction Rate ranges from 17.6% for Gemini 2.5 Pro to 92.8% for GPT-3.5.
- On multi-error prompting, Gemini 2.5 Pro reaches 81.8% macro F1 under the contains criterion on the 97-sample expert subset.

## Link
- [https://arxiv.org/abs/2606.30610v1](https://arxiv.org/abs/2606.30610v1)
