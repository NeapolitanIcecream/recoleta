---
source: arxiv
url: https://arxiv.org/abs/2607.18213v1
published_at: '2026-07-20T17:47:44'
authors:
- Yuhang Wang
- Yuling Shi
- Shaoqiu Zhang
- Jialiang Liang
- Shilin He
- Siyu Ye
- Yuting Chen
- Kai Cai
- Xiaodong Gu
topics:
- code-intelligence
- software-foundation-models
- context-pruning
- coding-agents
- automated-software-production
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# SWE-Pruner Pro: The Coder LLM Already Knows What to Prune

## Summary
SWE-Pruner Pro uses a coding agent's own hidden states to remove unnecessary tool-output lines without a separate pruning model or extra query. Across two open-weight backbones and four multi-turn benchmarks, it reports up to 39.4% token savings while largely preserving quality, with gains on MiMo-V2-Flash for Oolong and SWE-Bench Verified.

## Problem
- Coding agents accumulate redundant file, search, and terminal output across turns; tool outputs account for over 70% of tokens in one cited SWE-Bench setup.
- Existing compressors use task-agnostic signals or require a separate scorer and explicit goal-hint query, adding cost and potentially missing the agent's current information needs.
- The paper addresses whether long-context tool output can be reduced while preserving task quality and controlling inference overhead.

## Approach
- A lightweight pruning head reads the frozen backbone's last-layer hidden states during the normal tool-response prefill and predicts keep-or-prune labels for each token.
- Token predictions become line-level decisions through majority voting, preserving selected code lines and removing pruned lines from later turns.
- The head adds a learned embedding for the response's line count and uses a two-block feed-forward classifier.
- Training uses Claude Sonnet 4.6 line annotations from 22,609 multi-turn trajectory samples and a per-sample balanced focal loss that gives equal weight to keep and prune classes within each sample.

## Results
- A linear probe on approximately 2,260 tool responses and 155,000 lines achieved 0.83 AUC and 0.63 best-F1, compared with a majority-class F1 upper bound of 0.46, supporting the claim that pruning information is present in backbone representations.
- On Qwen3-Coder-Next, SWE-Pruner Pro reduced tokens by 34.7% on SWE-QA, 39.4% on SWE-QA-Pro, and 13.9% on Oolong, with quality changes of +0.02, +0.24, and -1.4 points relative to no pruning.
- On MiMo-V2-Flash, it reduced tokens by 6.9% on SWE-QA, 22.6% on SWE-QA-Pro, and 30.1% on Oolong; Oolong accuracy increased by 2.2 points to 94.6.
- On SWE-Bench Verified, MiMo-V2-Flash resolved 345/500 tasks versus 326/500 without pruning, a gain of 3.8 percentage points, while Qwen3-Coder-Next resolved 335/500 versus 341/500 and reduced input tokens by 13.5%.
- The in-server head added 15.0% aggregate wall time in a replay study and did not require an extra model call, although SWE-Bench API calls increased from 131.9 to 139.8 for Qwen3-Coder-Next.
- In an ablation, per-sample balanced focal loss reached 0.635 line F1 and 7.08 judge score, versus 0.475 and 5.95 for BCE; adding the length embedding raised the judge score from 6.86 to 7.08 at nearly unchanged F1.

## Link
- [https://arxiv.org/abs/2607.18213v1](https://arxiv.org/abs/2607.18213v1)
