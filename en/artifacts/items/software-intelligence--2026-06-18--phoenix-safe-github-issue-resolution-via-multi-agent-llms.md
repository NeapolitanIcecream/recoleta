---
source: arxiv
url: https://arxiv.org/abs/2606.20243v1
published_at: '2026-06-18T13:56:12'
authors:
- Kipngeno Koech
- Muhammad Adam
- Baimam Boukar Jean Jacques
- Joao Barros
topics:
- multi-agent-systems
- github-issue-resolution
- code-agents
- software-testing
- swe-bench
- automated-program-repair
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Phoenix: Safe GitHub Issue Resolution via Multi-Agent LLMs

## Summary
Phoenix is a six-agent LLM system that turns GitHub issues into reviewed pull requests while gating changes with tests and safety checks. Its strongest claim is 18/24 oracle-resolved tasks on a curated SWE-bench Lite slice, with clear limits on comparison to full benchmark leaderboards.

## Problem
- GitHub issue resolution takes developer time because each issue needs triage, reproduction, code changes, tests, and review handoff.
- Autonomous code agents can create useful patches, but they can also introduce regressions or unsafe repository changes if they optimize only for resolution rate.
- Many real repositories have broken or flaky test suites, so a system needs to separate pre-existing failures from failures caused by its own patch.

## Approach
- Phoenix splits the workflow across six agents: Planner, Reproducer, Coder, Tester, Failure Analyst, and PR Agent.
- A GitHub webhook state machine uses labels to move issues through states such as ready, review, revise, and failed.
- The Tester runs a baseline test pass on the unmodified branch, then compares it with the post-change test run; a patch is accepted only when it adds no new failing tests.
- Seven safety controls block path traversal, workflow-file writes, stale label states, runaway retries, concurrent clone edits, expired GitHub tokens, and prompt content that triggers gateway filtering.
- The system opens pull requests for human review and does not merge changes into the default branch.

## Results
- On a curated 24-instance SWE-bench Lite slice across 8 Python repositories, Phoenix oracle-resolved 18/24 tasks, or 75%.
- Repository-level SWE-bench Lite results were 3/3 for Astropy, Django, Requests, and SymPy; 2/3 for Flask and pytest; 1/3 for Matplotlib and scikit-learn.
- Successful SWE-bench Lite oracle runs had no PASS_TO_PASS regressions, and the mean time from ai:ready label to terminal label was 170 seconds.
- Six SWE-bench Lite runs did not pass: five ended with ai:failed and one scikit-learn run exceeded a 45-minute evaluator wait cap.
- In a 42-issue pilot across 14 repositories, Phoenix reported 42/42 correctness preservation, or 100%; this measured absence of new regressions, not confirmed issue fixes.
- Manual inspection found that about half of the 42 pilot pull requests were targeted fixes, while the other half often wrote generic code to invented paths such as src/core/config.py.

## Link
- [https://arxiv.org/abs/2606.20243v1](https://arxiv.org/abs/2606.20243v1)
