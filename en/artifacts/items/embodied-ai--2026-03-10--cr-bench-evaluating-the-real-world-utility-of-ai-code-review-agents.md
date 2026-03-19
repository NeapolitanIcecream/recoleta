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
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# CR-Bench: Evaluating the Real-World Utility of AI Code Review Agents

## Summary
This paper introduces **CR-Bench** and **CR-Evaluator** to more realistically assess the utility of AI code review agents in actual development, rather than only checking whether they “found issues.” The core conclusion is that code review agents exhibit a clear **recall–noise** trade-off: higher coverage often comes with more false positives, undermining developer trust and productivity.

## Problem
- Existing code review evaluations lack unified, fine-grained benchmarks grounded in realistic PR scenarios, making it difficult to measure the value of agents in real workflows.
- Looking only at resolution rate or hit rate obscures a key issue: **when false positives are frequent, the developer experience degrades significantly**, and this cost is especially high in code review.
- Existing benchmarks often mix subjective style issues with objective defects, and frequently lack full PR or multi-file context, making them insufficient for evaluating real defect detection ability.

## Approach
- Construct **CR-Bench**: a code review dataset converted from SWE-Bench, transforming real repository bug-fix cases into tasks asking whether they should have been caught during the PR review stage.
- Use Git blame and the GitHub API to trace linked PRs, then use an LLM to filter defects that are **detectable during code review**; the final dataset contains **CR-Bench 584** entries and a human-strengthened verified subset, **CR-Bench-verified 174** entries.
- Generate review comment targets and a labeling scheme for each sample, covering **bug category / impact / severity**, with a focus on more objective defect-identifying reviews involving functionality, performance, reliability, security, and similar concerns.
- Propose **CR-Evaluator**: using LLM-as-a-judge to classify agent comments into **Bug Hit / Valid Suggestion / Noise**, and compute **Recall, Precision, F1, Usefulness Rate, SNR**.
- Evaluate two classes of agents under this framework: **single-shot** one-pass review and **Reflexion** iterative reflective review, each paired with GPT-5.2 and GPT-5-mini.

## Results
- In terms of dataset scale, the authors claim CR-Bench is the first code review benchmark **focused on objective defect detection and containing full PR context**: **CR-Bench 584** entries and **CR-Bench-verified 174** entries.
- In terms of dataset complexity, CR-Bench averages **10.28** fix lines, **41.03** PR comments, and a PR description length of **906.63** per instance; the verified set has **8.69 / 35.83 / 893.59**, respectively, indicating substantial real-world contextual complexity.
- In the verified set’s defect distribution, **79.9%** are Structural Bugs and **93.1%** are medium-to-high severity; in the full set, **90.2%** are Medium/High/Critical, showing that the evaluation focuses on high-risk real defects.
- On **CR-Bench-verified**, **Single-shot + GPT-5.2** achieves the highest **SNR 5.11** and **Usefulness 83.63%**, but only **Recall 27.01% / Precision 3.56% / F1 6.30%**, indicating that the comments are overall “cleaner” but miss more issues.
- **Reflexion + GPT-5.2** achieves the highest **Recall 32.76%**, **Precision 5.10%**, and **F1 8.83%**; compared with single-shot, recall improves from **27.01% to 32.76%**. However, **Usefulness drops to 66.10%** and **SNR drops to 1.95**, showing that higher coverage comes with more noise.
- For the weaker model, **Single-shot + GPT-5-mini** scores **Recall 18.39% / Precision 3.51% / F1 5.90% / Usefulness 74.29% / SNR 2.89**; **Reflexion + GPT-5-mini** scores **27.59% / 3.19% / 5.72% / 47.72% / 0.91**. The strongest takeaway is: **pushing agents to “find more bugs” significantly lowers the signal-to-noise ratio, so real-world usability cannot be judged by recall alone.**

## Link
- [http://arxiv.org/abs/2603.11078v1](http://arxiv.org/abs/2603.11078v1)
