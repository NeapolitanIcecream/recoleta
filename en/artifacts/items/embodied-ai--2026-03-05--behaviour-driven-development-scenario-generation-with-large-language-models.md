---
source: arxiv
url: http://arxiv.org/abs/2603.04729v1
published_at: '2026-03-05T02:05:48'
authors:
- Amila Rathnayake
- Mojtaba Shahin
- Golnoush Abaei
topics:
- llm-evaluation
- bdd-scenario-generation
- software-testing
- prompt-engineering
- dataset-release
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Behaviour Driven Development Scenario Generation with Large Language Models

## Summary
This paper evaluates GPT-4, Claude 3, and Gemini on automatically generating BDD (Behavior-Driven Development) scenarios, and constructs a dataset containing 500 real-world industrial user stories, requirement descriptions, and corresponding BDD scenarios. The conclusion is that different models have different optimal prompting strategies, and detailed requirement descriptions are more important than user stories alone; in the overall evaluation, Claude 3 is closer to human preference, while DeepSeek as an evaluator shows stronger correlation with human judgment.

## Problem
- The paper addresses the problem of **how to use large language models to automatically generate high-quality BDD scenarios**, so as to reduce the time cost, experience dependence, and insufficient coverage involved in manually writing Given/When/Then test scenarios.
- This is important because manually writing BDD scenarios is a bottleneck in agile development: it is time-consuming, has unstable quality, and can easily miss boundary conditions, affecting test coverage and delivery speed.
- Existing research usually looks only at syntactic correctness or small-scale datasets, lacking a systematic comparison **across models, prompting methods, input types, and evaluation dimensions**.

## Approach
- The authors built a **500-sample industrial dataset** from 4 proprietary software products, where each sample contains a user story, a requirement description, and a manually written BDD scenario; the authors claim this is the first public dataset of its kind.
- They had 3 LLMs (GPT-4o, Claude 3 Opus, Gemini 1.5 Flash) generate BDD scenarios from different inputs, and systematically compared 4 research dimensions: baseline performance, prompting strategy, input type, and model parameters.
- The evaluation does not rely only on string matching, but instead uses a **multidimensional evaluation framework**: text similarity, semantic similarity, LLM-based evaluation, and human expert assessment.
- They further tested different prompting strategies (zero-shot, few-shot, chain-of-thought), different input combinations (user story + requirement description, user story only, requirement description only), and different decoding parameters (temperature, top_p).

## Results
- In terms of data scale: the experiments are based on **500** real industrial samples covering **4** software products; compared with approximately **≈50** public samples in comparable work mentioned in the paper, this is larger in scale.
- In terms of model performance: **GPT-4** scores higher on **text similarity and semantic similarity metrics**; however, **Claude 3** is rated best in **human expert assessment** and **LLM-based evaluation**. The abstract does not provide specific scores.
- In terms of evaluators: when used as an automatic evaluator, **DeepSeek's correlation with human judgment is stronger than its correlation with text/semantic similarity metrics**, indicating that LLM-based evaluation may be closer to true quality than surface-level similarity. The abstract does not provide correlation coefficient values.
- In terms of prompting strategy: the optimal method **varies by model** — **GPT-4 is best suited to zero-shot, Claude 3 benefits from chain-of-thought, and Gemini performs best under few-shot**.
- In terms of input type: **a detailed requirement description alone can generate high-quality scenarios**; in contrast, **using only a user story yields lower-quality results**. This suggests that input information quality is more important than input format itself.
- In terms of decoding parameters: across all models, **temperature = 0 and top_p = 1.0** produced the highest-quality BDD scenarios; however, the paper excerpt **does not provide specific quantitative metrics or improvement magnitudes**.

## Link
- [http://arxiv.org/abs/2603.04729v1](http://arxiv.org/abs/2603.04729v1)
