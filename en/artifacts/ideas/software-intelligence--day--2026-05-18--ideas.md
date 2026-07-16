---
kind: ideas
granularity: day
period_start: '2026-05-18T00:00:00'
period_end: '2026-05-19T00:00:00'
run_id: f4d60be8-002e-44a7-a834-d55624705ca0
status: succeeded
topics:
- coding agents
- software engineering agents
- agent evaluation
- code repair
- bug localization
- agent safety
- repository context
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering-agents
- topic/agent-evaluation
- topic/code-repair
- topic/bug-localization
- topic/agent-safety
- topic/repository-context
language_code: en
pass_output_id: 177
pass_kind: trend_ideas
upstream_pass_output_id: 176
upstream_pass_kind: trend_synthesis
---

# Coding agent execution controls

## Summary
Coding-agent teams can test runtime scope, trace quality, and file selection as separate parts of the execution path. The evidence supports practical checks before wider rollout: trap out-of-scope actions, score agent logs for process defects, and narrow repair context before iterative fixes.

## Permission prompts and filesystem audits for coding-agent runs
Teams giving coding agents shell, file, or network access can add a small authorization test suite before allowing broader use on developer machines or production-adjacent repos. Each test run should define the allowed files, plant harmless sensitive fixtures outside that scope, record shell actions through a shim, collect agent event streams, and compare filesystem snapshots after the run.

OverEager-Bench gives a concrete pattern for this. It counts out-of-scope writes and reads of declared sensitive locations during benign tasks, across Claude Code, OpenHands, Codex CLI, Gemini CLI, and base models. The reported overeager rate is much lower in an ask-to-continue OpenHands setup, between 0.2% and 4.5%, than in more permissive runtimes, between 5.4% and 27.7%. That makes runtime permission design a measurable product choice for coding-agent adoption. A small internal version can start with cleanup, migration, dependency update, and config-edit tasks, then fail a candidate setup when it touches traps outside the stated scope.

### Sources
- [Overeager Coding Agents: Measuring Out-of-Scope Actions on Benign Tasks](../Inbox/2026-05-18--overeager-coding-agents-measuring-out-of-scope-actions-on-benign-tasks.md): Defines overeager actions, describes the audit setup, and reports lower rates for ask-to-continue runtime permissions than permissive runtimes.
- [Overeager Coding Agents: Measuring Out-of-Scope Actions on Benign Tasks](../Inbox/2026-05-18--overeager-coding-agents-measuring-out-of-scope-actions-on-benign-tasks.md): Shows the benchmark focus on shell, file, and network privileges and out-of-scope actions during benign tasks.

## Trace defect scorecards for coding-agent evaluation
Agent owners can add a trace review step to coding-agent evaluations and release gates. The review should parse each run into ordered events, then flag repeated tool calls, stale or ghost context, dead steps, long chains, weak handoff, and poor reversibility. This catches runs that pass endpoint tests while leaving maintainers with brittle or hard-to-interrupt executions.

ProcBench provides a ready checklist for the first version: 11 defect classes grouped under context management, tool-use efficiency, workflow architecture, and tool-system consistency, with control preservation scored through interpretability, interruptibility, correctability, reversibility, and authority handoff. The cross-configuration SWE-bench study adds a warning for metric design: the same error-rate signal split almost evenly across configurations, with 47 resolving more issues when error rate was lower and 48 resolving more when it was higher. A useful implementation needs per-runtime calibration before teams treat one trace metric as a universal success rule.

### Sources
- [ProcBench: Evaluating Process-Level Defects and Control Preservation in LLM Coding Agents](../Inbox/2026-05-18--procbench-evaluating-process-level-defects-and-control-preservation-in-llm-coding-agents.md): Describes ProcBench’s trajectory format, defect classes, calibrated risk scorecards, and control-preservation dimensions.
- [Same Signal, Different Semantics: A Cross-Framework Behavioral Analysis of Software Engineering Agents](../Inbox/2026-05-18--same-signal-different-semantics-a-cross-framework-behavioral-analysis-of-software-engineering-agents.md): Shows that behavior-outcome signals vary by agent configuration, including the split interpretation of error rate and larger framework effects.

## File-level localization before automated repair
Repair pipelines can place a file-level localization step between the bug report and the patch agent. The step should index files with AST-aware chunks, attach relative paths to chunks, split the report into structural and behavioral queries, retrieve a small candidate set, and rerank the top files before any patch generation. The repair agent then works inside a tighter file set and can keep verdicts or test failures across repair attempts.

BLAgent shows why this is worth testing in large repositories: SWE-bench repositories average over 11,000 functions and 168,000 statements, and wrong file selection can break later repair stages. On SWE-bench Lite, BLAgent reports 86.7% Top-1 file accuracy with a closed-source model and 78.6% with an open-source model, plus improved Agentless repair success. A-ProS supports the second half of the workflow: after live judge feedback, stateful refinement beat stateless repair by 8.5 to 10.6 percentage points in its ablation and reduced repeated failures. A practical pilot can compare current repair runs against file-localized, stateful runs on recent internal bugs with known fix files.

### Sources
- [BLAgent: Agentic RAG for File-Level Bug Localization](../Inbox/2026-05-18--blagent-agentic-rag-for-file-level-bug-localization.md): Details BLAgent’s AST-aware indexing, dual-query retrieval, reranking, SWE-bench Lite accuracy, and downstream repair gains.
- [A-ProS: Towards Reliable Autonomous Programming Through Multi-Model Feedback](../Inbox/2026-05-18--a-pros-towards-reliable-autonomous-programming-through-multi-model-feedback.md): Reports the benefit of keeping repair history across feedback rounds and the acceptance gains after iterative refinement.
