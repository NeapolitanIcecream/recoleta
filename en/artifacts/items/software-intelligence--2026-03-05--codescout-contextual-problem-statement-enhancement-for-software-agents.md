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
- code-intelligence
- problem-statement-augmentation
- swebench
- repository-analysis
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# CodeScout: Contextual Problem Statement Enhancement for Software Agents

## Summary
CodeScout rewrites vague problem descriptions into more complete, actionable task specifications by performing lightweight pre-exploration of the code repository before a software agent actually begins fixing issues. It is a pluggable preprocessing layer that does not require changes to existing agent frameworks, yet can significantly improve real-world software bug-fixing performance.

## Problem
- The paper addresses the following issue: problem descriptions submitted by users to coding agents are often too brief and lack reproduction steps, expected behavior, and code context, causing agents to explore the repository blindly, repeatedly attempt incorrect fixes, and ultimately fail.
- This matters because prior research shows that input quality, rather than model capability alone, is often the key bottleneck for AI software engineering agents; unclear descriptions directly lengthen trajectories, increase cost, and reduce repair success rates.
- Existing methods mostly focus on retrieval or localization, but cannot turn the “context implicit in the repository” into natural-language task specifications that agents can actually execute.

## Approach
- CodeScout’s core mechanism is simple: first “understand the repository and the problem,” then rewrite the original issue into a better problem statement so downstream agents take fewer wrong turns.
- It first uses ASTs to build a repository knowledge graph representing structural relationships such as classes, functions, imports, dependencies, and scopes.
- It then performs high-level scoping: the LLM uses the original issue and the knowledge graph to select up to 15 of the most relevant code targets, instead of searching the entire repository blindly.
- Next, it conducts fine-grained analysis on those targets, extracting their relationship to the issue, likely edit locations, technical clues, and alternative root-cause hypotheses, while using relevance filtering to remove noise.
- Finally, it synthesizes the original issue and the filtered insights into an enhanced problem statement, explicitly adding an enriched description, reproduction steps, expected behavior, exploration hints, and repair hints; this workflow requires no modification to underlying scaffolds such as SWE-agent or OpenHands.

## Results
- On SWEBench-Verified, the paper claims that CodeScout improves resolution rate by about 20% relative to the default method, resolving up to 27 additional issues.
- In SWE-Agent ablation experiments, the number of solved issues increased from Default’s 114/194/183 to 125/209/207, corresponding to DeepSeek R1 +11 (+9.6%), GPT-5-mini +15 (+7.7%), and Qwen3 Coder +24 (+13.1%).
- Letting the agent perform enhancement during the execution trajectory was actually worse: 109/177/158, which is -5, -17, and -25 relative to Default, respectively, indicating that “independent pre-exploration” is much more effective than “supplementing the specification while solving.”
- After removing relevance filtering, the gains weakened noticeably: 116/190/190; using BM25 instead of LLM scoping yielded 119/195/198, which is still better than Default but weaker than full CodeScout, showing that both semantic scoping and filtering are critical.
- Cross-synthesis experiments show that a strong enhancer can significantly boost a weaker runtime model: when DeepSeek R1 was the runtime agent, the default was 108, but using Qwen3 Coder for problem enhancement raised it to 164, an increase of +56 (+51.9%); meanwhile, the stronger runtime model GPT-5-mini improved from 194 to 196/207/209, with smaller but still consistent gains.
- The paper also claims that post-enhancement file-level and function-level localization both outperform the default setting, especially for weaker models; cost/token analysis indicates that Qwen3 and DeepSeek typically solve more issues under the same token budget, though the excerpt does not provide a complete unified table of values.

## Link
- [http://arxiv.org/abs/2603.05744v1](http://arxiv.org/abs/2603.05744v1)
