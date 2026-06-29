---
kind: ideas
granularity: day
period_start: '2026-04-13T00:00:00'
period_end: '2026-04-14T00:00:00'
run_id: 2c820f02-ea9f-4551-985d-436f1ebff98d
status: succeeded
topics:
- coding-agents
- execution-verification
- software-analysis
- bug-validation
- traceability
tags:
- recoleta/ideas
- topic/coding-agents
- topic/execution-verification
- topic/software-analysis
- topic/bug-validation
- topic/traceability
language_code: en
pass_output_id: 69
pass_kind: trend_ideas
upstream_pass_output_id: 68
upstream_pass_kind: trend_synthesis
---

# Runnable verification artifacts

## Summary
Executable checks are moving into the handoff artifact for coding and analysis workflows. The clearest near-term builds are a CI receipt for agent-written patches, a PoC validator for security report triage, and a staged runbook agent for getting difficult analysis tools running with reproducible evidence.

## CI execution receipts for agent-written patches
A repository-level coding agent should return a patch plus the exact execution record that proved it. AgentForge gives the clearest support for this as a product requirement, not a research nicety: every code change runs in a network-isolated Docker sandbox before it can proceed, and the system reaches 40.0% resolution on SWE-bench Lite, 26 to 28 points above its single-agent baselines. The useful build here is a CI-facing execution receipt layer that stores the patch, generated tests, sandbox configuration, stdout and stderr, and the fail-to-pass and pass-to-pass outcome for each attempt.

This fits teams already experimenting with repo agents and struggling with review time. A reviewer does not need another summary of why a fix should work; they need a replayable record of what actually ran and whether it regressed anything. The first cheap test is narrow: require the agent to attach an execution receipt on one class of tasks such as flaky test repair or small bug fixes, then measure reviewer acceptance rate and time to merge against agent output that arrives as text and diffs alone. AnalysisBench supports the same workflow boundary from another angle. Its best agent only stops after tool-specific evidence is present, and self-validation still overstated success by 15%, which is a warning against letting the agent mark its own work complete without an external artifact check.

### Evidence
- [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](../Inbox/2026-04-13--agentforge-execution-grounded-multi-agent-llm-framework-for-autonomous-software-engineering.md): AgentForge requires sandbox execution for every patch and reports 40.0% resolution with a large gain over single-agent baselines.
- [Evaluating LLM Agents on Automated Software Analysis Tasks](../Inbox/2026-04-13--evaluating-llm-agents-on-automated-software-analysis-tasks.md): AnalysisBench shows evidence-based completion checks matter and self-validation overstated success by 15%.

## Executable proof-of-concept validation for bug report triage
Security teams can add an executable PoC gate between LLM bug finding and human triage. AnyPoC shows why this layer matters. It takes a candidate bug report, either produces a re-runnable proof-of-concept with logs or rejects the report, and it works across 12 large systems including Chromium, Firefox, LLVM, OpenSSL, SQLite, FFmpeg, and Redis. The reported gain is practical: 1.3x more valid PoCs for true bug reports, 9.8x more rejected false positives, and 45 generated PoCs adopted as official regression tests.

The immediate build is a validator service that consumes agent-generated bug reports, spins up the target project in an isolated environment, attempts PoC generation and re-execution, and writes back one of two outputs: confirmed with runnable artifact, or rejected with failure evidence. This is useful for internal AppSec teams and maintainers who already receive too many text-only reports to trust them at face value. A simple first deployment would target one bug class in one codebase with stable CI, then compare analyst time per confirmed finding and the share of rejected reports that would otherwise have reached manual review.

### Evidence
- [AnyPoC: Universal Proof-of-Concept Test Generation for Scalable LLM-Based Bug Detection](../Inbox/2026-04-13--anypoc-universal-proof-of-concept-test-generation-for-scalable-llm-based-bug-detection.md): AnyPoC validates bug reports by generating and re-running executable PoCs, with large gains in valid confirmations and false-positive rejection.

## Analysis runbook agents for first-time tool setup
Teams adopting analyzers, fuzzers, symbolic execution tools, or profilers need an agent that can finish the full setup and show tool-specific output, not an agent that stops after a build or a help screen. AnalysisBench is direct about the failure mode: baseline agents mixed stages, lost the root cause in long logs, and declared success after superficial signals. The custom AnalysisAgent reached 94% verified success on 35 tool-project tasks, versus 77% for the best baseline, by using explicit workflow stages, one action per cycle, deterministic log condensation, and evidence-based completion checks.

That points to a concrete support product for platform engineering and developer productivity teams: an analysis-runbook agent that installs the tool, prepares the project, captures the exact commands and environment, and refuses to finish until the expected analysis artifact exists. The first cheap check is to pick two hard internal tools with low adoption because setup is brittle, then measure whether the runbook agent increases first-success rate for engineers who have never configured those tools before. The value is less in model cleverness than in making each stage legible enough to debug when environment setup fails.

### Evidence
- [Evaluating LLM Agents on Automated Software Analysis Tasks](../Inbox/2026-04-13--evaluating-llm-agents-on-automated-software-analysis-tasks.md): AnalysisBench identifies end-to-end setup and evidence capture as the core bottleneck and reports higher verified success from staged workflows.
- [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](../Inbox/2026-04-13--agentforge-execution-grounded-multi-agent-llm-framework-for-autonomous-software-engineering.md): AgentForge independently supports mandatory execution checks before the system can accept work as complete.
