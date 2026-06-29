---
source: arxiv
url: http://arxiv.org/abs/2604.03447v1
published_at: '2026-04-03T20:38:14'
authors:
- Noshin Ulfat
- Ahsanul Ameen Sabit
- Soneya Binta Hossain
topics:
- llm-evaluation
- code-intelligence
- software-artifacts
- trust-calibration
- consistency-detection
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Measuring LLM Trust Allocation Across Conflicting Software Artifacts

## Summary
TRACE measures how LLM software assistants assign trust when code, documentation, signatures, and test context conflict. The paper shows that current models notice documentation problems more reliably than implementation drift, and their confidence usually does not match their actual detection quality.

## Problem
- LLM evaluations for software engineering usually score the final output, such as a generated test or patch, but they do not show whether the model trusted the right artifact while producing it.
- In real software tasks, Javadoc, method signatures, implementations, and test prefixes can disagree; a model can give a plausible answer while relying on the wrong source.
- This matters for correctness-critical workflows because hidden trust errors can pass downstream checks and still encode the wrong behavior.

## Approach
- The paper introduces **TRACE** (Trust Reasoning over Artifacts for Calibrated Evaluation), a framework that asks models to output a structured JSON trust trace over four artifacts: Javadoc, signature, method implementation, and test prefix.
- Each trace includes per-artifact quality scores, pairwise conflict judgments, inconsistency reports with affected-artifact attribution, source-priority rankings, and model confidence.
- The authors build a benchmark of **456** curated Java method bundles from **25** real-world systems, then create **6** perturbation variants per bundle plus the clean version, for **3,192** evaluation instances.
- Perturbations include missing documentation fields, injected Javadoc bugs, injected implementation bugs, and explicit Javadoc–implementation contradictions at **heavy / normal / subtle** severity levels.
- They run **7** models with the same prompts and blind perturbation setup, producing **22,339** valid traces out of **22,344** API calls.

## Results
- Across all seven models, quality penalties mostly stay on the perturbed artifact and increase with severity. For Javadoc bugs, the heavy-to-subtle score gap is **0.152–0.253**; for implementation bugs, it is only **0.049–0.123**.
- Removing both the Javadoc description and `@return` drops Javadoc scores by **-0.300 to -0.463**, while MUT scores change by less than **0.020** and overall scores drop by **-0.109 to -0.155**.
- Models detect explicit documentation bugs at about **67–95%** and Javadoc–MUT contradictions at about **50–91%**.
- When only the implementation drifts while the documentation remains plausible, inconsistency detection falls by about **7–42 percentage points** in the abstract and about **21–43 percentage points** in the RQ2 summary.
- Confidence is poorly calibrated for **6 of 7** models.
- Clean-input baseline calibration varies a lot by model: mean overall score is **0.713** for GPT-4o and Grok 4 Fast Reasoning, versus **0.555** for Claude Sonnet 4.6 on the same base dataset.

## Link
- [http://arxiv.org/abs/2604.03447v1](http://arxiv.org/abs/2604.03447v1)
