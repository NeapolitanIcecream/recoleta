---
kind: ideas
granularity: day
period_start: '2026-05-09T00:00:00'
period_end: '2026-05-10T00:00:00'
run_id: 8742da8e-f0ec-41b9-85e2-b060c55fe5cb
status: succeeded
topics:
- coding agents
- program repair
- execution feedback
- code generation
- formal verification
- agent safety
- multi-agent systems
tags:
- recoleta/ideas
- topic/coding-agents
- topic/program-repair
- topic/execution-feedback
- topic/code-generation
- topic/formal-verification
- topic/agent-safety
- topic/multi-agent-systems
language_code: en
pass_output_id: 139
pass_kind: trend_ideas
upstream_pass_output_id: 138
upstream_pass_kind: trend_synthesis
---

# Execution Checks for Coding Agents

## Summary
Coding-agent reliability work is converging on small, buildable checks around generated code, failed runs, and reusable skills. The practical pattern is to collect execution evidence at the point where a team already makes a trust decision: candidate selection, retry guidance, or skill maintenance.

## Execution-fingerprint selection for generated code candidates
Coding assistants that already sample multiple solutions should add a sandboxed execution stage before returning one answer. The concrete build is simple: generate a small set of diverse inputs, run each candidate with timeouts, record outputs, exception types, and timeouts as an execution fingerprint, then choose from the largest all-success behavior cluster.

Semantic Voting gives the clearest case for this as an adoption change. Across 18 HumanEval+ and MBPP+ configurations, execution-based selectors beat output-pattern majority voting by 19 to 52 percentage points, and sketch-based generated inputs were the best input source in its ablation. Sketch-and-Verify adds a useful candidate-generation rule for cheap model tiers: ask for distinct algorithmic sketches, fill each sketch several times, and verify the resulting candidates by execution. On 19 hard HumanEval+ problems for Gemini 3.1 Flash Lite, K=2,M=5 solved 11 problems, compared with 5 for flat N=10 sampling.

A practical first test is to run this selector on recent internal coding-assistant tasks where multiple candidates were already produced. Track pass rate, sandbox cost, and cases where no all-success cluster appears. DSDE can add a risk score when the top candidate’s behavior cluster is far from the alternatives, giving reviewers a reference-free signal before full validation.

### Evidence
- [Semantic Voting: Execution-Grounded Consensus for LLM Code Generation](../Inbox/2026-05-09--semantic-voting-execution-grounded-consensus-for-llm-code-generation.md): Semantic Voting reports execution fingerprints, sketch-based generated inputs, and 19 to 52 percentage-point gains over output-pattern majority voting.
- [Sketch-and-Verify: Structured Inference-Time Scaling via Program Sketching](../Inbox/2026-05-09--sketch-and-verify-structured-inference-time-scaling-via-program-sketching.md): Sketch-and-Verify reports structured algorithmic sketches and hard-problem gains for Gemini 3.1 Flash Lite at matched candidate counts.
- [Using Semantic Distance to Estimate Uncertainty in LLM-Based Code Generation](../Inbox/2026-05-09--using-semantic-distance-to-estimate-uncertainty-in-llm-based-code-generation.md): DSDE estimates pass@1 failure risk by comparing sampled programs on shared fuzzed inputs without model internals or LLM-as-judge calls.

## Span-level failed-run records for agent retry guidance
Software engineering agents need a retry record that explains the failed run at the span level. A useful implementation would store tool calls, logs, traces, agent intent, tool-environment state, evaluator outcomes, and repeated failure patterns, then produce a bounded retry instruction with a target, operation, verification signal, and boundary condition.

PROBE shows why this belongs beside the agent as an operational side channel. In 257 unresolved first attempts across SWE-bench, EnterpriseOps-Gym, and AIOpsLab, 66.93% of cases came from insufficient validation, tool or subprocess failure handling, or state and workflow error. PROBE reported 65.37% Top-1 diagnosis accuracy and 21.79% recovery, with a Microsoft IcM prototype attached without changing the agent policy, toolset, or execution budget.

The adoption blocker is the vague failed-run artifact: a final benchmark failure or incident label rarely tells the next run what to change. Teams running repo repair agents, service mitigation agents, or enterprise workflow agents can start by logging spans for failed tasks and measuring whether retry prompts tied to a specific failure anchor recover more cases than generic reruns.

### Evidence
- [Debugging the Debuggers: Failure-Anchored Structured Recovery for Software Engineering Agents](../Inbox/2026-05-09--debugging-the-debuggers-failure-anchored-structured-recovery-for-software-engineering-agents.md): PROBE describes span-level telemetry, anchor-first diagnosis, gated retry guidance, and recovery results across 257 unresolved cases.
- [Debugging the Debuggers: Failure-Anchored Structured Recovery for Software Engineering Agents](../Inbox/2026-05-09--debugging-the-debuggers-failure-anchored-structured-recovery-for-software-engineering-agents.md): The paper reports 65.37% Top-1 diagnosis accuracy, 21.79% recovery, and a non-intrusive Microsoft IcM prototype.

## Environment contracts for reusable agent skills
Teams maintaining agent skill libraries should turn operational assumptions inside each skill into checked contracts. The build is a skill scanner that extracts package versions, imports, URLs, API paths, environment variables, Docker images, GitHub Actions, CLI flags, and config files; labels each mention as operational or incidental; validates the operational mentions against live sources; and opens a localized repair prompt or pull request when a contract fails.

SkillGuard is a concrete template for this maintenance layer. DriftBench includes controlled drifts, real-world drifts, and negative controls. Contract-free CI probes produced 40% false positives, while SkillGuard reported 0 false positives over 599 no-drift and hard-negative cases. In a live scan of 49 real skills, it reached 86% conservative precision and 55% recall, and one-round contract-guided repair reached 78% success.

This is most useful for long-lived skills that call external services, install packages, configure infrastructure, or depend on authentication flows. The first deployment can run in report-only mode on a skill library, compare alerts against recent skill failures, and check whether localized drift reports reduce repair time.

### Evidence
- [Skill Drift Is Contract Violation: Proactive Maintenance for LLM Agent Skill Libraries](../Inbox/2026-05-09--skill-drift-is-contract-violation-proactive-maintenance-for-llm-agent-skill-libraries.md): SkillGuard extracts operational environment contracts from skill documents, validates them, and reports precision, recall, false-positive, and repair results.
- [Skill Drift Is Contract Violation: Proactive Maintenance for LLM Agent Skill Libraries](../Inbox/2026-05-09--skill-drift-is-contract-violation-proactive-maintenance-for-llm-agent-skill-libraries.md): The abstract states the practical problem of silent skill decay and the reported false-positive and one-round repair improvements.
