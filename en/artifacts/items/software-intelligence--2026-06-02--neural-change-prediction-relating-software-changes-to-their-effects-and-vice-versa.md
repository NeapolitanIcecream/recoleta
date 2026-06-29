---
source: arxiv
url: https://arxiv.org/abs/2606.03378v1
published_at: '2026-06-02T09:23:35'
authors:
- Laura Plein
- Souhila Zidane
- Jordan Samhi
- Andreas Zeller
topics:
- code-intelligence
- automated-code-editing
- program-repair
- change-impact-analysis
- software-testing
- foundation-models
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Neural Change Prediction: Relating Software Changes to Their Effects and Vice Versa

## Summary
Neural Change Prediction trains models on synthetic code and configuration mutations paired with observed output changes, then uses those pairs to predict either the effect of a change or the code change needed for a desired effect. The paper reports high accuracy on CSS and Python tasks, with fine-tuned GPT-4.1 well above reported LLM baselines.

## Problem
- Developers often need to know which code change will cause a desired behavior change, or what behavior a proposed code change will cause.
- Static reasoning and current LLMs struggle to infer dynamic program behavior without execution; the paper reports only 10% to 33% accuracy for current LLM systems on these tasks.
- Better predictions could aid debugging, feature localization, change impact analysis, software evolution, and repair, while proposed fixes can still be checked by running tests.

## Approach
- For a given program and test inputs, the system applies many synthetic mutations to source code or configuration files.
- It runs the original and mutated program, then records the input, original output, mutated output, changed code, and mutation location as training data.
- It trains models in both directions: code change plus current output -> output change, and desired output change -> likely code location or exact code edit.
- CSS experiments use natural-language intents such as changing a rendered element's color; Python experiments use output changes for given inputs.
- The study fine-tunes GPT-4.1/GPT-4.1-mini and also considers GPT-oss, CodeLlama, Qwen, and simpler machine learning baselines.

## Results
- CSS: fine-tuned GPT-4.1 reached up to 95% accuracy for predicting correct CSS changes under general learning across templates.
- CSS: project-specific learning on one template reached 100% accuracy.
- Python desired-behavior task: fine-tuned GPT-4.1 reached 82.6% accuracy for correct change location with single mutations.
- Python desired-behavior task: fine-tuned GPT-4.1 reached 71.6% accuracy for the exact change with single mutations.
- Python effect prediction: fine-tuned GPT-4.1 reached 95% accuracy for predicting output change from a single code mutation, and 99% accuracy for multiple mutations.
- Baseline context: current LLM systems are reported at 10% to 33% accuracy on these tasks.

## Link
- [https://arxiv.org/abs/2606.03378v1](https://arxiv.org/abs/2606.03378v1)
