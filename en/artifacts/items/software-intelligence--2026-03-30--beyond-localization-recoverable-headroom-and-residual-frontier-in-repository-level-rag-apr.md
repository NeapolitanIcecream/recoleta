---
source: arxiv
url: http://arxiv.org/abs/2603.29067v1
published_at: '2026-03-30T23:10:19'
authors:
- Pengtao Zhao
- Boyang Yang
- Bach Le
- Feng Liu
- Haoye Tian
topics:
- automated-program-repair
- repository-level-rag
- swe-bench
- code-generation
- fault-localization
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Beyond Localization: Recoverable Headroom and Residual Frontier in Repository-Level RAG-APR

## Summary
This paper studies repository-level automated program repair after fault localization is made much stronger. On SWE-bench Lite, it finds that oracle localization helps Agentless, KGCompass, and ExpeRepair, but large repair gaps remain and prompt-level context fusion recovers only a small part of the unsolved frontier.

## Problem
- Repository-level APR papers often treat better localization as the main route to better repair, but end-to-end scores mix together localization, prompt construction, patch generation, and validation.
- That makes it hard to tell what still limits performance after the right files and lines are already known.
- This matters because the next research step depends on the bottleneck: retrieval, evidence packaging, interface design, or patch synthesis.

## Approach
- The paper runs a controlled study on **SWE-bench Lite (300 instances)** with three repository-level RAG-APR systems: **Agentless, KGCompass, and ExpeRepair**.
- It injects **Oracle Localization** by giving each system gold-patch-derived pre-patch file and line spans, while keeping each system's own downstream prompt construction and repair pipeline.
- It measures remaining search headroom with **Best-of-K**, using **K = 10** sampled patch candidates and ideal selection inside that fixed pool.
- It tests added context under two fixed interfaces with control conditions: same-token filler prompts and same-repository hard negatives, to separate useful evidence from prompt-length effects.
- It also runs a **common-wrapper oracle check** to see how much oracle gains depend on each system's repair wrapper and prompt builder.

## Results
- **Oracle Localization improves all three systems, but none reaches 50% success in the native pipeline.** Agentless goes from **84/300 (28.0%)** to **121/300 (40.3%)**; KGCompass from **88/300 (29.3%)** to **129/300 (43.0%)**; ExpeRepair from **98/300 (32.7%)** to **117/300 (39.0%)**.
- **Completion rates also rise** under oracle localization: Agentless **84.7% -> 99.0%**, KGCompass **90.0% -> 98.7%**, ExpeRepair **92.0% -> 98.0%**. The paper states that **61.6% to 79.3%** of the total success gain comes from higher pass rates among completed runs, not only from more runs finishing.
- **Paired gains are positive but not monotonic.** Oracle-only wins vs baseline-only wins are **46/9** for Agentless, **54/13** for KGCompass, and **43/24** for ExpeRepair. Reported paired risk differences are **+12.3 points**, **+13.7 points**, and **+6.3 points**.
- **Backbone check with GPT-4.1 shows the same pattern.** Agentless improves from **74/300** to **109/300** with oracle localization, and KGCompass from **55/300** to **126/300**; paired wins/losses are **40/5** and **78/7**.
- **Wrapper choice changes results a lot for Agentless.** In the shared-wrapper check, Agentless moves from **35.7%** to **37.0%** with shared oracle, but reaches **51.0%** with a shared-builder oracle. KGCompass goes **17.0% -> 50.3% -> 51.0%**, and ExpeRepair **40.3% -> 51.3% -> 51.0%**.
- The abstract reports that **Best-of-K headroom exists but saturates quickly**, and that the **best fixed added-context probe solves only 6 extra instances** beyond the native three-system **Solved@10 union**. The excerpt does not include the full RQ2-RQ4 tables, so more detailed quantitative results for search saturation and context probes are not available here.

## Link
- [http://arxiv.org/abs/2603.29067v1](http://arxiv.org/abs/2603.29067v1)
