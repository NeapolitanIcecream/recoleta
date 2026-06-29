---
source: arxiv
url: https://arxiv.org/abs/2606.18168v1
published_at: '2026-06-16T17:06:51'
authors:
- Dipayan Banik
- Kowshik Chowdhury
- Shazibul Islam Shamim
topics:
- ai-coding-agents
- test-oracles
- code-intelligence
- software-testing
- empirical-software-engineering
- pull-requests
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# All Smoke, No Alarm: Oracle Signals in Agent-Authored Test Code

## Summary
AI coding agents often add test files that execute code without checking behavior. This paper measures that gap at scale and shows that stronger test oracles are linked to higher merge odds after controlling for PR and repository factors.

## Problem
- Test-file presence can make an agent-authored PR look verified even when the tests contain no explicit assertions.
- Weak tests matter because CI, coverage, and reviewer scans may pass code that was executed but never checked against expected behavior.
- Existing work studied LLM oracle quality in controlled settings, while this paper studies real GitHub PRs from coding agents.

## Approach
- The study analyzes 86,156 cumulative test-file patches from 33,596 agent-authored PRs across 2,807 GitHub repositories in the AIDev-pop dataset.
- It covers five agents: OpenAI Codex, GitHub Copilot, Devin, Cursor, and Claude Code.
- The authors define eight syntactic oracle categories: W1-W5 for weak signals such as no assertion, non-null checks, boolean-only checks, mock-only checks, and snapshots; S1-S3 for stronger checks such as value comparisons, error/type/containment checks, and multiple strong assertion types.
- Two authors manually labeled 384 stratified patches, then the taxonomy was applied at scale with a classifier.
- PR-level analysis compares oracle strength with merge outcomes and review effort, using logistic regression with controls for agent, PR size, repository stars, task type, and language.

## Results
- 80.2% of the 86,156 test-file patches contain weak or no explicit oracle signals.
- Strong value assertions, S1, account for 11.3% of patches; multi-signal strong oracles, S3, account for 5.7%.
- Human annotation agreement on 384 patches reached Cohen's kappa = 0.77, and the classifier matched human oracle-category labels for 86.7% of patches.
- New test files have strong-oracle rates ranging from 18% for OpenAI Codex to 67% for Claude Code.
- Raw merge rates are lower for S3 PRs than weak-oracle PRs, 59.7% versus 72.6%, but S3 PRs have 4.2x more code additions, 2.4x more review effort, and appear in repositories with 3.8x more stars.
- After adjustment, S3 oracles are associated with higher merge likelihood, with odds ratio OR = 1.28 and p < 0.001.

## Link
- [https://arxiv.org/abs/2606.18168v1](https://arxiv.org/abs/2606.18168v1)
