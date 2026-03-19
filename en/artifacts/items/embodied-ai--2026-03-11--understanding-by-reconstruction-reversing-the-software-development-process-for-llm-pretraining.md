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
- llm-pretraining
- code-generation
- synthetic-data
- agent-trajectories
- long-context
- software-engineering
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Understanding by Reconstruction: Reversing the Software Development Process for LLM Pretraining

## Summary
This paper proposes a pretraining paradigm of “understanding by reconstruction”: instead of looking only at the final state of code repositories, it reversely synthesizes the planning, reading/writing, debugging, and reasoning trajectories from the development process, and then uses these trajectories for continued LLM pretraining. Experiments show that this data transformation from static repositories into dynamic agent trajectories can improve long-context understanding, code generation, some reasoning abilities, and software engineering agent capabilities.

## Problem
- Existing code pretraining mainly uses the **final static state of repositories**, losing intermediate processes such as requirement analysis, architectural planning, dependency handling, debugging, and iteration.
- As a result, models are more likely to learn “what code looks like,” but are less able to learn the **long-horizon causal reasoning** and agentic behavior involved in complex software development.
- This matters because real software engineering depends on cross-file, long-context, step-by-step decision-making; memorizing only the final code is insufficient for supporting complex engineering tasks.

## Approach
- The core method treats a real code repository as the “ground truth answer” and **reconstructs in reverse** a synthetic agent trajectory for developing it.
- They use a **multi-agent simulation**: a Main Agent first generates project requirements and a file-level implementation plan; Sub-Agents execute per file by thinking, reading existing files, and then writing the current file.
- To avoid hallucinations from purely LLM-generated trajectories, the method injects the repository’s **real structural information**: file tree, cross-file dependency graph, and AST structure; it also replaces the observations of Read/Write and the final code outputs with real file contents.
- They then apply **search-based optimization** to the CoT in the trajectories: for each thinking step, they sample alternative versions and replace the original only if doing so reduces the perplexity of the target ground-truth code, with the goal of making the “thinking more conducive to generating correct code.”
- Finally, they flatten the hierarchical multi-agent trajectories into single-sequence documents for **continued pretraining** of Llama-3-8B, and apply loss masking to observation tokens so that only the Think/Action parts are trained.

## Results
- Data scale: about **300k GitHub repositories**, synthesizing about **4B tokens** of trajectories; continued pretraining on **20B tokens** with a **64k** context window. CoT search generates **2** candidates per step for **3** iterations.
- Long context: on **Ruler-65,536**, Repo2Agent-Search reaches **61.80**, higher than Prolong **57.10** and Raw-Repos **61.00**; on **Helmet-32,768**, it reaches **62.65**, higher than Raw-Repos **60.98** and Prolong **61.57**.
- Coding ability: on **HumanEval**, Repo2Agent-Search scores **37.20**, higher than Raw-Repos **34.76**, Repo2Agent **36.59**, and Prolong **16.46**; on **LongCodeBench-32k**, it scores **36.46**, higher than Raw-Repos **34.16** and Prolong **29.38**.
- Long-code tasks are not uniformly best: on **LongCodeBench-64k**, Repo2Agent **31.05** performs best, ahead of Repo2Agent-Search **30.26**, Prolong **30.52**, and Raw-Repos **27.37**, indicating that the gains from search optimization are not always monotonic.
- Reasoning transfer: on **BBH**, Repo2Agent-Search scores **67.03**, slightly above Prolong **66.69**; on **MATH**, it scores **3.76**, higher than Repo2Agent **3.72**, Raw-Repos **2.18**, and Prolong **1.64**; but on **GSM-8k**, Raw-Repos/Repo2Agent **61.94** is instead higher than Search **60.96**.
- Software engineering agent benchmark **APTBench**: overall average for Repo2Agent is **30.10**, higher than Repo2Agent-Search **29.65** and Raw-Repos **29.02**; this suggests that the non-search version is more stable on some agentic software engineering capabilities.

## Link
- [http://arxiv.org/abs/2603.11103v1](http://arxiv.org/abs/2603.11103v1)
