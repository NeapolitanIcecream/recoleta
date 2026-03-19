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
- performance-testing
- compiler-bugs
- differential-testing
- empirical-study
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Understanding and Finding JIT Compiler Performance Bugs

## Summary
This paper studies performance bugs in JIT compilers: these bugs do not cause programs to compute incorrect results, but they can make compilation or execution noticeably slower. The authors first analyze 191 real bugs from 4 mainstream JITs, and then propose an automated detection tool called Jittery.

## Problem
- The paper addresses the problem of understanding and automatically finding **JIT compiler performance bugs**, including two categories: **overly slow compilation** and **overly slow execution of generated code**.
- This matters because JITs optimize during program execution; once something goes wrong, applications directly suffer latency, throughput degradation, or fallback during real execution, while application developers often cannot fully fix the issue at the source-code level.
- Prior work has mainly focused on JIT **functional correctness bugs** or AOT/application-level performance bugs, with almost no systematic methods specifically targeting JIT performance bugs, even though JITs have unique complexities such as profiling, speculation, deoptimization, and tiered compilation.

## Approach
- The authors first conduct the first relatively systematic empirical study: they collect and manually filter real bugs from **HotSpot, Graal, V8, and SpiderMonkey**, ultimately analyzing **191** reports and summarizing triggering inputs, manifestation patterns, and root causes.
- The study finds that many performance bugs can be triggered by **small microbenchmarks**, rather than requiring full benchmark suites; many bugs are also exposed through **differential signals**, such as performance differences across different JIT configurations, different versions, or equivalent executions.
- Based on these insights, the authors propose **layered differential performance testing**: for a large number of randomly generated small programs, execute them under two JIT configurations and compare timing differences, marking clearly abnormal programs as candidate bugs.
- To balance speed and accuracy, the method uses **layered testing**: the earlier layers use a small number of iterations to quickly eliminate samples without anomalies, while later layers apply stricter measurements with higher iteration counts only to the remaining candidates.
- The tool **Jittery** also adds practical optimizations: **test prioritization** uses runtime information from earlier layers to prioritize more suspicious samples; and heuristics are used to automatically filter **false positives and duplicates**, reducing the burden of manual review.

## Results
- The empirical study covers **4** mainstream JIT compilers, with an initial collection of **272** issues; after manual filtering, **191** real performance bugs are retained and analyzed.
- The authors claim that **nearly half** of performance bugs can be exposed by **small, focused microbenchmarks** rather than requiring a full benchmark suite; this is an important basis for their test design.
- Jittery’s **test prioritization** reduces testing time by **92.40%**, while claiming **no loss** in bug-finding capability.
- Using Jittery, the authors discovered **12** previously unknown performance bugs in **Oracle HotSpot** and **Graal**.
- Of these **12** new bugs, **11** have been confirmed by developers, and **6** have already been fixed.
- The abstract does not provide more detailed standardized performance metrics (such as specific slowdown factors, precision/recall, per-compiler discovery rates, or direct comparisons with existing tools); the strongest quantitative conclusions are mainly the bug discovery count above and the **92.40%** time reduction.

## Link
- [http://arxiv.org/abs/2603.06551v1](http://arxiv.org/abs/2603.06551v1)
