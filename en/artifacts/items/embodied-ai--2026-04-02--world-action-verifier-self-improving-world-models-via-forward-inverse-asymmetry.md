---
source: arxiv
url: http://arxiv.org/abs/2604.01985v1
published_at: '2026-04-02T12:48:36'
authors:
- Yuejiang Liu
- Fan Feng
- Lingjing Kong
- Weifeng Lu
- Jinzhou Tang
- Kun Zhang
- Kevin Murphy
- Chelsea Finn
- Yilun Du
topics:
- world-models
- inverse-dynamics
- active-data-collection
- robot-learning
- simulated-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# World Action Verifier: Self-Improving World Models via Forward-Inverse Asymmetry

## Summary
WAV is a self-improving world-model framework that finds where an action-conditioned dynamics model is likely wrong by checking two simpler things: whether a future state looks plausible and whether the action could actually produce it. The paper claims this verification step is easier than direct next-state prediction in under-explored regions, which improves data collection efficiency and downstream policy learning.

## Problem
- World models need to predict outcomes for a wide range of actions, including bad or random ones, but action-labeled robot data is limited, expensive, and sometimes unsafe to collect.
- Existing verification methods such as uncertainty, ensemble disagreement, or learning progress often fail where they matter most: under-explored regions where the model has little prior support.
- This matters because poor verification leads to poor data selection, weaker world models, and worse policy evaluation, planning, and optimization.

## Approach
- WAV splits verification into two checks: **state plausibility** and **action reachability**. A predicted next state should both look like a valid future and be reachable under the given action.
- For plausibility, WAV trains a subgoal generator on large action-free video data and samples plausible future states from that prior.
- For reachability, WAV trains a sparse inverse dynamics model on action-labeled data to infer the action from only action-relevant state features, using a learned mask rather than the full observation.
- It then runs a reverse cycle: current state -> sampled plausible subgoal -> inferred action -> world-model rollout. The gap between the sampled subgoal and the world-model prediction is used as an estimated error signal for exploration and self-improvement.
- The theory section argues sparse inverse verification is easier than dense forward prediction when the action depends on a low-dimensional subset of state features, environment stochasticity is high, and labeled data is limited.

## Results
- Across **9 tasks** spanning **MiniGrid, RoboMimic, and ManiSkill**, WAV reports **2x higher sample efficiency** for world-model learning than existing methods.
- The paper reports an **18% improvement in downstream policy performance** compared with baselines.
- In controlled MiniGrid studies, the robustness evaluation varies labeled data size from **400 to 2000** transitions, tests scene complexity from **6 to 14 objects**, and adds **0 to 4** noisy floors to increase stochasticity.
- MiniGrid data setup uses **50k interaction sequences**, with **200 seed sequences** as labeled data and **20k unlabeled candidate sequences** for acquisition; half of the full data is used to train the action-free subgoal generator.
- The excerpt states that WAV is compared against **Random, Uncertainty, Progress, Vanilla IDM, and Oracle** baselines, but the detailed per-benchmark metric tables and exact baseline margins beyond the headline **2x** and **18%** are not included in the provided text.

## Link
- [http://arxiv.org/abs/2604.01985v1](http://arxiv.org/abs/2604.01985v1)
