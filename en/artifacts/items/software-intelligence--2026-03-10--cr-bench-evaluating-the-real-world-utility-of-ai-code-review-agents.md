---
source: arxiv
url: http://arxiv.org/abs/2603.11078v1
published_at: '2026-03-10T21:29:42'
authors:
- Kristen Pereira
- Neelabh Sinha
- Rajat Ghosh
- Debojyoti Dutta
topics:
- code-review
- benchmarking
- llm-evaluation
- software-engineering
- agent-evaluation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# CR-Bench: Evaluating the Real-World Utility of AI Code Review Agents

## Summary
This paper introduces **CR-Bench** and **CR-Evaluator** to more realistically assess the ability of AI code review agents to detect defects in real PRs. The core conclusion is that looking only at “how many bugs are found” is misleading, because code review agents exhibit a significant **recall–noise** trade-off.

## Problem
- Existing code review evaluations often lack standardized, fine-grained benchmarks grounded in real repositories, making it difficult to judge the true utility of agents in open-ended PR review.
- Unlike compilation/testing, code review has no clear objective pass/fail signal; if an agent pursues high recall by generating many false positives, it directly harms developer experience and adoption.
- Prior datasets often mix subjective style issues with objective defects, and many tasks are too small-scale or synthetic to reflect the key challenges of multi-file, large-repository settings.

## Approach
- Build **CR-Bench**: converted from **SWE-Bench** into real PR-level code review data, retaining only objective defects that could reasonably be discovered during code review; it provides **584** tasks, plus a manually strengthened and verified subset of **CR-Bench-verified 174** tasks.
- Preserve full PR context for each sample, and annotate **category / impact / severity** to support analysis by defect type and risk.
- Propose **CR-Evaluator**: using LLM-as-a-judge to classify agent comments into **Bug Hit / Valid Suggestion / Noise**.
- In addition to traditional **Precision / Recall / F1**, add **Usefulness Rate** and **SNR** to explicitly measure the developer acceptability of the “share of useful feedback” and “signal relative to noise.”
- Conduct preliminary experiments with two agent paradigms: **single-shot** (one-pass direct review) and **Reflexion** (iterative self-reflection to fill gaps), and compare them on **GPT-5.2** and **GPT-5-mini**.

## Results
- Dataset scale and positioning: **CR-Bench = 584**, **CR-Bench-verified = 174**; compared with prior benchmarks, the authors emphasize that this is the first code review benchmark focused on **objective defect detection**, preserving **full PR context**, and providing joint evaluation with **P/R/F1/Usefulness/SNR**.
- Dataset complexity: CR-Bench averages **10.28** fix lines, **41.03** PR comments, and a PR description length of **906.63** per sample; the verified subset has **8.69 / 35.83 / 893.59**, respectively, indicating that the tasks come from larger-scale real repositories.
- Verified subset distribution: **79.9%** are Structural Bugs, and **93.1%** of defects are **Medium/High severity**; in the full CR-Bench, **90.2%** of defects are **Medium/High/Critical**, indicating that the benchmark is skewed toward high-risk, production-grade issues.
- **Single-shot + GPT-5.2**: **Recall 27.01%**, **Precision 3.56%**, **F1 6.30%**, **Usefulness 83.63%**, **SNR 5.11**; the authors interpret this as lower noise and higher developer trust.
- **Reflexion + GPT-5.2**: **Recall 32.76%**, **Precision 5.10%**, **F1 8.83%**, **Usefulness 66.10%**, **SNR 1.95**; relative to single-shot, recall improves by **5.75** percentage points (from **27.01%** to **32.76%**), but the signal-to-noise ratio drops significantly.
- The same trade-off appears on **GPT-5-mini**: single-shot achieves **Recall 18.39% / SNR 2.89**, while Reflexion reaches **Recall 27.59% / SNR 0.91**. Overall, the paper’s key finding is not that one agent is “uniformly stronger,” but that code review agents are constrained by a frontier of “finding more bugs vs. generating more noise.”

## Link
- [http://arxiv.org/abs/2603.11078v1](http://arxiv.org/abs/2603.11078v1)
