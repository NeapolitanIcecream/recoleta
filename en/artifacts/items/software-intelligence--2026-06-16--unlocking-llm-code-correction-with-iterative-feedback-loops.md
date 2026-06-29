---
source: arxiv
url: https://arxiv.org/abs/2606.17514v1
published_at: '2026-06-16T04:47:42'
authors:
- Le Zhang
- Suresh Kothari
topics:
- code-correction
- iterative-feedback
- llm-code-generation
- execution-feedback
- code-intelligence
- reasoning-models
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Unlocking LLM Code Correction with Iterative Feedback Loops

## Summary
The paper tests whether LLMs can fix failed code by using compiler errors, runtime errors, failed test cases, and resource-limit feedback across repeated attempts. It finds that reasoning models improve more across iterations, while syntax and runtime failures are easier to fix than logic and algorithm errors.

## Problem
- Single-attempt pass@1 scores miss a common software workflow: code fails, tests return feedback, and the developer revises it.
- This matters because generated code that fails still needs repair; if an LLM can repair it automatically, it can reduce human correction work in coding tools.
- The paper asks which models benefit from feedback, which error types get fixed, and how many iterations are useful.

## Approach
- The study uses LeetCode tasks in Python and Java: 450 Core problems, 200 Strain problems focused on efficiency, and 32 Challenge problems selected from frequent failures.
- It evaluates four models: DeepSeek-R1, DeepSeek-V3, GPT-o4-mini, and GPT-4.1-mini, with reasoning vs. non-reasoning comparisons.
- The correction loop is simple: generate code, run it, send back the error or failed test details, then ask the model to revise the code.
- Feedback includes compile errors, runtime errors, wrong-answer test cases with expected and actual output, time-limit failures, and memory-limit failures.
- The paper defines pass@1 for the first attempt, ISR@k for success within k iterations, and MIS for the median number of iterations needed to solve a task.

## Results
- On the 450-problem Core Dataset, GPT-o4-mini had the best overall pass@1: 89.11% in Python and 87.33% in Java. DeepSeek-R1 scored 84.00% and 82.44%, GPT-4.1-mini scored 76.22% and 75.11%, and DeepSeek-V3 scored 72.44% and 71.56%.
- Hard problems showed the largest model gaps. GPT-o4-mini scored 80.00% pass@1 in Python and 74.00% in Java; DeepSeek-R1 scored 65.33% and 62.67%; GPT-4.1-mini scored 54.67% and 54.00%; DeepSeek-V3 scored 46.67% and 45.33%.
- Easy problems were near saturation: scores ranged from 97.33% to 100.00% across models and languages.
- In top-p calibration for iterative repair with DeepSeek-R1, ISR@10 was 65.6% at top-p 0.1, 68.8% at 0.3, 68.8% at 0.5, 65.6% at 0.7, and 62.5% at 0.9; the study chose top-p 0.3.
- The excerpt does not give exact ISR@10 values from the 32-problem Challenge Dataset figures. It states that all models improved over single-attempt results, with DeepSeek-R1 and GPT-o4-mini improving more consistently than DeepSeek-V3 and GPT-4.1-mini.
- The paper reports that an added instruction, “Optimize the time complexity of your algorithm,” reduced Java time-limit failures on the 200-problem Strain Dataset, but the excerpt does not provide the exact counts from the figure.

## Link
- [https://arxiv.org/abs/2606.17514v1](https://arxiv.org/abs/2606.17514v1)
