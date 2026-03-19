---
source: arxiv
url: http://arxiv.org/abs/2603.03406v1
published_at: '2026-03-03T16:57:14'
authors:
- Jan Miller
topics:
- code-synthesis
- multi-llm
- code-review
- planning-vs-review
- benchmarking
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Review Beats Planning: Dual-Model Interaction Patterns for Code Synthesis

## Summary
This paper studies how two language models can collaborate on code generation, with the core conclusion that “plan first, then write code” does not work well, while “write code first, then review and fix” is significantly stronger. Using two quantized open-source models on low-cost hardware, the authors achieve code benchmark results close to or even exceeding some proprietary models.

## Problem
- The paper aims to answer: **how should two language models with different strengths interact to generate better code than a single model**.
- This matters because many real-world deployments can only use smaller, quantized, locally runnable models, whose single-model performance is often insufficient, making model composition necessary to improve quality.
- The authors challenge a common assumption: whether having a “reasoning model plan first and a coding model implement afterward” is actually effective; experiments show it is not only unhelpful, but can even turn originally correct solutions into wrong ones.

## Approach
- The core method is **review-then-fix**: first let the code-specialized model freely generate a solution, then let the reasoning model act like a code reviewer to find bugs against the problem specification, and finally have the coding model revise based on specific feedback.
- Put simply: **do not teach it how to write before it writes; instead, point out what is wrong after it finishes**; specific error feedback is easier to execute correctly than abstract planning.
- The authors compare three modes: raw-coder single model, plan-then-code (plan first, then write), and review-then-fix (write first, then review), and additionally test a version with visible-test retries and an adversarial dual-generation setup with “two models generating independently and then cross-validating.”
- All experiments use the same models and hardware: Qwen2.5-Coder-14B-Instruct + Qwen3-32B, both in 4-bit AWQ, deployed on 2×A10G, at a cost of about **$2/hr**.
- The authors also identify a key moderating variable: **specification richness**. If the problem statement is richer (with more types, docstrings, examples, and boundary conditions), the review model can more accurately identify bugs, so the review mechanism yields greater gains.

## Results
- On **HumanEval+ (164 problems)**, raw-coder achieves **78.0% pass@1**; **plan-then-code reaches only 75.6%**, a **drop of 2.4 percentage points** relative to the baseline; meanwhile **review-then-fix reaches 87.8%**, a **gain of 9.8 percentage points** over the baseline.
- With retries based on visible docstring tests, **review-then-fix (+retry)** reaches **90.2% on HumanEval+**, which is **+12.2pp** over raw-coder; it is also higher than **GPT-4o 87.2%** and **O1 Preview 89.0%** listed in the paper.
- On **HumanEval**, the corresponding results are: raw-coder **81.1%**, plan-then-code **80.5%**, review-then-fix **89.6%**, review-then-fix (+retry) **93.3%**, and adversarial debate **91.5%**.
- Cross-benchmark validation shows that the benefit of review depends strongly on the quality of the problem specification: on richly specified **HumanEval+**, review-then-fix improves over baseline by **+9.8pp (78.0%→87.8%)**; on more sparsely specified **MBPP+ (378 problems)**, it improves by only **+2.3pp (67.5%→69.8%)**, about **4× smaller**, though still a net positive gain.
- “Specification enhancement” does not truly close this gap: on HumanEval+, enriched review is only **+0.6pp (87.8%→88.4%)** better than regular review; on MBPP+, there is **no improvement** (**69.8% vs 69.8%**).
- Failure mode analysis shows that on 164 problems, plan-then-code causes **15 regressions** and only **14 improvements**; the main errors include **7 cases of missing imports**, **5 cases of algorithm implementation deviation**, **2 cases of over-engineering**, and **1 case where “correcting” a variable name caused a signature error**.

## Link
- [http://arxiv.org/abs/2603.03406v1](http://arxiv.org/abs/2603.03406v1)
