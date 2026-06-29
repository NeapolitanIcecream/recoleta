---
source: arxiv
url: http://arxiv.org/abs/2604.09408v2
published_at: '2026-04-10T15:21:44'
authors:
- Mohamed Elfeki
- Tu Trinh
- Kelvin Luu
- Guangze Luo
- Nathan Hunt
- Ernesto Montoya
- Nandan Marwaha
- Yannis He
- Charles Wang
- Fernando Crabedo
- Alessa Castilo
- Bing Liu
topics:
- agent-benchmark
- coding-agents
- human-in-the-loop
- selective-escalation
- text-to-sql
- software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# HiL-Bench (Human-in-Loop Benchmark): Do Agents Know When to Ask for Help?

## Summary
HiL-Bench is a benchmark for one missing skill in coding agents: knowing when they need human clarification. The paper shows that strong models can solve the same tasks with full information, but fail badly when they must detect blockers and ask targeted questions.

## Problem
- Current coding and text-to-SQL benchmarks give complete specifications, so they miss a common deployment failure: agents guess when requirements are missing, ambiguous, or contradictory.
- This matters because real software tasks often hide key information in people’s heads or in context that only appears during exploration; a lucky guess and a well-judged clarification look the same on standard benchmarks.
- The paper targets **selective escalation**: deciding when to keep working alone and when to ask for help.

## Approach
- The authors build **HiL-Bench**, a 300-task benchmark across software engineering and text-to-SQL, derived from SWE-Bench Pro and BIRD. Tasks contain **1,131 human-validated blockers** with an average of **3.8 blockers per task**.
- Blockers come in three types: **missing information (42%)**, **ambiguous requests (36%)**, and **contradictory information (22%)**. They are designed to appear during execution, not from the initial prompt alone.
- Agents get an **ask_human(question)** tool. A frozen **Llama-3.3-70B-Instruct** judge checks whether a question matches a registered blocker and returns the needed clarification or the string **"irrelevant question"**.
- The main metric is **Ask-F1**, the harmonic mean of **question precision** and **blocker recall**. It rewards asking the right questions and penalizes question spam.
- The paper also studies failure traces and trains a **32B model** with RL on a shaped Ask-F1 reward to test whether help-seeking judgment can improve.

## Results
- On **SQL**, models reach **86% to 91% pass@3** with full information, but only **5% to 38% pass@3** when they must decide when to use `ask_human()`. The best reported SQL result is **Claude Opus 4.6: 38% pass@3, 62.0% recall, 61.8% precision, 62.0% Ask-F1**.
- On **SWE**, models reach **64% to 88% pass@3** with full information, but only **2% to 12% pass@3** with `ask_human()`. The best SWE completion result is **Claude Opus 4.6 at 12% pass@3**, while Ask-F1 scores remain low: **28.2% to 41.6%** across models.
- Average Ask-F1 is **40.5% on SQL** and **37.4% on SWE**, and **no model exceeds 50% recall on SWE**, which the authors use to argue that judgment, not raw task capability, is the main bottleneck.
- A spec-only SQL ablation shows progressive discovery matters: **Claude Opus 4.6 blocker recall drops from 63% with full environment access to 11% without it**.
- Figure 1 reports the broad gap another way: models have **75% to 89% pass@3** with complete information but only **4% to 24%** when they must judge when to ask, and near-zero **No Tool** performance shows the tasks really require clarification.
- The excerpt says RL on shaped Ask-F1 reward improves a **32B model** on help-seeking quality and pass rate, with transfer across domains, but it does **not provide detailed before/after numbers** in the provided text.

## Link
- [http://arxiv.org/abs/2604.09408v2](http://arxiv.org/abs/2604.09408v2)
