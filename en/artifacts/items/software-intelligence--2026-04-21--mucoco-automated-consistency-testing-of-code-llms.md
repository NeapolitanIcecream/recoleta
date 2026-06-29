---
source: arxiv
url: http://arxiv.org/abs/2604.19086v1
published_at: '2026-04-21T04:59:09'
authors:
- Chua Jin Chou
- Khant That Lwin
- Ezekiel Soremekun
topics:
- code-llm-testing
- consistency-testing
- mutation-analysis
- metamorphic-testing
- code-intelligence
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# MUCOCO: Automated Consistency Testing of Code LLMs

## Summary
MuCoCo is an automated test method for finding consistency failures in code LLMs. It mutates coding tasks into semantically equivalent versions and checks whether the model changes its behavior across the pair.

## Problem
- Code LLMs can give different answers for programs that mean the same thing, but common coding benchmarks mostly test correctness, not consistency.
- Hand-built benchmarks are static, take manual effort, and can leak into newer models over time.
- Consistency matters because unstable behavior can break trust in code generation, execution prediction, and other software tasks.

## Approach
- MuCoCo takes a coding query, creates semantically equivalent mutants, runs the LLM on the original and mutated versions, and compares the outcomes.
- It uses 11 semantic-preserving mutations in three groups: lexical, syntactic, and logical. Examples include variable renaming, loop rewrites, DeMorgan rewrites, and constant unfolding.
- A correctness oracle checks whether each output is correct, incorrect, or invalid using expected outputs and test suites.
- A consistency oracle flags an error when the original and mutated queries lead to different outcomes, such as pass vs fail, valid vs invalid, or different failed tests.
- The evaluation covers 4 benchmarks, 4 task types, and 7 code LLMs.

## Results
- Across all settings, MuCoCo found inconsistencies in **14.82%** of generated test pairs: **21,924 / 147,935** cases.
- Average model accuracy on these tasks was **69.13%** (**102,092 / 147,680**), so inconsistency remained common even when models were often correct.
- By model, inconsistency rates ranged from **2.92%** for **GPT-5** to **21.22%** for **LLaMA-3.1**; **GPT-4o** reached **18.15%**, **Gemma-3** **17.69%**, **DeepSeek-V3.2** **16.53%**, **Codestral** **14.51%**, and **Qwen2.5** **12.73%**.
- By mutation type, lexical mutations exposed the most inconsistencies overall at **16.28%** (**12,974 / 79,707**), followed by logical at **13.91%** (**6,259 / 45,008**) and syntactic at **11.59%** (**2,691 / 23,220**).
- By task, inconsistency was **27.15%** for **code generation**, **22.35%** for **MCQ**, **18.99%** for **output prediction**, and **6.65%** for **input prediction**.
- Against **Turbulence** on the Turbulence dataset, MuCoCo reports **41.39%** error rate versus **33.8%** for Turbulence overall, with **1,781,288 / 4,302,713** errors versus **279,241 / 826,084**; the paper states MuCoCo is up to **6x** more effective in some settings and finds new classes of consistency errors.

## Link
- [http://arxiv.org/abs/2604.19086v1](http://arxiv.org/abs/2604.19086v1)
