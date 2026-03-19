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
- agent-evaluation
- human-in-the-loop
- llm-benchmarking
- sim2real-gap
relevance_score: 0.75
run_id: materialize-outputs
language_code: en
---

# Mind the Sim2Real Gap in User Simulation for Agentic Tasks

## Summary
This paper systematically studies the “Sim2Real gap” in user simulation for interactive agent evaluation, that is, the gap between LLM-simulated users and real human users. Through real human experiments, the introduction of the USI metric, and evaluation of 31 simulators, the authors find that current LLM user simulation generally makes tasks too easy and evaluations overly optimistic.

## Problem
- The paper aims to answer: **Do LLM user simulators really behave and score like real humans**, and can this bias mislead the development and evaluation of agent systems?
- This matters because more and more multi-turn, tool-using benchmarks rely on simulated users to **generate dialogue** and **provide evaluation signals**; if the simulation is unrealistic, models may be optimized to “please the simulator” rather than serve real users.
- The authors further ask three questions: whether simulated user behavior resembles humans (RQ1), whether simulated evaluations align with real humans (RQ2), and whether rule-based rewards can replace human feedback (RQ3).

## Approach
- The authors **formally define** the Sim2Real gap in user simulation and break it into six parts: 4 behavioral dimensions (communication style D1, information provision pattern D2, clarification behavior D3, error response D4) + outcome calibration (ECE) + evaluation agreement (Eval).
- They propose a new composite metric, **User-Sim Index (USI)**, ranging from 0 to 100, to measure how closely an LLM simulator matches real users in interactive behavior and feedback.
- They run what is claimed to be the first full human-replacement experiment on **$\tau$-bench**: **451 real participants** interact with the same agent on **165 tasks**, and are directly compared with **31 LLM simulators**.
- Behavioral differences are measured using the **Sørensen–Dice coefficient**, simulator-human deviation at the task outcome level is measured with **ECE**, and evaluation bias is measured by the **MAE** between simulator scores and human questionnaires.
- The experiments cover proprietary, open-source, and specially trained user simulation models, using human-human agreement as a natural upper-bound reference.

## Results
- The best simulator achieves a **USI of only 76.0 (DeepSeek-V3.1)**, well below the **human inter-annotation upper bound of 92.9**, showing that even the best LLM simulator still has a substantial gap from real users.
- Among representative models, **Gemini2.0-Flash** has a USI of **73.3**, **GPT-5.1** scores **70.9**, and **GPT-4o** scores **69.3**; based on this, the authors argue that **stronger general capabilities do not necessarily lead to more realistic user simulation**.
- At the behavioral level, simulators are generally “overly cooperative, overly uniform, and lacking frustration and ambiguity.” For example, in **GPT-4o**, only **1.0%** of turns are short replies, compared with **29.0%** for real humans; **49.0%** of GPT-4o turns contain polite expressions, versus **15.3%** for real humans.
- At the evaluation level, simulator scores are overall more positive. A highlighted example given by the authors is that **GPT-5.1** **overestimates by 55%** the “human-likeness” score of the AI assistant relative to real humans, and **overestimates the overall score by 18% (on the rating-scale basis)**.
- For outcome calibration, the **ECE** of different models still differs substantially from humans: human inter-annotation is **0.069**, while **GPT-5.1 is 0.331**, **GPT-4o is 0.206**, and **DeepSeek-V3.1 is 0.122**, indicating that simulated interactions systematically inflate or distort agent success rates.
- Rule-based rewards are also insufficient to replace human feedback: the paper states that **$\tau$-bench’s binary rule-based rewards are “largely orthogonal” to human-perceived quality**, because they only check the final database state and cannot capture multidimensional experience such as policy-compliant refusal, interaction fluency, trust, and willingness to reuse.

## Link
- [http://arxiv.org/abs/2603.11245v1](http://arxiv.org/abs/2603.11245v1)
