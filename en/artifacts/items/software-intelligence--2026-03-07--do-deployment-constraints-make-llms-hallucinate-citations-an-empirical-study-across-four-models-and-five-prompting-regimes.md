---
source: arxiv
url: http://arxiv.org/abs/2603.07287v1
published_at: '2026-03-07T17:14:05'
authors:
- Chen Zhao
- Yuan Tang
- Yitian Qian
topics:
- llm-reliability
- citation-hallucination
- empirical-evaluation
- software-engineering
- bibliographic-verification
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Do Deployment Constraints Make LLMs Hallucinate Citations? An Empirical Study across Four Models and Five Prompting Regimes

## Summary
This paper investigates whether common deployment-time prompting constraints make large language models more likely to generate unverifiable academic citations, with a focus on evidence review scenarios such as software engineering. Under a closed-book setting, the authors systematically compare 4 models across 5 prompting conditions and find that the stronger the constraints, the worse citation verifiability tends to be; moreover, “looking correctly formatted” does not mean the cited work actually exists.

## Problem
- The paper addresses the question of whether LLMs, when generating academic text and references, produce more severe citation hallucinations under real deployment constraints such as **temporal restrictions, survey-style breadth requirements, and non-disclosure policies**.
- This matters because systematic reviews, related-work writing, and evidence synthesis in software engineering rely heavily on real literature; if fake citations enter the toolchain, they can contaminate research conclusions and automated workflows.
- Prior work has mostly examined only a single prompting setup or used a binary true/false citation distinction, which cannot reveal the middle ground of citations that are “hard to verify but high risk.”

## Approach
- The authors build a **closed-book citation generation benchmark**: for 144 academic claims (24 of them from SE & CS), they prompt 4 models under 5 conditions to generate academic paragraphs and structured references, yielding **2,880 runs and 17,443 citations** in total.
- The 4 models are **Claude Sonnet, GPT-4o, LLaMA 3.1–8B, Qwen 2.5–14B**; the 5 conditions are **Baseline, Temporal, Survey, Non-Disclosure, Combo**.
- The core mechanism is simple: each citation produced by a model is parsed into title/author/year/venue/DOI, then the system searches **Crossref + Semantic Scholar** for the closest candidate, scores it with weighted similarity, and assigns it to one of three categories: **Existing / Unresolved / Fabricated**.
- The verification pipeline is deterministic; a manual audit of 100 sampled citations shows an overall agreement rate of **75%** with human labels, with **Cohen's κ = 0.63**. A substantial portion of the *Unresolved* category is actually fabricated, so the authors retain it as a separate category rather than forcing a binary classification.

## Results
- **No model under any condition achieves a citation-level existence rate above 0.50**; the highest value in the paper is only **0.475 [0.425, 0.523] for Claude Sonnet under the Survey condition**. This means that even in the best case, fewer than half of citations can be verified as real.
- **Temporal constraints are the most damaging**: Claude Sonnet drops from **0.381 → 0.119** (Δ **-0.261**, 95% CI **[-0.317,-0.207]**); GPT-4o from **0.235 → 0.019** (Δ **-0.216**, CI **[-0.266,-0.168]**); Qwen from **0.090 → 0.014**; LLaMA from **0.068 → 0.011**. At the same time, the temporal violation rate remains very low (**0.001–0.026**), indicating that the models “follow the format/year requirements” while still inventing citations.
- **The Survey condition widens the gap between proprietary and open-weight models**: this gap reaches its maximum under Survey, at Δ **+0.310**, 95% CI **[0.274, 0.349]**. Claude Sonnet actually rises from **0.381 to 0.475** (Δ **+0.094**), while Qwen falls to **0.020**, with its fabricated rate reaching the study-wide maximum of **0.547**.
- **Non-Disclosure has a milder effect, but shifts errors toward the “hard to verify” category**: for example, Claude Sonnet existence changes from **0.381 → 0.349**, while unresolved changes from **0.462 → 0.487**; GPT-4o has Δ **-0.060** (CI **[-0.119,-0.001]**). The authors also note that reduced DOI completeness weakens verification signals.
- **Combo is the worst condition**: Claude Sonnet existence is **0.106**; GPT-4o **0.005**; LLaMA **0.008**; Qwen **0.001**. Meanwhile, the models still output **7.38–7.99** citations per prompt on average, indicating that under even worse verifiability they continue to “confidently produce more citations.”
- **Unresolved is the largest risk bucket**: across cells, unresolved accounts for **36–61%**. The manual audit shows that among 35 unresolved citations, **16 are actually fabricated, 4 are existing, and only 15 are truly unresolved**; if redistributed by this proportion, the fabricated rate would rise to **0.33–0.75**, suggesting that the reported fabrication rates may still be conservative.
- In terms of software-engineering relevance, the **SE & CS group** (24 claims, **2,926 citations**) has an overall existence rate of **0.132**, close to the all-domain average of **0.120**; among them, **Claude Sonnet reaches 0.349 on SE & CS**, while both open-weight models are **below 0.10**. The authors therefore argue that in SE literature reviews and toolchains, LLM outputs must undergo **post-hoc citation verification** before entering downstream use.

## Link
- [http://arxiv.org/abs/2603.07287v1](http://arxiv.org/abs/2603.07287v1)
