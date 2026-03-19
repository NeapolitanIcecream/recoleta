---
source: arxiv
url: http://arxiv.org/abs/2603.07668v1
published_at: '2026-03-08T15:02:47'
authors:
- Anh H. N. Nguyen
- Jack Le
- Ilse Lahnstein Coronado
- Tien N. Nguyen
topics:
- code-obfuscation
- program-comprehension
- human-study
- output-prediction
- software-security
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# The Effect of Code Obfuscation on Human Program Comprehension

## Summary
This paper studies how code obfuscation affects human understanding of programs, focusing on accuracy and response time in output-prediction tasks. The conclusion is that obfuscation generally makes people slower and more error-prone, but the idea that “stronger obfuscation always means greater difficulty” does not always hold monotonically, and Python and JavaScript show different patterns.

## Problem
- The paper aims to answer: **how code obfuscation actually affects human program comprehension**, not just automated metrics; this matters because the real purpose of obfuscation is precisely to make reverse engineering and understanding harder for humans.
- A common existing assumption is that “the stronger the obfuscation, the harder it is for people to understand,” but the authors point out that this may not always hold for humans; different obfuscation methods (renaming, misleading naming, control-flow rewriting) may operate through different mechanisms.
- It also asks whether this effect differs by language, and whether programming experience transfers across languages when understanding obfuscated code.

## Approach
- The authors designed a controlled human-subject experiment in which participants were given Python/JavaScript functions and inputs and asked to perform **output prediction**, while correctness, time taken, and self-reported language experience were recorded.
- They constructed 5 obfuscation levels: L0 original code, L1 uninformative renaming, L1b adversarial renaming with semantic but misleading names, L2 control-flow rewriting/flattening, and L3 a combination of renaming and control-flow transformations.
- The data came from the Python and JavaScript subsets of HumanEval-X, with 10 short but nontrivial functions sampled for each language; a total of 50 undergraduate CS students participated, each completing 12 questions, for 600 responses overall.
- The core mechanism of the method can be put simply: **by gradually increasing surface-level “misdirection” in the code and structural “detours,” the study examines whether people are forced to shift from fast, intuitive reading to slow, step-by-step tracing-based reasoning.**
- The authors interpret the findings using dual-process theory: unobfuscated code is easier to approach with fast heuristics (System 1), while obfuscated code—especially control-flow obfuscation—pushes people into slower, more effortful System 2 reasoning.

## Results
- The baseline L0 had the highest accuracy at **40.46% (53/131)**; the levels were **L1: 38.68% (41/106)**, **L1b: 38.02% (46/121)**, **L2: 34.15% (42/123)**, and **L3: 31.09% (37/119)**. Relative to L0, the declines were **-1.78%**, **-2.44%**, **-6.31%**, and **-9.37%**, respectively.
- The combined obfuscation **L3** was the hardest, indicating that stacking renaming and control-flow rewriting significantly increases comprehension burden; the authors also note that the largest accuracy drop was from **L1b to L2**, at **3.87 percentage points**, suggesting that control-flow obfuscation harms comprehension more than misleading naming alone.
- Overall performance across all participants was **36.5% correct (600 responses)**, showing that the task itself was already not easy; therefore, the drop from **40.46%** to **31.09%** represents a substantial and practically meaningful loss in human comprehension.
- In terms of response time, L0 averaged about **140 seconds**; after introducing obfuscation, **L1–L3 increased average time by about 1 minute**, supporting the claim that obfuscation pushes people from fast heuristics toward slower, more deliberate reasoning.
- In the fast/slow response groups, the slow group for **L2** had an accuracy rate **15.1 percentage points** higher than the fast group, showing that control-flow obfuscation is especially likely to make quick intuition fail, though investing more time can still recover some accuracy.
- The median response time for correct answers was **142.7 seconds**, versus **127 seconds** for incorrect answers; however, the authors emphasize that the relationship is not linear: taking somewhat longer is usually better, but **extremely long times** often indicate confusion rather than higher accuracy.

## Link
- [http://arxiv.org/abs/2603.07668v1](http://arxiv.org/abs/2603.07668v1)
