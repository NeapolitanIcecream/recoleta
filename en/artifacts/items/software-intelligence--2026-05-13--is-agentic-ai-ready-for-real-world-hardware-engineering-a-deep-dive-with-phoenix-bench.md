---
source: arxiv
url: https://arxiv.org/abs/2605.15226v1
published_at: '2026-05-13T14:14:54'
authors:
- Qingyun Zou
- Feng Yu
- Hongshi Tan
- Bingsheng He
- WengFai Wong
topics:
- hardware-engineering
- code-agents
- benchmark
- eda-verification
- verilog-systemverilog
- software-engineering-agents
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Is Agentic AI Ready for Real-World Hardware Engineering? A Deep Dive with Phoenix-bench

## Summary
Phoenix-bench tests whether software coding agents can fix real Verilog/SystemVerilog repository issues under executable EDA checks. The paper finds that current agents transfer poorly from SWE-bench to hardware tasks, mainly because they miss cross-module signal-flow dependencies.

## Problem
- Existing hardware LLM benchmarks usually test isolated module generation, syntax repair, or localized debugging, so they miss repository navigation, hierarchy-aware localization, EDA execution, and maintenance-style patching.
- Real hardware bugs often spread across instantiated modules through ports, parameters, clocks, resets, and signal flow. A software-style call-graph search can stop at the symptom file and miss the source of the bug.
- This matters because hardware patches must pass simulator, parser, synthesis, or testbench checks without breaking existing behavior.

## Approach
- Phoenix-bench contains 511 verified Verilator instances from 114 GitHub repositories, built from a crawl of 18,010 issues across 786 repositories.
- Each task includes the issue, repository snapshot, developer patch, design-flow labels, fail-to-pass tests, pass-to-pass tests, and a Docker-pinned open-source EDA environment.
- The evaluator accepts a patch only when the failing target test passes and the previously passing tests still pass.
- The study evaluates 4 commercial agents and 8 open-source agent structures across 4 LLM backbones, then adds two diagnostics: file-level oracle localization and one round of testbench-log feedback.

## Results
- Top commercial resolved rates on Phoenix-bench are low: Claude Code with Claude Opus 4.7 reaches 38.6%, OpenAI Codex with GPT-5.5 reaches 38.0%, Gemini CLI reaches 37.4%, and GitHub Copilot coding agent reaches 32.7%.
- OpenHands is the strongest open-source structure in the table: 33.9% with GPT-5.2, 33.5% with Gemini-3-Pro, 32.3% with Qwen3-Coder-480B, and 26.0% with DeepSeek-V3.2.
- The same agents lose 37 to 58 percentage points from SWE-bench Verified to Phoenix-bench. OpenHands with Qwen3-Coder-480B drops from 69.6% on SWE-bench Verified to 32.3% on Phoenix-bench.
- File-level oracle localization improves resolved rate by only 1.4 percentage points, because agents still edit the wrong modules or break files that did not need changes.
- One round of testbench-log feedback raises resolved rate to about 42% to 45%, which shows that concrete failing-test evidence gives agents more useful guidance than file names alone.
- Phoenix-bench instances are larger and more cross-file than SWE-bench Verified: the average gold patch edits 737.5 HDL lines and 5.7 HDL files, and the corpus includes 71,048 TESTCASE checks with 99.91% patch-line coverage.

## Link
- [https://arxiv.org/abs/2605.15226v1](https://arxiv.org/abs/2605.15226v1)
