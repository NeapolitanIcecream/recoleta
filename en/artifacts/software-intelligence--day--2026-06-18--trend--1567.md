---
kind: trend
trend_doc_id: 1567
granularity: day
period_start: '2026-06-18T00:00:00'
period_end: '2026-06-19T00:00:00'
topics:
- coding agents
- software engineering
- agent safety
- code evaluation
- compiler tuning
- benchmarking
run_id: materialize-outputs
aliases:
- recoleta-trend-1567
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/agent-safety
- topic/code-evaluation
- topic/compiler-tuning
- topic/benchmarking
language_code: en
pass_output_id: 266
pass_kind: trend_synthesis
---

# Coding agents need failure-tested guidance and gated execution

## Overview
Coding-agent work in this period is judged by operational evidence: repository instructions tested against failures, pull requests gated by baseline tests, and benchmarks that expose language and project-scale gaps. Probe-and-Refine, Phoenix, and Multi-LCB set the tone: useful automation needs a harness that records what was tried and where it failed.

## Findings

### Repository issue agents
Repository context is becoming an object to test, edit, and reuse. Probe-and-Refine starts with generated repository guidance, runs synthetic bug-fix probes, and folds the failures back into a compact guidance file. On 500 SWE-bench Verified instances, it reports a 33.0% mean resolve rate, compared with 28.3% for static repository guidance and 25.5% with no context. The gain mainly comes from more evaluable patches, which suggests that better guidance helps the agent find the right area of the codebase.

Phoenix applies a similar engineering instinct to GitHub issue resolution. It splits work across planner, reproducer, coder, tester, failure analyst, and pull-request agents. Its tester compares a clean baseline run with the patched run, then opens a pull request only when the change adds no new failing tests. On a curated 24-task SWE-bench Lite slice, Phoenix reports 18 oracle-resolved tasks and no PASS_TO_PASS regressions on successful runs.

#### Sources
- [Probe-and-Refine Tuning of Repository Guidance for Coding Agents](../Inbox/2026-06-18--probe-and-refine-tuning-of-repository-guidance-for-coding-agents.md): Probe-and-Refine method and SWE-bench Verified results
- [Phoenix: Safe GitHub Issue Resolution via Multi-Agent LLMs](../Inbox/2026-06-18--phoenix-safe-github-issue-resolution-via-multi-agent-llms.md): Phoenix architecture, baseline-aware testing, and SWE-bench Lite result

### Agent safety controls
Tool permissions are now a measurable agent failure mode. ToolPrivBench gives each task lower-privilege and higher-privilege tools that can all finish the job, so unnecessary high-privilege choice is counted directly. Across 11 models, six exceed 30% over-privileged tool use. Qwen3-8B reaches 64.9%, and LLaMA-3.1-8B reaches 55.9%. General safety tuning transfers poorly in the reported examples, which points to privilege choice as its own target for training and evaluation.

Production-facing agent writeups make the same boundary concrete. Vercel’s Eve packages durable sessions, sandboxes, approvals, channels, traces, and evals into an open-source TypeScript runtime. A separate production brief argues that auth, payments, secrets, and untrusted input need specs, tests, threat modeling, review, audit trails, and named human owners before merge. The common requirement is simple: agents may act quickly, but sensitive changes need explicit gates.

#### Sources
- [When Lower Privileges Suffice: Investigating Over-Privileged Tool Selection in LLM Agents](../Inbox/2026-06-18--when-lower-privileges-suffice-investigating-over-privileged-tool-selection-in-llm-agents.md): ToolPrivBench design and over-privileged tool-selection results
- [Eve](../Inbox/2026-06-18--eve.md): Eve production runtime controls, approvals, sandboxes, tracing, and evals
- [The Line Vibe Coding Can't Cross](../Inbox/2026-06-18--the-line-vibe-coding-can-t-cross.md): Production guidance for gated AI-generated code

### Broader code benchmarks
Python-only code scores look too narrow for current claims about coding ability. Multi-LCB extends LiveCodeBench to 12 languages while keeping release-date filtering and hidden tests. It reports that GPT-OSS-120B Medium has the best average in the excerpt at 67.8 Pass@1, while Qwen3-235B-A22B-Thinking-2507 scores higher in Python and C++ but falls in Rust, Ruby, and Go. The result makes cross-language variance visible instead of hiding it behind a single Python number.

JAMER adds another pressure test: project-level game code on Godot. Its pipeline filters more than 240,000 candidate repositories down to 8,133 behavior-valid projects, then evaluates compile success, structural completeness, and runtime behavior. On code completion, runtime pass rates fall from 80.4% on small projects to 5.7% on large ones. Agent runs improve compilation and runtime pass rates in some settings, but the paper reports no gain in runtime behavioral quality.

#### Sources
- [Multi-LCB: Extending LiveCodeBench to Multiple Programming Languages](../Inbox/2026-06-18--multi-lcb-extending-livecodebench-to-multiple-programming-languages.md): Multi-LCB multilingual benchmark design and Pass@1 results
- [JAMER: Project-Level Code Framework Dataset and Benchmark on Professional Game Engines](../Inbox/2026-06-18--jamer-project-level-code-framework-dataset-and-benchmark-on-professional-game-engines.md): JAMER dataset construction and project-scale benchmark results

### Measured reliability and optimization loops
Reliability work is testing whether cheap agent diversity can mask defects. The N-version programming study generated 69 implementations across five agent harnesses, 23 model configurations, and three languages. After acceptance screening, 48 versions ran on one million randomized inputs. The independence assumption failed: 429 coincident-failure cases appeared where random independence predicted 115.36. Majority voting still helped, cutting mean failures across three-version units from 387.44 for single versions to 130.99.

AutoPass applies the evidence-loop pattern to compiler tuning. It uses LLVM intermediate representation, optimization remarks, runtime measurements, and hardware counters to revise pass pipelines. Across 64 workloads, the three-iteration version reports the best result in 9 of 10 platform-suite settings under the paper’s budget, with geometric-mean speedups over LLVM -O3 of 1.043× on x86-64 and 1.117× on ARM64.

#### Sources
- [N-Version Programming with Coding Agents](../Inbox/2026-06-18--n-version-programming-with-coding-agents.md): N-version programming setup, common-mode failure, and majority-vote results
- [AutoPass: Evidence-Guided LLM Agents for Compiler Performance Tuning](../Inbox/2026-06-18--autopass-evidence-guided-llm-agents-for-compiler-performance-tuning.md): AutoPass evidence-guided compiler tuning method and speedup results
