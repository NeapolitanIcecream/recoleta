---
source: arxiv
url: http://arxiv.org/abs/2603.03233v1
published_at: '2026-03-03T18:25:00'
authors:
- Zihang Zeng
- Jiaquan Zhang
- Pengze Li
- Yuan Qi
- Xi Chen
topics:
- multi-agent-systems
- scientific-code-generation
- bayesian-optimization
- low-code-platform
- llm-reliability
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# AI-for-Science Low-code Platform with Bayesian Adversarial Multi-Agent Framework

## Summary
This paper proposes a low-code platform for AI4S that splits task planning, code generation, and test evaluation across three agents, and uses Bayesian updating to continuously improve prompts, test cases, and candidate code. The core goal is to reduce LLM hallucinations and error propagation in multi-agent systems, enabling smaller models to generate scientific code more reliably.

## Problem
- Scientific code generation not only suffers from ordinary coding errors, but can also violate domain constraints, physical laws, or complex execution-flow requirements, so single-pass generation and static unit tests are not reliable enough.
- Although multi-agent systems allow division of labor, incorrect code or faulty tests produced by one agent can be passed downstream, causing errors to be amplified rather than corrected.
- Domain scientists often express ambiguous requirements in natural language and are not skilled in prompt engineering, which makes models more likely to misunderstand tasks and produce untrustworthy outputs.

## Approach
- The paper proposes a three-agent framework: the Task Manager is responsible for decomposing user requirements into an executable plan and generating/updating tests; the Solution Generator produces multiple candidate code solutions; the Evaluator scores code, tests, and prompts jointly.
- An adversarial loop is used so that the TM acts like a “problem setter,” continually constructing tests that better expose weaknesses, while the SG acts like a “solver,” iteratively improving code based on feedback, thereby jointly improving quality.
- A non-LLM Bayesian updating rule is used to recursively select better combinations of test cases and example code based on the historical performance score \(S_3\) associated with prompts, reducing the system’s dependence on the reliability of any single LLM.
- To avoid the high cost of executing all candidate code in every round, the framework uses Bayesian optimization based on AST structure and code embeddings to predict the potential of insufficiently tested code and prioritize evaluation of more promising candidates.
- The platform allows users to review the task plan and provide feedback first, after which the system converts high-level natural-language requirements into clearer scientific subtasks, constraints, and initial tests, lowering the barrier for non-programmers.

## Results
- On SciCode, the framework delivers consistent improvements across all base models; the authors claim the largest relative gain for an open-source model is **87.1%**, corresponding to **Qwen3-8B** improving from **13.2** to **24.7** on the **Without Knowledge / Sub** metric.
- On SciCode, **Qwen3-14B + this framework** reaches **30.6** on **Without Knowledge / Sub**, matching the **30.6** baseline of **Qwen3-235B-A22B-Instruct**, which the authors use to emphasize that small models can catch up with large ones.
- The abstract specifically claims that on the ScienceCode/SciCode benchmark, with this framework, a **32B open-source model can outperform a 235B model**; correspondingly, in the table **Qwen3-32B + Ours** scores **33.0** on **Without Knowledge / Sub**, higher than the **30.6** of the **Qwen3-235B baseline**.
- Other SciCode examples: **GPT-4o** improves from **24.1/1.5** to **37.2/7.7** (Sub/Main under Without Knowledge), and under the with-knowledge setting from **33.7/7.7** to **40.6/10.8**; **Claude-sonnet-4** improves from **31.3/7.7** to **42.7/13.8**.
- On **ScienceAgentBench**, using **GPT-4o** as the base model, the authors claim a new SOTA, especially on **VER**: **90.2% (without knowledge)** and **87.3% (with knowledge)**, significantly outperforming other methods; the paper also says it leads on **SR** and **CBS**, but the provided excerpt does not include the full comparative table values.
- In the experimental setup, the system by default generates **20** code samples per round, starts with **15** initial tests, retains at least **20** tests, and then uses an acquisition function to select **5** code samples for further evaluation, indicating that the method is practically designed for iterative screening rather than one-shot generation.

## Link
- [http://arxiv.org/abs/2603.03233v1](http://arxiv.org/abs/2603.03233v1)
