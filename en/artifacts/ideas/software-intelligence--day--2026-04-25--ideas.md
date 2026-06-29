---
kind: ideas
granularity: day
period_start: '2026-04-25T00:00:00'
period_end: '2026-04-26T00:00:00'
run_id: f9f4ae89-06b0-46d4-b288-2d12297bfb6b
status: succeeded
topics:
- agent-evaluation
- coding-agents
- benchmarks
- software-engineering
- repository-execution
tags:
- recoleta/ideas
- topic/agent-evaluation
- topic/coding-agents
- topic/benchmarks
- topic/software-engineering
- topic/repository-execution
language_code: en
pass_output_id: 109
pass_kind: trend_ideas
upstream_pass_output_id: 108
upstream_pass_kind: trend_synthesis
---

# Executable coding evidence

## Summary
Executable evidence is becoming the practical standard for both agent evaluation and coding workflows. The clearest near-term builds are a replayable evaluator that checks real state and tool traces, a repository intake layer that proves environments can run before patch generation starts, and a scientific coding workflow that uses teacher examples when no test cases exist yet.

## Replayable episode evaluation for tool-using agents
Teams building customer-support, ops, or browser agents can now justify an evaluation harness that records the whole run and grades state changes, tool use, and user-visible artifacts. The case is stronger than transcript review alone. The sim/eval paper lays out a concrete stack: separate scenario design, simulation, and grading; log world state, tool traces, transcripts, and screenshots or telemetry; prefer deterministic checks for end state and procedure; use model judges only for narrow questions. CUJBench adds a hard operational example. It freezes browser and backend evidence into deterministic incident snapshots, and six frontier models still reach only 19.7% accuracy, with cross-modal synthesis as the main failure. A practical build here is a replayable episode runner for one narrow workflow such as refunds, order changes, or failed checkout diagnosis, with pass/fail gates on backend state and required tool calls. A cheap first check is to take ten recent support or incident cases, replay them in a sandbox, and compare transcript-only scores against outcome and tool-trace checks. If the rankings differ, the current eval stack is missing failures that matter in production.

### Evidence
- [Simulating and Evaluating Agentic Systems](../Inbox/2026-04-25--simulating-and-evaluating-agentic-systems.md): Defines the sim/eval stack around full-run artifacts, deterministic assertions, tool traces, and state changes.
- [CUJBench: Benchmarking LLM-Agent on Cross-Modal Failure Diagnosis from Browser to Backend](../Inbox/2026-04-25--cujbench-benchmarking-llm-agent-on-cross-modal-failure-diagnosis-from-browser-to-backend.md): Shows low accuracy on deterministic browser-to-backend diagnosis and identifies cross-modal synthesis as a persistent failure mode.

## Repository environment readiness checks before code generation
Repository coding agents need an environment-setup stage with its own success metric before any patch benchmark or deployment workflow. RAT reports that automated setup can succeed on a large share of real repositories, with ESSR of 63.2% on Python, 41.3% on Java, 98.7% on Rust, and 68.7% on JS/TS across a 2,000-plus repository benchmark. The open-source commit study shows why this stage should stay separate from patch generation. Even on small real commits in C projects, generated changes still fail to compile, trigger static-analysis warnings, and miss tests. That points to a concrete product gap: a repository intake worker that detects language, selects a base image, installs dependencies, runs smoke tests, and emits a machine-readable readiness report before any code-edit agent starts. The first users are internal developer-tools teams and benchmark builders who waste time on tasks that fail before execution begins. A cheap validation step is to run the intake worker across a mixed set of fifty repositories and measure how often it reaches a reproducible build or test command without manual fixes.

### Evidence
- [RAT: RunAnyThing via Fully Automated Environment Configuration](../Inbox/2026-04-25--rat-runanything-via-fully-automated-environment-configuration.md): Provides benchmark evidence that automated repository environment configuration is feasible and measurable across languages.
- [Can LLMs be Effective Code Contributors? A Study on Open-source Projects](../Inbox/2026-04-25--can-llms-be-effective-code-contributors-a-study-on-open-source-projects.md): Shows that compile, static-analysis, and test failures remain common even after code generation on real repository tasks.

## Teacher-guided code generation for scientific workflows without test cases
Scientific coding teams can test a code-generation workflow built for cases where no input/output test set exists yet. MOSAIC gives a concrete pattern: use domain-specific teacher examples to produce rationale templates and pseudocode, keep a compact rolling context of prior function signatures and summaries, and limit automatic debugging to syntax and import repair. On SciCode, that setup improves results across GPT-4o, Claude Sonnet 4, and Gemini 2.5 Flash, and the compact context window matters because keeping all prior code drops performance sharply in the ablation. This is useful for labs and research software groups that write numerical or simulation code from method descriptions, where validation often depends on domain review more than fixed test answers. A practical pilot is a scaffold that asks a domain lead to curate a small teacher set for one subfield, then generates workflow code with explicit intermediate steps and handoff points for human review. The first check is simple: compare generated code quality on a small internal task set with and without the compact context and teacher examples, then see whether reviewers spend less time correcting algorithm structure.

### Evidence
- [No Test Cases, No Problem: Distillation-Driven Code Generation for Scientific Workflows](../Inbox/2026-04-25--no-test-cases-no-problem-distillation-driven-code-generation-for-scientific-workflows.md): Shows a concrete alternative to I/O-test-driven generation for scientific workflows and reports gains across several model backbones.
