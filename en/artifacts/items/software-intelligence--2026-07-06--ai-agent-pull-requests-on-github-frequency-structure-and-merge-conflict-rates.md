---
source: arxiv
url: https://arxiv.org/abs/2607.04697v2
published_at: '2026-07-06T05:58:12'
authors:
- George Xu
- Arjun Subramanian
- Nithilan Karthik
topics:
- ai-coding-agents
- pull-requests
- merge-conflicts
- software-engineering
- multi-agent-systems
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# AI Agent Pull Requests on GitHub: Frequency, Structure, and Merge Conflict Rates

## Summary
AI coding-agent PRs on GitHub often overlap in time, and same-agent overlap is the main case today. The paper measures how often these PRs overlap and how often real git merges between overlapping PRs produce textual conflicts.

## Problem
- AI coding agents can open multiple PRs against the same repository at the same time, which can create merge conflicts before a human maintainer sees the work.
- Prior work measured conflicts between a single agent PR and its base branch, but did not measure conflicts between two concurrent agent-authored PRs.
- The issue matters because uncoordinated agent output can add maintainer work, CI cost, and failed integration in automated software production.

## Approach
- The study uses AIDev-pop: 33,596 agent-authored PRs across 2,807 GitHub repositories.
- It defines co-active PRs by overlapping open-close intervals, with time windows of 0, 1, 3, and 7 days.
- It separates same-agent PR pairs from cross-agent PR pairs.
- It samples 747 co-active pairs with one pair per repository, then replays three-way git merges using `git merge-tree`.
- It classifies git-reported conflicts by conflict type and by file category.

## Results
- At exact temporal overlap, 1,129 of 2,807 repositories had co-active agent PRs, or 40.2% with a 95% CI of [38.4%, 42.0%]. These pairs covered 26,691 of 33,596 agent PRs, or 79.4%.
- With a 7-day window, 1,498 repositories were co-active, or 53.4% with a 95% CI of [51.5%, 55.2%]. At the PR level, 31,916 PRs were co-active, or 95.0%.
- Cross-agent overlap was rare: at exact overlap, 2,896 of 580,913 co-active pairs were cross-agent, or 0.50%, across 122 of 2,807 repositories.
- In the merge replay, 716 of 747 sampled pairs were evaluable. Same-agent pairs had a 19.8% textual conflict rate, 119 of 601, with a 95% CI of [16.8%, 23.2%].
- Cross-agent pairs had a 41.7% textual conflict rate, 48 of 115, with a 95% CI of [33.1%, 50.9%].
- Across 167 conflicting pairs and 1,646 conflicted files, 84.4% of conflicted files were source code, 3.9% were manifests or lockfiles, 57.6% of conflict reports were content conflicts, 26.8% were modify/delete, and 15.1% were add/add.

## Link
- [https://arxiv.org/abs/2607.04697v2](https://arxiv.org/abs/2607.04697v2)
