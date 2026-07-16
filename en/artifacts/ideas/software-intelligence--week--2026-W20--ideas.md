---
kind: ideas
granularity: week
period_start: '2026-05-11T00:00:00'
period_end: '2026-05-18T00:00:00'
run_id: 52aaa7e8-11ce-4900-9433-534e4c85cb37
status: succeeded
topics:
- code agents
- agent evaluation
- executable feedback
- software engineering benchmarks
- runtime traces
- agent security
tags:
- recoleta/ideas
- topic/code-agents
- topic/agent-evaluation
- topic/executable-feedback
- topic/software-engineering-benchmarks
- topic/runtime-traces
- topic/agent-security
language_code: en
pass_output_id: 161
pass_kind: trend_ideas
upstream_pass_output_id: 160
upstream_pass_kind: trend_synthesis
---

# Code Agent Run Provenance

## Summary
Code-agent work now has enough evidence to support narrower adoption gates: require runnable setup and test proof before accepting agent pull requests, audit evaluation harnesses for score exploits before trusting leaderboard numbers, and use paired crashing and safe executions for vulnerability repair. The common operational need is a record that explains what ran, what failed, what changed, and which permissions were available.

## Agent pull-request checks that require setup logs, generated tests, and passing runtime evidence
Engineering teams piloting code agents can add a CI gate for agent-authored pull requests: the agent must show repository setup steps, the verification test it wrote or selected, and the exact command output proving the patch passed. The gate should fail when the environment was prebuilt by a human, when tests are missing, or when the agent stops after a partial fix.

SWE-Cycle gives a concrete template for this workflow. It separates environment reconstruction, code implementation, and verification test generation, then tests a FullCycle run in a bare repository. The reported FullCycle solve rates stay below 14% even when isolated setup and test-generation scores are much higher, which is a direct warning for teams that accept code-agent output after a narrow unit-test pass. SaaSBench adds the full-stack case: more than 95% of failures happen before deep business logic, mainly in setup, integration, premature stopping, and repeated debugging loops. A useful pilot can start with ten internal bug tickets and measure where each agent run fails across those same phases.

### Sources
- [SWE-Cycle: Benchmarking Code Agents across the Complete Issue Resolution Cycle](../Inbox/2026-05-13--swe-cycle-benchmarking-code-agents-across-the-complete-issue-resolution-cycle.md): SWE-Cycle defines end-to-end issue resolution as environment reconstruction, code implementation, and verification test generation, with FullCycle solve rates below 14%.
- [SaaSBench: Exploring the Boundaries of Coding Agents in Long-Horizon Enterprise SaaS Engineering](../Inbox/2026-05-17--saasbench-exploring-the-boundaries-of-coding-agents-in-long-horizon-enterprise-saas-engineering.md): SaaSBench reports that enterprise SaaS agent failures are concentrated in setup, configuration, integration, premature stopping, and debugging loops.

## Benchmark release checks that include exploit audits and per-run rollout records
Teams publishing agent scores should run a reward-hacking audit against the benchmark harness and attach rollout records for scored runs. The audit should map task files, scoring code, environment boundaries, and permissions, then attempt a score-maximizing exploit before the benchmark is used for model selection. The rollout record should include task state, observations, model outputs, tool calls, tool results, artifacts, timing, terminal status, failures, and the reporting rule used to compute the score.

BenchJack shows why this belongs in the release process. It generated working reward-hacking exploits on all 10 audited benchmarks and found 219 distinct flaws. On four benchmarks with fixable designs, repeated audit-and-patch cycles reduced the hackable-task ratio from near 100% to under 10%. Rollout Cards covers the trace side: an audit of 50 popular repositories found none reporting failed, errored, or skipped rollouts beside headline scores, and re-grading fixed artifacts changed reported scores by up to 20.9 percentage points.

### Sources
- [Do Androids Dream of Breaking the Game? Systematically Auditing AI Agent Benchmarks with BenchJack](../Inbox/2026-05-12--do-androids-dream-of-breaking-the-game-systematically-auditing-ai-agent-benchmarks-with-benchjack.md): BenchJack audits agent benchmarks for reward-hacking paths, found exploits across 10 benchmarks, and showed iterative patching can reduce hackable tasks.
- [Rollout Cards: A Reproducibility Standard for Agent Research](../Inbox/2026-05-12--rollout-cards-a-reproducibility-standard-for-agent-research.md): Rollout Cards specifies per-episode records and reporting rules, and shows that reporting choices can change agent benchmark results.

## Vulnerability repair runs that compare crashing and safe executions before patching
Security engineering teams can change automated vulnerability repair runs so the agent first creates nearby proof-of-concept variants, separates crashing and non-crashing executions, and records state probes around the fault site. The patch step should start from a repair specification that names the source location and safety condition, then accept the change only after compilation and re-execution on the original and mutated crashing inputs.

ContraFix is a concrete example of this loop. Its Analyzer compares runtime state across paired executions, then the Patcher turns the inferred safety condition into source edits. The system also stores verified repair specifications and mutation strategies for later cases. Reported results are high enough to justify small internal tests on recurring vulnerability classes: 84.0% resolved on SEC-Bench and 73.8% on PatchEval, with ablations attributing a 27.0 percentage-point gain to contrastive runtime analysis and a 9.0-point gain to skill accumulation.

### Sources
- [ContraFix: Agentic Vulnerability Repair via Differential Runtime Evidence and Skill Reuse](../Inbox/2026-05-17--contrafix-agentic-vulnerability-repair-via-differential-runtime-evidence-and-skill-reuse.md): ContraFix uses paired crashing and safe executions, runtime probes, repair specifications, verification runs, and reusable repair knowledge for vulnerability repair.
