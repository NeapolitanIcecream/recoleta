---
source: arxiv
url: https://arxiv.org/abs/2605.02033v1
published_at: '2026-05-03T19:52:39'
authors:
- H. M. Sazzad Quadir
- Sakib Al Hasan
- Md. Nurul Ahad Tawhid
topics:
- commit-classification
- conventional-commits
- prompt-engineering
- code-intelligence
- software-repository-mining
- large-language-models
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Conventional Commit Classification using Large Language Models and Prompt Engineering

## Summary
The paper tests whether open-source LLMs can classify code diffs into Conventional Commit types without fine-tuning. Few-shot prompts give the best average accuracy, but the best single result is only 0.6154 accuracy on one InfluxDB dataset.

## Problem
- Many repositories have unstructured commit messages, which limits changelog generation, semantic versioning, and release automation.
- Existing commit classifiers often need labeled datasets, preprocessing, feature work, and retraining when project terms or labels change.
- The paper studies whether prompt-only LLM classification can reduce that setup cost for Conventional Commit labels.

## Approach
- The authors mine 3,200 approximately balanced commits from the InfluxDB GitHub repository and use the Conventional Commit type as the ground-truth label.
- Each example is classified from its code diff; no model is fine-tuned.
- They test zero-shot, few-shot, and chain-of-thought prompts.
- They evaluate Mistral-7B-Instruct, LLaMA-3-8B, and DeepSeek-R1-32B with accuracy, precision, recall, and F1.

## Results
- Best single run: Mistral-7B-Instruct with few-shot prompting reaches 0.6154 accuracy, 0.3823 precision, 0.6154 recall, and 0.4706 F1 on 3,200 InfluxDB commits.
- DeepSeek-R1-32B has the best average model performance across prompts: 0.563 accuracy, 0.587 precision, 0.563 recall, and 0.538 F1.
- Few-shot prompting has the best average prompt performance across models: 0.531 accuracy and 0.468 F1, compared with zero-shot at 0.431 accuracy and 0.399 F1.
- Chain-of-thought prompting does not improve accuracy: its average accuracy is 0.468, below few-shot at 0.531.
- LLaMA-3-8B is weakest on average, with 0.372 accuracy and 0.366 F1 across prompts.
- The paper does not compare against trained ML or fine-tuned LLM baselines, so the results support prompt-selection guidance more than a new accuracy benchmark.

## Link
- [https://arxiv.org/abs/2605.02033v1](https://arxiv.org/abs/2605.02033v1)
