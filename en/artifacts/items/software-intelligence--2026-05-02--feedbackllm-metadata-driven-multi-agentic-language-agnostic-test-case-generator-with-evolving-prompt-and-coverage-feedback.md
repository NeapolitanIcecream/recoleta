---
source: arxiv
url: https://arxiv.org/abs/2605.01264v1
published_at: '2026-05-02T05:43:29'
authors:
- Kushal Jasti
- Tejamani Prashanth Sahu
- Rishitha Pentyala
- Muvvala Mohit
- Vivek Yelleti
topics:
- llm-test-generation
- code-coverage
- multi-agent-systems
- software-testing
- code-intelligence
- automated-software-engineering
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# FeedbackLLM: Metadata driven Multi-Agentic Language Agnostic Test Case Generator with Evolving prompt and Coverage Feedback

## Summary
FeedbackLLM automates test-input generation for C and Python by feeding uncovered line and branch data back into later LLM prompts. The paper claims higher branch coverage than KS-LLM on many PALS/RERS C programs, with several large gains on specific benchmarks.

## Problem
- Manual test-case generation takes developer time, and random or symbolic tools can struggle with branch constraints and large state spaces.
- Single-shot LLM test generation can repeat inputs, miss branches, and hallucinate test cases.
- The problem matters because line and branch coverage affect whether edge cases and logic bugs are exercised before release.

## Approach
- FeedbackLLM uses Gemini-2.5-Flash agents in an iterative loop with a target combined coverage threshold of 90% and a maximum of 10 iterations.
- A Test Case Generator reads the source code and a baseline prompt, then emits JSON test inputs.
- A Line Feedback Agent reads missed line numbers and infers input patterns that could execute those lines.
- A Branch Feedback Agent reads partially covered conditions and suggests inputs that flip true/false outcomes.
- A redundancy cache stores generated input tuples, filters duplicates with set lookup, and adds prior inputs to later prompts so the model avoids repeated test cases.

## Results
- The evaluation uses 20 C programs from PALS/RERS and 20 Python programs with nested conditionals, loops, and mathematical constraints.
- On PS-P1-L-R18-B4 at bound 1, FeedbackLLM reports 100% branch coverage and 100% line coverage, compared with KS-LLM at 46.10% branch and 62.97% line coverage.
- On PS-P1-L-T-R16-B2 at bound 1, FeedbackLLM reports 93.09% branch and 92.17% line coverage, compared with KS-LLM at 1.79% branch and 10.57% line coverage.
- On PS-P2-L-R16-B3 at bound 1, FeedbackLLM reports 98.5% branch and 98.17% line coverage, compared with KS-LLM at 13.44% branch and 20.44% line coverage.
- At bound 10, PS-P1-L-T-R16-B2 reports 94.88% branch and 100% line coverage for FeedbackLLM, compared with 2.17% branch and 10.57% line coverage for KS-LLM.
- The table also shows weaker cases: on Mpals2-B10-cil at bound 1, FeedbackLLM branch coverage is higher than KS-LLM, 30.00% vs 21.25%, but line coverage is lower, 48.57% vs 52.14%. No aggregate mean coverage is provided in the excerpt.

## Link
- [https://arxiv.org/abs/2605.01264v1](https://arxiv.org/abs/2605.01264v1)
