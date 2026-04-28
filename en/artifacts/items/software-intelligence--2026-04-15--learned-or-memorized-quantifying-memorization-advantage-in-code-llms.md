---
source: arxiv
url: http://arxiv.org/abs/2604.13997v1
published_at: '2026-04-15T15:43:10'
authors:
- "Djir\xE9 Alb\xE9rick Euraste"
- "Kabor\xE9 Abdoul Kader"
- Jordan Samhi
- Earl T. Barr
- Jacques Klein
- "Tegawend\xE9 F. Bissyand\xE9"
topics:
- code-llm-evaluation
- memorization-detection
- benchmark-contamination
- perturbation-analysis
- software-engineering-benchmarks
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Learned or Memorized ? Quantifying Memorization Advantage in Code LLMs

## Summary
This paper measures how much code LLM performance depends on memorized benchmark data instead of general code understanding. It uses input perturbations to estimate a model's "memorization advantage" across many software engineering tasks and benchmarks.

## Problem
- Code LLM training data is usually opaque, so benchmark leakage is hard to verify directly.
- If evaluation examples appeared in training, reported benchmark scores can overstate real generalization.
- This matters for code generation, repair, testing, and security tasks, where a model that recalls known examples may fail on small variations of new problems.

## Approach
- The paper defines **memorization advantage** as the performance gap between an original input and slightly perturbed versions of that input.
- For each sample, it creates progressively stronger but still human-preserving perturbations, prompts the model on each variant, and measures task performance against the reference output.
- It uses the maximum drop between consecutive perturbation levels as the sample's sensitivity score: high sensitivity suggests reliance on memorized patterns or weak generalization.
- The study evaluates 8 open-source code LLMs on 19 benchmarks spanning code generation, code understanding, vulnerability detection, bug identification, test generation, and program repair.
- It compares sensitivity distributions across models and across benchmarks, using Mann-Whitney U tests with Bonferroni correction, 3 repeats, temperature 0.3, and top_k 0.5.

## Results
- **StarCoder** shows high sensitivity on some benchmarks, reaching **0.8** on **APPS**, while **QwenCoder** stays below **0.4** on most benchmarks.
- **Code summarization** has low sensitivity, usually **<0.3**, which the paper reads as stronger generalization on that task.
- **Test generation** has higher sensitivity, around **0.4-0.7** with **p < 0.001**, making it one of the hardest settings for stable generalization.
- **Defects4J** has lower sensitivity than other program repair benchmarks, around **0.2-0.4** with **p < 0.01**, versus **0.5-0.8** on other repair datasets.
- **CVEFixes** stays below **0.1** across models, which weakens the common claim that this benchmark is heavily contaminated.
- The paper's main claim is that suspected leakage benchmarks such as **CVEFixes** and **Defects4J** may reflect real generalization more than simple memorization, while sensitivity varies widely by model family and task category.

## Link
- [http://arxiv.org/abs/2604.13997v1](http://arxiv.org/abs/2604.13997v1)
