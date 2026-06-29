---
kind: ideas
granularity: day
period_start: '2026-04-04T00:00:00'
period_end: '2026-04-05T00:00:00'
run_id: e30d1f13-3c1f-4ef7-8316-e547eaa9439c
status: succeeded
topics:
- coding-agents
- repository-level-generation
- program-repair
- runtime-debugging
- agent-safety
- context-pruning
tags:
- recoleta/ideas
- topic/coding-agents
- topic/repository-level-generation
- topic/program-repair
- topic/runtime-debugging
- topic/agent-safety
- topic/context-pruning
language_code: en
pass_output_id: 15
pass_kind: trend_ideas
upstream_pass_output_id: 14
upstream_pass_kind: trend_synthesis
---

# Execution-Aware Agent Control

## Summary
Execution evidence is moving into the center of coding-agent workflows. The clearest product changes are a retry controller that preserves useful state across repository-level attempts, a debugger-integrated repair loop for reproducible C and C++ security bugs, and permission checks that inspect file-edit paths with the same rigor as shell commands.

## Persistent attempt memory for repository-level generation
Repository-level coding agents need a retry controller that keeps explicit memory across full attempts and always returns the best artifact seen so far. The current evidence points to a specific design: store structured success notes, failure notes, and the highest-scoring repository after each run, then feed those records back into the next attempt together with execution feedback. LiveCoder reports up to 22.94 points of functional improvement on RAL-Bench, repository reuse up to 81.58%, and cost reduction up to 53.63%. EnvGraph supports the same operational change from a different angle: many repository failures are still installation, dependency, and cross-file reference failures, so retries need runtime diagnosis, not just more sampling.

The practical build is a repository runner that logs each attempt as a durable artifact with test results, install logs, runtime errors, and a compact diagnosis record. Teams evaluating coding agents on internal scaffolding or greenfield service generation can test this cheaply by comparing three conditions on the same task set: single-shot generation, repeated attempts without memory, and repeated attempts with persistent attempt memory plus best-artifact fallback. If the win is real, later attempts should stop erasing earlier partial successes, and the system should recover more executables without paying for the same failures again.

### Evidence
- [Persistent Cross-Attempt State Optimization for Repository-Level Code Generation](../Inbox/2026-04-04--persistent-cross-attempt-state-optimization-for-repository-level-code-generation.md): LiveCoder reports cross-attempt state, best-repository retention, functional gains, repository reuse, and cost reduction.
- [Toward Executable Repository-Level Code Generation via Environment Alignment](../Inbox/2026-04-04--toward-executable-repository-level-code-generation-via-environment-alignment.md): EnvGraph shows that execution failures often come from dependency and internal reference alignment, which supports runtime-informed retry control.

## Debugger-integrated patch loops for C and C++ vulnerability repair
C and C++ repair agents can justify a debugger-first workflow for memory-safety bugs. DebugHarness gives a concrete pattern: start from a reproducible crash and sanitizer signal, inspect runtime state through GDB and pwndbg, use rr to move backward through execution, test root-cause hypotheses with watchpoints and breakpoints, then generate and validate a patch in the same loop. On SEC-bench, the paper reports about 90% resolution across 200 real-world vulnerabilities in 29 projects, above PatchAgent at 57.5% and VulnResolver at 67.5%.

The near-term product change is a repair harness for security teams that already have fuzzing outputs and PoC crashes but still hand off root-cause analysis to senior engineers. A cheap check is narrow and concrete: take a backlog of reproducible AddressSanitizer or crash-triggered bugs, restrict the agent to runtime inspection plus patch validation, and measure time to first plausible root-cause hypothesis and validated patch rate against a static-code baseline. The evidence here is strongest for low-level memory faults where the crash site and the real defect are far apart.

### Evidence
- [DebugHarness: Emulating Human Dynamic Debugging for Autonomous Program Repair](../Inbox/2026-04-04--debugharness-emulating-human-dynamic-debugging-for-autonomous-program-repair.md): DebugHarness describes the debugger-driven loop and reports the resolution-rate gains on SEC-bench.

## Effect-based permission checks for agent file edits
Permission gates for coding agents need action-level coverage over file edits, not only shell commands. AmPermBench shows why: in Claude Code auto mode, 36.8% of state-changing actions flowed through Tier 2 file edits that the classifier never inspected, producing 51 false negatives there alone. End-to-end false negatives reached 81.0% across 253 state-changing actions, and artifact cleanup was especially exposed because agents could edit `objects.json` to achieve the same effect as a blocked command. This supports a concrete control change for DevOps and internal platform teams: normalize proposed edits into their real operational effect before approval, then evaluate policy on that effect.

A usable build is an interposition layer that classifies writes, patches, and generated config changes by resource touched and state change implied, then routes them through the same policy engine used for command execution. The first test does not require a full benchmark suite. Take a handful of ambiguous cleanup or restart tasks in your own repos, run the agent with shell-only permission checks, then add edit-path classification and compare unsafe action escapes at the individual action level. The main adoption blocker is straightforward: teams that trust command gating alone are leaving an uninspected path for equivalent destructive actions.

### Evidence
- [Measuring the Permission Gate: A Stress-Test Evaluation of Claude Code's Auto Mode](../Inbox/2026-04-04--measuring-the-permission-gate-a-stress-test-evaluation-of-claude-code-s-auto-mode.md): AmPermBench reports the end-to-end false negative rate, the Tier 2 coverage gap, and the artifact-cleanup failure mode through file edits.
- [Measuring the Permission Gate: A Stress-Test Evaluation of Claude Code's Auto Mode](../Inbox/2026-04-04--measuring-the-permission-gate-a-stress-test-evaluation-of-claude-code-s-auto-mode.md): The paper explains that agents achieve equivalent state changes through file edits that the classifier does not evaluate.
