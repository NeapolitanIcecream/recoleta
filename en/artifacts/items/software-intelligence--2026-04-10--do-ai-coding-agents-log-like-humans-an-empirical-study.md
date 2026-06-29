---
source: arxiv
url: http://arxiv.org/abs/2604.09409v1
published_at: '2026-04-10T15:22:58'
authors:
- Youssef Esseddiq Ouatiti
- Mohammed Sayagh
- Hao Li
- Ahmed E. Hassan
topics:
- ai-coding-agents
- software-logging
- empirical-software-engineering
- code-review
- observability
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Do AI Coding Agents Log Like Humans? An Empirical Study

## Summary
This paper studies how AI coding agents handle software logging in real open-source pull requests. It finds that agents touch logging less often than humans, often ignore explicit logging instructions, and leave humans to repair many logging problems after generation.

## Problem
- Logging is a core observability requirement for debugging and operating software, but prior work did not show how AI coding agents handle it in real repositories.
- Teams need to know whether agents follow human logging habits, respond to logging instructions, and reduce or increase maintenance work.
- Poor logging can leave systems harder to diagnose, while excessive logging adds noise and overhead.

## Approach
- The authors analyze **4,550 agentic PRs** and **3,276 human PRs** across **81 open-source repositories** from the AIDev dataset; after excluding repositories with no logging changes on either side, the main analysis uses **77 repositories**.
- They detect logging changes in Python, Java, and JS/TS diffs with language-specific regex rules, excluding generated artifacts and test/build noise. A manual check on **380 diffs** reports **96% precision** and **94% recall**.
- They compare agent and human PRs within each repository using logging prevalence, log density, message traits, log levels, and syntactic placement.
- They collect agent instructions from linked issues, repo instruction files, and PR review comments, then classify logging-related intent with a three-model voting setup using GPT-4o, GLM-4.7, and DeepSeek-V3.2. On **100 manually labeled samples**, the prompt refinement reached **Cohen's kappa = 0.83**.
- They also trace post-generation logging regulation to see whether humans or agents make later logging repairs.

## Results
- In **45 of 77 repositories (58.4%)**, humans changed logging more often than agents. The paired difference is reported as statistically significant with **p = 0.019**. The median normalized score is **0.45**, which the authors interpret as agents changing logging about **16% less often** than humans in a typical project.
- In repositories where both sides add logs, agents introduce **30% more logs per 1,000 modified LOC** than humans, so agents log less often across PRs but can be denser when they do log.
- Explicit logging instructions are rare: only **4.7%** of studied instruction sources contain them.
- Agents fail to comply with constructive logging requests **67%** of the time, and the paper says this low compliance holds even when instructions are specific.
- Humans perform **72.5%** of post-generation logging repairs, usually through later commits rather than explicit review comments, which shows a hidden maintenance burden.
- The paper also claims agents match human error-logging patterns better than informational-context logging, but the excerpt does not provide detailed numeric breakdowns for log levels or syntactic context.

## Link
- [http://arxiv.org/abs/2604.09409v1](http://arxiv.org/abs/2604.09409v1)
