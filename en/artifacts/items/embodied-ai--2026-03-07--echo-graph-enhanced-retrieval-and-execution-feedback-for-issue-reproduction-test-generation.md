---
source: arxiv
url: http://arxiv.org/abs/2603.07326v1
published_at: '2026-03-07T20:11:30'
authors:
- Zhiwei Fei
- Yue Pan
- Federica Sarro
- Jidong Ge
- Marc Liu
- Vincent Ng
- He Ye
topics:
- issue-reproduction
- test-generation
- code-graph-retrieval
- execution-feedback
- fail-to-pass-validation
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Echo: Graph-Enhanced Retrieval and Execution Feedback for Issue Reproduction Test Generation

## Summary
Echo is an agent system for automatically generating “issue-reproducing tests,” aiming to produce executable, verifiable failing tests from vague issue descriptions. It combines code-graph retrieval, automatic execution, patch-assisted validation, and feedback-driven iterative refinement, achieving a new open-source SOTA on SWT-Bench Verified.

## Problem
- The paper addresses the problem of **automatically generating bug reproduction tests from issue reports**; this matters because the lack of reproducible tests slows down root-cause identification, defect fixing, and CI quality assurance.
- Common bottlenecks in existing methods include inaccurate code-context retrieval, difficulty automatically discovering test execution commands in real repositories, and the lack of a reliable oracle to determine whether a test is truly reproducing the bug.
- If a test merely “throws an error” but not due to the target bug, developers still have to investigate manually, so it must satisfy **fail-to-pass**: failing on the original version and passing on the fixed version.

## Approach
- Echo first converts the repository into a **heterogeneous code graph** (files, syntax-tree nodes, text chunks, and their relations), then uses LLM-driven **automatic query rewriting** for repeated retrieval until it obtains sufficiently rich yet compact focal code and relevant regression tests.
- It uses a patch generator to produce **candidate fix patches**, treating the patched codebase as an approximate oracle to help determine whether a generated test satisfies fail-to-pass.
- During test generation, the LLM uses the issue, focal code, related tests, and patches to generate **a single standalone minimal reproduction test file**, rather than sampling many candidates and then ranking them.
- Echo **automatically infers and executes test commands**, runs the test in a restricted read-only container, and collects execution logs as feedback.
- If the test fails semantic validation or the dual-version check, the system feeds the execution logs back to the generator for iterative revision; the dual-version check is **rule-based**, does not rely on the LLM, and retries at most twice.

## Results
- On **SWT-Bench Verified (SWT-Bench-V)**, Echo reports a **66.28% success rate**, which the paper claims is a **new SOTA among open-source methods**.
- Compared with the common previous approach of “generate multiple candidates and then filter them,” Echo emphasizes **generating only one test per issue**, aiming for a better **cost-performance trade-off**; however, the excerpt does not provide specific cost figures or per-baseline percentage differences.
- The paper explicitly claims that its **automatic execution of generated tests** is a “**first-of-its-kind**” feature that can integrate more naturally into real development workflows.
- The excerpt does not provide the full leaderboard numbers, variance, significance tests, or detailed numerical comparisons against specific baselines (such as e-Otter++ / Issue2Test); the most clearly confirmed core quantitative result is **66.28%**.

## Link
- [http://arxiv.org/abs/2603.07326v1](http://arxiv.org/abs/2603.07326v1)
