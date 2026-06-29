---
source: arxiv
url: https://arxiv.org/abs/2606.13053v1
published_at: '2026-06-11T08:35:37'
authors:
- Kailin Wang
- Haoxiang Jie
- Yaoyuan Yan
- Jiacheng Zhou
- Zhiyou Heng
topics:
- world-model
- robot-manipulation
- event-prediction
- task-grounding
- model-based-planning
- libero
relevance_score: 0.77
run_id: materialize-outputs
language_code: en
---

# EA-WM: Event-Aware World Models with Task-Specification Grounding for Long-Horizon Manipulation

## Summary
EA-WM solves a planning gap in long-horizon robot manipulation: a visual world model can predict future features, but it still may not tell whether the future satisfies task rules or contact constraints. The paper adds task-grounded event prediction and verification on top of pretrained feature rollouts so planning can rank candidate actions by task progress, feasibility, and confidence.

## Problem
- Long-horizon manipulation needs state changes like open/close, moved, on-target, and contact status, not just a plausible future image or latent vector.
- Visual-only world models can miss task preconditions, predicate order, and whether a predicted future is safe or executable.
- In LIBERO, the task specification is available through BDDL rules and simulator predicates, but standard feature-space planning does not use that structure.

## Approach
- Use a frozen visual encoder and an action-conditioned feature world model to roll out candidate futures.
- Decode each imagined future into task events such as object movement, spatial relations, contact progress, and success predicates.
- Score candidates with a verifier that combines task progress, semantic consistency, physical feasibility, and uncertainty.
- Train the event predictor from simulator-derived labels, so the model needs no manual frame annotation.
- Use verifier-guided CEM for PointMaze, Deformable, Wall-Single, and LIBERO-goal, and add a PPO proposal policy for the contact-sensitive LIBERO wine-rack task.

## Results
- On PointMaze random-state planning, EA-WM raises success from 0.90 to 0.94 and lowers mean state distance from 0.93568 to 0.90573 after calibration.
- On PointMaze dataset goals, both DINO-WM and EA-WM reach 1.00 success; EA-WM keeps the baseline performance while changing the scoring rule.
- On Deformable, retrieval-initialized EA-CEM reaches 94% success on the e10 blocks setting.
- On Wall-Single, archive-validated EA-CEM reaches 95% success.
- On LIBERO-goal, the check-success-aligned verifier reaches AUC 0.993947.
- On the LIBERO wine-rack task, the PPO proposal study improves online hybrid success to 97/100 at H=20.

## Link
- [https://arxiv.org/abs/2606.13053v1](https://arxiv.org/abs/2606.13053v1)
