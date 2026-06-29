---
source: arxiv
url: https://arxiv.org/abs/2604.26892v1
published_at: '2026-04-29T17:01:01'
authors:
- Carol Hanna
- Karine Even-Mendoza
- W. B. Langdon
- "Mar Zamorano L\xF3pez"
- Justyna Petke
- Federica Sarro
topics:
- hot-fixing
- autonomous-coding-agents
- software-maintenance
- code-intelligence
- human-ai-collaboration
- empirical-software-engineering
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Hot Fixing in the Wild

## Summary
This paper measures how GitHub hot fixes differ from routine bug fixes and how autonomous coding agents behave during urgent repairs. It studies PRs linked to issues in the Hao-Li/AIDev dataset across more than 61,000 repositories.

## Problem
- Hot fixes matter because they address production failures under time pressure, where teams may reduce review, testing, and collaboration to restore service faster.
- GitHub issue labels give inconsistent urgency and severity signals, so large-scale hot-fix studies need other cues.
- Coding agents now submit PRs in real projects, but their behavior in urgent production fixes has little direct measurement.

## Approach
- The authors classify GitHub issue criticality with one-shot prompts on three local LLMs: Llama 3.2, Qwen2.5-3B-Instruct, and Phi-4-mini.
- They add two timing filters: the PR must open within 12 hours of issue creation, and the PR must close within 24 hours of PR creation.
- Four reviewers manually inspect 20% of LLM-flagged hot fixes, using issue text, PR text, and repo context when needed.
- The study links issues to PRs in AIDev and compares contributors, commits, reviewers, changed files, lines changed, test-file edits, and merge rates for hot fixes and routine bug fixes.
- The authors split hot-fix PRs by author type, human versus bot, and compare PR text with bag-of-words word clouds.

## Results
- Timing filters reduced Llama3.2 critical issues from 1,348 to 269, Phi-4-mini from 425 to 105, and Qwen from 148 to 33; urgent wording alone produced many candidates that failed action-timing checks.
- Manual validation found overall LLM-human agreement of 0.37; Qwen aligned fully with reviewers in the sampled cases, Phi-4-mini agreed in about 50%, and Llama3.2 had a 49% disagreement rate.
- Hot fixes were smaller than routine fixes. With Qwen labels, hot-fix PRs averaged 2.7 commits, 3.9 files, 25.7 added lines, and 9.3 deleted lines, compared with routine PR means of 4.9 commits, 27.7 files, 90 added lines, and 54.4 deleted lines.
- Hot fixes had fewer people involved: contributors ranged from 1 to 5 for hot fixes versus 1 to 13 for routine fixes, and reviewers ranged up to 5 for hot fixes versus 16 for routine fixes.
- Hot fixes touched tests less often than routine fixes: Qwen-labeled hot fixes included tests in 29.73% of PRs versus 54.42% for routine PRs, a 24.69 percentage-point gap.
- Hot fixes merged more often: Qwen-labeled hot fixes merged at 70.27% versus 45.30% for routine PRs; bot hot-fix merge rates were close to human rates, such as 66.67% versus 70.97% under Qwen.

## Link
- [https://arxiv.org/abs/2604.26892v1](https://arxiv.org/abs/2604.26892v1)
