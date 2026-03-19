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
- agentic-llm
- blocksworld
- classical-planning
relevance_score: 0.67
run_id: materialize-outputs
language_code: en
---

# Agentic LLM Planning via Step-Wise PDDL Simulation: An Empirical Characterisation

## Summary
This paper investigates whether large language models can improve task planning ability by interacting step by step with a PDDL environment, and releases the open-source tool PyPDDLEngine. The conclusion is: step-wise interaction provides only a small improvement over one-shot generation, while incurring significantly higher cost.

## Problem
- Task planning requires generating an action sequence from an initial state to reach a goal, which is critical for robots and autonomous agent systems.
- Existing research has not yet clarified whether, when LLMs act as planners, step-wise execution, state observation, and retrying are more effective than directly generating a complete plan in one shot.
- This question matters because software agents perform well under the “execute-observe feedback-correct” paradigm, but it is unclear whether feedback is equally useful in the planning domain.

## Approach
- The authors propose **PyPDDLEngine**: an interactive simulation engine supporting STRIPS-style PDDL, which exposes 7 types of planning operations as LLM tool calls through MCP, such as initialization, querying state, querying available actions, executing a single action step, resetting, viewing history, and validating a complete plan.
- They design two LLM planning modes: **Direct LLM**, which outputs a complete plan in one shot and retries from scratch after failure; and **Agentic LLM**, which selects one action at a time, observes the new state, and continues searching after resetting when necessary.
- These are compared with two classical planners: Fast Downward **lama-first** as the main classical baseline, and **seq-sat-lama-2011** as a plan-quality reference.
- Under a uniform **180-second** budget on 102 IPC Blocksworld instances, they compare success rate, failure modes, plan length on commonly solved instances, and token cost.

## Results
- The classical planners are strongest: Fast Downward **lama-first** and **seq-sat-lama-2011** both solve **87/102 = 85.3%**; Direct LLM solves **65/102 = 63.7%**; Agentic LLM solves **68/102 = 66.7%**, only **3.0 percentage points** higher than Direct.
- Cost rises substantially: Direct averages **28,488 tokens** per run, while Agentic averages **169,864 tokens**; normalized per successful solution, these are **44,705** vs **254,796 tokens/solution** respectively. Agentic costs about **5.7×** more, solves only **3** additional instances, and corresponds to roughly **14.4 million** extra tokens.
- Agentic introduces new failure modes: in **6** instances there is “premature exit,” meaning the model incorrectly judges the problem unsolvable; among these, **4/6** instances are actually solved by Direct LLM, showing that interactive feedback does not reliably improve judgment.
- On the **49** instances solved by all four methods, both LLM approaches produce shorter plans than **seq-sat-lama-2011** across most difficulty ranges. For example, in the **30–40** range, the average lengths for Direct/Agentic/FD-seq are **59.7 / 60.3 / 63.3**, and in **40–50** they are **78.0 / 78.6 / 92.6**. The authors argue this looks more like pattern recall from training data than generalizable planning ability.
- There is one notable hard-case example: on instance **101**, both Fast Downward variants and Direct LLM time out, while Agentic LLM finds a valid **186-step** plan in **108–136 seconds**; however, the authors emphasize that a single sample is insufficient to demonstrate a stable breakthrough.
- The strongest overall claim is that the benefit of step-wise PDDL feedback is limited because it mainly tells the model whether an action is legal, unlike compiler errors or test failures, which provide external, objective, and directionally useful error-correction signals.

## Link
- [http://arxiv.org/abs/2603.06064v1](http://arxiv.org/abs/2603.06064v1)
