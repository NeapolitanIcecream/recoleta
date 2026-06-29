---
source: arxiv
url: http://arxiv.org/abs/2604.07223v1
published_at: '2026-04-08T15:46:14'
authors:
- Yen-Shan Chen
- Sian-Yao Huang
- Cheng-Lin Yang
- Yun-Nung Chen
topics:
- llm-safety
- agentic-workflows
- tool-calling
- guardrails
- benchmarking
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# TraceSafe: A Systematic Assessment of LLM Guardrails on Multi-Step Tool-Calling Trajectories

## Summary
This paper studies whether LLM guardrails can catch unsafe actions inside multi-step tool-calling traces, instead of only screening user prompts or final answers. It introduces TraceSafe-Bench, a static benchmark for step-level safety in agent workflows, and finds that current guardrails miss many trajectory risks and depend heavily on structured-data competence.

## Problem
- Existing safety benchmarks mostly judge final text outputs or end-to-end agents, so they miss harmful intermediate tool calls that can already leak data, follow prompt injection, or misuse APIs.
- Independent guardrails are widely used for LLM safety, but it was unclear whether they can read and block risks embedded in multi-step execution traces with JSON arguments, tool schemas, and prior observations.
- This matters for autonomous software agents because a benign final answer does not undo a bad earlier action such as sending secrets to a tool or following malicious instructions from tool output.

## Approach
- The paper builds **TraceSafe-Bench**, a benchmark for mid-trajectory guardrail evaluation with **12 risk categories** across prompt injection, privacy leakage, hallucination/environment grounding, and interface inconsistencies.
- The dataset uses a **Benign-to-Harmful Editing** pipeline: start from correct multi-step trajectories from the Berkeley Function Calling Leaderboard, then inject targeted unsafe mutations at specific steps while keeping the rest of the trace realistic.
- A two-stage **Check** and **Mutate** method filters which edits are plausible at each step, then applies code-controlled structural edits such as inserting or replacing JSON keys, tool names, parameter values, or tool descriptions.
- The benchmark contains **over 1,000 execution instances** overall, and the final evaluation set samples **90 traces per risk category**. The authors evaluate **13 LLM-as-a-guard models** and **7 specialized guardrails**.
- The study also compares guardrail performance with outside benchmarks and trajectory position to test three claims: whether structure matters more than alignment, whether architecture matters more than scale, and whether longer traces hurt or help detection.

## Results
- Main benchmark result: current guardrails are weak on multi-step trajectory safety. The abstract reports evaluation of **13 LLM guard models** and **7 specialized guardrails** on **12 risk categories** over **1,000+ instances**.
- The strongest reported analysis result is a **Spearman correlation of 0.79** between TraceSafe performance and **structured-to-text benchmarks**, while correlation with standard **jailbreak robustness is near zero**. The paper argues that parsing and reasoning over structure matters more than standard alignment scores for this task.
- The paper claims **architecture matters more than model size** for trajectory risk detection, and that **general-purpose LLMs outperform specialized safety guardrails** on this benchmark.
- The paper claims **longer trajectories do not reduce accuracy**. Accuracy stays stable across extended traces, and later steps can even improve detection because models can use execution behavior instead of only static tool definitions.
- In the visible table, model behavior is uneven and category-sensitive. For example, **gpt-oss-120b** shows **59.34 average**, **53.52 unsafe**, **65.17 benign** in the shown setting, while **GPT-5 mini** shows **51.70 average**, **86.36 unsafe**, **17.05 benign**, suggesting a strong unsafe-detection/benign-rejection tradeoff.
- The excerpt does not include the full aggregate ranking across all 20 evaluated systems, so the exact best overall score and full baseline comparisons are not available here.

## Link
- [http://arxiv.org/abs/2604.07223v1](http://arxiv.org/abs/2604.07223v1)
