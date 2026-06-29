---
kind: ideas
granularity: week
period_start: '2026-04-13T00:00:00'
period_end: '2026-04-20T00:00:00'
run_id: 2c820f02-ea9f-4551-985d-436f1ebff98d
status: succeeded
topics:
- coding-agents
- verification
- evaluation
- repositories
- agent-operations
tags:
- recoleta/ideas
- topic/coding-agents
- topic/verification
- topic/evaluation
- topic/repositories
- topic/agent-operations
language_code: en
pass_output_id: 83
pass_kind: trend_ideas
upstream_pass_output_id: 82
upstream_pass_kind: trend_synthesis
---

# Execution control layers for software agents

## Summary
The clearest near-term builds are operational control layers around coding agents: a hard sandbox replay gate before patch acceptance, an agent-run software analysis setup flow that stops on verified project evidence, and a typed action contract layer for enterprise actions. Each case is supported by papers that move past fluent traces and report concrete execution, validation, or permission mechanisms with measurable effects.

## Sandbox replay gate for repository patch acceptance
A repository agent can ship with a mandatory execution gate before any patch is accepted. The evidence this week is specific enough to support a concrete build: run every proposed edit inside an isolated container, require fail-to-pass tests to pass with no pass-to-pass regressions, and feed real stdout, stderr, and test failures back into a repair loop. AgentForge reports 40.0% resolution on SWE-bench Lite with this structure, using a network-isolated Docker sandbox and up to three debugger retries. That is a stronger operational pattern than accepting patches from model output alone.

The first user is the team already trying code agents on test-bearing repositories and seeing plausible diffs fail in CI. A cheap check is narrow: take one repository with stable tests, insert a hard execution requirement before merge, and measure how many agent patches survive replay without human cleanup. If the pass rate rises while review burden falls, the gate is doing useful work. If the repository lacks reliable tests, this workflow stalls fast, so the build should begin where execution already has teeth.

### Evidence
- [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](../Inbox/2026-04-13--agentforge-execution-grounded-multi-agent-llm-framework-for-autonomous-software-engineering.md): Shows a coding agent workflow where every change must survive sandboxed execution before it advances, with benchmark results and concrete sandbox constraints.
- [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](../Inbox/2026-04-13--agentforge-execution-grounded-multi-agent-llm-framework-for-autonomous-software-engineering.md): Confirms the closed-loop Tester–Debugger design, live repository index, and execution of every patch inside a constrained Docker sandbox.

## Agent-run software analysis setup with evidence-based completion checks
Teams adopting analyzers, fuzzers, symbolic execution tools, and profilers can use an agent that owns the full setup-and-proof workflow, not just command generation. AnalysisBench gives a concrete target for that build: create an isolated container, install the tool, build the project, generate any tool-specific prerequisites, run the analysis, and stop only when the run produces project-specific evidence. AnalysisAgent reached 94% verified success on 35 tool-project tasks, while the best baseline reached 77%. The paper also shows why this support layer matters: self-validation still overstated success, with a 15% false-positive rate against manual verification.

The practical product is a setup runner for internal AppSec and performance teams who lose time wiring tools into unfamiliar repositories. The fast validation step is to pick one painful internal analyzer rollout, have the agent produce a reproducible environment plus one evidence artifact that a human would already trust, and compare elapsed setup time with the current manual path. Stopping criteria need to be strict. A successful build or a `--help` screen is not enough if the analyzer did not produce real project output.

### Evidence
- [Evaluating LLM Agents on Automated Software Analysis Tasks](../Inbox/2026-04-13--evaluating-llm-agents-on-automated-software-analysis-tasks.md): Provides the benchmark, verified success gap, false-positive rate for self-validation, and the explicit staged workflow for automated software analysis.
- [Evaluating LLM Agents on Automated Software Analysis Tasks](../Inbox/2026-04-13--evaluating-llm-agents-on-automated-software-analysis-tasks.md): Details common failure modes such as premature stopping and poor error localization, which support a concrete evidence-based completion layer.

## Typed action contract layer for enterprise agent execution
Enterprise coding and operations agents need an execution layer that exposes only typed actions the current user is allowed to run, validates inputs before side effects, and routes execution through the application's own services. Two papers point to the same adoption blocker. Claude Code’s analyzed codebase puts most of its complexity in permission modes, context compaction, hooks, and tool control around a simple model loop. BAL reports that typed action contracts, runtime permission filtering, workspace scoping, and approval gates completed 23 of 25 enterprise scenarios with zero unsafe executions, while an unconstrained setup completed 17 of 25.

A concrete build is a contract registry for high-risk actions such as deployment, ticket changes, user administration, and data export. Each action definition needs an input schema, permission predicate, validation function, execution callback, and result format. The first buyer is the team blocked on letting agents touch production systems. The cheapest test is to wrap a small set of existing internal actions and replay known bad cases, especially wrong-entity edits and cross-workspace requests, to see whether the contract layer blocks them before execution.

### Evidence
- [Bounded Autonomy for Enterprise AI: Typed Action Contracts and Consumer-Side Execution](../Inbox/2026-04-16--bounded-autonomy-for-enterprise-ai-typed-action-contracts-and-consumer-side-execution.md): Shows typed action contracts, permission-aware capability exposure, consumer-side execution, and enterprise trial results with zero unsafe executions under the bounded layer.
- [Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems](../Inbox/2026-04-14--dive-into-claude-code-the-design-space-of-today-s-and-future-ai-agent-systems.md): Shows that production coding-agent complexity concentrates in permissions, context management, extensibility, and control systems around a simple agent loop.
