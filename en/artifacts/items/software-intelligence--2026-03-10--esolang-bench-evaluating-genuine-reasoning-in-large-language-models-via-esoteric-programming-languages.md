---
source: arxiv
url: http://arxiv.org/abs/2603.09678v1
published_at: '2026-03-10T13:47:15'
authors:
- Aman Sharma
- Paras Chopra
topics:
- code-benchmark
- ood-generalization
- reasoning-evaluation
- esoteric-languages
- code-generation
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# EsoLang-Bench: Evaluating Genuine Reasoning in Large Language Models via Esoteric Programming Languages

## Summary
This paper introduces **EsoLang-Bench**, which uses five esoteric programming languages that appear extremely rarely in training corpora to test whether large models possess transferable, genuine programming reasoning rather than relying on memory and benchmark contamination. The results show that models near the ceiling on mainstream code benchmarks almost completely fail on these equivalent but strongly OOD tasks.

## Problem
- Existing code generation benchmarks (such as HumanEval and MBPP) are increasingly likely to overestimate capability, because high scores may come from memorizing training data, contamination, or pattern matching rather than true algorithmic reasoning.
- The problem the study aims to solve is: how to construct an evaluation that is **low-contamination, low-gaming-incentive, yet still requires the same computational primitives**, so as to separate “retrieval/memory” from “transferable reasoning.”
- This matters because if models only perform well within heavily covered training distributions, they will be hard to rely on for software foundation models, automated software production, and reliable code intelligence in new environments.

## Approach
- The authors build **EsoLang-Bench**: 80 language-agnostic programming problems, divided into 4 difficulty tiers and mapped into 5 esoteric languages (Brainfuck, Befunge-98, Whitespace, Unlambda, and Shakespeare), yielding 400 evaluation instances in total.
- The core mechanism is simple: the problems themselves are equivalent to basic algorithmic problems in Python, but the expression language is swapped to esolangs that are extremely scarce in training data; if a model can still perform well, that more likely indicates it truly understands loops, state, conditionals, and algorithms rather than having memorized templates.
- These languages were chosen because they are both **Turing-complete** and share the computational essence of mainstream languages, while also having **1,000–100,000×** fewer public repositories than Python, significantly reducing pretraining coverage and contamination probability.
- The evaluation covers 5 frontier models and 5 prompting/scaffolding strategies, including zero-shot, few-shot, self-scaffolding, textual self-scaffolding, and ReAct, with automatic verification via interpreter execution and 6 test cases.
- The authors also emphasize allowing document reading, interpreter feedback, and iterative correction to better approximate the process of “a human learning a new language,” while testing whether test-time learning truly exists.

## Results
- The paper claims that frontier models typically achieve **85–95%** on mainstream code benchmarks, but only **0–11%** on equivalent esolang tasks, revealing a massive capability gap.
- From Table 2, **few-shot remains almost ineffective**: for example, GPT-5.2 on Brainfuck is **2.5%→2.5%**, on Befunge-98 **2.5%→8.8%**, and on both Whitespace and Unlambda **0%**; this suggests ICL provides very limited help for transfer to strongly OOD languages.
- According to the abstract and table notes, **all difficulties above Easy are 0%**: all **Medium/Hard/Extra-Hard = 0%**, meaning models are completely unable to transfer across languages on even slightly more complex algorithmic tasks.
- Looking only at the zero-shot / 3-shot table, the best language-model results are still only single digits: O4-mini reaches **6.2%** zero-shot and **7.5%** few-shot on Befunge-98; GPT-5.2 reaches **8.8%** few-shot on Befunge-98; most models remain at **0%** for long stretches on Whitespace and Unlambda.
- In the average accuracy across five languages shown in Figure 1, **Self-Scaffolding reaches at best only 6.2% (GPT-5.2)**, and “all models remain **below 7%** even with advanced scaffolding.”
- Figure 2 provides an even stronger contrast: the best model achieves only **3.8%** on esolangs, versus **100%** on the **equivalent Python problems**; the authors also report in their error analysis that **59% are compilation errors**, indicating the first bottleneck is syntax and representation rather than only high-level algorithm design.

## Link
- [http://arxiv.org/abs/2603.09678v1](http://arxiv.org/abs/2603.09678v1)
