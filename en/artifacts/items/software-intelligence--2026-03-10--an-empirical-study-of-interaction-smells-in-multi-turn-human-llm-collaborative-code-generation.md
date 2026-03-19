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
- multi-turn-code-generation
- human-llm-collaboration
- interaction-smells
- multi-agent-framework
- code-intelligence
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# An Empirical Study of Interaction Smells in Multi-Turn Human-LLM Collaborative Code Generation

## Summary
This paper studies “interaction smells” in multi-turn human-LLM collaborative programming: even when the final code may be usable, the dialogue process itself can repeatedly lose context, miss requirements, and break existing functionality. Based on real chat data, the authors build the first taxonomy of such smells and propose a lightweight multi-agent mitigation framework, InCE.

## Problem
- Existing code generation evaluations mostly focus only on the functional correctness of the final output, overlooking hidden interaction problems during multi-turn collaboration that cause repeated rework and interrupt development flow.
- In long conversations, LLMs often exhibit phenomena such as forgetting historical constraints, becoming inconsistent across turns, and rolling back previously completed functionality, harming collaboration efficiency and user satisfaction.
- There is a lack of systematic research based on real user logs: what typical interaction smells exist, how common they are, and whether they remain prevalent across different models.

## Approach
- The authors sampled code-related conversations from WildChat and LMSYS-Chat-1M, merging them into 60,949 interactions; after LLM-based decoupling and filtering, they obtained 66,371 programming logs, of which 19,507 were multi-turn dialogues.
- They manually performed open card sorting on 378 real multi-turn samples to construct an interaction smell taxonomy; the final taxonomy defines 3 top-level categories and 9 subcategories, such as ambiguous-instruction, must-do-omission, partial-functionality-breakdown, and code-rollback.
- They conducted quantitative analysis with 6 mainstream LLMs (GPT-4o, DeepSeek-Chat, Gemini 2.5, Qwen2.5-32B, Qwen2.5-72B, Qwen3-235B) on WildBench to compare the distribution of different smells.
- They propose the InCE (Invariant-aware Constraint Evolution) multi-agent framework: one module extracts cross-turn “global invariants/constraints,” while another performs smell auditing before generation to proactively prevent violations of historical requirements or damage to existing implementations.

## Results
- The authors claim to establish the first interaction smell taxonomy for human-LLM collaborative code generation, containing **3** top-level categories and **9** fine-grained categories.
- In the manually annotated samples, the reported smell proportions include **Must-Do Omission 38.35%**, **Incomplete Instruction 4.39%**, **Ambiguous Instruction 3.84%**, and **Must-Not Violate 3.22%**; the paper also notes that **Must-Do Omit** and **Partial Functionality Breakdown** are the most prevalent across models.
- For data processing validation, among **383** checked decoupled samples, annotator agreement reached **Cohen’s Kappa = 0.87** with an overall accuracy of **92%**; during the open card sorting stage, experts achieved average **Kappa ≥ 0.78**, and in the student annotation stage, the average was **Kappa = 0.82**.
- On the extended WildBench benchmark, InCE improves the **Task Success Rate by up to 6.67%**.
- InCE also suppresses the occurrence of key interaction smells (such as **Repetitive Response** and **Must-Do Omission**) by about **13.5%**.
- The paper’s abstract does not provide more detailed per-model or per-benchmark score tables, nor a full numerical comparison against a clearly specified baseline, but its core quantitative claim is that lightweight InCE can both improve task success rate and significantly reduce interaction smells.

## Link
- [http://arxiv.org/abs/2603.09701v1](http://arxiv.org/abs/2603.09701v1)
