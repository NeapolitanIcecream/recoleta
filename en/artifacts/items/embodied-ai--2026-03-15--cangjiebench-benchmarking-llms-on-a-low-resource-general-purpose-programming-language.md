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
- llm-benchmark
- code-generation
- code-translation
- low-resource-language
- program-synthesis
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# CangjieBench: Benchmarking LLMs on a Low-Resource General-Purpose Programming Language

## Summary
This paper introduces **CangjieBench** to systematically evaluate large language models' code generation and code translation capabilities on Cangjie, a low-resource general-purpose programming language. The core finding is: direct generation performs poorly, adding concise syntax constraints is the most cost-effective approach, while Agent achieves the highest accuracy but at a high cost.

## Problem
- Existing LLMs are strong on high-resource languages such as Python and C++, but there is a lack of rigorous evaluation of their generalization ability on **low-resource general-purpose languages**.
- Previous low-resource code research has mostly focused on DSLs, which can easily conflate “not understanding new syntax” with “lacking domain knowledge,” making it impossible to purely measure syntax transfer ability.
- In industry, there is a need to migrate code from high-resource languages to new languages (such as Python to Cangjie), but there are few benchmarks for **high-resource → low-resource** general-purpose language translation. This is important because the expansion of the HarmonyOS ecosystem will create real migration demand.

## Approach
- Build **CangjieBench**: **manually translate** HumanEval and ClassEval into Cangjie, producing **248** high-quality, contamination-free samples, of which **164** come from HumanEval and **84** from ClassEval.
- The benchmark covers two task types simultaneously: **Text-to-Code** (natural language to Cangjie code) and **Code-to-Code** (Python-to-Cangjie translation), spanning both function-level and class-level difficulty.
- To ensure fairness, the authors use manual translation rather than web scraping, thereby emphasizing **zero contamination**; they also build a Docker sandbox to execute compilation and testing.
- They systematically compare four paradigms that require no fine-tuning: **Direct Generation**, **Syntax-Constrained Generation** (adding concise syntax rules into the prompt), **RAG** (document retrieval or code retrieval), and **Agent** (CLI-based autonomous document lookup and self-correction).
- The central mechanism can be understood simply as: instead of changing model parameters, use “**syntax prompts / external knowledge / agent-style trial and error**” to help the model temporarily learn a new language it has barely seen before.

## Results
- Under **Direct Generation**, overall model performance is poor: the table shows average **Pass@1** at about **22.1%–24.3%** and average **Compile** at about **52.1%–56.1%**, indicating that pretraining knowledge alone is insufficient for stably mastering Cangjie syntax.
- **Syntax-Constrained Generation** is clearly stronger and more stable: for example, **GPT-5** achieves average **Pass@1=53.8%** and **Compile=38.1%** (recorded according to the original presentation in the paper’s table); compared with Direct’s **24.3% / 56.1%**, the authors therefore argue that syntax constraints provide the best trade-off between accuracy and cost.
- On HumanEval, **GPT-5 + Syntax-Constrained** reaches **67.1% Pass@1**; on ClassEval it reaches **40.5% Pass@1**, making it one of the strongest fully visible results in the table.
- Other strong baselines also benefit from syntax constraints: for example, **Kimi-K2** averages **Pass@1=42.4%**, and **Qwen3** averages **40.0%**, both significantly higher than their respective Direct results.
- **RAG** is not always optimal: in the visible tables, average Pass@1 for **RAG(Code)** mostly falls within **8.5%–31.3%** or **10.1%–23.7%** (depending on the model), and is generally worse than syntax constraints overall; based on this, the authors argue that external examples or documents cannot reliably replace explicit syntax guidance.
- The abstract also explicitly states that **Agent achieves state-of-the-art accuracy**, but with **high token consumption**; at the same time, **Code-to-Code often underperforms Text-to-Code**, which the authors interpret as **negative transfer** from source-language patterns. Since the provided excerpt does not fully show the specific numbers for Agent and translation tasks, they cannot be listed precisely here.

## Link
- [http://arxiv.org/abs/2603.14501v1](http://arxiv.org/abs/2603.14501v1)
