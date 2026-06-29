---
source: arxiv
url: https://arxiv.org/abs/2606.25514v1
published_at: '2026-06-24T07:48:05'
authors:
- Yang Chen
- Aliya Ahmad
- Yiheng Zhou
- Reyhaneh Jabbarvand
topics:
- software-engineering-agents
- swe-bench
- multi-agent-systems
- automated-bug-fixing
- code-intelligence
- context-management
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Unlocking Model Potentials Through Adaptive Multi-Agent Scaffolding for Efficient Issue Resolution

## Summary
i cat-agent is a decentralized multi-agent scaffold for resolving GitHub issues with long codebase workflows. It improves SWE-bench issue resolution by isolating explorer, patch editor, and validator contexts and passing only structured events between them.

## Problem
- Automated bug fixing often fails when issue reports omit files, functions, reproduction details, or fix hints; the paper reports 35.2% of SWE-bench Verified and 41.2% of SWE-bench Pro issues do not name the buggy file or function.
- Single-agent and leader-based multi-agent systems keep too much shared context, which can degrade reasoning and let patch generation overfit to weak tests or validator outputs.
- The problem matters because issue resolution requires finding the root cause, reproducing the failure, editing code, and checking the patch across long trajectories.

## Approach
- i cat-agent uses three separate agents: Explorer locates relevant files/functions and call chains, Patch Editor edits code, and Validator writes and runs reproduction/regression tests.
- A rubric-based Quality Checker labels an issue high quality only if it names the buggy file, names the function, gives a fix strategy, and gives reproduction information.
- High-quality issues skip initial exploration and run Patch Editor and Validator in parallel; low-quality issues first run Explorer to gather repository context.
- Agents do not share a global conversation. They exchange synchronous event messages such as pass/fail results, suspicious statements, and structured repository context.
- Validator hides test code and assertions from Patch Editor, while Patch Editor hides internal reasoning from Validator; this is meant to reduce test overfitting and patch overfitting.

## Results
- On SWE-bench Verified, i cat-agent improves over SWE-agent, mini-SWE-agent, and Claude Code by 3.6-8.4 percentage points when using the same backbone models.
- On SWE-bench Pro, it improves over those baselines by 6.3-18.5 percentage points across the same-model comparisons.
- i cat-agent + GPT-5.4-xhigh solves 67.4% of SWE-bench Pro, beating mini-SWE-agent + GPT-5.4-xhigh at 59.10% by 8.3 percentage points.
- On SWE-bench Pro, i cat-agent costs $1.27 per instance with Claude Sonnet 4.5 and $1.49 with GPT-5.4-xhigh, compared with $2.67 for Claude Code.
- The paper evaluates all 500 SWE-bench Verified instances and all 731 SWE-bench Pro instances, and says gains hold across difficulty levels and programming languages.

## Link
- [https://arxiv.org/abs/2606.25514v1](https://arxiv.org/abs/2606.25514v1)
