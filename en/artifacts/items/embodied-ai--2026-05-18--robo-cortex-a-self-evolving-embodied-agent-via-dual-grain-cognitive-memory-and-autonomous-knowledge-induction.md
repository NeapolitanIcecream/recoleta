---
source: arxiv
url: https://arxiv.org/abs/2605.18729v1
published_at: '2026-05-18T17:52:14'
authors:
- Nga Teng Chan
- Yi Zhang
- Yechi Liu
- Renwen Cui
- Fanhu Zeng
- Zeyuan Ding
- Xiancong Ren
- Zhang Zhang
- Qifeng Chen
- Jian Liu
- Yong Dai
- Xiaozhu Ju
topics:
- embodied-navigation
- world-model-planning
- robot-memory
- self-improving-agents
- vision-language-agents
- heuristic-induction
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Robo-Cortex: A Self-Evolving Embodied Agent via Dual-Grain Cognitive Memory and Autonomous Knowledge Induction

## Summary
Robo-Cortex is an embodied navigation agent that turns past navigation episodes into reusable natural-language heuristics for later planning. It combines short-horizon world-model planning, short-term reflection, long-term memory, and online heuristic induction.

## Problem
- The paper targets navigation in unseen or partially observed environments, where agents must use visual input, goals, spatial context, and action outcomes under uncertainty.
- Prior navigation agents often keep maps, trajectories, or local memories, but the paper argues that they do not reliably convert past episodes into reusable decision rules.
- This matters for real robots because repeated failures, detours, and successful search patterns should improve later behavior without retraining the whole model.

## Approach
- At each step, Robo-Cortex proposes candidate actions or subtask plans, uses a world model to predict short future visual outcomes, and asks a vision-language evaluator to choose the candidate with the best expected goal progress.
- Short-Term Reflective Memory summarizes a recent sliding window of subtasks, including progress and failure patterns, then feeds that summary back into the next planning step.
- Long-Term Principle Memory stores episode and subtask graphs, then retrieves related past experiences and success or failure principles through goal-conditioned state embeddings.
- Autonomous Knowledge Induction extracts recurring success and failure patterns from stored trajectories into a Navigation Heuristic Library with pattern IDs, problem descriptions, recommended strategies, confidence scores, and success/failure labels.
- Robo-Cortex++ keeps updating the heuristic library during inference, while the static Robo-Cortex variant uses fixed memory and heuristics during evaluation.

## Results
- On IGNav, Robo-Cortex improves over World-In-World from 38.57 to 41.26 SR and from 27.50 to 31.66 SPL. Robo-Cortex++ reaches 45.07 SR and 35.06 SPL.
- On AR, Robo-Cortex improves SR from 20.68 for World-In-World to 22.39, while Robo-Cortex++ reaches 23.88. Mean trajectory length is 6.97 for Robo-Cortex versus 7.09 for World-In-World.
- On AEQA, Robo-Cortex improves answer score from 27.19 for World-In-World to 29.78, while Robo-Cortex++ reaches 30.59. Robo-Cortex++ also reaches 25.57 SPL, above the best listed baseline value of 23.60 from WMNav.
- In the memory accumulation study on the seen split, IGNav improves from the Basic Pipeline at 36.11 SR and 28.16 SPL to 44.29 SR and 34.74 SPL with LPM plus SRM by round 3.
- In the heuristic transfer table, transferred heuristics improve IGNav SPL from 24.03 for the Basic Pipeline to 39.33, a +15.30 gain, and raise IGNav SR from 34.72 to 48.61.
- The excerpt says preliminary real-world robot experiments support the method, but it does not provide real-world success rates or trajectory metrics.

## Link
- [https://arxiv.org/abs/2605.18729v1](https://arxiv.org/abs/2605.18729v1)
