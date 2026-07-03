---
source: arxiv
url: https://arxiv.org/abs/2607.01378v1
published_at: '2026-07-01T18:41:33'
authors:
- William English
- Hao Zheng
- Rickard Ewetz
topics:
- vision-language-action
- robot-safety
- flow-matching
- control-barrier-functions
- collision-avoidance
- generalist-robot-policy
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Neuro-Symbolic Safety Guidance for Vision-Language-Action Models via Constrained Flow Matching

## Summary
The paper adds trajectory-level collision guidance to flow-matching VLA robot policies. It guides π0.5 action chunks during denoising so the robot can avoid collisions that appear several steps ahead.

## Problem
- Flow-matching VLAs output action chunks, but common safety filters repair only the next action, which can react too late in cluttered manipulation.
- Unsafe manipulation can fail the task or damage robot hardware; training-time safety also requires retraining.
- On SafeLIBERO, the unguided π0.5 baseline reaches only 18.69% collision avoidance rate and 50.88% task success rate.

## Approach
- The method treats each intermediate flow-matching action chunk as a predicted 10-step end-effector trajectory.
- It models the gripper as an ellipsoid, obstacles as spheres, and computes a signed clearance score with a safety margin.
- It applies discrete-time control barrier function constraints across the whole predicted trajectory, not only the next transition.
- When a future violation appears, it solves a minimum-norm constrained optimization with SLSQP to adjust the translational action components.
- The corrected action chunk goes back into the next denoising step, so π0.5 continues generation from the safety-corrected trajectory.

## Results
- On SafeLIBERO overall, the method reports 82.81% collision avoidance rate and 81.62% task success rate.
- Against AEGIS single-step CBF filtering, it improves collision avoidance from 77.85% to 82.81% and task success from 68.13% to 81.62%.
- Against unguided π0.5, it improves collision avoidance from 18.69% to 82.81% and task success from 50.88% to 81.62%.
- On Long tasks, it reports 82.50% collision avoidance and 76.75% task success, compared with AEGIS at 79.63% and 43.75%.
- The cost is slower execution: 299.97 average execution time steps versus 262.30 for AEGIS and 278.24 for unguided π0.5.

## Link
- [https://arxiv.org/abs/2607.01378v1](https://arxiv.org/abs/2607.01378v1)
