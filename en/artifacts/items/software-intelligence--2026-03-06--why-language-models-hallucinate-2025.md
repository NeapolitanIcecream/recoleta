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
relevance_score: 0.59
run_id: materialize-outputs
language_code: en
---

# Why Language Models Hallucinate (2025)

## Summary
The paper explains language model hallucinations as behavior jointly induced by training and evaluation procedures that encourage "guessing when uncertain," rather than as some mysterious defect. Its core claim is: if benchmark scoring continues to reward correct guesses while penalizing admitting uncertainty, hallucinations will persist systematically.

## Problem
- The paper aims to address: **why language models produce plausible but incorrect statements (hallucination)**, and why this phenomenon still exists even in the most advanced systems.
- This matters because hallucinations undermine users' trust in models; in high-stakes or knowledge-intensive tasks, confident errors are more dangerous than explicitly saying "I don't know."
- The authors argue that the problem does not stem only from insufficient model capability, but also from modern training and leaderboard evaluation mechanisms themselves: they often **reward guessing rather than expressing uncertainty**.

## Approach
- The authors propose a simplified mechanistic explanation: hallucinations can essentially be viewed as **binary classification errors**—when a model fails to distinguish false statements from true facts, incorrect outputs naturally arise during pretraining.
- The paper analyzes the modern training pipeline from a statistical perspective, arguing that when data and objective functions do not adequately reward "uncertainty / abstention," the optimal strategy shifts toward generating answers that are "possibly correct" rather than admitting not knowing.
- Furthermore, the authors point out that most evaluations are like "exam grading": giving a guessed answer usually earns a higher score than leaving it blank or indicating uncertainty, so models are optimized into "good test-takers" that guess.
- Based on this analysis, the paper argues that the key to mitigating hallucinations is not to add more new hallucination tests, but to **modify the scoring rules of existing mainstream benchmark** so that uncertain responses are no longer systematically penalized.

## Results
- The excerpt **does not provide specific experimental numbers, dataset names, metric improvements, or quantitative comparisons with baselines**.
- The strongest qualitative conclusion is that hallucinations "need not be mysterious"; they can be explained jointly by **binary classification errors + statistical pressure + misaligned evaluation incentives**.
- The authors claim that hallucinations persist because many current mainstream evaluations make "guessing when uncertain" yield better test scores.
- The paper's main intervention recommendation is a **socio-technical mitigation**: prioritize rewriting the scoring of existing benchmark that dominate leaderboards, rather than separately introducing more hallucination evaluations.

## Link
- [https://arxiv.org/abs/2509.04664](https://arxiv.org/abs/2509.04664)
