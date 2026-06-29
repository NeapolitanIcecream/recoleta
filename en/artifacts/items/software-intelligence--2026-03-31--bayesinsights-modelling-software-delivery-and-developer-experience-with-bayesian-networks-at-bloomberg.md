---
source: arxiv
url: http://arxiv.org/abs/2603.29929v1
published_at: '2026-03-31T16:02:49'
authors:
- Serkan Kirbas
- Federica Sarro
- David Williams
topics:
- bayesian-networks
- developer-experience
- software-delivery
- causal-modeling
- engineering-analytics
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# BayesInsights: Modelling Software Delivery and Developer Experience with Bayesian Networks at Bloomberg

## Summary
BayesInsights is an internal Bloomberg tool that uses Bayesian networks to connect software delivery metrics and developer experience factors, then lets users run what-if analysis on those links. The paper shows how Bloomberg built the networks from survey data, literature, expert input, and structure-learning algorithms, then tested the tool with senior practitioners.

## Problem
- Engineering dashboards show metrics such as DORA and developer survey scores, but they do not explain why a metric changed or what other metrics a change may affect.
- Software delivery and developer experience data have many confounders, and survey-based software engineering data is noisy, so simple correlation views or data-only causal discovery can give misleading conclusions.
- This matters because teams need a way to find likely root causes, reason about trade-offs, and choose engineering improvements with better evidence.

## Approach
- Bloomberg built two Bayesian networks: one for software delivery performance and one for developer experience, with nodes mapped to internal survey questions and delivery factors.
- The network structure came from a hybrid process: DORA and prior literature for an initial causal graph, an expert survey of 8 DevX specialists to score candidate links, and HC and PC structure-learning algorithms with bootstrap checks as extra validation.
- For the expert survey, 24 possible relationships were rated with weighted scores; links scoring below 0.70 were dropped. This removed 2 relationships and added 3.
- The final models used the expert-refined structures because they had the best BIC compared with HC and PC. Conditional probability tables were then estimated from one internal survey with 20 questions and more than 2,000 responses, using BDeu smoothing for sparse cases.
- The tool exposes the networks through a Django-based client-server app where users click evidence on nodes and see updated probability distributions in real time.

## Results
- Performance tests reported **24 ms average** latency for a single inference request.
- Under **50 concurrent users**, median response time stayed **below 40 ms**, which the authors claim is fast enough for real-time interactive use.
- In user evaluation, **28** senior practitioners attended focus groups and **24** completed the questionnaire.
- **95.8%** of respondents said the tool was useful for identifying delivery challenges at the team or organizational level.
- **75%** found the outputs easy to interpret, **83.3%** said they clearly understood how metric changes propagated through the model, and **70.9%** expressed confidence in the outputs.
- **79.2%** said they would use or recommend BayesInsights; **62.5%** saw value for leadership decisions, **62.5%** for what-if analysis, **50%** for root-cause identification, and **37.5%** for reviewing team practices. The tool is in early access with **7 engineering teams**.

## Link
- [http://arxiv.org/abs/2603.29929v1](http://arxiv.org/abs/2603.29929v1)
