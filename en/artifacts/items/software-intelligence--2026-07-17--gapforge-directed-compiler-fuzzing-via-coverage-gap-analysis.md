---
source: arxiv
url: https://arxiv.org/abs/2607.15762v1
published_at: '2026-07-17T08:53:19'
authors:
- Mingxuan Zhu
- Qingyuan Liang
- Junjie Chen
- Zhihong Xue
- Dan Hao
topics:
- compiler-fuzzing
- code-intelligence
- llm-test-generation
- coverage-guided-testing
- automated-software-production
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# GapForge: Directed Compiler Fuzzing via Coverage-Gap Analysis

## Summary
GapForge is an LLM-based compiler fuzzing technique that targets specific source-code coverage gaps instead of generating tests without compiler-wide guidance. On GCC 14.3.0 and LLVM 19.1.0, it improves 72-hour coverage and finds 12 real-world compiler failures.

## Problem
- Large compilers such as GCC and LLVM contain long-tail, under-tested code regions that general-purpose fuzzers repeatedly miss.
- Reaching an uncovered region often requires both a particular program structure and specific compiler options, which file-level summaries and program-driven generation do not reliably infer.
- This matters because compiler defects can cause crashes and silent miscompilations in downstream software.

## Approach
- GapForge scores source files with `L_f × (1-C_f)^2`, favoring large files with low line coverage, then samples one target file per iteration.
- An LLM analyzes each uncovered line span together with nearby covered context to infer the control-flow, data, and compilation-option requirements for reaching the target basic blocks.
- It synthesizes a prompt combining general C/C++ generation constraints, these target requirements, and previously failed prompts for the same file.
- Generated programs are compiled, measured with coverage feedback, and used to guide subsequent target selection and prompt refinement.

## Results
- Within 72 hours, GapForge reached 68.13% line coverage on GCC core modules and 69.11% on LLVM core modules.
- It covered 24,736 more lines than WhiteFox on GCC and 19,798 more lines on LLVM; WhiteFox reached 64.62% and 65.02%, respectively.
- Compared with the strongest reported baseline, LegoFuzz, which reached 64.99% on GCC and 66.59% on LLVM, GapForge also improved coverage of the official test suites by 3,452 GCC lines and 531 LLVM lines, versus LegoFuzz's 705 and 143 lines.
- GapForge found 12 real-world compiler failures: 5 in GCC and 7 in LLVM, including 8 crashes and 4 miscompilations.
- Nine ablation variants performed worse than the complete system, supporting contributions from target selection, targeted summarization, compilation-option inference, and failure reflection.

## Link
- [https://arxiv.org/abs/2607.15762v1](https://arxiv.org/abs/2607.15762v1)
