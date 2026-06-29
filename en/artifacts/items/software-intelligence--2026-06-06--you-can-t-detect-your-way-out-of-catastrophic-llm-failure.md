---
source: hn
url: https://github.com/joseteiadirector/teia-igo-vs-claude-opus-4.8/blob/main/README.en.md
published_at: '2026-06-06T23:25:17'
authors:
- joseteia26
topics:
- llm-safety
- ai-governance
- failure-containment
- model-monitoring
- red-teaming
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# You can't detect your way out of catastrophic LLM failure

## Summary
The paper argues that LLM safety cannot rely on detection alone for catastrophic actions; systems need containment that makes ruinous actions unreachable. It presents Observational Governance Infrastructure (IGO) with public KAPI formulas, production measurements, and a recorded stress test with Claude Opus 4.8.

## Problem
- It addresses catastrophic LLM failure where a harmful action can happen before monitoring metrics detect the jump.
- This matters for AI agents and automated systems because some errors are recoverable, while actions involving irreversible harm need a hard operating boundary.
- The paper separates routine model drift and hallucination detection from ruin-risk control, where a second learning cycle may arrive too late.

## Approach
- IGO uses a 4-layer architecture: Layers 1-3 monitor recoverable failures, while Layer 4 contains actions that must remain out of reach.
- The core metric shown in the excerpt is CPI: `CPI = max(0, 100 - (σ_temporal × 2))`, where temporal confidence variance lowers the score.
- CPI bands are public: above 80 means stable, below 50 means critical cognitive volatility.
- The study combines public formulas on Zenodo, production database measurements, and an epistemic red-team debate with Claude Opus 4.8.
- In simple terms, the method watches model instability where recovery is possible and blocks high-consequence actions where recovery is unacceptable.

## Results
- The authors report KAPI measurements across 4 documented institutions in public health, higher education, and design, using database data with no simulated or estimated values.
- The audits covered 4 global LLMs; public client-level data is anonymized or aggregated.
- CPI reportedly ranged from about 22 to 55 across production cases, which sits below the stated stable band of greater than 80 and near or below the critical threshold of 50.
- Native hallucination detection reportedly caught serious errors, including one Claude error graded HIGH.
- Claude Opus 4.8 reportedly conceded 3 theses during the recorded stress test: hash-like unpredictability, sufficiency of derivative detection, and parity between detection and containment.
- The paper claims the main result is an architectural boundary: detection handles recoverable failures, while Layer 4 containment handles ruin-risk actions.

## Link
- [https://github.com/joseteiadirector/teia-igo-vs-claude-opus-4.8/blob/main/README.en.md](https://github.com/joseteiadirector/teia-igo-vs-claude-opus-4.8/blob/main/README.en.md)
