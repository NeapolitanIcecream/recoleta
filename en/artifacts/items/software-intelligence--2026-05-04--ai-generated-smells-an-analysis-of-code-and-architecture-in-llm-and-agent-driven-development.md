---
source: arxiv
url: https://arxiv.org/abs/2605.02741v1
published_at: '2026-05-04T15:41:13'
authors:
- Yuecai Zhu
- Nikolaos Tsantalis
- Peter C. Rigby
topics:
- llm-code-generation
- code-maintainability
- technical-debt
- static-analysis
- multi-agent-software-engineering
- ai-generated-code-smells
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# AI-Generated Smells: An Analysis of Code and Architecture in LLM and Agent-Driven Development

## Summary
The paper argues that LLM and agent-generated code can pass functional tests while still carrying maintainability debt. It studies code smells in single-file coding tasks and MetaGPT-generated repositories.

## Problem
- Functional correctness benchmarks miss code smells such as long methods, high coupling, unstable dependencies, and God Class structures.
- This matters because these defects raise maintenance cost, make refactoring riskier, and can hide inside working AI-generated software.
- The paper asks whether prompting and agent collaboration reduce these defects as project complexity grows.

## Approach
- Experiment I generated Python solutions for 90 CodeContest problems using Gemini 2.5 Pro, Llama 3.3 70B, deepseek-coder-v2 16B, qwen3-coder 30B, and qwen3-coder 480B under zero-shot and few-shot prompts.
- The same 90 problems also used one verified human Python submission each as a baseline.
- Experiment II used MetaGPT with Qwen-Coder 480B to create full Python repositories for 5 application scenarios, each with 4 stages of increasing requirements.
- PyExamine detected code, structural, and architectural smells; cloc measured total lines of code; the study also logged total files and Agent Action Count.
- The core mechanism is simple: generate code at controlled task sizes, run the same static smell detector on every artifact, and compare smell counts and types against model, prompt, correctness, and code volume.

## Results
- Experiment I covers 90 problems, 5 LLM variants, 2 prompt conditions, and a human baseline; the excerpt gives no exact smell-count tables or pass rates.
- For algorithmic tasks, the paper claims stronger models such as qwen3-coder 480B produce more Long Method bloat as they handle harder logic; human submissions more often show Temporal Fields.
- Experiment II covers 5 scenarios × 4 stages = 20 MetaGPT projects; the paper claims smell patterns shift toward Too Many Branches, Potential Improper API Usage, Unstable Dependency, and God Class structures.
- The paper claims total lines of code is a near-perfect predictor of architectural decay, but the excerpt gives no coefficient, p-value, or regression table.
- It claims few-shot or detailed prompts do not reduce maintainability decay, and functional correctness is decoupled from structural quality; the excerpt gives no numeric effect size.

## Link
- [https://arxiv.org/abs/2605.02741v1](https://arxiv.org/abs/2605.02741v1)
