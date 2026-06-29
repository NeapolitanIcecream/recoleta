---
source: arxiv
url: https://arxiv.org/abs/2604.26102v1
published_at: '2026-04-28T20:35:09'
authors:
- Yikai Zhang
- Jiaxin Pei
- Kenan Li
- Maoquan Wang
- Jin Pan
- Yu Kang
- Shengyu Fu
- Elsie Nallipogu
- Junjie Hu
- Yufan Huang
- Zijian Jin
topics:
- code-editing
- swe-bench
- coding-agents
- multi-agent-systems
- reinforcement-learning
- software-engineering
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# SWE-Edit: Rethinking Code Editing for Efficient SWE-Agent

## Summary
SWE-Edit is a coding-agent design that splits file viewing and patch writing into separate subagents so the main model keeps a cleaner context and avoids strict edit formatting work. On SWE-bench Verified, it claims higher issue resolution, better edit success, and lower inference cost than a strong monolithic baseline.

## Problem
- Standard coding agents inspect files, plan fixes, and emit edits in one context window, so exploratory file content stays in context and can bury the code that matters.
- Edit formats create failure modes: find-and-replace needs exact string matches, while whole-file rewrite costs more tokens and can change unrelated code.
- This matters because SWE agents spend much of their budget on repository search and patch application; context noise and edit-format failures reduce resolved issues and raise cost.

## Approach
- SWE-Edit adds a Viewer subagent that receives a file path plus a natural-language query, then returns only task-relevant code blocks instead of the full file.
- It adds an Editor subagent that receives a file path plus a natural-language edit instruction, then applies the patch without making the main agent write exact find-and-replace commands.
- The main agent still reasons about the bug and the fix, while GPT-5-mini handles viewing and editing in the main experiments.
- For editor training, the authors fine-tune Qwen3-8B with GRPO to choose between find-and-replace and whole-file rewrite based on the edit request.
- The reward uses normalized match after removing comments and normalizing whitespace, giving a cheap proxy for whether the produced edit matches the target.

## Results
- On SWE-bench Verified with 500 issues and 3-run averages, SWE-Edit raises resolved rate from 69.9% to 72.0%, a +2.1 point gain over the baseline.
- Total inference cost drops from $243.7 to $200.1, a 17.9% reduction, while edit success rises from 93.4% to 96.9%, a +3.5 point gain.
- The Viewer alone returns 39.7% of requested file content on average, cutting code surface by 60.3%; main-agent non-cached input tokens fall from 276.7K to 181.3K in the combined setup.
- Against retrieval baselines on 50 held-out PR-Edit examples, the LLM Viewer gets 93.8% recall and 0.272 F1; dense retrieval gets 86.8% recall and 0.140 F1, while BM25 gets 53.7% recall and 0.083 F1.
- With other main reasoning models on 100 SWE-bench Verified instances, SWE-Edit improves resolved rate by +2.7 points for Kimi K2 Thinking, +4.1 for MiniMax-M2.1, and +1.6 for GLM-4.7; edit success gains range from +12.8 to +18.3 points.
- GRPO improves Qwen3-8B on PR-Edit from 76.8% to 90.4% format success, 56.0% to 68.4% GPT Grader accuracy, and 32.0% to 38.8% normalized match; as an editor on SWE-bench Verified, it raises resolved rate from 68.5% to 69.9% and edit success from 68.6% to 81.1%.

## Link
- [https://arxiv.org/abs/2604.26102v1](https://arxiv.org/abs/2604.26102v1)
