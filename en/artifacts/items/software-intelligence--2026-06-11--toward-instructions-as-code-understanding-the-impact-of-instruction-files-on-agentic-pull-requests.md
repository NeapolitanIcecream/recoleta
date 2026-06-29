---
source: arxiv
url: https://arxiv.org/abs/2606.13449v1
published_at: '2026-06-11T15:09:32'
authors:
- Ali Arabat
- Mohammed Sayagh
topics:
- instruction-files
- agentic-pull-requests
- copilot
- merge-rate
- software-engineering
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Toward Instructions-as-Code: Understanding the Impact of Instruction Files on Agentic Pull Requests

## Summary
The paper studies whether instruction files improve agent-generated pull requests, and it finds mixed effects across 148 projects and 15,549 Agentic-PRs. Projects with better merge outcomes tend to have longer, more structured instruction files.

## Problem
- Software teams write instruction files for coding agents, but it is unclear whether those files actually improve pull request success and merge effort.
- The paper asks whether instruction files change merge rate, task complexity, merge time, and discussion volume for agentic pull requests.
- This matters because teams are treating agents like contributors, and instruction quality may shape how well they work in a repository.

## Approach
- The authors analyze 15,549 agentic pull requests from 148 GitHub projects in the AIDev dataset.
- They split each project into periods before and after the first instruction file, and also before the first file versus after the last file when multiple files exist.
- They measure success with merge rate, task complexity with description length, code churn, modified files, and commit count, and merge effort with comment count and merge time.
- They use Mann-Whitney U tests and Cliff’s delta for the complexity and effort comparisons.
- They compare instruction file length and header structure between projects with merge-rate increases and decreases.

## Results
- 27.7% of projects increased merge rate by at least 20% after the first instruction file, while 26.35% decreased by at least 20%.
- After all instruction files are added, 31.93% of projects increase merge rate by at least 20%, while 27.73% decrease by at least 20%.
- For task complexity, 35.35% of projects show a statistically significant increase in description length, 10.10% in code churn, 12.12% in commit count, and 8.08% in changed files after the first instruction file; smaller shares show decreases, including 4.04% for description length and 7.07% for code churn and commits.
- For merge effort, 13.13% of projects show a statistically significant increase in merge time and 15.15% in discussion volume, while 8.8% decrease in both metrics.
- Projects with at least 20% merge-rate gains have longer instruction files, with a median of 976 words versus 569 words for projects with at least 20% merge-rate drops, and they also have more H1, H2, and H3 headers.
- The paper does not claim a universal gain; it claims that instruction files help some projects and hurt others, and that better-structured files line up with better merge outcomes.

## Link
- [https://arxiv.org/abs/2606.13449v1](https://arxiv.org/abs/2606.13449v1)
