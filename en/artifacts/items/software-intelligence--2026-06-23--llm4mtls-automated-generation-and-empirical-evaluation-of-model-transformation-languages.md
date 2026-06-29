---
source: arxiv
url: https://arxiv.org/abs/2606.25193v1
published_at: '2026-06-23T21:36:42'
authors:
- Bowen Jiang
- Nathan Hagel
- Haowei Cheng
- Benedikt Jutz
- Arne Lange
- Weixing Zhang
- Rahul Sharma
- Ralf Reussner
- Anne Koziolek
topics:
- llm-code-generation
- model-transformation
- domain-specific-languages
- prompt-engineering
- software-engineering-benchmark
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# LLM4MTLs: Automated Generation and Empirical Evaluation of Model Transformation Languages

## Summary
LLM4MTLs automates prompt construction and evaluation for LLM-generated model transformation language code. It targets low-resource DSLs where LLMs often produce code that parses poorly or fails transformation tests.

## Problem
- Model transformation languages such as ATL, ETL, QVTo, and Reactions require language syntax knowledge plus source and target metamodel knowledge.
- LLMs have limited training data for these DSLs, so direct prompting often returns code with syntax errors or wrong transformation behavior.
- Prior work lacks a reproducible benchmark with executable reference transformations and tests across multiple MTLs.

## Approach
- The workflow builds task prompts from existing reference transformations, then uses those prompts to ask LLMs to regenerate MTL code.
- It tests prompt variants that combine few-shot examples, grammar text, and language-specific helper methods.
- It evaluates generated code with syntactic similarity, syntactic correctness, and semantic correctness against reference scripts and test suites.
- The authors implement the workflow in n8n, containerize the components, and release a replication package.

## Results
- The evaluation suite contains 47 transformation examples across 4 MTLs: ATL, ETL, QVTo, and Reactions.
- The empirical study compares 3 LLMs across the 4 MTLs and multiple prompt configurations.
- Few-shot prompting improves syntactic quality across all 4 MTLs, but semantic correctness gains vary by language.
- For ATL, Pass@1 stays unchanged across all tested strategies and models, which means syntax gains did not translate into better first-try semantic success for that language.
- Grammar prompting helps when paired with few-shot examples, but used alone it can hurt or fail for some model-language pairs.
- The excerpt does not provide exact numeric Pass@1, syntax, semantic, or ChrF scores beyond the 47-example, 4-language, and 3-model study scale.

## Link
- [https://arxiv.org/abs/2606.25193v1](https://arxiv.org/abs/2606.25193v1)
