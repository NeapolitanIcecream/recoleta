---
source: arxiv
url: http://arxiv.org/abs/2604.02547v1
published_at: '2026-04-02T21:56:23'
authors:
- Tural Mehtiyev
- "Wesley Assun\xE7\xE3o"
topics:
- coding-agents
- software-engineering
- trajectory-analysis
- swe-bench
- llm-evaluation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Beyond Resolution Rates: Behavioral Drivers of Coding Agent Success and Failure

## Summary
This paper studies why coding agents fail by analyzing 9,374 trajectories from 19 agents on 500 SWE-bench Verified tasks. It argues that resolution rate alone hides the main drivers of failure: wrong architectural judgment, weak trajectory structure, and LLM limits that matter more than framework choice.

## Problem
- Coding agents still fail on a large share of software tasks, with top systems missing over 20% of benchmarked problems, but benchmark scores do not explain why they fail.
- Prior analyses often mix up task difficulty, agent identity, and behavior, so common claims such as "longer trajectories mean failure" may be confounded.
- This matters for automated software production because teams need to know whether failures come from hard tasks, poor search/validation behavior, weak models, or bad framework design.

## Approach
- The authors analyze 9,374 agent trajectories from 19 agents, covering 8 frameworks and 14 LLMs, on the same 500 SWE-bench Verified tasks so they can compare agents on identical problems.
- They encode each trajectory into a compact sequence of 13 action/response symbols, including code reading, patching, re-patching, test runs, reproduction scripts, setup steps, and error-triggering edits such as syntax or import failures.
- For task difficulty, they extract 90 features per task across patch complexity, test demand, issue text, and metadata, then compare never-solved and always-solved simple-patch tasks.
- For behavior, they use two paired analyses: one that fixes the agent and compares its successes vs. failures across tasks, and one that fixes the task and compares successful vs. failed agents on that same task.
- For model vs. framework effects, they compare agents that share a framework but use different LLMs, and agents that share an LLM but use different frameworks.

## Results
- The dataset contains 500 tasks: 55 never solved by any agent (11%), 416 contested (83%), and 29 always solved (6%).
- Among the 55 never-solved tasks, 12 need only a single-file patch with <=10 total changes, and all 12 were still failed by all 19 agents. Human annotators had labeled these as easy or short tasks, often <15 minutes or 15 minutes-1 hour.
- Patch complexity did not separate these easy-looking failures from simple always-solved tasks: mean total changes were 4.75 vs. 3.76, with Mann-Whitney p=0.24 and Cliff's delta=0.24.
- Only 5 of 90 task features showed significant differences for those simple-patch cases, all outside raw patch size: fail-to-pass count 2.42 vs. 1.24 (p<0.001), FTP test files 2.17 vs. 1.20 (p=0.001), test patch files 1.58 vs. 1.00 (p=0.003), test patch changes 21.25 vs. 12.64 (p=0.025), and presence of repro code 0.67 vs. 0.24 (p=0.014).
- In the 12 never-solved simple-patch tasks, the best agent found the gold-patch file in 12/12 cases and edited it in 10/12, yet still failed every task. The paper attributes 10/12 of these failures to architectural judgment errors, plus 1 behavioral failure and 1 domain-knowledge failure.
- The excerpt claims that trajectory length changes direction once task difficulty is controlled, so length alone is an unreliable failure signal. It also claims that agents that gather context before editing and run more validation succeed more often, and that these tactics are mostly set by the agent rather than adapted per task.
- The excerpt also claims that the LLM is the main driver of both outcomes and behavior: agents with the same LLM agree on more tasks than agents with the same framework, and framework gaps shrink as LLM quality improves. The excerpt does not provide the numeric effect sizes for these RQ2 and RQ3 claims.

## Link
- [http://arxiv.org/abs/2604.02547v1](http://arxiv.org/abs/2604.02547v1)
