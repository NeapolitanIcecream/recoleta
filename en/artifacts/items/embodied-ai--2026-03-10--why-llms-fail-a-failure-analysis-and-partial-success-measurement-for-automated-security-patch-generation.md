---
source: arxiv
url: http://arxiv.org/abs/2603.10072v1
published_at: '2026-03-10T05:34:56'
authors:
- Amir Al-Maamari
topics:
- llm-security
- automated-program-repair
- vulnerability-patching
- failure-analysis
- benchmarking
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Why LLMs Fail: A Failure Analysis and Partial Success Measurement for Automated Security Patch Generation

## Summary
This paper systematically evaluates why LLMs fail at automatically generating security patches. The conclusion is that the models mostly do not fail because they cannot write Java, but because they do not truly understand how the vulnerability should be fixed. The authors also propose a continuous metric, SRS, to measure the degree of being "partially fixed but not fully correct."

## Problem
- The paper addresses the question: **How reliable are LLM-generated security patches, how do they typically fail, and are there cases where they come close to fixing the issue**.
- This matters because traditional testing only checks whether functionality passes; **a patch can pass tests yet still leave an exploitable vulnerability**, allowing it to masquerade as a "correct fix" in CI/CD.
- Security repair differs from ordinary program repair in that it must simultaneously be **compilable, non-exploitable, and preserve original functionality**, which existing APR evaluations often fail to fully capture.

## Approach
- The authors evaluate **64 reproducible Java vulnerabilities** from **Vul4J**, using **Gemini 3.0 Flash** in a **zero-shot** setting to generate **5 patches** per vulnerability, yielding **319 valid patches** in total.
- They use a **three-axis evaluation**: (1) whether the patch compiles; (2) whether it truly fixes the security issue (PoV exploit tests + Semgrep static scanning); and (3) whether it preserves functionality (developer test suites).
- The patches are divided into five categories: **Correct & Secure, Compilation Error, Security Failure, Functionality Failure, Insecure & Breaking**, enabling analysis of failure modes.
- They propose the **Security Repair Score (SRS)**: only patches that compile are scored, and then the **security score** and **functionality score** are weighted equally at 50%, with a range from 0 to 1, to characterize "partial success."
- They further analyze which factors predict repair difficulty, including **CWE type, lines of code, cyclomatic complexity, and human patch size**.

## Results
- Among **319** patches, only **79 (24.8%)** are fully correct; **164 (51.4%)** fail on both security and functionality; **42 (13.2%)** fail to compile; **33 (10.3%)** preserve functionality but remain insecure; and **1 (0.3%)** is secure but breaks functionality.
- The main cause of failure is **semantic misunderstanding / incorrect repair strategy**, not syntax problems: the compilation rate reaches **86.8%**, but the correct repair rate is only **24.8%**. The authors note that **143 (44.8%)** patches use the wrong strategy and alter program behavior, **17 (5.3%)** violate API contracts, and **4 (1.3%)** over-fix.
- The continuous metrics show that the model is better at **preserving functionality** than **fixing security**: the **mean Functionality Score is 0.832**, the **mean Security Score is 0.251**, a gap of about **3.3×**; the **mean SRS is 0.542**, with a median of **0.499**.
- The SRS shows a **bimodal distribution**: **79 (24.8%)** are perfect successes (**SRS=1.0**), only **1 (0.3%)** is a near-success (**0.8≤SRS<1.0**), **188 (58.9%)** are merely partial successes, and **51 (16.0%)** are complete failures. Based on this, the authors argue that security patch generation is more like "all or nothing" rather than something that can easily approach the correct answer through small revisions.
- There is **no significant trade-off** between security and functionality: the correlation is **r = 0.267, p > 0.05**, indicating that fixing security does not necessarily come at the cost of breaking functionality; failure looks more like a failure to understand the essence of the vulnerability.
- Different vulnerability types vary greatly: **CWE-835 (Infinite Loop)** has a repair rate of **45%** and **SRS 0.725**; **CWE-611 (XXE)** has a repair rate of **40%** and a compilation rate of **80%**; **CWE-20 (Input Validation)** has a compilation rate of **95%** but a repair rate of **0%**; **CWE-264 (Permissions)** has **35%** of patches that are "functionally correct but still insecure," far above the overall **10.3%**. In addition, human patch size is significantly negatively correlated with success rate: **Spearman ρ = -0.331, p = 0.008**.

## Link
- [http://arxiv.org/abs/2603.10072v1](http://arxiv.org/abs/2603.10072v1)
