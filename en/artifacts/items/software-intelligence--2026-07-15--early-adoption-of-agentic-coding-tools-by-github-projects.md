---
source: arxiv
url: https://arxiv.org/abs/2607.14037v1
published_at: '2026-07-15T17:05:06'
authors:
- Maliha Noushin Raida
- Daqing Hou
topics:
- ai-coding-agents
- software-engineering
- github-analytics
- human-agent-collaboration
- project-adoption
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Early Adoption of Agentic Coding Tools by GitHub Projects

## Summary
This study examines how GitHub projects adopt and manage agent-generated pull requests at the project level. Across 2,361 repositories and 25,264 agentic PRs from May–July 2025, adoption was usually light, concentrated in small projects and a limited set of highly active repositories, and organized mainly around one-person oversight.

## Problem
- Prior research has focused mainly on individual agentic pull requests, leaving project-level adoption, productivity, and coordination less understood.
- This matters because the value of coding agents depends on how projects allocate review, modification, and integration work, not only on agent capability.
- The evidence is an early snapshot of popular GitHub repositories and uses contributor counts and agentic PRs as operational proxies for team size and productivity.

## Approach
- Analyze the AIDev-pop dataset for merged or closed PRs created by GitHub Copilot, OpenAI Codex, and Claude Code during May–July 2025.
- Measure adoption using agentic PRs per repository and the proportion of repository contributors involved in agentic PR workflows.
- Compare small projects with 1–5 contributors, medium projects with 6–15, and large projects with 16 or more contributors; test participation differences with Kruskal–Wallis, Dunn, and Cliff’s Delta analyses.
- Estimate project-level productivity as agentic PRs per human participant and compare it with a contextual reference of 36 PRs per developer over three months.
- Classify PRs by reviewer and committer roles to identify single-human and multi-human collaboration patterns.

## Results
- The dataset contains 25,264 agentic PRs, 2,361 repositories, and 291,866 commits. The median repository produced only 1–2 agentic PRs during the three-month period.
- Participation was limited in most projects: 998 repositories (42.27%) had fewer than 5% of contributors involved, 1,657 (70.18%) had participation below 20%, and 1,776 (75.22%) had participation below 30%.
- Small projects averaged 50.2 agentic PRs per repository, compared with 5.6 for medium projects and 6.7 for large projects, although the distributions were highly skewed and typical repository activity remained low.
- Participation ratios differed significantly across project-size groups (Kruskal–Wallis H=1211.79, p<0.001, eta-squared=0.6157); all pairwise comparisons were significant with large Cliff’s Delta effects.
- Only 25 of 2,361 projects (1%) exceeded the contextual benchmark of 36 agentic PRs per human participant over three months, showing that high project-level activity was rare.
- Single-human oversight dominated: one person both reviewed and modified the agent’s contribution in 19,488 PRs (78.9%), while one-person workflows overall accounted for 88.7%; PRs involving at least two humans accounted for 11.3%.

## Link
- [https://arxiv.org/abs/2607.14037v1](https://arxiv.org/abs/2607.14037v1)
