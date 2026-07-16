---
source: arxiv
url: https://arxiv.org/abs/2607.13196v1
published_at: '2026-07-14T18:48:20'
authors:
- Suzhen Zhong
- Shayan Noei
- Bram Adams
- Ying Zou
topics:
- agentic-code-review
- code-intelligence
- automated-software-production
- multi-agent-software-engineering
- human-ai-interaction
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# From Human-Centric to Agentic Code Review: The Impact of Different Generations of Generative AI Technology on Review Quality

## Summary
This study examines how LLM and AI-agent participation changes code-review efficiency and quality across 1.02 million pull requests from 207 GitHub projects. Agent-involved reviews were often associated with faster decisions, but review-smell prevalence generally increased, so the evidence does not show a consistent quality improvement.

## Problem
- Code review is a growing bottleneck as AI increases the volume of software changes, but empirical evidence about LLM-assisted and agentic review remains limited.
- The study asks which AI-adoption patterns and human-AI collaboration patterns are associated with review efficiency and quality risks.

## Approach
- The authors analyze reviewed pull requests from projects spanning three project-specific eras: pre-LLM human-centric review, LLM-assisted review, and agentic review.
- They cluster normalized monthly AI-reviewer participation time series with soft-DTW, identifying common adoption trajectories.
- They model review discussions as sequences involving human, LLM, and AI-agent reviewers, then compare review duration per KLOC and six review smells, including Sleeping Review, Review Buddies, Large Changeset, and Lack of Review.
- Logistic regression models assess human-AI collaboration alongside pull-request characteristics, review activity, and reviewer experience; pull-request types are classified with GPT-4.1-mini, which achieved Cohen's kappa of 0.91 on a validation sample.

## Results
- The dataset contains 1.02 million reviewed pull requests from 207 open-source projects selected from 2,490 candidates; AI-reviewer behavior was grouped into three practices: Gradual AI Adoption (46% of projects), Rapid LLM Adoption (22%), and Rapid AI Agent Adoption (32%).
- In Gradual AI Adoption, LLMs reviewed 8% of pull requests in the LLM era and agents 36% in the agent era; normalized review efficiency improved by 2.5 units in the agent era, while overall smell prevalence increased by 2.0 percentage points.
- In Rapid AI Agent Adoption, LLMs reviewed 19% of pull requests and agents 76%; efficiency improved by 4.5 units in the agent era, while smell prevalence increased by 2.5 percentage points.
- Rapid LLM Adoption was associated with worse quality indicators: smell prevalence increased by 8.0 percentage points in the LLM era and 4.4 points in the agent era, while Review Buddies increased by 26.0 and 23.2 points, respectively.
- Reviews initiated by AI agents or involving multiple agents were significantly faster than human-only reviews under Gradual AI Adoption and Rapid AI Agent Adoption, but most LLM- or agent-involving patterns carried higher review-quality risk than human-only review.
- The findings are observational associations based on project-specific era definitions and smell proxies; they do not establish that AI reviewers caused either the efficiency gains or the quality risks.

## Link
- [https://arxiv.org/abs/2607.13196v1](https://arxiv.org/abs/2607.13196v1)
