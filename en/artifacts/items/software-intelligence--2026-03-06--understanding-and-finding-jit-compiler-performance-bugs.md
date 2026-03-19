---
source: arxiv
url: http://arxiv.org/abs/2603.06551v1
published_at: '2026-03-06T18:39:33'
authors:
- Zijian Yi
- Cheng Ding
- August Shi
- Milos Gligoric
topics:
- jit-compilers
- performance-bugs
- differential-testing
- compiler-testing
- java-javascript
relevance_score: 0.58
run_id: materialize-outputs
language_code: en
---

# Understanding and Finding JIT Compiler Performance Bugs

## Summary
This paper studies performance bugs in JIT compilers, a class of problems that had previously seen almost no systematic research. The paper first analyzes real-world bugs from four mainstream JITs, then proposes an automated detection tool, Jittery, to find such bugs.

## Problem
- The paper addresses the understanding and detection of **JIT compiler performance bugs**: a compiler may generate code that runs too slowly, or its own compilation process may be too slow, while existing work mainly focuses on semantic errors rather than performance degradation.
- This matters because JITs optimize at runtime, so performance bugs directly slow down real applications, and application developers often cannot fully avoid them merely by changing business logic code.
- The dynamic nature of JITs makes the problem harder to detect: runtime profiling, speculative optimization, deoptimization, tiered compilation, and interactions with the runtime system can all introduce complex and unstable performance anomalies.

## Approach
- The authors first conduct the first systematic empirical study: they collected and manually analyzed **191** fixed performance bugs from the issue trackers of four mainstream JITs—HotSpot, Graal, V8, and SpiderMonkey—to summarize triggering inputs, external symptoms, and root-cause patterns.
- Based on these findings, they propose **layered differential performance testing**: run a large number of small random programs under two JIT configurations and compare the performance difference, treating unusually large differences as candidate performance bugs.
- The core of the “layered” mechanism is simple: first use low-cost, low-iteration quick tests to filter out most normal samples, then gradually increase iterations and measurement intensity for a small number of suspicious programs, balancing throughput and measurement reliability.
- The tool **Jittery** also includes engineering optimizations: it uses runtime information from early layers to prioritize tests, and automatically filters false positives and duplicate samples, reducing manual inspection effort.
- The method design directly reflects the empirical findings: many performance bugs can be triggered by small **micro-benchmarks**, and are often exposed through “performance differences of the same program under different configurations/versions,” making differential testing an appropriate detection mechanism.

## Results
- The empirical study analyzed **191** real JIT performance bugs, covering **4** widely used JIT compilers (HotSpot, Graal, V8, SpiderMonkey); **272** issues were originally collected, and 191 were retained after manual filtering.
- The paper claims that **nearly half** of performance bugs can be exposed by small, focused **micro-benchmarks**, without requiring a full benchmark suite.
- Jittery’s test-prioritization optimization reduces testing time by **92.40%** while **not losing bug-detection capability**.
- Using Jittery, the authors found **12 previously unknown** performance bugs in **Oracle HotSpot and Graal**, of which **11 have been confirmed by developers** and **6 have been fixed**.
- The paper also claims that these new bugs involve not only traditional optimization/code-generation issues, but also JIT-specific mechanisms such as **speculation** and runtime interaction.
- The abstract does not provide more fine-grained standardized benchmark metrics (such as precision/recall on a unified benchmark, throughput, or direct numerical comparisons with existing tools); the strongest quantitative evidence is mainly the number of discovered bugs and the **92.40%** reduction in time.

## Link
- [http://arxiv.org/abs/2603.06551v1](http://arxiv.org/abs/2603.06551v1)
