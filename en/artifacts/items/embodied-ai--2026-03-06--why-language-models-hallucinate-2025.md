---
source: hn
url: https://arxiv.org/abs/2509.04664
published_at: '2026-03-06T23:21:25'
authors:
- doener
topics:
- llm-hallucination
- evaluation
- uncertainty
- benchmark-design
- trustworthy-ai
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Why Language Models Hallucinate (2025)

## Summary
This paper explains hallucinations in large language models as behavior jointly induced by training and evaluation mechanisms that encourage "guessing when uncertain," rather than as a mysterious emergent defect. The authors argue that the key to mitigating hallucinations is not just to add new evaluations, but to modify the scoring rules of the benchmarks that currently dominate leaderboards, so that admitting uncertainty is no longer penalized.

## Problem
- The paper aims to answer why even the most advanced language models still generate plausible but incorrect content when uncertain—i.e., "hallucinations"—and why this phenomenon persists.
- This matters because hallucinations undermine system trustworthiness; if training and evaluation continue to reward "guessing" rather than "admitting not knowing," models will be systematically biased toward unreliable responses.
- The authors argue that the root cause lies not only in the models themselves, but also in the incentive imbalance created by modern training pipelines and benchmark scoring methods that favor confidently wrong answers.

## Approach
- The core mechanism is to reduce hallucinations to a simple statistical decision problem: when a model cannot reliably distinguish true statements from false ones, binary classification errors naturally arise during pretraining, and these errors manifest as hallucinations.
- The authors further analyze modern training and evaluation pipelines, pointing out that common benchmark scoring methods reward "answering" more than "expressing uncertainty," causing models, like "students who are good at taking tests," to choose guessing when they do not know.
- Therefore, the paper's main proposal is not to add separate hallucination tests, but to modify the scoring rules of existing dominant leaderboards so that uncertain responses are incorporated into a reasonable scoring mechanism.
- This is a socio-technical mitigation strategy: simultaneously adjusting evaluation culture, benchmark design, and optimization targets to reduce at the source the incentive structure in which "guessing is better than caution."

## Results
- The abstract **does not provide specific quantitative results**; it gives no datasets, metrics, baseline methods, or numerical improvements.
- The strongest concrete theoretical conclusion is that if false statements are indistinguishable from facts in the training signal, then pretrained language models will produce hallucinations under natural statistical pressures.
- Another core conclusion is that hallucinations persist not only because of insufficient model knowledge, but also because existing evaluations optimize models into "good test-takers," where guessing under uncertainty yields higher test scores.
- The paper's main intervention recommendation is to modify the scoring of existing widely used benchmarks that are misaligned with truthfulness goals, rather than merely adding extra hallucination evaluations; the abstract does not report any quantified improvement from this proposal.

## Link
- [https://arxiv.org/abs/2509.04664](https://arxiv.org/abs/2509.04664)
