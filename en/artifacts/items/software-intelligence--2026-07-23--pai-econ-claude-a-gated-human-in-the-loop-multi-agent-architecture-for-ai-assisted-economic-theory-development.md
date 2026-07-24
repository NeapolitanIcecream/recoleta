---
source: arxiv
url: https://arxiv.org/abs/2607.21268v1
published_at: '2026-07-23T12:40:47'
authors:
- Chen Zhu
- Xiaolu Wang
- Weilong Zhang
topics:
- multi-agent-systems
- human-ai-interaction
- agent-reliability
- quality-gates
- ai-for-social-science
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# pAI-Econ-claude: A Gated Human-in-the-Loop Multi-Agent Architecture for AI-Assisted Economic Theory Development

## Summary
pAI-Econ-claude is a gated, human-in-the-loop multi-agent workflow for developing economic theory when no automated system can certify correctness. In five matched-task comparisons, blinded evaluators preferred the gated workflow in four tasks, while the authors report improved auditability rather than formal verification.

## Problem
- LLM-generated economic theories can contain canonical-model mismatches, trivial propositions, proof gaps, unsupported welfare interpretations, and unreliable citations.
- These errors matter because economic theory requires judgments about institutions, assumptions, equilibrium concepts, mechanisms, and welfare that cannot be jointly checked by a cheap, machine-readable correctness signal.

## Approach
- The workflow uses specialized agents coordinated through a persistent shared workspace, where each stage writes inspectable records rather than passing only transient messages.
- Nine quality gates target specific failure modes, diagnose problems, and recommend loopbacks without certifying correctness.
- Human checkpoints retain authority over high-cost decisions, especially the equilibrium concept, proposition set, counterexamples, and responses to negative gate verdicts.
- A canonical model library and theory-lineage protocol compare proposed models with named economic traditions before the model is fixed.

## Results
- Across 5 matched economic-theory tasks, 2 blinded evaluators agreed on all 5 pairwise rankings and preferred the full workflow in 4 tasks; the baseline was preferred in 1.
- Mean failure severity decreased from 1.58 with the ungated baseline to 1.16 with the gated workflow, while mean overall usefulness increased from 2.60 to 3.10.
- The largest gain occurred when a reality check rejected a false market-structure premise and proof review prompted revision of a false welfare claim.
- The negative case showed that the workflow could simplify an economically important human-capital mechanism too aggressively; the richer baseline was preferred despite unresolved formal errors.
- The full workflow used 4.6 to 18 times the paired baseline's plan-relative rolling five-hour usage allowance, so the evaluation does not establish cost-effectiveness.
- The evidence supports improved auditability and targeted error interception, not formal correctness certification or reliable autonomous theory development.

## Link
- [https://arxiv.org/abs/2607.21268v1](https://arxiv.org/abs/2607.21268v1)
