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
relevance_score: 0.45
run_id: materialize-outputs
language_code: en
---

# The Effect of Code Obfuscation on Human Program Comprehension

## Summary
This paper studies how code obfuscation affects program comprehension through controlled human experiments, using output prediction tasks to measure accuracy and response time. The conclusion is that obfuscation generally makes people slower and less accurate, but its effect does not always increase monotonically with “obfuscation strength,” and it manifests differently in Python and JavaScript.

## Problem
- The paper aims to answer: **how code obfuscation actually affects human program comprehension**, rather than only automated metrics; this matters because the real purpose of obfuscation is precisely to hinder human analysis, reverse engineering, and understanding of code.
- A common existing assumption is that “the stronger the obfuscation, the harder it is for people to understand,” but the authors point out that this may not hold for human cognition; different obfuscation methods (renaming, misleading naming, control-flow rewriting, combinations) may act on different cognitive cues.
- It also addresses cross-language and experience-transfer questions: whether obfuscation has different effects in Python/JavaScript, and whether experience in one language transfers to understanding obfuscated code in another.

## Approach
- The authors designed a human experiment based on **output prediction**: participants were given a function and its input and asked to write the exact output; this allows program comprehension to be measured objectively through correctness/incorrectness and response time.
- They constructed 5 obfuscation levels: L0 original code, L1 semantics-free identifier renaming, L1b adversarially misleading naming, L2 control-flow rewriting/flattening, and L3 renaming + control-flow combination.
- The data came from the Python and JavaScript subsets of **HumanEval-X**; for each language, **10** function snippets were randomly selected, with cyclomatic complexity limited to **4–8**, lines of code **<15**, and semantic equivalence preserved across all obfuscated versions.
- A controlled in-person experiment was conducted with **50** undergraduate computer science students, each completing **12** questions within **75 minutes**; the study recorded accuracy, per-question response time, and self-reported Python/JavaScript experience.
- The authors use dual-process theory to explain the phenomenon: unobfuscated code is more likely to trigger fast heuristics (System 1), while obfuscation forces participants to shift toward slower, more deliberate line-by-line tracing (System 2).

## Results
- Overall, unobfuscated code **L0 had the highest accuracy at 40.46% (53/131)**; the strongest combined obfuscation **L3 had the lowest at 31.09% (37/119)**. Relative to L0, **L1 -1.78%**, **L1b -2.44%**, **L2 -6.31%**, and **L3 -9.37%**, indicating that control-flow obfuscation harms comprehension more than simple renaming.
- Accuracy by level was: **L0 40.46% (53/131)**, **L1 38.68% (41/106)**, **L1b 38.02% (46/121)**, **L2 34.15% (42/123)**, and **L3 31.09% (37/119)**. Based on this, the authors argue that humans are relatively resilient to renaming but more vulnerable to control-flow disruption.
- There were **600** total responses, with an overall accuracy of only **36.5%**, indicating that the task itself was not easy even without obfuscation; obfuscation further “taxes” an already challenging comprehension setting.
- In terms of response time, **L0 averaged 140 seconds**; once obfuscation was introduced (**L1–L3**), average response time **increased by about 1 minute** and remained high, indicating a shift from a fast mode to a more effortful analytic mode.
- In the “fast responses vs. slow responses” comparison, **L2 showed the largest accuracy gap between slow and fast responses, at Δ15.1%**, suggesting that control-flow obfuscation is particularly likely to mislead quick heuristic judgments, but spending more time on step-by-step tracing can partially recover performance.
- The time distributions of correct and incorrect answers show an “optimal moderate thinking” pattern: the median for correct answers was **142.7 seconds**, while the median for incorrect answers was **127 seconds**; however, extremely long times often corresponded to confusion rather than higher accuracy. The paper also notes that under **L3**, even the slow-response group achieved only **34.5%** accuracy, close to the baseline **32.4%**, indicating that combined obfuscation can overwhelm comprehension.

## Link
- [http://arxiv.org/abs/2603.07668v1](http://arxiv.org/abs/2603.07668v1)
