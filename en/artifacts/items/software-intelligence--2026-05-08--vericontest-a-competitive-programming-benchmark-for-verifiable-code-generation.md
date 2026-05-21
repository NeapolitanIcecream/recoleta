---
source: arxiv
url: https://arxiv.org/abs/2605.08553v1
published_at: '2026-05-08T23:25:05'
authors:
- Zichen Xie
- Mrigank Pawagi
- Yuxin Liu
- Aaditi Rai
- Lize Shao
- John Berberian
- Sicong Che
- Wenxi Wang
topics:
- verifiable-code-generation
- code-generation-benchmark
- formal-verification
- rust-verus
- proof-generation
- specification-generation
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# VeriContest: A Competitive-Programming Benchmark for Verifiable Code Generation

## Summary
VeriContest is a 946-problem Rust/Verus benchmark for testing whether models can generate code with formal specifications and machine-checked proofs. The reported results show a large gap between passing ordinary code tests and producing fully verified programs.

## Problem
- LLM-generated code can pass visible tests while still having functional errors or security defects, because tests sample behavior rather than prove correctness.
- Existing verifiable-code benchmarks are often small, omit ground-truth proofs, test only one stage, or use settings far from normal software development.
- The paper targets competitive-programming tasks because they require concrete algorithmic reasoning, including greedy methods, dynamic programming, binary search, and sliding windows.

## Approach
- The benchmark contains 946 tasks: 690 from LeetCode and 256 from Codeforces. Each task includes a natural-language prompt, expert-validated Verus specifications, judge-accepted Rust code, Verus-checked proofs, and positive and negative tests.
- Construction starts with 91 manually verified seed problems, then expands with a Copilot/GPT-5.3-Codex agent plus human review, and keeps only tasks that fit the Verus-supported Rust subset.
- Human experts check online-judge acceptance, specification soundness and completeness, and Verus proof validity with `--no-cheating`.
- The authors generate positive tests from verified programs and negative tests through semantic, syntactic, and direct output mutation.
- Post2Exe converts supported Verus postconditions into executable Rust checks so negative tests can expose incomplete specifications.

## Results
- VeriContest has 946 tasks. Median task size is 188 description words, 32 lines of code, 23 lines of specification, 83 lines of proof, 11.5 loop invariants, 14 assertions, 276 positive tests, and 2,670 negative tests.
- Average test generation produces 252.7 positive tests and 2,315.6 negative tests per task, with 99.66% line coverage over verified code.
- Post2Exe converts 83% of benchmark postconditions and finds 60 incomplete postconditions that require revision.
- On pass@1, GPT-5.5 reaches 92.18% on natural-language-to-code generation, but only 48.31% on specification generation, 13.95% on proof generation, and 5.29% end-to-end verified generation.
- All evaluated models score below 6% end-to-end. Claude Opus 4.7 reaches 2.22%, Claude Sonnet 4.6 reaches 2.85%, Gemini 3.1 Pro reaches 2.64%, and Qwen 3.6 reaches 0.21%.
- Adding formal specifications to code generation does not solve the task: GPT-5.5 scores 67.65% on spec-to-code and 74.52% on natural-language-plus-spec-to-code, both below its 92.18% natural-language-to-code score.

## Link
- [https://arxiv.org/abs/2605.08553v1](https://arxiv.org/abs/2605.08553v1)
