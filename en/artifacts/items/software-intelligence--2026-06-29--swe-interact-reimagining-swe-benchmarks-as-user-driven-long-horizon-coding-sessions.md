---
source: arxiv
url: https://arxiv.org/abs/2606.30573v1
published_at: '2026-06-29T17:17:45'
authors:
- Mohit Raghavendra
- Anisha Gunjal
- Aakash Sabharwal
- Yunzhong He
topics:
- coding-agents
- swe-benchmark
- multi-turn-evaluation
- user-simulation
- human-ai-interaction
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# SWE-INTERACT: Reimagining SWE Benchmarks as User-Driven Long-Horizon Coding Sessions

## Summary
SWE-INTERACT tests coding agents in multi-turn software tasks where a simulated user starts with a vague request, inspects the code, and reveals requirements over time. On the same underlying tasks, this setting cuts top-model resolve rates from about 50% to about 25–27% while raising steps, tokens, and cost.

## Problem
- Standard SWE benchmarks give the agent a full task spec in one prompt, while many real coding-agent sessions start with short, incomplete user requests and several rounds of review.
- Existing user-in-loop SWE benchmarks often start with a fairly clear prompt or use a user simulator that cannot inspect the workspace, so they miss goal discovery, revision, and requirement retention.
- This matters because an agent that solves a fully specified task may still fail when it has to work with a developer who reveals constraints through feedback.

## Approach
- The authors convert 75 tasks into interactive sessions: 25 each from SWE-bench Pro, SWE Atlas Refactoring, and DeepSWE.
- Each task keeps the original Docker environment and final verifier, but the full requirement set is hidden inside a user simulator.
- The simulator uses an Expert Nitpicker persona based on SWE-chat data: short messages, exact API concerns, iterative critique, and delayed requirement disclosure.
- The simulated user can inspect the agent workspace with tools such as `git`, `grep`, `sed`, and `find`, then give grounded feedback through an `ask_user` tool in Harbor.
- Agents save an initial `PLAN.md` and commit revisions after user feedback, which lets the authors measure goal discovery and audit failures over the trajectory.

## Results
- Best single-turn resolve rates were Opus 4.8 at 50.7% and GPT 5.5 at 48.0%; in SWE-INTERACT they fell to 26.7% and 24.7%, drops of 24.0 and 23.3 percentage points.
- All five evaluated agents scored lower in multi-turn mode: Kimi K2.6 fell from 25.3% to 14.7%, Gemini 3.5 Flash from 29.3% to 17.3%, and Sonnet 4.6 from 21.3% to 18.8%.
- Multi-turn runs used more compute. GPT 5.5 rose from 108.6 to 424.8 steps per trial, 0.14M to 0.36M tokens, and $2.78 to $9.84 per trial.
- Interaction traces averaged about 7 user messages per trial; one long run had 27 user messages, 332 user tool calls, and more than 1000 agent steps.
- Goal discovery did not guarantee correctness: GPT 5.5, Opus 4.8, and Sonnet 4.6 eventually addressed more than 90% of task goals on average, yet many final patches still failed the verifier.
- In 287 failed trajectories, the most common semantic failure labels were technical implementation bug and forgotten requirement, each about one third of assigned labels; misinterpretation or bad assumption was about 14%, and missing user requirement was about 12%.

## Link
- [https://arxiv.org/abs/2606.30573v1](https://arxiv.org/abs/2606.30573v1)
