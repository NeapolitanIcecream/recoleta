---
source: arxiv
url: https://arxiv.org/abs/2605.12731v1
published_at: '2026-05-12T20:33:33'
authors:
- Caleb Helbling
- Graham Leach-Krouse
- Michael Crystal
topics:
- code-translation
- symbolic-execution
- program-equivalence
- rust-migration
- software-assurance
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# Finding a Crab in the C: Assured Translation via Comparative Symbolic Execution

## Summary
cozy checks whether a C binary and a Rust binary behave the same across explored symbolic paths, then shows the developer the remaining differences. The paper applies the existing tool to C-to-Rust translation assurance, including handwritten Rust ports and C2Rust outputs.

## Problem
- Legacy C and C++ code carries memory-safety risk, but rewriting whole codebases in Rust can be too costly and risky.
- Manual ports, transpilers, and ML-based translators can change program behavior; some changes fix bugs, while others introduce errors.
- Developers need path-level evidence about semantic differences, not only a pass/fail equivalence result.

## Approach
- cozy compiles both programs to binaries and runs them in angr with the same symbolic inputs.
- It compares terminal states only when their path constraints are jointly satisfiable, meaning one concrete input could reach both states.
- It uses Z3 to prove selected outputs, memory locations, and other state elements equal, or to generate concrete inputs that expose a difference.
- It caches unsat cores to avoid repeated SMT calls during the naive n^2 terminal-state compatibility check.
- It uses annotations plus Rust interop choices such as repr(C), extern "C", and DWARF layout data to align C and Rust data locations.

## Results
- The authors report 3 C/Rust comparison experiments: insertion sort, a datetime watch update function, and a box blur image filter.
- In the insertion-sort experiment, cozy verified equivalence among handwritten C, handwritten Rust, and C2Rust versions; it also verified equivalent sorted outputs between C insertion sort and Rust bubble sort for bounded input lengths.
- In the watch experiment, C and Rust first diverged because of overflow semantics; after adding input bounds such as sensible year ranges, Z3 proved equal outputs.
- In the box-blur experiment, cozy verified equivalent outputs for small images and kernel sizes, including Rust data modeled through the array2d crate.
- The GUI includes 3 focus mechanisms: highlighting, pruning, and compression; compression has 2 levels.
- The paper gives no timing, memory, benchmark-size, or solver-query reduction numbers, so the strongest concrete result is functional validation across the 3 toy-to-small experiments rather than a measured scalability gain.

## Link
- [https://arxiv.org/abs/2605.12731v1](https://arxiv.org/abs/2605.12731v1)
