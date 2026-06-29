---
source: arxiv
url: https://arxiv.org/abs/2605.26548v1
published_at: '2026-05-26T04:59:49'
authors:
- Hwiwon Lee
- Jiawei Liu
- Dongjun Kim
- Ziqi Zhang
- Chunqiu Steven Xia
- Lingming Zhang
topics:
- software-security
- code-intelligence
- llm-agents
- vulnerability-discovery
- benchmarking
- proof-of-concept-generation
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# SEC-bench Pro: Can Language Models Solve Long-Horizon Software Security Tasks?

## Summary
SEC-bench Pro is a benchmark for testing whether LLM coding agents can find and prove real long-horizon software security bugs in large JavaScript engines. The paper reports that current agents solve fewer than 40% of tasks on V8 and SpiderMonkey.

## Problem
- Existing security benchmarks often rely on fuzzing harnesses, sanitizer traces, generated bug descriptions, or patch-specific grading, which can give agents clues that real bug hunters do not get.
- Real JS engine bugs matter because V8 and SpiderMonkey run untrusted code in browsers and runtimes, and exploits can lead to remote code execution.
- Long-horizon bug hunting requires source inspection, environment setup, dynamic testing, and PoC construction across JIT, garbage collection, object layout, sandbox, and memory-safety behavior.

## Approach
- SEC-bench Pro builds tasks from disclosed reports that include a concrete PoC and a linked fix.
- A three-phase pipeline collects reports, reconstructs the historical vulnerable environment with coding agents, and validates each instance with automated oracles.
- Each accepted task ships Docker images for the vulnerable version, fixed version, and latest version.
- The grading system runs each submitted PoC on all three images, then uses an LLM judge to decide whether the evidence matches the target vulnerability rather than an unrelated crash.
- In simple terms, the benchmark turns real bug reports into repeatable security tasks and checks whether an agent can produce a working PoC under realistic conditions.

## Results
- The dataset has 183 validated vulnerabilities: 103 in V8 and 80 in SpiderMonkey.
- The V8 subset includes 86 bounty-qualified reports and 17 non-bounty reports, with $1,540,750 in cumulative Google VRP awards.
- The strongest single-agent configuration solves 33/103 V8 tasks, or 32.0%, and 31/80 SpiderMonkey tasks, or 38.8%.
- The open-weight Kimi-K2.6 baseline solves 12/103 V8 tasks, or 11.7%.
- ClaudeCode and Codex solve different task sets; their union reaches 39/103 on V8, or 37.9%, and 39/80 on SpiderMonkey, or 48.8%.
- A crash-only grader would count 168 configuration-instance successes versus 117 judged successes, an overcount of 51, or 43.6%, showing that target attribution changes the measured score.

## Link
- [https://arxiv.org/abs/2605.26548v1](https://arxiv.org/abs/2605.26548v1)
