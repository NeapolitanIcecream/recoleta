---
source: arxiv
url: https://arxiv.org/abs/2606.31706v1
published_at: '2026-06-30T14:11:54'
authors:
- Xiaofan Liu
- Zecan Li
- Zhuang Zhao
- Ziqi Shuai
- Yanming Yang
- Qi Xin
- Jifeng Xuan
topics:
- c-to-rust
- code-transformation
- llm-code-repair
- compiler-feedback
- rust-ownership
- software-migration
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# AdaTrans: Automated C to Rust Transformation via Error-Adaptive Repair

## Summary
AdaTrans turns self-contained C files into mostly safe Rust by using compiler and test failures to guide repeated LLM repairs. It targets the ownership and borrowing errors that make direct C-to-Rust conversion fail or fall back to unsafe Rust.

## Problem
- C-to-Rust migration matters because C code often contains memory-risk patterns, while Rust can enforce ownership, borrowing, and lifetime rules at compile time.
- General LLMs often generate Rust that fails the borrow checker, changes program behavior, or uses `unsafe` blocks to bypass Rust’s safety checks.
- Existing repair loops often feed raw compiler errors back to the model without mapping the error to a specific repair action.

## Approach
- AdaTrans uses a generate-verify-repair loop for file-level, self-contained C modules with standard input/output behavior.
- A validation pipeline first runs `cargo build`, then executes tests and compares Rust output against the original C output.
- Its Strategy-Driven RAG maps compiler error codes to repair templates and Rust documentation snippets, so the model gets targeted guidance instead of raw diagnostics alone.
- Its Error-Stratified Transformation Strategy groups failures into syntactic-linking, memory-semantic, logic-behavioral, and ambiguous-fallback categories.
- The repair loop changes sampling temperature by error type: lower for syntax fixes, moderate for ownership repairs, and higher for behavioral failures.

## Results
- On 104 LeetCode Weekly Contest algorithmic problems, AdaTrans reports a mean compilation pass rate of 95.51% with ±1.11% across three independent runs.
- It reports a mean solve rate of 81.09% with ±3.09% under a fuzz-based test oracle.
- It reports a mean unsafe file rate of 1.19%.
- It improves solve rate by 59.94 percentage points over the strongest existing LLM-based C-to-Rust tool in the comparison.
- The paper also reports a zero-shot `gpt-4o-mini` pass@100 estimate of 70.58% from 200 samples per problem, used as a high-budget brute-force reference.

## Link
- [https://arxiv.org/abs/2606.31706v1](https://arxiv.org/abs/2606.31706v1)
