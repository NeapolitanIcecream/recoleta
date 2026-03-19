---
source: arxiv
url: http://arxiv.org/abs/2603.03406v1
published_at: '2026-03-03T16:57:14'
authors:
- Jan Miller
topics:
- code-synthesis
- multi-model-collaboration
- code-review
- llm-agents
- benchmarking
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Review Beats Planning: Dual-Model Interaction Patterns for Code Synthesis

## Summary
This paper studies how two models can collaborate to generate better code, with the central conclusion that “review-then-fix” clearly outperforms the common “plan-then-code” approach. On open-source quantized models and commodity GPUs, this pattern reaches 90.2% pass@1 on HumanEval+, surpassing several larger or proprietary models.

## Problem
- The paper addresses the question: **how should two language models interact so they can generate more reliable code than a single model**, which is important for low-cost, on-premise code generation systems.
- The common approach is to have a reasoning model make a plan first and then a code model implement it, but the authors find that this “plan-then-code” setup can **actually steer correct solutions off course** on coding tasks.
- This matters because many software agents and multi-model programming systems default to the “plan → execute” paradigm; if the interaction direction is wrong, system complexity may increase while performance declines.

## Approach
- They use two models with different roles: the **code-specialist model** Qwen2.5-Coder-14B-Instruct and the **general reasoning model** Qwen3-32B, both AWQ 4-bit quantized and run on two A10Gs.
- They compare three dual-model patterns: **plan-then-code** (plan first, then code), **review-then-fix** (code first, then review and fix), and **adversarial dual-generation** (both generate independently and then cross-check).
- The core method is **review-then-fix**: first let the code model write code freely, then have the reasoning model inspect it for bugs against the problem specification, and finally let the code model fix it based on concrete feedback. Put simply, **do not tell the programmer how to write it in advance; instead, point out what is wrong after it is written**.
- The authors also add an optional **retry** variant: using visible doctests/examples from the prompt for compilation and execution checks, feeding errors back to the model after failures, with up to 3 retries; they emphasize that hidden tests are not used, avoiding leakage.
- They further compare HumanEval+ (specification-rich) and MBPP+ (lean specifications) to analyze a key moderating factor: **the more detailed the specification, the more effective the review**.

## Results
- On **HumanEval+**, the standalone code model achieves **78.0%** and the standalone reasoning model **84.1%**; meanwhile, **plan-then-code reaches only 75.6%**, which is **2.4 percentage points lower** than the code-model baseline.
- **review-then-fix (without retry)** reaches **87.8%** on HumanEval+, improving by **+9.8pp** over the code-model baseline; with retry, it reaches **90.2%**, a **+12.2pp** gain over baseline.
- On **HumanEval**, review-then-fix + retry reaches **93.3%**; adversarial debate scores **86.6%** on HumanEval+, better than baseline but worse than review-then-fix.
- Compared with public reference results, the authors’ system achieves **90.2%** on **HumanEval+**, higher than **GPT-4o 87.2%**, **O1 Preview 89.0%**, and **Qwen2.5-Coder-32B FP16 87.2%**; hardware cost is about **$2/hour** (2×A10G).
- Validation across **542 problems** (HumanEval+ 164 + MBPP+ 378) finds that review effectiveness is strongly affected by specification richness: gains are **+9.8pp** on **HumanEval+** but only **+2.3pp** on **MBPP+**; the former is about **4×** the latter, though both still produce net-positive gains.
- Failure analysis shows that, across 164 problems, plan-then-code caused **15 regressions** and only **14 improvements**; the main causes of degradation include **7 cases of missing imports**, **5 cases of algorithm translation errors**, **2 cases of over-engineering**, and **1 case of incorrect variable-name “correction.”**

## Link
- [http://arxiv.org/abs/2603.03406v1](http://arxiv.org/abs/2603.03406v1)
