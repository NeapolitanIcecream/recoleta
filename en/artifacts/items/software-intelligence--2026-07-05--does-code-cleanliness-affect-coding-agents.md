---
source: hn
url: https://arxiv.org/abs/2605.20049
published_at: '2026-07-05T23:03:55'
authors:
- softwaredoug
topics:
- coding-agents
- code-cleanliness
- software-engineering
- code-intelligence
- agent-evaluation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Does Code Cleanliness Affect Coding Agents?

## Summary
This paper tests whether cleaner code changes how Claude Code performs on software tasks. In 660 controlled trials, cleanliness did not change pass rate, but it reduced token use and file revisits.

## Problem
- Coding-agent evaluations usually keep the target codebase fixed, so they do not show whether code quality changes agent behavior.
- The paper asks whether structural and stylistic cleanliness affects an agent's ability to navigate and modify code.
- This matters because agent cost and speed depend on token use and code navigation, even when final task success is unchanged.

## Approach
- The study builds minimal-pair repositories: each pair keeps architecture, dependencies, and public behavior the same while changing cleanliness.
- Cleanliness is changed through static-analysis rule violations and cognitive complexity.
- The authors create pairs in both directions: one pipeline degrades a clean repository, and another cleans a messy repository.
- They write 33 tasks across 6 repository pairs and evaluate outputs with hidden tests at the application's public surface.
- They run 660 trials using Claude Code.

## Results
- Cleaner code did not change Claude Code's pass rate compared with messier paired repositories. The excerpt gives no pass-rate percentage.
- Cleaner code used 7% to 8% fewer tokens than the messier matched variants.
- Cleaner code reduced file revisitations by 34%.
- The main claimed gain is lower operational cost and better navigation, measured against matched repositories with the same external behavior.

## Link
- [https://arxiv.org/abs/2605.20049](https://arxiv.org/abs/2605.20049)
