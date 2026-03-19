---
source: arxiv
url: http://arxiv.org/abs/2603.06064v1
published_at: '2026-03-06T09:16:49'
authors:
- "Kai G\xF6bel"
- Pierrick Lorang
- Patrik Zips
- "Tobias Gl\xFCck"
topics:
- llm-planning
- pddl-simulation
- agentic-agents
- symbolic-planning
- blocksworld
relevance_score: 0.54
run_id: materialize-outputs
language_code: en
---

# Agentic LLM Planning via Step-Wise PDDL Simulation: An Empirical Characterisation

## Summary
This paper studies whether LLMs can behave like agents by executing actions step by step in a PDDL simulator and using state feedback to improve task planning. The conclusion is that this “agentic” closed-loop method provides only a small improvement over directly generating a complete plan in one shot, while costing much more, and it still clearly lags behind classical planners.

## Problem
- The problem addressed is: when LLMs perform task planning, is step-by-step execution with observation of PDDL state feedback more effective than directly generating a complete plan in one shot? This is important for autonomous robot task planning.
- Existing LLM planning work mostly either generates plans directly or hands PDDL to classical solvers, lacking systematic evaluation of placing an LLM inside a real symbolic state space for step-by-step search.
- The key significance is distinguishing whether LLMs are actually “planning” or mainly relying on training-data memory, and whether closed-loop feedback is as effective in planning as it is in coding agents.

## Approach
- The authors propose **PyPDDLEngine**: an open-source step-wise PDDL simulation engine that exposes 7 types of planning operations as LLM tool calls through MCP, such as initialization, querying the current state, querying executable actions, single-step execution, reset, querying history, and validating a complete plan.
- In the agentic setting, the LLM does not write the full plan first; instead, it chooses one action each time, reads the new state after execution, and then decides the next step. When necessary, it can reset and retry, effectively treating the LLM as an interactive search policy.
- The paper compares 4 methods on 102 IPC Blocksworld instances: Fast Downward lama-first, Fast Downward seq-sat-lama-2011, direct LLM planning (Claude Haiku 4.5), and agentic LLM planning based on PyPDDLEngine; the budget is uniformly 180 seconds.
- Evaluation metrics include success rate, plan length on jointly solved instances, failure modes, and token cost, in order to analyze the benefits and costs brought by agentic feedback.
- The authors also compare different difficulty ranges and the hardest instances to analyze whether step-wise feedback provides a real signal of global progress.

## Results
- On **102 IPC Blocksworld** instances, the two **Fast Downward** configurations both solve **87/102 (85.3%)**; **direct LLM** solves **65/102 (63.7%)**; **agentic LLM** solves **68/102 (66.7%)**. In other words, agentic improves over the direct method by only **3.0 percentage points**, but still trails classical planners by **18.6 percentage points**.
- In terms of cost, direct LLM uses **28,488 tokens** per run on average, while agentic uses **169,864 tokens**, about **5.97×**; normalized by “per successful solution,” the direct method is **44,705 tokens/solution**, and agentic is **254,796 tokens/solution**, about **5.7×**. The extra **3** solutions cost roughly an additional **14.4 million tokens** in total.
- In failure modes, the agentic method adds **6 early exits** (instances 32, 88, 89, 96, 98, 100), and **4/6** of these instances were actually solved by the direct LLM, indicating that it can incorrectly judge problems as “unsolvable.”
- Among the hardest **15** instances that Fast Downward timed out on, the two LLM methods jointly solve only **1** (instance 86); agentic additionally solves **3** (76, 78, 101), while the direct method additionally solves **1** (100). Instance **101** is the most notable: both Fast Downward configurations and the direct LLM time out, while agentic finds a valid **186-step** plan within **108–136 seconds**.
- On **49 jointly solved instances**, both LLM methods produce shorter plans than **seq-sat-lama-2011** in most difficulty ranges. For example, in the **40–50** range, FD lama is **197.1** steps, FD seq is **92.6** steps, direct LLM is **78.0** steps, and agentic is **78.6** steps; in the **30–40** range, FD seq is **63.3**, direct LLM is **59.7**, and agentic is **60.3**. The authors argue this looks more like recall of near-optimal patterns from training data than generalizable planning reasoning.
- The paper’s central conclusion is that step-wise PDDL feedback only tells the model whether an action is executable, and lacks the external, objective, directional error-correction signals found in compiler errors or test failures, so the gains from the agentic closed loop are limited in this task.

## Link
- [http://arxiv.org/abs/2603.06064v1](http://arxiv.org/abs/2603.06064v1)
