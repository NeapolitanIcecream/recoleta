---
source: arxiv
url: http://arxiv.org/abs/2603.09701v1
published_at: '2026-03-10T14:12:18'
authors:
- Binquan Zhang
- Li Zhang
- Lin Shi
- Song Wang
- Yuwei Qian
- Linhui Zhao
- Fang Liu
- An Fu
- Yida Ye
topics:
- llm-code-generation
- multi-turn-interaction
- human-llm-collaboration
- evaluation-benchmarking
- multi-agent-framework
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# An Empirical Study of Interaction Smells in Multi-Turn Human-LLM Collaborative Code Generation

## Summary
This paper studies “interaction smells” in multi-turn human-LLM collaborative code generation—latent problems that may not directly appear in the final functional correctness but can undermine the collaboration process. Based on real conversation data, the authors propose the first taxonomy of such smells and use a lightweight multi-agent framework to reduce them.

## Problem
- Existing code generation evaluations focus more on whether the final code is correct, but overlook process issues common in multi-turn collaboration, such as loss of context, violations of historical constraints, and response degradation.
- These “interaction smells” can cause models to drift from the user’s true intent in long conversations and break previously implemented functionality, leading developers to repeatedly rework things and harming efficiency and experience.
- The paper asks: what kinds of smells are there, are they prevalent across different mainstream LLMs, and can they be systematically mitigated?

## Approach
- Real programming-related conversations were sampled from **WildChat** and **LMSYS-Chat-1M**, merged into **60,949** records; after decoupling and filtering, this yielded **66,371** programming sessions, of which **19,507** were multi-turn dialogues.
- By manually performing open card sorting on **378** multi-turn samples, the authors built an interaction smells taxonomy. The final taxonomy reported in the paper contains **3** top-level categories and **9** second-level categories: **user-intent-quality、historical-instruction-compliance、historical-response-violation**, including ambiguous instruction, incomplete instruction, must-do omission, must-not violate, signature mismatch, cross-turn inconsistency, partial functionality breakdown, code rollback, repetitive response.
- On **WildBench**, the paper evaluates **6** mainstream models—GPT-4o, DeepSeek-Chat, Gemini 2.5, Qwen2.5-32B, Qwen2.5-72B, and Qwen3-235B-a22b—to analyze the distribution and prevalence of different smells.
- The authors propose **InCE (Invariant-aware Constraint Evolution)**: first use **IEM** to extract “global invariants / constraints that must continue to be satisfied” from dialogue history, then use **PSD** to conduct a quality audit before generation and check in advance whether those constraints would be violated.
- Put as simply as possible, the core mechanism is: **first organize the rules across the whole conversation that must not change, then check before each response whether the new response would break those rules.**

## Results
- The authors claim this is the **first** systematic taxonomy study of interaction smells in multi-turn human-LLM collaborative code generation, based on real user-LLM logs rather than purely simulated tasks.
- In the manual annotations, among user-intent-related smells: **Ambiguous Instruction 3.84%**, **Incomplete Instruction 4.39%**.
- Among historical-instruction-compliance smells: **Must-Do Omission 38.35%**, **Must-Not Violate 3.22%**; the paper explicitly points out that **Must-Do Omission** is one of the high-frequency problems common across models.
- The paper also qualitatively notes that **Partial Functionality Breakdown** is likewise common across different models, while **Ambiguous Instruction** and **Incomplete Instruction** are relatively less frequent; however, the provided excerpt does not include complete distribution numbers for all categories or all models.
- On the extended **WildBench**, **InCE** improves **Task Success Rate** by up to **6.67%**.
- **InCE** also reduces the incidence of key interaction smells (such as **Repetitive Response** and **Must-Do Omission**) by about **13.5%**.

## Link
- [http://arxiv.org/abs/2603.09701v1](http://arxiv.org/abs/2603.09701v1)
