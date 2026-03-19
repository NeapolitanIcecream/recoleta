---
source: arxiv
url: http://arxiv.org/abs/2603.11245v1
published_at: '2026-03-11T19:12:31'
authors:
- Xuhui Zhou
- Weiwei Sun
- Qianou Ma
- Yiqing Xie
- Jiarui Liu
- Weihua Du
- Sean Welleck
- Yiming Yang
- Graham Neubig
- Sherry Tongshuang Wu
- Maarten Sap
topics:
- user-simulation
- sim2real
- llm-evaluation
- interactive-agents
- human-feedback
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Mind the Sim2Real Gap in User Simulation for Agentic Tasks

## Summary
This paper systematically studies the Sim2Real gap between LLMs acting as "user simulators" and real humans in interactive agent evaluation, and proposes a unified metric, USI. Based on comparisons involving 451 real participants, 165 tasks, and 31 simulators, the authors find that current simulators generally make evaluation too easy and produce overly optimistic feedback.

## Problem
- The paper addresses the question of whether LLM user simulators truly interact and score like real humans; if they are not realistic, interactive benchmarks may overestimate agent performance and mislead optimization.
- This matters because an increasing number of NLP/agent benchmarks rely on simulated users to both **generate dialogue** and **provide evaluation signals**; once the simulation deviates from real humans, both training and evaluation will incur systematic bias.
- The authors further ask whether rule-based rewards can substitute for human feedback; if not, relying only on automatic rewards will miss aspects of experience quality that users actually care about.

## Approach
- The authors formally define the Sim2Real gap in user simulation, decomposing it into four behavioral dimensions: communication style, information pattern, clarification, and error reaction, as well as two evaluation dimensions: outcome calibration and evaluative alignment.
- They propose the **User-Sim Index (USI)**, which aggregates the above dimensions into a 0–100 score to measure how closely an LLM simulator matches real humans in interactive behavior and feedback.
- They conduct a case study on **τ-bench**: replacing the original LLM user simulators with **451 real participants**, covering **165 tasks**, and directly comparing them with **31 LLM simulators** on the same tasks with the same agent.
- Behavioral alignment is measured with the Sørensen–Dice coefficient to compare lexical/structural features; outcome calibration uses ECE; evaluative alignment uses MAE between humans and simulated users on multidimensional questionnaires.
- The core mechanism can be understood simply as: first let the "real users" and the "LLM users" complete the same tasks with the same agent, then compare **how they speak, when they ask for clarification, how they react after errors, and how they score**, and finally aggregate everything into USI.

## Results
- The upper bound of human-human agreement is **USI 92.9±0.9**, while the best among the **31 LLM simulators is only 76.0±1.2 (DeepSeek-V3.1)**, showing a clear Sim2Real gap; other high performers include **Llama-4-Maverick 73.9±0.8**, **Gemini2.0-Flash 73.3±0.4**, and **Qwen3-235B 71.2±0.8**.
- The authors explicitly claim that LLM simulators create an "easy mode," raising agent success rates above the real-human baseline; in ECE, which quantifies this outcome bias, humans score **0.069±0.022**, while many models are higher, such as **GPT-5.1: 0.331±0.030**, **GPT-4o-mini: 0.382±0.035**, and **GPT-3.5-turbo: 0.582±0.035**.
- At the behavioral level, simulators are significantly more cooperative, more uniform, and show less frustration than humans. One example in the paper: the share of short replies for **GPT-4o** is only **1.0%**, versus **29.0%** for humans; the share of polite replies for **GPT-4o** is **49.0%**, while humans are only **15.3%**.
- On the aggregate dimensions, although **DeepSeek-V3.1** achieves the highest overall score, it still remains significantly below humans: **D1 45.1 vs human 87.4**, **D2 86.6 vs 97.9**, **D3 74.5 vs 88.0**, **D4 87.6 vs 93.5**, **Eval 74.3 vs 97.4**.
- On the evaluation side, simulated LLM users systematically give higher scores; the paper notes that **GPT-5.1** overestimates the AI assistant's **human-likeness by 55%** and **overall score by 18% of the rating scale**.
- Rule-based rewards also cannot replace human feedback: the binary reward in τ-bench is "largely orthogonal" to human-perceived quality because it only checks the final database state and cannot capture humans' multidimensional judgments on success, policy constraints, efficiency, fluency, willingness to reuse, and more.

## Link
- [http://arxiv.org/abs/2603.11245v1](http://arxiv.org/abs/2603.11245v1)
