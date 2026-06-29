---
source: arxiv
url: https://arxiv.org/abs/2606.09395v1
published_at: '2026-06-08T12:13:58'
authors:
- Yewei Song
- Prateek Rajput
- Tiezhu Sun
- Saad Ezzini
- "Tegawend\xE9 F. Bissyand\xE9"
- Jacques Klein
topics:
- structured-output
- code-intelligence
- llm-decoding
- software-engineering
- function-calling
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Empirical Study for Structured Output Control in LLMs for Software Engineering

## Summary
This paper studies why LLMs fail at structured software-engineering outputs such as JSON, SQL, code, and function calls. Its main claim is that syntax control helps, but it does not solve schema-level and value-level failures.

## Problem
- LLM outputs often feed parsers, APIs, deployment tools, and data pipelines, so a correct idea can still fail if the output violates JSON syntax, SQL grammar, a function signature, or a local schema.
- The paper separates failures into syntax errors, structural errors, and value errors, because each failure type needs a different fix.
- The problem matters for automated software workflows: malformed API calls, configs, or queries can break pipelines or pass wrong data into later steps.

## Approach
- The study evaluates structured-output behavior across 4 software-engineering task types: text-to-code on BigCodeBench, text-to-SQL on Spider, text-to-JSON on CallNavi, and function calling on BFCL.
- It compares 9 LLMs: 7 general-purpose models and 2 code-focused models, with sizes listed for several models from 7B to 70B.
- It uses pass@1 for Python and SQL tasks, and AST-based evaluation for JSON and function-call tasks.
- It tests decoder-side controls: grammar-constrained decoding, regex-based validation, and Template Token Match Generation, or TTMG.
- TTMG fixes fixed-format parts by matching template tokens, then lets the model generate only the variable content, using mode switches between template copying and free generation.

## Results
- The provided excerpt does not include final pass@1 scores, AST accuracy scores, or full error-rate tables, so it does not support a precise numerical claim about overall task accuracy.
- The strongest claim is that TTMG nearly eliminates syntax errors, while structural errors and value errors still remain.
- The evaluation spans 4 task families and 4 named benchmarks: BigCodeBench, Spider, CallNavi, and BFCL.
- The model set contains 9 models: LLaMA-3.1-8B, Qwen-2.5-7B-it, Gemma2-9B-it, Qwen3-30B-A3B-IT, Mixtral-8x7B-Instruct-v0.1, LLaMA-3.1-70B GGUF, GPT-4.1-mini, Qwen2.5-Coder-7B-it, and Seed-Coder-8B-it.
- The paper reports that prompt tuning uses 5% of each dataset’s samples before the main benchmark.
- The background survey reports 8 structured-output tools and notes specific system costs or claims, such as LLGuidance at about 50 µs CPU per token for a 128k vocabulary and XGrammar claiming up to 5× faster token generation under load.

## Link
- [https://arxiv.org/abs/2606.09395v1](https://arxiv.org/abs/2606.09395v1)
