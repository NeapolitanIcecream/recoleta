---
source: arxiv
url: https://arxiv.org/abs/2606.18733v1
published_at: '2026-06-17T06:22:28'
authors:
- Qiao Zhao
- JianYing Qu
- Jun Zhang
- Yehua Yang
- Hanwen Du
- Zhongkai Sun
topics:
- software-engineering-agents
- code-agent-benchmarks
- synthetic-data-generation
- benchmark-contamination
- software-evolution
- multi-agent-task-construction
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# SWE-Future: Forecast-Conditioned Data Synthesis for Future-Oriented Software Engineering Agents

## Summary
SWE-Future generates coding-agent tasks by forecasting likely future repository work, then using validated forecast families to synthesize executable tasks. It aims to keep GitHub-repository realism while reducing direct replay of public pull requests.

## Problem
- Many coding-agent benchmarks replay public GitHub issues and pull requests, which raises contamination risk when those artifacts enter pretraining, fine-tuning, synthetic data, or benchmark selection.
- Fully synthetic tasks avoid direct replay, but they can miss real repository needs, project conventions, dependency limits, and maintainer priorities.
- The paper targets realistic future-oriented tasks for software engineering agents without turning later pull requests into task prompts or reference solutions.

## Approach
- For each repository, SWE-Future builds an evidence bundle from issues, pull requests, labels, titles, and short text visible before a forecast snapshot T0.
- It clusters repeated pre-T0 signals into task families for feature implementation or enhancement, bugfixes, and refactors. Each family names an anchor, expected behavior, evidence references, target hints, and acceptance criteria.
- It freezes those forecasts, then checks them against later pull-request metadata in a six-month validation window. Patches are not shown to the judge.
- Validated families condition task synthesis at a task-generation snapshot Tgen. A multi-agent construction loop writes the public issue, designs tests, writes a gold patch, and verifies executable behavior.
- Released tasks expose the repository snapshot and issue-style request. Tests, gold patches, validation labels, provenance, and execution logs stay hidden.

## Results
- In an 80-repository retrospective study, the forecaster emitted 260 families across 76 repositories: 139 bugfix families, 93 feature/enhancement families, and 28 refactor families.
- The main future-work relevance result is 151/260 families, or 58.1%, counted as strong or related semantic matches against post-T0 pull-request metadata.
- The stricter strong-match rate is 111/260, or 42.7%.
- Bugfix forecasts performed best: 89/139 bugfix families matched as strong or related. Feature/enhancement forecasts had 45/93 strong or related matches.
- An independent semantic audit agreed with the primary relevance-versus-rejected decision in 216/260 cases, or 83.1%.
- The final dataset contains 200 synthesized executable tasks across 61 repositories: 120 bugfix tasks, 60 feature/enhancement tasks, and 20 refactor tasks. Of these, 160 are conditioned on strong forecast matches and 40 on related matches.

## Link
- [https://arxiv.org/abs/2606.18733v1](https://arxiv.org/abs/2606.18733v1)
