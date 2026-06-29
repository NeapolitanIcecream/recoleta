---
source: arxiv
url: https://arxiv.org/abs/2606.20373v1
published_at: '2026-06-18T15:35:40'
authors:
- Zepeng Li
- Jie Ren
- Zhanyong Tang
- Jie Zheng
- Zheng Wang
topics:
- compiler-optimization
- llm-agents
- llvm
- code-intelligence
- performance-tuning
- multi-agent-systems
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# AutoPass: Evidence-Guided LLM Agents for Compiler Performance Tuning

## Summary
AutoPass is an inference-only LLM agent system for LLVM pass tuning. It uses compiler evidence and measured runtime feedback to choose, repair, test, and revise optimization pass pipelines.

## Problem
- Runtime compiler tuning matters because fixed LLVM -O3 pipelines do not perform best on every program and target.
- The search space is large: LLVM 17 exposes over 100 transformation passes, and the paper evaluates 74 passes with sequences up to 107 passes.
- Runtime speed is noisy and hardware-dependent, so PGO, black-box autotuning, and learned policies can miss profitable pass orders or need more data and runs than a deployment budget allows.

## Approach
- AutoPass starts from the LLVM -O3 pipeline and uses four agents: Score, Analysis, Reasoning, and Evaluation.
- The Score Agent ranks functions using call graphs and IR features such as block, loop, call, and conditional-branch counts.
- The Analysis Agent reads LLVM IR plus -Rpass, -Rpass-missed, and -Rpass-analysis remarks, then emits structured JSON about semantic hints and missed optimizations.
- The Reasoning Agent edits pass order and pass parameters, such as unroll factors or inlining thresholds, using compiler evidence and prior runtime results.
- The Evaluation Agent compiles, verifies, runs candidates, measures runtime and hardware counters, keeps only faster valid pipelines, and rolls back to -O3 when no candidate improves.

## Results
- Across 5 benchmark suites with 64 workloads, AutoPass R3 reports the best result in 9 of 10 platform-suite settings against Instrumented PGO, CSSPGO, AutoFDO, and OpenTuner under a 3-iteration budget.
- The abstract reports geometric-mean speedups over LLVM -O3 of 1.043× on x86-64 and 1.117× on ARM64.
- On x86-64, AutoPass R3 reports 1.059× on cBench, 1.009× on PolyBench, 1.137× on CoreMark, 1.008× on MiniFE, and 1.102× on LULESH.
- On ARM64, AutoPass R3 reports 1.111× on cBench, 1.149× on PolyBench, 1.091× on CoreMark, 1.068× on MiniFE, and 1.046× on LULESH.
- The motivating Qsort and BitCount experiment reports an average 1.259× speedup over -O3 across x86-64 and ARM64.
- One-shot AutoPass R1 is weaker than R3 in the table, for example ARM64 PolyBench improves from 1.129× at R1 to 1.149× at R3, and ARM64 CoreMark improves from 1.006× to 1.091×.

## Link
- [https://arxiv.org/abs/2606.20373v1](https://arxiv.org/abs/2606.20373v1)
