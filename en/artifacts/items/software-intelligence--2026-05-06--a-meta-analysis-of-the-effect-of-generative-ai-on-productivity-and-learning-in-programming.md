---
source: arxiv
url: https://arxiv.org/abs/2605.04779v1
published_at: '2026-05-06T11:32:25'
authors:
- Sebastian Maier
- "Moritz Gunzenh\xE4user"
- Jonas Schweisthal
- Manuel Schneider
- Stefan Feuerriegel
topics:
- code-intelligence
- ai-coding-assistants
- developer-productivity
- programming-education
- meta-analysis
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# A meta-analysis of the effect of generative AI on productivity and learning in programming

## Summary
This meta-analysis finds that GenAI coding assistants give a moderate productivity gain in programming, with much smaller gains in enterprise and open-source settings. It finds no reliable improvement in programming learning unless students can use AI during the assessment.

## Problem
- Evidence on GenAI coding assistants is mixed across lab studies, open-source projects, enterprise work, and education.
- The question matters because teams may overestimate productivity gains from short controlled tasks, while educators may confuse AI-aided exam performance with retained programming skill.
- The paper measures two outcomes: programming productivity through task time, commits, and lines of code; and learning through exam performance.

## Approach
- The authors searched ACM, arXiv, Scopus, and Web of Science for studies from 2019 to 2025.
- They screened 10,115 records and included 23 studies with 27 effect sizes.
- They compared GenAI-assisted programming against unassisted programming using Hedges' g under random-effects meta-analysis.
- They assessed bias with RoB2 and ROBINS-I.
- They ran moderator analyses for study setting, tool interface, programming language, participant type, randomization, study design, assessment access, and study duration.

## Results
- Productivity: 14 studies produced 16 effect sizes, covering 3,535 participants and 6,355 repositories. The pooled effect was positive and significant: Hedges' g = 0.33, 95% CI [0.09, 0.58], SE = 0.13, p = 0.008.
- Productivity effects varied heavily across studies: I² = 99%, τ² = 0.22, Q(15) = 206.06, p < 0.001.
- Study setting explained about 36% of productivity heterogeneity: lab studies showed g = 0.73, p < 0.001; enterprise studies showed g = 0.19, p = 0.448; open-source studies showed g = 0.01, p = 0.975.
- Learning: 10 studies produced 11 effect sizes with 1,069 participants. The pooled learning effect was small and non-significant: Hedges' g = 0.14, 95% CI [-0.18, 0.47], SE = 0.17, p = 0.389.
- Learning effects also varied: I² = 86%, τ² = 0.25, Q(10) = 54.96, p < 0.001.
- Assessment access drove learning differences: when AI was allowed during assessment, g = 0.76, 95% CI [0.24, 1.28], p = 0.004; when AI was blocked during assessment, g = -0.06, 95% CI [-0.36, 0.24], p = 0.674.

## Link
- [https://arxiv.org/abs/2605.04779v1](https://arxiv.org/abs/2605.04779v1)
