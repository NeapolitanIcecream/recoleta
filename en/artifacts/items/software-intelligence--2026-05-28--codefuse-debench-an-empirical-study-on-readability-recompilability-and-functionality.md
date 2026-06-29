---
source: arxiv
url: https://arxiv.org/abs/2605.29490v1
published_at: '2026-05-28T07:17:53'
authors:
- Puzhuo Liu
- Yuhan Huang
- Jianlei Chi
- Peng Di
- Yu Jiang
topics:
- binary-decompilation
- code-intelligence
- llm-evaluation
- automated-repair
- software-security
- program-analysis
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# CODEFUSE-DEBENCH: An Empirical Study on Readability, Recompilability, and Functionality

## Summary
CODEFUSE-DeBench evaluates binary decompilers by asking whether their output is readable, can be recompiled after bounded repair, and behaves like the original binary. The study finds a large gap between code that compiles and code that preserves behavior.

## Problem
- Binary decompilers are often judged with surface metrics such as line counts, character matches, or readability scores, which do not show whether the recovered code can be reused.
- This matters for reverse engineering, security analysis, automated patching, cross-architecture migration, and static analysis on binaries when source code is missing or unreliable.
- Readable decompiled code can still be wrong, while messy code can preserve behavior, so one metric gives users poor tool guidance.

## Approach
- DeBench uses 240 atomic test functions across 8 source-code dimensions, compiled into 640 binaries across compilers, optimization levels, debug-symbol settings, architectures, and related build choices.
- It evaluates 5 whole-program decompilers: IDA, Ghidra, RetDec, Angr, and BinaryAI.
- Readability is scored with URAF, an LLM-judged rubric with 18 sub-dimensions covering naming, structure, types, semantic clarity, and context.
- Recompilability is measured by iterative compile-and-repair with 3 independent repair LLMs under a fixed 50-iteration budget.
- Functionality is checked with Frida-based differential dynamic tracing at program, function, and instruction levels.

## Results
- The best decompiler plus repair-LLM pair reaches 22.3% Exact+Partial program-level behavioral overlap, but only 1.2% exact stdout match.
- The paper reports an approximately 50 percentage-point drop from recompilability to functional equivalence, showing that successful recompilation often fails to preserve runtime behavior.
- Optimization and compiler choice change outcomes: O3 gives the lowest readability but the highest functionality, and Clang produces 2.6x higher functionality than GCC while scoring lower on readability.
- Decompiler choice matters more than repair-LLM choice: the cross-decompiler functional swing is 20x, while the cross-LLM swing is 1.6x.
- Failure analysis finds syntactic noise that repair can often fix, type-system collapse at about 19% of all repair errors, and upstream losses such as ARM64 relocation idioms and C++ ABI features that repair LLMs do not recover.

## Link
- [https://arxiv.org/abs/2605.29490v1](https://arxiv.org/abs/2605.29490v1)
