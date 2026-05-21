---
source: arxiv
url: https://arxiv.org/abs/2605.08927v1
published_at: '2026-05-09T12:55:54'
authors:
- Martin Rinard
topics:
- coding-agents
- compiler-verification
- credible-compilation
- lean4
- software-foundation-models
- code-intelligence
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Quantitative Comparison of Credible Compilation and Verification In Coding Agent Compiler Development

## Summary
The paper compares credible compilation with full verification for compiler optimizations built by Claude Code Opus 4.7 in Lean 4 under human supervision. It finds that credible compilation needed far less development work, while full verification produced larger proof burdens and slower optimization code for the tested passes.

## Problem
- Compiler builders need correct optimizations, but they must choose between translation validation and full machine-checked verification with little direct cost data.
- This matters for coding-agent software engineering because proof work can dominate agent time, supervisor time, and update cost.
- The paper studies three optimizations in the Axon verified compiler: unreachable code elimination, dead assignment elimination, and constant propagation/folding.

## Approach
- Credible compilation uses an unverified optimization plus a verified certificate checker. If the checker rejects the certificate, the transformation is discarded.
- Full verification proves the optimization itself correct in Lean 4, so the pass runs without certificate generation or certificate checking.
- The authors supervised Claude Code Opus 4.7 in Visual Studio while it implemented both versions for the same optimizations in Axon.
- They measured sessions, active time, generated tokens, cache reads, code lines, proof lines, supervisor prompts, and compile-time costs on the Livermore benchmarks.

## Results
- Verified optimization development took much more active time than credible compilation: UCE 5:58 vs 0:18, UCE+DAE 8:11 vs 1:05, and CP 9:40 vs 1:10.
- Token use was also higher for verified versions: UCE 12.27M vs 0.49M, UCE+DAE 16.35M vs 1.86M, and CP 17.86M vs 1.75M.
- The paper reports verified-to-credible active-time ratios of 19.9 for UCE, 7.6 for UCE+DAE, and 8.3 for CP; token ratios were 25.0, 8.8, and 10.2.
- Proof code dominated verified development: UCE VF added 4,348 proof lines, UCE+DAE VF added 8,158 proof lines, and CP VF added 6,131 proof lines. Credible compilation optimization rows added 0 proof lines, though checker updates required proofs.
- The agent often reduced optimization scope to ease proofs, including replacing removed instructions with halt or noop operations, adding runtime checks, and limiting assignment cases; supervisors had to push these limits back.
- Runtime measurements on Livermore show verified passes were slower than credible optimization execution alone. For k18_hydro_2d, CP VF took 4,127.36 while CP CC opt took 24.93, and UCE+DAE VF took 606.52 while UCE+DAE CC opt took 4.18. Certificate checks often dominated CC cost, such as 401.17 for CP and 395.86 for UCE+DAE on k18_hydro_2d.

## Link
- [https://arxiv.org/abs/2605.08927v1](https://arxiv.org/abs/2605.08927v1)
