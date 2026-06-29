---
source: arxiv
url: http://arxiv.org/abs/2604.22750v1
published_at: '2026-04-24T17:54:47'
authors:
- Longju Bai
- Zhemin Huang
- Xingyao Wang
- Jiao Sun
- Rada Mihalcea
- Erik Brynjolfsson
- Alex Pentland
- Jiaxin Pei
topics:
- llm-agents
- agentic-coding
- token-efficiency
- cost-prediction
- swe-bench
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks

## Summary
This paper studies how coding agents spend tokens on real software tasks and whether they can predict those costs before execution. It finds that agentic coding is far more expensive than code chat or code reasoning, cost varies a lot even on the same task, and current frontier models are poor at forecasting their own token usage.

## Problem
- The paper asks where token costs come from in agentic coding, which models use tokens more efficiently, and whether an agent can estimate its token bill before it starts.
- This matters because coding agents are priced by token use, users often do not know the final cost in advance, and failed runs still incur cost.
- Cost control is hard because agentic coding involves long trajectories, repeated tool use, and large carried-forward context.

## Approach
- The authors analyze full execution trajectories from **eight frontier LLMs** on **SWE-bench Verified** using the **OpenHands** agent framework.
- They run each problem **4 times** per model and extract token counts, token type breakdowns, monetary cost, and fine-grained action traces such as file views and edits.
- They compare **agentic coding** against **code reasoning** and **code chat** to measure how much more expensive long-horizon agent workflows are.
- They study variance across tasks and repeated runs, relate token cost to task success, and compare token efficiency across models on shared success and shared failure subsets.
- They also define a **pre-execution token prediction task** where the agent must estimate its own input and output token usage before solving the task.

## Results
- **Agentic coding is much more expensive**: it uses about **3500×** more tokens than single-round code reasoning and about **1200×** more than multi-turn code chat. The paper says **input tokens** are the main driver of this gap.
- **Token use is highly variable**: across **500 problems**, the most expensive instance costs about **7 million** more tokens than the cheapest. On the same problem, repeated runs can differ by up to **30×** in total tokens, and the most expensive run is about **2×** the cheapest on average across model/problem settings shown in Figure 2.
- **More tokens do not mean better results**: accuracy tends to peak at an intermediate cost level and then saturate or decline at higher cost. Expensive failed runs show more repeated file viewing and editing, which the authors link to inefficient search and redundant actions.
- **Model efficiency differs a lot**: on the same tasks, **Kimi-K2** and **Claude Sonnet-4.5** consume on average **more than 1.5 million tokens** more than **GPT-5**. On shared failure tasks, **GPT-5/GPT-5.2** increase by **less than 0.5M** tokens, while **Kimi-K2** rises by about **2M** tokens.
- **Human difficulty labels are weak cost predictors**: expert-rated task difficulty has only a modest correlation with token consumption (**Kendall τb = 0.32**). Also, **6.7%** of tasks labeled **<15 min** consume more tokens than the average **>1 hour** task, while **11.1%** of **>1 hour** tasks consume fewer tokens than the average **<15 min** task.
- **Self-prediction is weak**: frontier models show only **weak-to-moderate** correlation with actual token usage, with the best reported correlation up to **0.39**, and they **systematically underestimate** true token costs before execution.

## Link
- [http://arxiv.org/abs/2604.22750v1](http://arxiv.org/abs/2604.22750v1)
