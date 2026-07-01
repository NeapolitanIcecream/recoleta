---
source: hn
url: https://artificialanalysis.ai/articles/claude-sonnet-5-agentic-cost
published_at: '2026-06-30T23:35:07'
authors:
- himata4113
topics:
- llm-evaluation
- agentic-ai
- code-intelligence
- knowledge-work
- model-cost
- reasoning-benchmarks
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Claude Sonnet 5: strong agentic performance at a higher cost per task

## Summary
This evaluation finds that Claude Sonnet 5 reaches top-tier agentic performance, with stronger knowledge-work and coding benchmark scores than Sonnet 4.6, while costing more per task because it uses more tokens and agentic turns.

## Problem
- Frontier models are often compared by token price, but agentic tasks also depend on how many tokens and tool-use turns the model spends to finish a task.
- Anthropic needed an external benchmark view of Claude Sonnet 5 against Sonnet 4.6, Opus 4.8, GPT-5.5, and other leading models.
- The result matters for teams using models for knowledge work, coding, and agent workflows because higher capability can raise total task cost even when per-token pricing stays flat.

## Approach
- Artificial Analysis evaluated Claude Sonnet 5 before release and scored it on the Artificial Analysis Intelligence Index.
- The evaluation compared effort settings, including max effort and the added xhigh setting, to measure quality, token use, turns, latency-related behavior, and cost per task.
- It tested agentic knowledge work with AA-Briefcase and GDPval-AA using the open source Stirrup agent harness.
- It also reported benchmark changes on CritPt, Terminal-Bench v2.1, Humanity’s Last Exam, and SciCode.

## Results
- Claude Sonnet 5 scores 53 on the Artificial Analysis Intelligence Index, a 6-point gain over Sonnet 4.6, matching GPT-5.5 with high reasoning and ranking #5 overall.
- It is 2 to 3 Intelligence Index points behind GPT-5.5 xhigh and Claude Opus 4.8 max, and remains behind Opus 4.7 and Opus 4.8 on the overall index.
- At max effort, Sonnet 5 uses about 40% more output tokens per Intelligence Index task than Sonnet 4.6 and about 3x the agentic turns on AA-Briefcase and GDPval-AA.
- On GDPval-AA, max effort uses about 6x more turns than low effort.
- Standard pricing is $3 per 1M input tokens and $15 per 1M output tokens, the same as Sonnet 4.6; measured cost is $2.29 per Intelligence Index task, about 2x Sonnet 4.6 and about 15% more than Opus 4.8 before promotional pricing.
- Reported gains over Sonnet 4.6 include +9 points on Terminal-Bench v2.1, +10 points on Humanity’s Last Exam, +7 points on SciCode, and a CritPt score of 17%, which is 14 points higher than Sonnet 4.6.

## Link
- [https://artificialanalysis.ai/articles/claude-sonnet-5-agentic-cost](https://artificialanalysis.ai/articles/claude-sonnet-5-agentic-cost)
