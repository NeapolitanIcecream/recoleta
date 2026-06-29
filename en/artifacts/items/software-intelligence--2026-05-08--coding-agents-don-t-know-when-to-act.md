---
source: arxiv
url: https://arxiv.org/abs/2605.07769v1
published_at: '2026-05-08T14:10:00'
authors:
- Thibaud Gloaguen
- "Niels M\xFCndler"
- "Mark M\xFCller"
- Veselin Raychev
- Martin Vechev
topics:
- coding-agents
- software-maintenance
- code-intelligence
- swe-bench
- agent-evaluation
- abstention
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Coding Agents Don't Know When to Act

## Summary
Coding agents often edit already-fixed code when they should leave it unchanged. FixedBench tests this abstention skill on 200 SWE-bench Verified tasks where the golden patch has already been applied.

## Problem
- Autonomous maintenance agents will see stale or duplicate bug reports; the paper cites prior work saying duplicates can reach 49% of bug reports.
- If an agent patches code that is already correct, it can add technical debt and hide whether the issue was verified.
- Existing coding benchmarks mainly reward patch generation, so they miss the decision to submit no code change.

## Approach
- The authors build FixedBench by taking 200 SWE-bench Verified issues and applying each issue's golden patch before giving the task to the agent.
- The correct output in the Resolved task is an empty executable-code patch; changes to tests, comments, and documentation are ignored for abstention scoring.
- They test five models across four agent harnesses, including Sonnet-4.6, GPT-5.3 Codex, GPT-5.4 mini, Gemini-3 Pro, and Qwen3.5-122B.
- They compare prompts: Issue, Edit, Reproduce, and Abstain or Fix, plus Best and Worst scenarios with or without git history and a ready environment.
- A Partial task applies an incorrect prior patch to 150 instances to test whether abstention prompts cause agents to skip real fixes.

## Results
- In the main Resolved setting with the Issue prompt, agents made undesirable executable-code edits in 35% to 65% of already-fixed cases.
- In the Best scenario, Sonnet-4.6 abstained 65.0%±6.6 and GPT-5.4 mini abstained 60.5%±6.8 under the Issue prompt.
- The Edit prompt reduced abstention: GPT-5.4 mini fell from 60.5% to 36.5%, and Sonnet-4.6 fell from 65.0% to 56.5%.
- The Abstain or Fix prompt improved abstention in the Best scenario to 80.5% for Sonnet-4.6 and 88.5% for GPT-5.4 mini; reported uplifts were 15.5 points (p=9.5e-3) and 28.0 points (p=2.3e-8).
- Reproduce alone failed to fix the behavior: Sonnet-4.6 moved from 65.0% to 65.5%, while GPT-5.4 mini dropped from 60.5% to 47.5%.
- On the Partial task, the same Abstain or Fix prompt increased incorrect abstention: GPT-5.4 mini abstained incorrectly 93.6%±4.3 and resolved only 2.9%±2.8 of cases; Sonnet-4.6 abstained incorrectly 81.3%±6.2 and resolved 6.0%±3.8.

## Link
- [https://arxiv.org/abs/2605.07769v1](https://arxiv.org/abs/2605.07769v1)
