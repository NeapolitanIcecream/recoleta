---
source: arxiv
url: http://arxiv.org/abs/2604.00917v1
published_at: '2026-04-01T13:58:30'
authors:
- Razvan Mihai Popescu
- David Gros
- Andrei Botocan
- Rahul Pandita
- Prem Devanbu
- Maliheh Izadi
topics:
- autonomous-coding-agents
- software-engineering
- github-pull-requests
- code-churn
- human-ai-collaboration
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Investigating Autonomous Agent Contributions in the Wild: Activity Patterns and Code Change over Time

## Summary
This paper studies how autonomous coding agents contribute to real GitHub projects and how their code changes after merge. Using a new dataset of about 112k pull requests across five agents and a human comparison set, it finds that agent use is growing, especially in low-star repositories, and that agent-authored code shows higher later churn than human-authored code.

## Problem
- Existing evaluations of coding agents rely heavily on benchmarks, user studies, or small datasets, so they miss how agents behave in real collaborative software work.
- Prior field studies often cover one agent, a small PR sample, or only popular repositories, which makes it hard to compare agent behavior at scale.
- Code generation is only part of software engineering; maintainability matters because code must survive and be edited over time after the pull request is merged.

## Approach
- The authors build a GitHub dataset of **111,969 pull requests** from **June-August 2025**, covering five autonomous agents: **OpenAI Codex, Claude Code, GitHub Copilot, Google Jules, and Devin**, plus a matched human-authored PR set.
- They identify agent PRs with concrete GitHub signals such as branch prefixes (`head:codex/`, `head:copilot/`), bot authors (`google-labs-jules[bot]`, `devin-ai-integration[bot]`), and Claude watermark text in PR descriptions.
- The dataset includes PRs plus linked **commits, comments, reviews, issues, and changed files**, with counts in the tens of thousands per agent and millions of lines of code overall.
- They compare agent and human PRs on collaboration and activity measures such as merge frequency, merge latency, edited file types, change size, commit density, comments, reviews, and repository characteristics.
- They also run a longitudinal analysis of post-merge code evolution using survival and churn estimates to measure how much agent-authored code is later kept or rewritten.

## Results
- The final dataset contains **111,969 PRs**: **20,835 Codex**, **19,148 Claude Code**, **18,563 Copilot**, **18,468 Jules**, **14,045 Devin**, and **20,910 human** PRs.
- Associated activity volume is large: for example, the dataset includes **102,037 human commits**, **82,755 Claude commits**, **69,896 Copilot commits**, **51,641 Devin commits**, **41,032 Jules commits**, and **27,530 Codex commits**; changed files range from **90,822** for Codex to **255,275** for Claude.
- The paper claims agent activity in open-source projects is increasing and is concentrated more in **low-star repositories** than earlier studies suggested.
- The main substantive finding is that **agent-authored contributions are associated with more code churn over time than human-authored code**, which points to lower long-term stability or more follow-up maintenance.
- The excerpt does **not provide the actual churn, survival, merge-rate, or latency numbers**, so the quantitative size of those differences cannot be verified from the provided text.
- As a concrete research asset, the authors release the dataset publicly on Hugging Face for follow-up work on agentic software development.

## Link
- [http://arxiv.org/abs/2604.00917v1](http://arxiv.org/abs/2604.00917v1)
