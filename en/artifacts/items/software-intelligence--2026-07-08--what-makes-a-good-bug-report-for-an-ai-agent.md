---
source: arxiv
url: https://arxiv.org/abs/2607.07593v1
published_at: '2026-07-08T16:13:15'
authors:
- Lara Khatib
- Noble Saji Mathews
- Meiyappan Nagappan
- Pengyu Nie
- Thomas Zimmermann
topics:
- automated-program-repair
- bug-reports
- code-intelligence
- swe-bench
- llm-agents
- fault-localization
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# What Makes a Good Bug Report for an AI Agent?

## Summary
The paper studies which bug-report details help LLM repair agents fix real software bugs. It finds that agents benefit most from executable evidence, code and location hints, and fix suggestions, while longer reports are linked to lower success.

## Problem
- APR agents now read bug reports written for humans, then inspect repositories and submit patches without asking clarifying questions.
- Human bug-report guidelines may not match agent needs; poor starting information makes agents search more, guess, or patch the wrong code.
- Knowing which fields help agents matters for issue templates, developer tools, and automated software production workflows.

## Approach
- Study 1 analyzes 433 SWE-bench Verified bug-fix issues attempted by 87 agents, for 37,671 agent-issue outcomes and a 47.7% overall solve rate.
- The authors annotate each report for 27 features, including reproduction steps, stack traces, error messages, code snippets, reproduction scripts, fix suggestions, section headers, report length, and fault-localization cues.
- A mixed-effects logistic regression estimates which features correlate with successful repair while accounting for issue difficulty and agent capability.
- Study 2 runs controlled ablations on SWE-bench Pro across 2 models and 17 problem-statement mutations, removing or isolating report content and changing structure while holding the task fixed.

## Results
- In Study 1, fix suggestions have the largest positive association with success: odds ratio 3.61, 95% CI [2.01, 6.47], p < 0.001.
- Repository source code in the report raises resolution odds: OR 2.82, 95% CI [1.23, 6.44], p < 0.05.
- Reproduction scripts also help: OR 2.52, 95% CI [1.41, 4.51], p < 0.01.
- Naming a file changed by the ground-truth patch is linked to higher success: OR 2.33, 95% CI [1.18, 4.60], p < 0.05.
- Longer reports correlate with worse outcomes: a one-standard-deviation increase in log report length has OR 0.49, 95% CI [0.35, 0.68], p < 0.001.
- The excerpt does not provide exact solve-rate deltas for Study 2, but it reports that both tested models rely on localization cues and expected behavior, and that removing list structure or section headers can reduce solve rates even when the same text remains.

## Link
- [https://arxiv.org/abs/2607.07593v1](https://arxiv.org/abs/2607.07593v1)
