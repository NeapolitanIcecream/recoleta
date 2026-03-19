---
source: arxiv
url: http://arxiv.org/abs/2603.05744v1
published_at: '2026-03-05T23:10:09'
authors:
- Manan Suri
- Xiangci Li
- Mehdi Shojaie
- Songyang Han
- Chao-Chun Hsu
- Shweta Garg
- Aniket Anand Deshmukh
- Varun Kumar
topics:
- software-agents
- query-refinement
- code-repair
- repo-understanding
- swebench
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# CodeScout: Contextual Problem Statement Enhancement for Software Agents

## Summary
CodeScout improves the repair success rate of software engineering agents by performing lightweight pre-exploration of the codebase before agent execution, rewriting vague problem descriptions into more complete, actionable task specifications. The core idea is to first “understand the problem clearly” and then “start solving it,” without requiring any changes to downstream agent frameworks.

## Problem
- The paper addresses the problem that **software engineering agents often fail when faced with underspecified issue reports**; this matters because real-world development issues often lack reproduction steps, expected behavior, and code context, causing agents to blindly explore for long periods or repeatedly attempt the same fix.
- The authors point out that existing failures often manifest as **over-exploration** and **stubbornly repeated fixes**; the bottleneck is not necessarily model reasoning ability, but insufficient input specification quality.
- The goal is to enhance the original problem statement into a clearer, more actionable specification **without modifying the agent scaffold**, thereby improving downstream task performance.

## Approach
- CodeScout is a **preprocessing-style query/problem enhancement pipeline**: it takes the original problem statement and code repository as input, outputs an enhanced problem statement, and then passes it to existing software agents for execution.
- It first builds a **repository knowledge graph**, extracting structured entities and relationships such as classes, functions, import relationships, and variable scopes from the AST to form a semantic index of the codebase.
- It then uses an LLM for **high-level scoping**, selecting up to 15 of the most relevant exploration targets based on the original issue and the knowledge graph, rather than blindly searching the entire repository directly.
- For each target, it performs **fine-grained contextual analysis**, extracting its relationship to the issue, possible fix locations, technical implementation clues, and alternative root-cause hypotheses, while filtering noise through a relevance threshold.
- Finally, it performs **problem synthesis**: merging the original description with the filtered insights into an enhanced problem specification that explicitly adds reproduction steps, expected behavior, exploration hints, and fix hints; in essence, this translates implicit repository knowledge into a natural-language task specification that agents can use more effectively.

## Results
- On **SWEBench-Verified**, the paper claims that CodeScout delivers a **20% improvement in resolution rate** over the default method, and **resolves up to 27 additional issues**.
- In SWE-Agent ablation experiments, compared with Default, CodeScout increased the number of solved issues from **114→125 (DeepSeek R1, +11, +9.6%)**, **194→209 (GPT-5-mini, +15, +7.7%)**, and **183→207 (Qwen3 Coder, +24, +13.1%)**.
- Letting the agent **perform enhancement on its own during execution** was actually worse: relative to Default, it became **109 vs 114 (DeepSeek R1, -5)**, **177 vs 194 (GPT-5-mini, -17)**, and **158 vs 183 (Qwen3 Coder, -25)**, showing that an independent pre-execution enhancement stage is more effective than “patching while solving.”
- After removing relevance filtering, gains dropped noticeably: **116/190/190** compared with Default’s **114/194/183**, indicating that filtering noisy context is a key component.
- Replacing LLM scoping with **BM25 entity selection** still outperformed the default, but was weaker than the full method: **119/195/198**, below CodeScout’s **125/209/207**, suggesting that semantic scoping is better than lexical retrieval.
- Cross-enhancement results show that a strong enhancer can significantly help a weaker execution model: when DeepSeek R1 was used as the execution agent, enhancement by Qwen3 improved performance from **108 to 164 (+56, +51.9%)**; meanwhile, the stronger execution model GPT-5-mini improved only from **194 to 196 (+2, +1.0%)** when enhanced by DeepSeek, suggesting that the gains are more pronounced for weaker agents.

## Link
- [http://arxiv.org/abs/2603.05744v1](http://arxiv.org/abs/2603.05744v1)
