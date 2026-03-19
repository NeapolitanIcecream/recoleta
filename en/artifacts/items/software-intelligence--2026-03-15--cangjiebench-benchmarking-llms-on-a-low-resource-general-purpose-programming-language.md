---
source: arxiv
url: http://arxiv.org/abs/2603.14501v1
published_at: '2026-03-15T17:35:03'
authors:
- Junhang Cheng
- Fang Liu
- Jia Li
- Chengru Wu
- Nanxiang Jiang
- Li Zhang
topics:
- code-benchmark
- low-resource-pl
- code-generation
- code-translation
- llm-evaluation
- syntax-constrained-prompting
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# CangjieBench: Benchmarking LLMs on a Low-Resource General-Purpose Programming Language

## Summary
This paper introduces **CangjieBench**, a benchmark for systematically evaluating large language models' code generation and translation capabilities in Cangjie, a low-resource general-purpose programming language. The authors find that direct generation performs very poorly for mainstream models, while adding concise syntax constraints is usually the most cost-effective approach; Agent is the strongest, but also the most expensive.

## Problem
- Existing code LLMs mainly perform well on high-resource languages such as Python and C++, but there is a lack of rigorous evaluation of their generalization ability on **low-resource general-purpose languages**.
- Previous low-resource code research has mostly focused on DSLs, which can easily conflate “not knowing the syntax” with “lacking domain knowledge,” making it hard to purely measure language generalization.
- In practice, there is demand to migrate projects from high-resource languages to new languages/new ecosystems (such as HarmonyOS/Cangjie), so evaluating both **Text-to-Code** and **Code-to-Code** is important.

## Approach
- Built the first benchmark for Cangjie, **CangjieBench**: **248** high-quality samples manually translated from **HumanEval** and **ClassEval**, including **164** from HumanEval and **84** from ClassEval.
- The dataset covers two task types: **Text-to-Code** (natural language to Cangjie code) and **Code-to-Code** (Python-to-Cangjie translation), and emphasizes **zero contamination** enabled by manual construction.
- Designed a Docker sandbox for execution-based evaluation, validating according to the original test logic: function tasks are judged by whether tests pass, while class tasks require all class methods and the main tests to pass.
- Systematically evaluated multiple LLMs under **4** no-parameter-update paradigms: **Direct Generation**, **Syntax-Constrained Generation**, **RAG** (Docs/Code), and **Agent**.
- The core of the syntax-constrained method is very simple: directly place streamlined but critical Cangjie syntax rules into the prompt to help models make fewer mistakes from “applying other languages’ syntax patterns.”

## Results
- In terms of benchmark scale, the authors report that the dataset contains **248** problems in total, including **164** function-level problems and **84** class-level problems; this is one of the clearest quantitative results in the paper.
- Under **Direct Generation**, models perform poorly overall. The table shows average **Pass@1** is only about **12%–24%**, and average **Compile** is roughly **51%–56%** (with variation across models/subtasks), indicating that models often struggle to consistently generate even compilable code.
- **Syntax-Constrained Generation** significantly improves results and offers the best cost-performance trade-off. For example, under this setting **GPT-5** achieves average **Pass@1 = 53.8%** and average **Compile = 38.1%** (using the Avg. values reported in the table); on HumanEval, **Pass@1 = 67.1%**, and on ClassEval, **Pass@1 = 40.5%**. The paper argues that it is the most balanced in terms of accuracy and computational cost.
- Other syntax-constrained results are also strong: for example, **Kimi-K2** has average **Pass@1 = 42.4%**, **Qwen3 = 40.0%**, and **DeepSeek-V3 = 32.2%**; all show clear improvement over direct generation.
- The paper also claims that **Agent** achieves state-of-the-art accuracy, but consumes a large number of tokens; however, the complete quantitative table for **Agent** is not provided in the given excerpt, so its exact gains cannot be restated accurately.
- The authors also observe that **Code-to-Code often underperforms Text-to-Code**, and interpret this as a form of **negative transfer**: models overfit to source-language patterns (such as Python), making it harder to generate correct Cangjie syntax. The excerpt does not provide the full comparative figures for this phenomenon.

## Link
- [http://arxiv.org/abs/2603.14501v1](http://arxiv.org/abs/2603.14501v1)
