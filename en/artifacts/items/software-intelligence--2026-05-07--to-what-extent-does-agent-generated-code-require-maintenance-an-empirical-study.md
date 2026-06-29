---
source: arxiv
url: https://arxiv.org/abs/2605.06464v2
published_at: '2026-05-07T15:52:41'
authors:
- Shota Sawada
- Tatsuya Shirai
- Yutaro Kashiwa
- Ken'ichi Yamaguchi
- Hiroshi Iwata
- Hajimu Iida
topics:
- agentic-coding
- software-maintenance
- ai-generated-code
- code-intelligence
- empirical-software-engineering
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# To What Extent Does Agent-generated Code Require Maintenance? An Empirical Study

## Summary
The paper finds that files created by coding agents need less maintenance than matched human-created files over six months, but humans still do most follow-up work. AI-created files are more often extended with features than fixed for bugs.

## Problem
- Teams use coding agents to add code, but they lack evidence about what happens after agent-created files are merged.
- This matters because long-term maintenance can reduce productivity gains and force humans to edit code they did not write.
- Prior work mostly measured generation-time quality or short-term effects, leaving post-merge maintenance under-measured.

## Approach
- The study uses the AIDev dataset, which contains more than 456,000 pull requests from autonomous coding agents across about 61,000 repositories.
- It identifies files added by Claude Code, Cursor, GitHub Copilot, and Devin through bot committer names, and excludes Codex because ownership could not be verified from commits.
- It samples 508 AI-generated files and 508 matched human-generated files from 100 repositories with more than 100 stars.
- It tracks post-creation commits through January 31, 2026, giving each file at least a six-month observation window.
- It compares commit frequency, percent of file size changed, commit type using Conventional Commits Classification System, and whether the maintainer was a bot or a human.

## Results
- The dataset includes 1,543 maintenance commits to AI-generated files and 1,695 maintenance commits to human-generated files; initial file-creation commits are excluded.
- During the first month, AI-generated files receive about half as many commits as human-generated files. The paper reports lower maintenance frequency for AI-generated files across the first six months.
- AI-generated files also have a smaller percentage of lines changed per month than human-generated files, so their maintenance changes are usually smaller relative to file size.
- For AI-generated files, the most common maintenance type is feature work: 336 of 1,543 commits, or 21.78%. Bug fixes are 181 commits, or 11.73%.
- For human-generated files, bug fixes are the most common type: 284 of 1,695 commits, or 16.76%. Documentation changes are 275 commits, or 16.22%, and feature work is 256 commits, or 15.10%.
- Humans perform 1,284 of 1,543 commits to AI-generated files, or 83.21%. AI agents perform 259 commits, or 16.79%; on human-generated files, agents perform 119 of 1,695 commits, or 7.02%.

## Link
- [https://arxiv.org/abs/2605.06464v2](https://arxiv.org/abs/2605.06464v2)
