---
source: arxiv
url: http://arxiv.org/abs/2603.11103v1
published_at: '2026-03-11T09:23:20'
authors:
- Zhiyuan Zeng
- Yichi Zhang
- Yong Shan
- Kai Hua
- Siyuan Fang
- Zhaiyu Liu
- Jiaheng Liu
- Haozhe Wang
- Yining Zheng
- Ming Ding
- Ke Shen
- Ge Zhang
- Wenhao Huang
- Xipeng Qiu
topics:
- code-pretraining
- synthetic-trajectories
- multi-agent-simulation
- software-engineering
- long-context
- code-llm
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Understanding by Reconstruction: Reversing the Software Development Process for LLM Pretraining

## Summary
This paper proposes a pretraining paradigm of “understanding by reconstruction”: instead of looking only at the final output of code repositories, it synthesizes the underlying trajectories of planning, reading, writing, and debugging to train models. The authors show that continuing to pretrain Llama-3-8B on these reconstructed multi-agent software development trajectories improves long-context understanding, code generation, and some agentic capabilities.

## Problem
- Existing code pretraining mainly uses **static repository snapshots**, which contain only the final code and lose key reasoning processes such as requirement analysis, architectural planning, debugging, and iteration.
- This causes models to learn “surface-level code patterns” more easily, while struggling to acquire the **long-horizon, causal reasoning abilities required for complex software engineering**.
- This problem matters because real software development depends on cross-file dependencies, long-term context, and step-by-step decision-making, which determine the upper bound of code agents and automated software production.

## Approach
- A **multi-agent simulation framework** is used to “unroll” existing high-quality repositories backward into development trajectories: a main agent first generates project requirements and a file-level implementation plan, then sub-agents complete the implementation file by file.
- Sub-agents simulate development through simple **Read / Write tool calls**: they first read already implemented files to obtain context, then write the code for the current file; the full trajectory includes Think, Action, and Observation.
- To reduce hallucinations, the method **injects the real repository structure into the simulation process**, including the file tree, cross-file dependency graph, and internal AST structure of files; it also replaces the observations of Read/Write and the final code with real repository content.
- It further uses **search-based CoT optimization** to progressively rewrite reasoning steps: if an alternative chain of thought can reduce the perplexity of the target ground-truth code, that rewrite is retained, thereby maximizing \(\log p(x|z)\).
- Finally, the hierarchical multi-agent trajectories are flattened into a single long sequence for **continued pretraining**, and loss masking is applied to Observation tokens so that the model is trained only to predict Think and Action, reinforcing causal learning from “reasoning to action.”

## Results
- Data and training scale: about **4B tokens** of synthetic trajectories are generated from roughly **300k GitHub repositories**; **Llama3-8B-Instruct** is continually pretrained for **20B tokens** using a **64k** context window.
- Long-context understanding: on **Ruler 65,536**, **Repo2Agent-Search 61.80**, outperforming **Raw-Repos 61.00** and **Prolong 57.10**; on **Helmet 32,768**, **62.65**, outperforming **Raw-Repos 60.98** and **Prolong 61.57**.
- Coding ability: on **HumanEval**, **Repo2Agent-Search 37.20**, higher than **Raw-Repos 34.76** and **Prolong 16.46**; on **LongCodeBench-32k**, **36.46**, higher than **Raw-Repos 34.16** and **Prolong 29.38**.
- Long code tasks are not uniformly best: on **LongCodeBench-64k**, **Repo2Agent 31.05** performs best, exceeding **Repo2Agent-Search 30.26**, **Prolong 30.52**, and **Raw-Repos 27.37**, indicating that search optimization is not optimal for all ultra-long-code scenarios.
- Reasoning transfer: on **BBH**, **Repo2Agent-Search 67.03**, slightly higher than **Prolong 66.69** and **Raw-Repos 66.27**; on **MATH**, **3.76**, higher than **Repo2Agent 3.72**, **Raw-Repos 2.18**, and **Prolong 1.64**; but on **GSM-8k** it does not surpass Raw-Repos (**60.96 vs 61.94**).
- Agentic/software-engineering foundational ability: on **APTBench Overall Average**, **Repo2Agent 30.10** outperforms **Repo2Agent-Search 29.65** and **Raw-Repos 29.02**; for example, **Issue-Fix Average 34.84 vs 33.72**, showing that the original trajectories without search optimization are stronger on some agentic software tasks.

## Link
- [http://arxiv.org/abs/2603.11103v1](http://arxiv.org/abs/2603.11103v1)
