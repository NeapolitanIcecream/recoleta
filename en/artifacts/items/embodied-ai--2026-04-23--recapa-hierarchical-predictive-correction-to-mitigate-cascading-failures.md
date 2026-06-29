---
source: arxiv
url: http://arxiv.org/abs/2604.21232v1
published_at: '2026-04-23T02:57:50'
authors:
- Xiyin Zeng
- Yuyu Sun
- Haoyang Li
- Shouqiang Liu
- Hao Wang
topics:
- vision-language-action
- embodied-agents
- hierarchical-planning
- error-correction
- long-horizon-control
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# ReCAPA: Hierarchical Predictive Correction to Mitigate Cascading Failures

## Summary
ReCAPA is a vision-language-action framework for long-horizon embodied tasks that tries to stop early mistakes from spreading through the rest of a plan. It adds correction at the action, subgoal, and full-trajectory levels, then reports gains on VisualAgentBench, MineDojo, and AI2-THOR.

## Problem
- Long-horizon VLA agents often fail after one bad intermediate step, because local errors change later subgoals and actions and create cascading failures.
- Existing methods often rely on fixed task decompositions or post-hoc fixes, so they react late and may keep local steps aligned while drifting away from the overall task intent.
- This matters because embodied tasks such as navigation, manipulation, and crafting require many dependent decisions; the paper cites prior results where one subgoal error can cut later-step performance by over 60% on benchmarks such as VirtualHome and AI2-THOR.

## Approach
- ReCAPA builds a three-level hierarchy over behavior: actions, subgoals, and full trajectories. Lower levels predict the representation of the next higher level, so the model can detect mismatch early.
- The main module, Hierarchical Predictive Correction (HPCC), uses Transformer predictors and an InfoNCE loss to make action segments predict subgoal embeddings and subgoal segments predict trajectory embeddings.
- It adds prompt-trajectory alignment in two ways: a Sinkhorn optimal-transport loss for global alignment between the whole trajectory and the instruction, and a score-field module that gives local corrective gradients for step-wise deviations.
- During inference, an LLM (GPT-4o-mini) proposes subgoals and completion criteria. ReCAPA then filters or reranks candidate actions using subgoal similarity and trajectory-level Sinkhorn consistency, with fallback rules if thresholds fail.
- The paper also introduces two diagnostics for failure dynamics: Error Propagation Rate (EPR), which measures how much one error raises later error probability, and Propagation Attenuation Coefficient (PAC), which measures how fast error effects decay.

## Results
- On **AI2-THOR**, ReCAPA reaches **SR 0.75**, beating **LLaMAR 0.68** and **GPT-4V 0.66**; it also reports **TR 0.93** and **Balance 0.93**.
- On **VisualAgentBench**, ReCAPA reports **58.65 AVG**, above **GPT-4o mini 54.15**, **Gemini 2.5 Flash 53.00**, and **Claude-4-Sonnet 50.25**. Per domain, it scores **50.6** on OmniGibson and **66.7** on Minecraft.
- The paper states relative gains of **+5.65% on VisualAgentBench**, **+9% on MineDojo**, and **+7% on AI2-THOR** over strong baselines.
- For error propagation, on **OmniGibson** at **k=10**, ReCAPA reports **EPR_10 = 0.082**, compared with about **0.3** for **GPT-4o-mini** and **Gemini-2.5**, and above **0.45** for **Claude-4-sonnet**.
- In ablations, removing HPCC drops **Behavior SR from 72.2 to 59.3**. On AI2-THOR, **HPCC-AT** reaches **0.73 SR** and **HPCC-ST 0.69**, both above the action+subgoal-only variant. The paper says using Sinkhorn and Score-field together gives the best overall performance.
- The excerpt gives strong qualitative claims for **MineDojo** such as leading in **8 of 10** long-horizon tasks, but it does not include the full task table in the provided text.

## Link
- [http://arxiv.org/abs/2604.21232v1](http://arxiv.org/abs/2604.21232v1)
